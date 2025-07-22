from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from django.utils import timezone
from django.http import JsonResponse
from .models import Product, Category, Review, ProductQuestion, ProductImage
from marketplace.forms import AddToCartForm
from .forms import (
    ProductForm,
    ProductImageForm,
    ReviewForm,
    ProductQuestionForm,
    ProductAnswerForm,
    ProductSearchForm
)

class ProductListView(ListView):
    """Pamja për listimin e produkteve"""
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(availability='in_stock')
        
        # Merr parametrat e kërkimit
        form = ProductSearchForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            category = form.cleaned_data.get('category')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            is_organic = form.cleaned_data.get('is_organic')
            in_stock = form.cleaned_data.get('in_stock')
            sort = form.cleaned_data.get('sort')

            # Apliko filtrat
            if q:
                queryset = queryset.filter(
                    Q(name__icontains=q) |
                    Q(description__icontains=q) |
                    Q(farmer__farm_name__icontains=q)
                )
            if category:
                queryset = queryset.filter(category=category)
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            if is_organic:
                queryset = queryset.filter(is_organic=True)
            if in_stock:
                queryset = queryset.filter(stock__gt=0)

            # Apliko renditjen
            if sort:
                if sort == 'price_asc':
                    queryset = queryset.order_by('price')
                elif sort == 'price_desc':
                    queryset = queryset.order_by('-price')
                elif sort == 'name':
                    queryset = queryset.order_by('name')
                elif sort == 'name_desc':
                    queryset = queryset.order_by('-name')
                elif sort == 'rating':
                    queryset = queryset.annotate(
                        avg_rating=Avg('reviews__rating')
                    ).order_by('-avg_rating')
                elif sort == 'date':
                    queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProductSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    """Pamja për detajet e produktit"""
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['question_form'] = ProductQuestionForm()
        context['add_to_cart_form'] = AddToCartForm()
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        context['questions'] = self.object.questions.filter(
            is_public=True
        ).order_by('-asked_at')
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context

@login_required
def add_product(request):
    """Pamja për shtimin e produktit të ri"""
    if not hasattr(request.user, 'farmer_profile'):
        messages.error(request, 'Vetëm fermerët mund të shtojnë produkte.')
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, farmer=request.user.farmer_profile)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        if form.is_valid() and image_form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user.farmer_profile
            product.save()
            
            if request.FILES:
                image = image_form.save(commit=False)
                image.product = product
                image.is_primary = True
                image.save()
            
            messages.success(request, 'Produkti u shtua me sukses!')
            return redirect('product:detail', slug=product.slug)
    else:
        form = ProductForm(farmer=request.user.farmer_profile)
        image_form = ProductImageForm()

    return render(request, 'product/product_form.html', {
        'form': form,
        'image_form': image_form,
        'title': 'Shto Produkt të Ri'
    })

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Pamja për përditësimin e produktit"""
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'

    def test_func(self):
        product = self.get_object()
        return self.request.user.farmer_profile == product.farmer

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['farmer'] = self.request.user.farmer_profile
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Përditëso Produktin'
        context['image_form'] = ProductImageForm()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Produkti u përditësua me sukses!')
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Pamja për fshirjen e produktit"""
    model = Product
    success_url = reverse_lazy('product:manage_products')
    template_name = 'product/product_confirm_delete.html'

    def test_func(self):
        product = self.get_object()
        return self.request.user.farmer_profile == product.farmer

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Produkti u fshi me sukses!')
        return super().delete(request, *args, **kwargs)

@login_required
def add_review(request, slug):
    """Pamja për shtimin e vlerësimit"""
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Vlerësimi juaj u shtua me sukses!')
            return redirect('product:detail', slug=slug)
    
    return redirect('product:detail', slug=slug)

@login_required
def add_question(request, slug):
    """Pamja për shtimin e pyetjes"""
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ProductQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.product = product
            question.user = request.user
            question.save()
            messages.success(request, 'Pyetja juaj u dërgua me sukses!')
    
    return redirect('product:detail', slug=slug)

@login_required
def answer_question(request, pk):
    """Pamja për përgjigjen e pyetjes"""
    question = get_object_or_404(ProductQuestion, pk=pk)
    
    if request.user.farmer_profile != question.product.farmer:
        messages.error(request, 'Nuk keni të drejtë të përgjigjeni në këtë pyetje.')
        return redirect('product:detail', slug=question.product.slug)

    if request.method == 'POST':
        form = ProductAnswerForm(request.POST, instance=question)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.answered_by = request.user
            answer.answered_at = timezone.now()
            answer.save()
            messages.success(request, 'Përgjigja juaj u ruajt me sukses!')
    
    return redirect('product:detail', slug=question.product.slug)

@login_required
def manage_product_images(request, slug):
    """Pamja për menaxhimin e imazheve të produktit"""
    product = get_object_or_404(Product, slug=slug)
    
    if request.user.farmer_profile != product.farmer:
        messages.error(request, 'Nuk keni të drejtë të menaxhoni këtë produkt.')
        return redirect('product:detail', slug=slug)

    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()
            messages.success(request, 'Imazhi u ngarkua me sukses!')
            return redirect('product:manage_images', slug=slug)
    else:
        form = ProductImageForm()

    return render(request, 'product/manage_images.html', {
        'product': product,
        'form': form
    })

@login_required
def delete_product_image(request, pk):
    """Pamja për fshirjen e imazhit të produktit"""
    image = get_object_or_404(ProductImage, pk=pk)
    
    if request.user.farmer_profile != image.product.farmer:
        messages.error(request, 'Nuk keni të drejtë të fshini këtë imazh.')
        return redirect('product:detail', slug=image.product.slug)

    image.delete()
    messages.success(request, 'Imazhi u fshi me sukses!')
    return redirect('product:manage_images', slug=image.product.slug)

def category_products(request, slug):
    """Pamja për produktet e një kategorie"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, availability='in_stock')
    
    return render(request, 'product/category_products.html', {
        'category': category,
        'products': products
    })

@login_required
def toggle_product_feature(request, slug):
    """Pamja për ndryshimin e statusit të veçantë të produktit"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    product = get_object_or_404(Product, slug=slug)
    product.is_featured = not product.is_featured
    product.save()
    
    return JsonResponse({
        'status': 'success',
        'is_featured': product.is_featured
    })

@login_required
def manage_products(request):
    """Pamja për menaxhimin e produkteve të fermerit"""
    if not hasattr(request.user, 'farmer_profile'):
        messages.error(request, 'Vetëm fermerët mund të aksesojnë këtë faqe.')
        return redirect('farmer:register')
    
    # Marrja e produkteve të fermerit
    products = Product.objects.filter(farmer=request.user.farmer_profile).order_by('-created_at')
    
    context = {
        'products': products,
        'farmer': request.user.farmer_profile,
    }
    
    return render(request, 'product/manage_products.html', context)
