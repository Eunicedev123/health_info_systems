# Health Information System

A comprehensive web application for managing healthcare clients and programs. This system allows healthcare providers to register clients, create health programs, and manage enrollments efficiently.

## Features

- **Client Management**: Register and manage client profiles with personal information
- **Program Management**: Create and manage health programs (TB, Malaria, HIV, etc.)
- **Enrollment Management**: Enroll clients in multiple health programs
- **Search Functionality**: Quickly find clients in the system
- **RESTful API**: Access client and program data programmatically
- **Secure Authentication**: API endpoints protected with JWT authentication

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLAlchemy ORM with SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **API Security**: JWT Authentication

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/health_info_system.git
   cd health_info_system
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set environment variables (optional):
   ```
   # For development
   set FLASK_ENV=development
   # For JWT authentication
   set JWT_SECRET_KEY=your-secret-key
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Access the application at `http://localhost:5000`

## API Documentation

The system exposes RESTful API endpoints for integration with other systems:

- `GET /api/health` - Health check endpoint
- `GET /api/clients` - List all clients
- `GET /api/clients/{id}` - Get specific client details
- `POST /api/clients` - Create a new client
- `PUT /api/clients/{id}` - Update client information
- `GET /api/clients/{id}/programs` - List programs a client is enrolled in
- `POST /api/clients/{id}/programs/{program_id}` - Enroll client in a program
- `DELETE /api/clients/{id}/programs/{program_id}` - Remove client from a program
- `GET /api/programs` - List all health programs
- `GET /api/programs/{id}` - Get specific program details
- `POST /api/programs` - Create a new program
- `PUT /api/programs/{id}` - Update program information

All API endpoints require authentication with a JWT token in the Authorization header.

## Security Considerations

- API endpoints are protected with JWT authentication
- Passwords and sensitive data are not stored in plaintext
- Input validation is performed to prevent injection attacks

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
