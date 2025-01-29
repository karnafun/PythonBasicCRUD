from db import db
from datetime import datetime

class User(db.Model):
    """User model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    active = db.Column(db.Boolean, default=True)  # active status
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # "admin" or "user"

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = generate_password_hash(password)  
        self.role = role

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        """Convert the model instance into a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "city": self.city,
            "age": self.age,
            "phone_number": self.phone_number,
            "birth_date": self.birth_date,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None            
        }
