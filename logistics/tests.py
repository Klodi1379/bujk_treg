from django.test import TestCase
from .models import TransportCompany, Vehicle, Warehouse, Shipment
from django.contrib.auth.models import User
from datetime import datetime, timezone

class LogisticsModelTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')

        # Create a TransportCompany
        self.transport_company = TransportCompany.objects.create(
            name="Test Transport",
            contact_person="Test Contact",
            contact_email="test@transport.com",
            contact_phone="123-456-7890"
        )

        # Create a Vehicle
        self.vehicle = Vehicle.objects.create(
            company=self.transport_company,
            vehicle_type="truck",
            plate_number="TEST1234",
            capacity=10000,
            availability=True,
            model="Test Model",
            year=2023,
            last_maintenance=datetime.today().date(),
            next_maintenance=datetime.today().date(),
            insurance_expiry=datetime.today().date()
        )
        
        # Create a Warehouse
        self.warehouse = Warehouse.objects.create(
            company = self.transport_company,
            name="Test Warehouse",
            location="Test Location",
            address="123 Test St",
            capacity=50000,
            manager = "Test Manager",
            contact_phone = "123-456-7890"
        )

        # Create a Shipment
        self.shipment = Shipment.objects.create(
            company=self.transport_company,
            origin="Origin",
            destination="Destination",
            sender_name="Sender",
            sender_phone="111-111-1111",
            receiver_name="Receiver",
            receiver_phone="222-222-2222",
            departure_date = timezone.now(),
            estimated_arrival = timezone.now()
        )

    def test_transport_company_str(self):
        self.assertEqual(str(self.transport_company), "Test Transport")

    def test_vehicle_str(self):
        self.assertEqual(str(self.vehicle), "Truck - TEST1234")

    def test_warehouse_str(self):
        self.assertEqual(str(self.warehouse), "Test Warehouse - Test Location")

    def test_shipment_str(self):
        self.assertEqual(str(self.shipment), f"Shipment {self.shipment.tracking_number} - Origin to Destination")
