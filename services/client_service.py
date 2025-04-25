from datetime import datetime
from models import db
from models.client import Client
from models.program import Program

class ClientService:
    @staticmethod
    def create_client(client_data):
        """Create a new client in the system"""
        client = Client(
            first_name=client_data['first_name'],
            last_name=client_data['last_name'],
            date_of_birth=datetime.strptime(client_data['date_of_birth'], '%Y-%m-%d').date(),
            gender=client_data['gender'],
            phone=client_data.get('phone', ''),
            email=client_data.get('email', ''),
            address=client_data.get('address', '')
        )
        db.session.add(client)
        db.session.commit()
        return client
    
    @staticmethod
    def update_client(client_id, client_data):
        """Update an existing client"""
        client = Client.query.get(client_id)
        if not client:
            return None
        
        client.first_name = client_data.get('first_name', client.first_name)
        client.last_name = client_data.get('last_name', client.last_name)
        if 'date_of_birth' in client_data:
            client.date_of_birth = datetime.strptime(client_data['date_of_birth'], '%Y-%m-%d').date()
        client.gender = client_data.get('gender', client.gender)
        client.phone = client_data.get('phone', client.phone)
        client.email = client_data.get('email', client.email)
        client.address = client_data.get('address', client.address)
        
        db.session.commit()
        return client
    
    @staticmethod
    def get_client(client_id):
        """Get a client by ID"""
        return Client.query.get(client_id)
    
    @staticmethod
    def get_all_clients():
        """Get all clients"""
        return Client.query.all()
    
    @staticmethod
    def search_clients(search_term):
        """Search for clients by name"""
        return Client.query.filter(
            (Client.first_name.ilike(f'%{search_term}%')) | 
            (Client.last_name.ilike(f'%{search_term}%'))
        ).all()
    
    @staticmethod
    def enroll_client_in_program(client_id, program_id):
        """Enroll a client in a program"""
        client = Client.query.get(client_id)
        program = Program.query.get(program_id)
        
        if not client or not program:
            return False
        
        # Check if client is already enrolled
        if program in client.programs:
            return True  # Already enrolled
        
        client.programs.append(program)
        db.session.commit()
        return True
    
    @staticmethod
    def remove_client_from_program(client_id, program_id):
        """Remove a client from a program"""
        client = Client.query.get(client_id)
        program = Program.query.get(program_id)
        
        if not client or not program:
            return False
        
        if program in client.programs:
            client.programs.remove(program)
            db.session.commit()
            return True
        
        return False