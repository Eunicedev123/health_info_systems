from models import db
from models.program import Program
from datetime import datetime

class ProgramService:
    @staticmethod
    def create_program(program_data):
        """Create a new health program"""
        program = Program(
            name=program_data['name'],
            description=program_data.get('description', ''),
            active=program_data.get('active', True)
        )
        
        if 'start_date' in program_data:
            program.start_date = datetime.strptime(program_data['start_date'], '%Y-%m-%d').date()
        
        if 'end_date' in program_data:
            program.end_date = datetime.strptime(program_data['end_date'], '%Y-%m-%d').date()
        
        db.session.add(program)
        db.session.commit()
        return program
    
    @staticmethod
    def update_program(program_id, program_data):
        """Update an existing program"""
        program = Program.query.get(program_id)
        if not program:
            return None
        
        program.name = program_data.get('name', program.name)
        program.description = program_data.get('description', program.description)
        program.active = program_data.get('active', program.active)
        
        if 'start_date' in program_data:
            program.start_date = datetime.strptime(program_data['start_date'], '%Y-%m-%d').date()
        
        if 'end_date' in program_data:
            program.end_date = datetime.strptime(program_data['end_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        return program
    
    @staticmethod
    def get_program(program_id):
        """Get a program by ID"""
        return Program.query.get(program_id)
    
    @staticmethod
    def get_all_programs():
        """Get all programs"""
        return Program.query.all()
    
    @staticmethod
    def get_active_programs():
        """Get all active programs"""
        return Program.query.filter_by(active=True).all()