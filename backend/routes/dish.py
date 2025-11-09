"""
Dish and recipe routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models.dish import Dish
    from models.recipe import Recipe
    from config import Config
    from services.recipe_service import RecipeService
    import sys
    # Add project root for ai_module
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from ai_module.dish_recognizer import DishRecognizer
except ImportError:
    try:
        from backend.models.dish import Dish
        from backend.models.recipe import Recipe
        from backend.config import Config
        from backend.services.recipe_service import RecipeService
        from backend.ai_module.dish_recognizer import DishRecognizer
    except ImportError:
        Dish = None
        Recipe = None
        Config = None
        RecipeService = None
        DishRecognizer = None

bp = Blueprint('dish', __name__)

# MongoDB connection is handled in app.py - no need to connect here

# Initialize services
if RecipeService and DishRecognizer:
    recipe_service = RecipeService()
    dish_recognizer = DishRecognizer()
else:
    print("Error: Could not import required services")


@bp.route('/search', methods=['POST'])
@jwt_required()
def search_dish():
    """Search for dish and fetch recipe"""
    try:
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        recipe_url = data.get('recipe_url', '').strip()
        
        # If URL is provided, extract recipe from URL
        if recipe_url:
            # Extract recipe from URL using recipe service
            recipe_data = recipe_service._parse_recipe_page(recipe_url, '')
            
            if not recipe_data:
                return jsonify({'error': 'Could not extract recipe from URL. Please try a different URL.'}), 404
            
            # Extract dish name from URL or use a default
            dish_name = recipe_data.get('dish_name', '')
            if not dish_name:
                dish_name = 'Custom Recipe'
            
            # Normalize dish name
            normalized_name = dish_recognizer.normalize_dish_name(dish_name)
            
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
                source_url=recipe_url,
                source_type='manual',
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


@bp.route('/extract-url', methods=['POST'])
@jwt_required()
def extract_recipe_from_url():
    """Extract recipe from a URL"""
    try:
        data = request.get_json()
        recipe_url = data.get('recipe_url', '').strip()
        
        if not recipe_url:
            return jsonify({'error': 'Recipe URL is required'}), 400
        
        # Parse recipe from URL
        recipe_data = recipe_service._parse_recipe_page(recipe_url, '')
        
        if not recipe_data:
            return jsonify({'error': 'Could not extract recipe from URL. Please try a different URL.'}), 404
        
        # Extract dish name from URL or use a default
        dish_name = recipe_data.get('dish_name', '')
        if not dish_name:
            # Try to extract from URL or use a generic name
            dish_name = 'Custom Recipe'
        
        # Normalize dish name
        normalized_name = dish_recognizer.normalize_dish_name(dish_name)
        
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
            source_url=recipe_url,
            source_type='manual',
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


@bp.route('/recipe/<recipe_id>/pdf', methods=['GET'])
@jwt_required()
def download_recipe_pdf(recipe_id):
    """Download recipe as PDF"""
    try:
        from services.pdf_generator import PDFGenerator
        
        recipe = Recipe.objects(id=recipe_id).first()
        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404
        
        # Create a temporary grocery list structure for PDF generation
        class TempGroceryList:
            def __init__(self, recipe):
                self.id = recipe.id
                self.dish_name = recipe.dish_name
                self.household_size = recipe.servings
                self.items = [
                    type('Item', (), {
                        'ingredient_name': ing.name,
                        'quantity': ing.quantity,
                        'unit': ing.unit,
                        'category': ing.category or 'other'
                    })() for ing in recipe.ingredients
                ]
                self.notes = f"Recipe from {recipe.source_url}" if recipe.source_url else ""
        
        temp_list = TempGroceryList(recipe)
        pdf_generator = PDFGenerator()
        pdf_path = pdf_generator.generate_pdf(temp_list)
        
        return jsonify({
            'pdf_url': pdf_path,
            'message': 'Recipe PDF generated successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """Get user's favorite dishes"""
    try:
        user_id = get_jwt_identity()
        try:
            from models.user import User
        except ImportError:
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


