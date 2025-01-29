from db import db
from sqlalchemy.exc import SQLAlchemyError
from db.models import User
from datetime import datetime
from werkzeug.security import generate_password_hash


class DBManager:
    @staticmethod
    def create_user(data):
        """Creates a new user with optional fields, including password hashing and role assignment."""
        try:
            new_user = User(
                name=data.get("name"),
                city=data.get("city"),
                age=data.get("age"),
                phone_number=data.get("phone_number"),
                birth_date=data.get("birth_date"),
                role=data.get("role", "user"),  # Default role is 'user'
                password=generate_password_hash(data.get("password")),  # Hash the password
                active=True  # Default value is True
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_users():
        """Fetch all users."""
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_user_by_id(user_id):
        """Fetch a user by ID."""
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_user(user_id, data):
        """Update a user with new data, excluding the password."""
        try:
            user = User.query.get(user_id)
            if user:
                # Exclude password from being updated here
                for key, value in data.items():
                    if hasattr(user, key) and key != "password":
                        setattr(user, key, value)
                db.session.commit()
                return user
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_password(user_id, new_password):
        """Update a user's password separately, hashing it before storing."""
        try:
            user = User.query.get(user_id)
            if user:
                user.password = generate_password_hash(new_password)  # Hash the new password
                db.session.commit()
                return user
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def soft_delete_user(user_id):
        """Set active=False to delete (soft delete)."""
        try:
            user = User.query.get(user_id)
            if user:
                user.active = False
                db.session.commit()
                return user
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def hard_delete_user(user_id):
        """Permanently delete a user from the database."""
        try:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def toggle_user_active_status(user_id):
        """Toggle the active status of a user."""
        try:
            user = User.query.get(user_id)
            if user:
                # Toggle the 'active' status
                user.active = not user.active
                db.session.commit()
                return user
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def get_user_by_name(name):
        """Retrieve a user by username."""
        return User.query.filter_by(name=name).first()

    def check_password(user, password):
        """Check if the user's password is valid."""
        from werkzeug.security import check_password_hash
        return check_password_hash(user.password_hash, password)