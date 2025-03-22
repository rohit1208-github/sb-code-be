# management/tests.py
from django.test import TestCase
from .models import Country, Branch

class CountryModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            name='Test Country',
            code='TST',
            is_active=True
        )
    
    def test_country_creation(self):
        self.assertEqual(self.country.name, 'Test Country')
        self.assertEqual(self.country.code, 'TST')
        self.assertTrue(self.country.is_active)
    
    def test_country_str(self):
        self.assertEqual(str(self.country), 'Test Country')

class BranchModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            name='Test Country',
            code='TST',
            is_active=True
        )
        self.branch = Branch.objects.create(
            name='Test Branch',
            country=self.country,
            address='123 Test St',
            phone='1234567890',
            email='test@example.com',
            is_active=True,
            has_online_ordering=True
        )
    
    def test_branch_creation(self):
        self.assertEqual(self.branch.name, 'Test Branch')
        self.assertEqual(self.branch.country, self.country)
        self.assertEqual(self.branch.address, '123 Test St')
        self.assertEqual(self.branch.phone, '1234567890')
        self.assertEqual(self.branch.email, 'test@example.com')
        self.assertTrue(self.branch.is_active)
        self.assertTrue(self.branch.has_online_ordering)
    
    def test_branch_str(self):
        self.assertEqual(str(self.branch), 'Test Branch (Test Country)')