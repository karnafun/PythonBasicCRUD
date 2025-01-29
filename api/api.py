from flask import Blueprint, jsonify, request
from business.business_layer import BusinessLayer
from utils.auth import auth_required, generate_jwt_token

# Create a Blueprint for the API
api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return a JWT token."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Assuming you have a method in BusinessLayer to authenticate users
    user = BusinessLayer.authenticate_user(username, password)
    if user:
        # Generate JWT token
        token = generate_jwt_token(user)
        return jsonify({"token": token, "user":user.to_dict()}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@api_blueprint.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")  

    new_user = BusinessLayer.create_user(username, password, role)
    if new_user:
        token = generate_jwt_token(new_user)
        return jsonify({"token": token}), 201
    else:
        return jsonify({"error": "User registration failed"}), 400

@api_blueprint.route("/users", methods=["GET"])
@auth_required(role=["user", "admin"])  
def get_users(auth_user):
    """Fetch all users. Admin gets all users; regular users get only themselves."""
    if auth_user.role == "admin":
        users = BusinessLayer.fetch_all_users()
    else:
        users = [BusinessLayer.fetch_user_by_id(auth_user.id)] 
    
    return jsonify([user.to_dict() for user in users]), 200

@api_blueprint.route("/users/<int:user_id>", methods=["GET"])
@auth_required(role=["user", "admin"])  
def get_user(auth_user, user_id):
    """Fetch a single user. Regular users can only get themselves."""
    if auth_user.role != "admin" and auth_user.id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    user = BusinessLayer.fetch_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@api_blueprint.route("/users", methods=["POST"])
@auth_required(role="admin")  
def create_user(auth_user):
    """Create a new user. Admin-only."""
    data = request.get_json()
    try:
        new_user = BusinessLayer.create_user(data)
        return jsonify(new_user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route("/users/<int:user_id>", methods=["PUT"])
@auth_required(role=["user", "admin"])  
def update_user(auth_user, user_id):
    """Update a user. Admin can update anyone; users can only update themselves."""
    if auth_user.role != "admin" and auth_user.id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    updated_user = BusinessLayer.update_user(user_id, data)
    if updated_user:
        return jsonify(updated_user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@api_blueprint.route("/users/<int:user_id>/soft_delete", methods=["DELETE"])
@auth_required(role=["user", "admin"])  
def soft_delete_user(auth_user, user_id):
    """Soft delete a user. Admin can deactivate anyone; users can deactivate only themselves."""
    if auth_user.role != "admin" and auth_user.id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    user = BusinessLayer.soft_delete_user(user_id)
    if user:
        return jsonify({"message": "User deactivated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@api_blueprint.route("/users/<int:user_id>/hard_delete", methods=["DELETE"])
@auth_required(role="admin")  
def hard_delete_user(auth_user, user_id):
    """Hard delete a user. Admin-only."""
    success = BusinessLayer.hard_delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@api_blueprint.route("/users/<int:user_id>/toggle_active", methods=["PATCH"])
@auth_required() 
def toggle_user_active_status(auth_user, user_id):
    """Toggle user active status. Admin can toggle anyone; users can only toggle themselves."""
    if auth_user.role != "admin" and auth_user.id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    user = BusinessLayer.toggle_user_active_status(user_id)
    if user:
        status = "activated" if user.active else "deactivated"
        return jsonify({"message": f"User successfully {status}"}), 200
    return jsonify({"error": "User not found"}), 404

@api_blueprint.route("/users/me", methods=["GET"])
@auth_required()
def get_user_info(auth_user):
    return jsonify({
        "name": auth_user.name,
        "city": auth_user.city,
        "age": auth_user.age,
        "phone_number": auth_user.phone_number,
        "birth_date": auth_user.birth_date
    })

@api_blueprint.route("/users/me", methods=["PUT"])
@auth_required()
def update_user_info(auth_user):
    data = request.json
    auth_user.name = data.get('name', auth_user.name)
    auth_user.city = data.get('city', auth_user.city)
    auth_user.age = data.get('age', auth_user.age)
    auth_user.phone_number = data.get('phone_number', auth_user.phone_number)
    auth_user.birth_date = data.get('birth_date', auth_user.birth_date)

    db.session.commit()

    return jsonify({"success": True, "message": "User info updated."})