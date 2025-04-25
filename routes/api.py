from flask import Blueprint, jsonify, request
from services.client_service import ClientService
from services.program_service import ProgramService
import jwt
import datetime
import os

api = Blueprint('api', __name__, url_prefix='/api')

# Simple API authentication middleware
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Authentication token is missing!'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            jwt.decode(token, os.environ.get('JWT_SECRET_KEY', 'dev-key'), algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid authentication token!'}), 401
            
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated

@api.route('/health')
def health_check():
    """API health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Health Information System API is running',
        'timestamp': datetime.datetime.utcnow().isoformat()
    })

# Client API endpoints
@api.route('/clients', methods=['GET'])
@token_required
def get_clients():
    """Get all clients or search for clients"""
    search_term = request.args.get('search', '')
    if search_term:
        clients = ClientService.search_clients(search_term)
    else:
        clients = ClientService.get_all_clients()
    
    return jsonify({
        'count': len(clients),
        'clients': [client.to_dict_basic() for client in clients]
    })

@api.route('/clients/<int:client_id>', methods=['GET'])
@token_required
def get_client(client_id):
    """Get a specific client profile"""
    client = ClientService.get_client(client_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    
    return jsonify(client.to_dict())

@api.route('/clients', methods=['POST'])
@token_required
def create_client():
    """Create a new client"""
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'date_of_birth', 'gender']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    client = ClientService.create_client(data)
    return jsonify({
        'message': 'Client created successfully',
        'client': client.to_dict()
    }), 201

@api.route('/clients/<int:client_id>', methods=['PUT'])
@token_required
def update_client(client_id):
    """Update a client"""
    data = request.get_json()
    client = ClientService.update_client(client_id, data)
    
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    
    return jsonify({
        'message': 'Client updated successfully',
        'client': client.to_dict()
    })

@api.route('/clients/<int:client_id>/programs', methods=['GET'])
@token_required
def get_client_programs(client_id):
    """Get all programs a client is enrolled in"""
    client = ClientService.get_client(client_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    
    return jsonify({
        'client_id': client_id,
        'client_name': f"{client.first_name} {client.last_name}",
        'programs': [program.to_dict_basic() for program in client.programs]
    })

@api.route('/clients/<int:client_id>/programs/<int:program_id>', methods=['POST'])
@token_required
def enroll_client(client_id, program_id):
    """Enroll a client in a program"""
    success = ClientService.enroll_client_in_program(client_id, program_id)
    
    if not success:
        return jsonify({'message': 'Failed to enroll client'}), 400
    
    return jsonify({'message': 'Client enrolled successfully'})

@api.route('/clients/<int:client_id>/programs/<int:program_id>', methods=['DELETE'])
@token_required
def remove_from_program(client_id, program_id):
    """Remove a client from a program"""
    success = ClientService.remove_client_from_program(client_id, program_id)
    
    if not success:
        return jsonify({'message': 'Failed to remove client from program'}), 400
    
    return jsonify({'message': 'Client removed from program successfully'})

# Program API endpoints
@api.route('/programs', methods=['GET'])
@token_required
def get_programs():
    """Get all programs"""
    active_only = request.args.get('active', '').lower() == 'true'
    
    if active_only:
        programs = ProgramService.get_active_programs()
    else:
        programs = ProgramService.get_all_programs()
    
    return jsonify({
        'count': len(programs),
        'programs': [program.to_dict() for program in programs]
    })

@api.route('/programs/<int:program_id>', methods=['GET'])
@token_required
def get_program(program_id):
    """Get a specific program"""
    program = ProgramService.get_program(program_id)
    if not program:
        return jsonify({'message': 'Program not found'}), 404
    
    return jsonify(program.to_dict())

@api.route('/programs', methods=['POST'])
@token_required
def create_program():
    """Create a new program"""
    data = request.get_json()
    
    if 'name' not in data:
        return jsonify({'message': 'Program name is required'}), 400
    
    program = ProgramService.create_program(data)
    return jsonify({
        'message': 'Program created successfully',
        'program': program.to_dict()
    }), 201

@api.route('/programs/<int:program_id>', methods=['PUT'])
@token_required
def update_program(program_id):
    """Update a program"""
    data = request.get_json()
    program = ProgramService.update_program(program_id, data)
    
    if not program:
        return jsonify({'message': 'Program not found'}), 404
    
    return jsonify({
        'message': 'Program updated successfully',
        'program': program.to_dict()
    })