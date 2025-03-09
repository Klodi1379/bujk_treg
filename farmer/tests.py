from django.test import TestCase
from django.contrib.auth.models import User
from .models import FarmLocation, CultivationMethod, Certification, Crop, FarmerProfile, FarmerCrop, ProductionLog
from datetime import date

class FarmerModelTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')

        # Create a FarmLocation
        self.location = FarmLocation.objects.create(
            latitude=40.7128,
            longitude=-74.0060,
            address="New York, NY",
            region="NY",
            city="New York",
            country="USA"  # Added country field, as it's not nullable by default
        )

        # Create a CultivationMethod
        self.method = CultivationMethod.objects.create(name="Organic")

        # Create a Certification
        self.certification = Certification.objects.create(
            name="USDA Organic",
            issuing_organization="USDA",
            document="path/to/document.pdf",
            issue_date = date(2023,1,1),
            expiry_date = date(2024,1,1)
        )

        # Create a Crop
        self.crop = Crop.objects.create(name="Tomato")

        # Create a FarmerProfile
        self.profile = FarmerProfile.objects.create(
            user=self.user,
            farm_name="Test Farm",
            location=self.location
        )
        self.profile.cultivation_methods.add(self.method)
        self.profile.certifications.add(self.certification)


        # Create a FarmerCrop
        self.farmer_crop = FarmerCrop.objects.create(
            farmer=self.profile,
            crop=self.crop,
            cultivation_method=self.method,
            land_area = 1.5
        )

        # Create a ProductionLog
        self.production_log = ProductionLog.objects.create(
            farmer=self.profile,
            crop=self.crop,
            activity_type="fertilizing",
            date=date(2024, 2, 1),
            description="Applied organic fertilizer",
        )

    def test_farm_location_str(self):
        self.assertEqual(str(self.location), "New York, NY, New York, USA")

    def test_cultivation_method_str(self):
        self.assertEqual(str(self.method), "Organic")

    def test_certification_str(self):
        self.assertEqual(str(self.certification), "USDA Organic (USDA)")

    def test_crop_str(self):
        self.assertEqual(str(self.crop), "Tomato")

    def test_farmer_profile_str(self):
        self.assertEqual(str(self.profile), "Test Farm (testuser)")

    def test_farmer_profile_full_address(self):
        self.assertEqual(self.profile.full_address, "New York, NY, New York, USA")

    def test_farmer_crop_str(self):
        self.assertEqual(str(self.farmer_crop), "Tomato - Test Farm")

    def test_production_log_str(self):
        self.assertEqual(str(self.production_log), "Plehërim - Tomato - 2024-02-01")
