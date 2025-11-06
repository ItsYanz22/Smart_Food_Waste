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
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_password(password):
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        if User.objects(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.objects(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=username,
            email=email,
            household_size=data.get('household_size', '1'),
            user_type=data.get('user_type', 'household')
        )
        user.set_password(password)
        user.save()
        
        # Generate access token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """User login endpoint"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
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
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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


