"""
Authentication routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models.user import User
    from config import Config
    from utils.validators import validate_email, validate_password
except ImportError:
    from backend.models.user import User
    from backend.config import Config
    from backend.utils.validators import validate_email, validate_password

bp = Blueprint('auth', __name__)

# MongoDB connection is handled in app.py - no need to connect here


@bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    """User registration endpoint"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        origin = request.headers.get('Origin', 'http://localhost:8000')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    try:
        # Get JSON data
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip() if data.get('username') else ''
        email = data.get('email', '').strip().lower() if data.get('email') else ''
        password = data.get('password', '') if data.get('password') else ''
        household_size = data.get('household_size', '1')
        
        # Validate required fields
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password
        if not validate_password(password):
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        if User.objects(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.objects(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        try:
            user = User(
                username=username,
                email=email,
                household_size=str(household_size) if household_size else '1',
                user_type=data.get('user_type', 'household')
            )
            user.set_password(password)
            user.save()
            
            # Generate access token
            access_token = create_access_token(identity=str(user.id))
            
            # Add CORS headers to response
            response = jsonify({
                'message': 'User registered successfully',
                'access_token': access_token,
                'user': user.to_dict()
            })
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', 'http://localhost:8000'))
            return response, 201
        except Exception as db_error:
            # Handle duplicate key errors
            if 'duplicate' in str(db_error).lower() or 'E11000' in str(db_error):
                if 'username' in str(db_error):
                    return jsonify({'error': 'Username already exists'}), 400
                elif 'email' in str(db_error):
                    return jsonify({'error': 'Email already exists'}), 400
            raise db_error
    
    except Exception as e:
        error_msg = str(e)
        print(f"Registration error: {error_msg}")  # Debug logging
        # Return user-friendly error message
        if 'already exists' in error_msg.lower() or 'duplicate' in error_msg.lower():
            return jsonify({'error': 'Username or email already exists'}), 400
        return jsonify({'error': error_msg or 'Registration failed. Please try again.'}), 500


@bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """User login endpoint"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        origin = request.headers.get('Origin', 'http://localhost:8000')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    try:
        # Get JSON data
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip() if data.get('username') else ''
        password = data.get('password', '') if data.get('password') else ''
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Find user by username or email
        user = User.objects(username=username).first()
        if not user:
            user = User.objects(email=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is inactive'}), 403
        
        # Generate access token
        access_token = create_access_token(identity=str(user.id))
        
        # Add CORS headers to response
        response = jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        })
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', 'http://localhost:8000'))
        return response, 200
    
    except Exception as e:
        error_msg = str(e)
        print(f"Login error: {error_msg}")  # Debug logging
        return jsonify({'error': error_msg or 'Login failed. Please check your credentials.'}), 500


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


