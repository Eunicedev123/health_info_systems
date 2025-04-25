import unittest
from datetime import date
from app import create_app
from models import db
from models.program import Program
from services.program_service import ProgramService

class ProgramTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test program data
        self.program_data = {
            'name': 'Test Program',
            'description': 'This is a test program',
            'start_date': '2025-01-01',
            'active': True
        }
        
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_program(self):
        """Test program creation"""
        program = ProgramService.create_program(self.program_data)
        
        self.assertIsNotNone(program)
        self.assertEqual(program.name, 'Test Program')
        self.assertEqual(program.description, 'This is a test program')
        self.assertEqual(program.start_date, date(2025, 1, 1))
        self.assertTrue(program.active)
    
    def test_update_program(self):
        """Test program update"""
        program = ProgramService.create_program(self.program_data)
        
        update_data = {
            'name': 'Updated Program',
            'active': False
        }
        
        updated_program = ProgramService.update_program(program.id, update_data)
        
        self.assertEqual(updated_program.name, 'Updated Program')
        self.assertFalse(updated_program.active)
        # Description should remain unchanged
        self.assertEqual(updated_program.description, 'This is a test program')
    
    def test_get_active_programs(self):
        """Test getting only active programs"""
        # Create an active program
        ProgramService.create_program(self.program_data)
        
        # Create an inactive program
        inactive_program = self.program_data.copy()
        inactive_program['name'] = 'Inactive Program'
        inactive_program['active'] = False
        ProgramService.create_program(inactive_program)
        
        # Get active programs
        active_programs = ProgramService.get_active_programs()
        
        self.assertEqual(len(active_programs), 1)
        self.assertEqual(active_programs[0].name, 'Test Program')
        
        # All programs should be 2
        all_programs = ProgramService.get_all_programs()
        self.assertEqual(len(all_programs), 2)

if __name__ == '__main__':
    unittest.main()