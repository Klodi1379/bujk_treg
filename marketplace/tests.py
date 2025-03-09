from django.test import TestCase
from django.urls import reverse
from product.models import Product, Category, Crop
from farmer.models import FarmerProfile, FarmLocation, CultivationMethod
from django.contrib.auth.models import User
from marketplace.models import Cart, CartItem, Order, OrderItem
from marketplace.forms import CheckoutForm

class GuestCheckoutTest(TestCase):
    def setUp(self):
        # Set up test data
        self.location = FarmLocation.objects.create(address='Test Address', city='Test City', region='Test Region')
        self.cultivation_method = CultivationMethod.objects.create(name='Test Method', description='Test Description')
        self.crop = Crop.objects.create(name='Test Crop')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.farmer_user = User.objects.create_user(username='farmer1', password='password')
        self.farmer_profile = FarmerProfile.objects.create(user=self.farmer_user, farm_name='Test Farm', location=self.location)
        self.product = Product.objects.create(
            farmer=self.farmer_profile,
            category=self.category,
            crop=self.crop,
            name='Test Product',
            slug='test-product',
            price=10.00,
            stock=100
        )

    def test_guest_checkout_success(self):
        # Initialize cart for guest user (no user associated)
        cart = Cart.objects.create() 
        
        # Add item to cart
        CartItem.objects.create(cart=cart, product=self.product, quantity=2, unit_price=self.product.price)

        # Prepare checkout form data for guest user
        checkout_data = {
            'guest_name': 'Test Guest',
            'guest_email': 'test_guest@example.com',
            'shipping_address': 'Guest Shipping Address',
            'shipping_city': 'Guest City',
            'shipping_phone': '123-123-1234',
            'payment_method': 'cash',
            'notes': 'Guest order notes',
        }

        # Simulate POST request to checkout view
        response = self.client.post(reverse('marketplace:checkout'), checkout_data)

        # Assertions
        self.assertEqual(response.status_code, 302) # Redirect to success page
        self.assertRedirects(response, reverse('marketplace:order_success', kwargs={'pk': Order.objects.last().pk}))

        # Check if order is created
        order = Order.objects.last()
        self.assertIsNotNone(order)
        self.assertIsNone(order.user) # Assert order is created for guest user (no user associated)
        self.assertEqual(order.guest_name, 'Test Guest') # Assert guest user info is saved
        self.assertEqual(order.guest_email, 'test_guest@example.com')
        self.assertEqual(order.total_amount, 20.00) # 2 items * $10.00 each

        # Check if cart is cleared
        cart = Cart.objects.get(id=cart.id) # Re-fetch cart
        self.assertFalse(cart.items.exists()) # Assert cart items are cleared

        # Check if stock is updated
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 98) # Initial stock - 2 items ordered
