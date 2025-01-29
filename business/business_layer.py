from db.db_manager import DBManager


class BusinessLayer:
    @staticmethod
    def create_user(data):
        """Validate and create a new user with password and role."""
        # Basic validation for required fields
        if not data.get("name"):
            raise ValueError("Name is required")
        if not data.get("password"):
            raise ValueError("Password is required")

        if "role" not in data:
            data["role"] = "user"

        user = DBManager.create_user(data)
        return user

    def authenticate_user(name, password):
        """Authenticate a user by username and password."""
        # Get the user from the db_manager
        user = DBManager.get_user_by_name(name)
        
        if user and DBManager.check_password(user, password):
            return user
        return None

    @staticmethod
    def fetch_all_users():
        """Fetch all users from the database."""
        return DBManager.get_users()

    @staticmethod
    def fetch_user_by_id(user_id):
        """Fetch a single user by ID."""
        return DBManager.get_user_by_id(user_id)

    @staticmethod
    def update_user(user_id, data):
        """Validate and update a user (excluding password)."""
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")

        # Ensure password is not updated here
        if "password" in data:
            raise ValueError("Password cannot be updated using this method")

        # Update the user in DB
        user = DBManager.update_user(user_id, data)
        return user

    @staticmethod
    def update_user_password(user_id, new_password):
        """Validate and update a user's password separately."""
        if not new_password:
            raise ValueError("New password is required")
        if len(new_password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        user = DBManager.update_password(user_id, new_password)
        return user

    @staticmethod
    def soft_delete_user(user_id):
        """Soft delete a user (set active=False)."""
        user = DBManager.soft_delete_user(user_id)
        return user

    @staticmethod
    def hard_delete_user(user_id):
        """Hard delete a user (delete from database)."""
        success = DBManager.hard_delete_user(user_id)
        return success

    @staticmethod
    def toggle_user_active_status(user_id):
        """Toggle the active status of a user."""
        user = DBManager.toggle_user_active_status(user_id)
        return user
