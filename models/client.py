from datetime import datetime
from . import db

# Association table for many-to-many relationship between clients and programs
client_program = db.Table(
    'client_program',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('program_id', db.Integer, db.ForeignKey('program.id'), primary_key=True),
    db.Column('enrollment_date', db.DateTime, default=datetime.utcnow)
)

class Client(db.Model):
    """Client model for storing patient information"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many-to-many relationship with programs
    programs = db.relationship('Program', secondary=client_program, 
                              backref=db.backref('clients', lazy='dynamic'))
    
    def __repr__(self):
        return f"<Client {self.id}: {self.first_name} {self.last_name}>"
    
    def to_dict(self):
        """Convert client object to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'programs': [program.to_dict_basic() for program in self.programs],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def to_dict_basic(self):
        """Convert client object to basic dictionary without programs"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender
        }