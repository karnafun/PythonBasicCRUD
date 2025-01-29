# utils/auth.py
import jwt
from functools import wraps
from flask import request, jsonify,current_app
import datetime  # Importing the datetime module
from db.db_manager import DBManager



def generate_jwt_token(user):
    try:
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expiry time
        }
        # Use your secret key and algorithm for JWT encoding
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
        return token
    except Exception as e:
        print(e)
        return None


def decode_auth_token(auth_token):
    try:
        decoded = jwt.decode(auth_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        print("decoded token: "+ str(decoded["user_id"]))
        return  DBManager.get_user_by_id(decoded["user_id"])
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token



def get_authenticated_user():
    """
    Retrieves the authenticated user.
    Example: decode the auth token and return the user object.
    """
    auth_token = request.headers.get('Authorization')
    if auth_token:
        token = auth_token.split(" ")[1]  # This splits the string at space and takes the token part

        # Logic to decode the token and retrieve the user (this can vary depending on your authentication system)
        # For example, decode token and fetch user
        return decode_auth_token(token)
    return None

def auth_required(role=None):
    """
    Decorator to enforce authentication and optional role-based access.
    If role is provided, only users with that role will have access.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_user = get_authenticated_user()  # Directly calling the function in the same file
            if not auth_user:
                return jsonify({"error": "Unauthorized"}), 401

            if role and auth_user.role not in role:
                print("unknown role" + str(auth_user.role))
                return jsonify({"error": "Forbidden"}), 403

            return f(auth_user, *args, **kwargs)
        return decorated_function
    return decorator
