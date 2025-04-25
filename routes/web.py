from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.client_service import ClientService
from services.program_service import ProgramService
from datetime import datetime

web = Blueprint('web', __name__)

@web.route('/')
def index():
    """Home page"""
    return render_template('index.html')

# Program Routes
@web.route('/programs')
def programs():
    """List all health programs"""
    programs = ProgramService.get_all_programs()
    return render_template('programs.html', programs=programs)

@web.route('/programs/add', methods=['GET', 'POST'])
def add_program():
    """Add a new health program"""
    if request.method == 'POST':
        program_data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'active': 'active' in request.form,
        }
        
        if request.form.get('start_date'):
            program_data['start_date'] = request.form['start_date']
            
        if request.form.get('end_date'):
            program_data['end_date'] = request.form['end_date']
            
        program = ProgramService.create_program(program_data)
        flash(f'Program "{program.name}" created successfully!', 'success')
        return redirect(url_for('web.programs'))
        
    return render_template('program_form.html', program=None)

@web.route('/programs/<int:program_id>/edit', methods=['GET', 'POST'])
def edit_program(program_id):
    """Edit an existing health program"""
    program = ProgramService.get_program(program_id)
    if not program:
        flash('Program not found', 'danger')
        return redirect(url_for('web.programs'))
    
    if request.method == 'POST':
        program_data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'active': 'active' in request.form,
        }
        
        if request.form.get('start_date'):
            program_data['start_date'] = request.form['start_date']
            
        if request.form.get('end_date'):
            program_data['end_date'] = request.form['end_date']
            
        program = ProgramService.update_program(program_id, program_data)
        flash(f'Program "{program.name}" updated successfully!', 'success')
        return redirect(url_for('web.programs'))
        
    return render_template('program_form.html', program=program)

# Client Routes
@web.route('/clients')
def clients():
    """List all clients"""
    search_term = request.args.get('search', '')
    if search_term:
        clients = ClientService.search_clients(search_term)
    else:
        clients = ClientService.get_all_clients()
    return render_template('clients.html', clients=clients, search_term=search_term)

@web.route('/clients/add', methods=['GET', 'POST'])
def add_client():
    """Add a new client"""
    if request.method == 'POST':
        client_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'date_of_birth': request.form['date_of_birth'],
            'gender': request.form['gender'],
            'phone': request.form.get('phone', ''),
            'email': request.form.get('email', ''),
            'address': request.form.get('address', '')
        }
        
        client = ClientService.create_client(client_data)
        flash(f'Client {client.first_name} {client.last_name} added successfully!', 'success')
        return redirect(url_for('web.clients'))
        
    return render_template('client_form.html', client=None)

@web.route('/clients/<int:client_id>')
def client_details(client_id):
    """View client details"""
    client = ClientService.get_client(client_id)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('web.clients'))
        
    all_programs = ProgramService.get_all_programs()
    return render_template('client_details.html', client=client, all_programs=all_programs)

@web.route('/clients/<int:client_id>/edit', methods=['GET', 'POST'])
def edit_client(client_id):
    """Edit an existing client"""
    client = ClientService.get_client(client_id)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('web.clients'))
    
    if request.method == 'POST':
        client_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'date_of_birth': request.form['date_of_birth'],
            'gender': request.form['gender'],
            'phone': request.form.get('phone', ''),
            'email': request.form.get('email', ''),
            'address': request.form.get('address', '')
        }
        
        client = ClientService.update_client(client_id, client_data)
        flash(f'Client {client.first_name} {client.last_name} updated successfully!', 'success')
        return redirect(url_for('web.client_details', client_id=client_id))
        
    return render_template('client_form.html', client=client)

@web.route('/clients/<int:client_id>/enroll', methods=['POST'])
def enroll_client(client_id):
    """Enroll client in a program"""
    program_id = request.form.get('program_id')
    if not program_id:
        flash('Program not selected', 'danger')
        return redirect(url_for('web.client_details', client_id=client_id))
    
    success = ClientService.enroll_client_in_program(client_id, program_id)
    if success:
        flash('Client enrolled in program successfully!', 'success')
    else:
        flash('Failed to enroll client in program', 'danger')
    
    return redirect(url_for('web.client_details', client_id=client_id))

@web.route('/clients/<int:client_id>/programs/<int:program_id>/remove', methods=['POST'])
def remove_from_program(client_id, program_id):
    """Remove client from a program"""
    success = ClientService.remove_client_from_program(client_id, program_id)
    if success:
        flash('Client removed from program successfully!', 'success')
    else:
        flash('Failed to remove client from program', 'danger')
    
    return redirect(url_for('web.client_details', client_id=client_id))