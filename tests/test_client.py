import unittest
from datetime import date
from app import create_app
from models import db
from models.client import Client
from services.client_service import ClientService

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test client
        self.client_data = {
            'first_name': 'Test',
            'last_name': 'Client',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'phone': '1234567890',
            'email': 'test@example.com',
            'address': '123 Test St'
        }
        
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_client(self):
        """Test client creation"""
        client = ClientService.create_client(self.client_data)
        
        self.assertIsNotNone(client)
        self.assertEqual(client.first_name, 'Test')
        self.assertEqual(client.last_name, 'Client')
        self.assertEqual(client.date_of_birth, date(1990, 1, 1))
        self.assertEqual(client.gender, 'Male')
    
    def test_search_clients(self):
        """Test client search functionality"""
        # Create test clients
        ClientService.create_client(self.client_data)
        
        client_data2 = self.client_data.copy()
        client_data2['first_name'] = 'Jane'
        client_data2['last_name'] = 'Doe'
        ClientService.create_client(client_data2)
        
        # Search for clients
        results = ClientService.search_clients('Test')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].first_name, 'Test')
        
        results = ClientService.search_clients('Doe')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].last_name, 'Doe')
        
        # Test partial match
        results = ClientService.search_clients('e')
        self.assertEqual(len(results), 2)
    
    def test_client_to_dict(self):
        """Test client serialization to dictionary"""
        client = ClientService.create_client(self.client_data)
        
        client_dict = client.to_dict()
        self.assertEqual(client_dict['first_name'], 'Test')
        self.assertEqual(client_dict['last_name'], 'Client')
        self.assertEqual(client_dict['gender'], 'Male')
        self.assertIn('programs', client_dict)
        self.assertEqual(len(client_dict['programs']), 0)

if __name__ == '__main__':
    unittest.main()