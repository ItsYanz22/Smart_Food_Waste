"""
Dish and recipe routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import connect
from backend.models.dish import Dish
from backend.models.recipe import Recipe
from backend.config import Config

try:
    from backend.services.recipe_service import RecipeService
    from backend.ai_module.dish_recognizer import DishRecognizer
except ImportError:
    RecipeService = None
    DishRecognizer = None

bp = Blueprint('dish', __name__)

# Connect to MongoDB
connect(host=Config.MONGO_URI)

# Initialize services
if RecipeService and DishRecognizer:
    recipe_service = RecipeService()
    dish_recognizer = DishRecognizer()
else:
    from backend.services.recipe_service import RecipeService
    from backend.ai_module.dish_recognizer import DishRecognizer
    recipe_service = RecipeService()
    dish_recognizer = DishRecognizer()


@bp.route('/search', methods=['POST'])
@jwt_required()
def search_dish():
    """Search for dish and fetch recipe"""
    try:
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        
        if not dish_name:
            return jsonify({'error': 'Dish name is required'}), 400
        
        # Normalize dish name using AI module
        normalized_name = dish_recognizer.normalize_dish_name(dish_name)
        
        # Check if dish exists in database
        dish = Dish.objects(normalized_name=normalized_name).first()
        
        if dish and dish.recipe_id:
            # Fetch recipe from database
            recipe = Recipe.objects(id=dish.recipe_id).first()
            if recipe:
                recipe.times_accessed += 1
                recipe.save()
                dish.times_used += 1
                dish.save()
                return jsonify({
                    'dish': dish.to_dict(),
                    'recipe': recipe.to_dict(),
                    'from_cache': True
                }), 200
        
        # Fetch recipe from external API
        recipe_data = recipe_service.fetch_recipe(dish_name)
        
        if not recipe_data:
            return jsonify({'error': 'Recipe not found. Please try a different dish name.'}), 404
        
        # Create or update dish
        dish = Dish.objects(normalized_name=normalized_name).first()
        if not dish:
            dish = Dish(
                name=dish_name,
                normalized_name=normalized_name,
                servings=recipe_data.get('servings', 4)
            )
            dish.save()
        
        # Create or update recipe
        recipe = Recipe(
            dish_name=dish_name,
            source_url=recipe_data.get('source_url', ''),
            source_type=recipe_data.get('source_type', 'google_search'),
            servings=recipe_data.get('servings', 4),
            ingredients=recipe_data.get('ingredients', []),
            instructions=recipe_data.get('instructions', []),
            raw_data=recipe_data.get('raw_data', {})
        )
        recipe.save()
        
        # Link recipe to dish
        dish.recipe_id = str(recipe.id)
        dish.save()
        
        return jsonify({
            'dish': dish.to_dict(),
            'recipe': recipe.to_dict(),
            'from_cache': False
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """Get user's favorite dishes"""
    try:
        user_id = get_jwt_identity()
        from backend.models.user import User
        
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        favorite_dishes = []
        for dish_name in user.favorite_dishes:
            dish = Dish.objects(normalized_name=dish_recognizer.normalize_dish_name(dish_name)).first()
            if dish:
                favorite_dishes.append(dish.to_dict())
        
        return jsonify({'favorite_dishes': favorite_dishes}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    """Add dish to favorites"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        
        if not dish_name:
            return jsonify({'error': 'Dish name is required'}), 400
        
        from backend.models.user import User
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        normalized_name = dish_recognizer.normalize_dish_name(dish_name)
        
        if normalized_name not in user.favorite_dishes:
            user.favorite_dishes.append(normalized_name)
            user.save()
        
        return jsonify({'message': 'Dish added to favorites', 'favorite_dishes': user.favorite_dishes}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


