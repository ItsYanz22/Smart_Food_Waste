"""
User profile and preferences routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import connect
from backend.models.user import User
from backend.config import Config

bp = Blueprint('user', __name__)

# Connect to MongoDB
connect(host=Config.MONGO_URI)


@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'household_size' in data:
            user.household_size = str(data['household_size'])
        
        if 'dietary_restrictions' in data:
            user.dietary_restrictions = data['dietary_restrictions']
        
        if 'preferred_stores' in data:
            user.preferred_stores = data['preferred_stores']
        
        if 'user_type' in data:
            if data['user_type'] in ['household', 'restaurant', 'grocery_shop']:
                user.user_type = data['user_type']
        
        user.save()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

