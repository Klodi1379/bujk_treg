from django.urls import path
from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'product'

from . import views

app_name = 'product'

urlpatterns = [
    # Listimi dhe kërkimi i produkteve
    path('', views.ProductListView.as_view(), name='list'),
    path('menaxho/', views.manage_products, name='manage_products'),
    path('kategoria/<slug:slug>/', views.category_products, name='category_products'),

    # Detajet dhe menaxhimi i produkteve
    path('shto/', views.add_product, name='add'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('<slug:slug>/perditeso/', views.ProductUpdateView.as_view(), name='update'),
    path('<slug:slug>/fshi/', views.ProductDeleteView.as_view(), name='delete'),

    # Menaxhimi i imazheve
    path('<slug:slug>/imazhet/', views.manage_product_images, name='manage_images'),
    path('imazh/<int:pk>/fshi/', views.delete_product_image, name='delete_image'),

    # Vlerësimet dhe pyetjet
    path('<slug:slug>/vlereso/', views.add_review, name='add_review'),
    path('<slug:slug>/pyet/', views.add_question, name='add_question'),
    path('pyetje/<int:pk>/pergjigju/', views.answer_question, name='answer_question'),

    # Veçoritë e produktit
    path('<slug:slug>/toggle-feature/', views.toggle_product_feature, name='toggle_feature'),

    # API endpoints për AJAX
    path('api/products/', views.ProductListView.as_view(
        template_name='product/product_list_partial.html'
    ), name='api_product_list'),
]
