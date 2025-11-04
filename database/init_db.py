"""
Initialize MongoDB database and collections
"""
from mongoengine import connect
from backend.config import Config
from backend.models.user import User
from backend.models.dish import Dish
from backend.models.recipe import Recipe
from backend.models.ingredient import Ingredient
from backend.models.grocery_list import GroceryList


def init_database():
    """Initialize database connection and create indexes"""
    print("Connecting to MongoDB...")
    connect(host=Config.MONGO_URI)
    print("Connected to MongoDB successfully!")
    
    # Create indexes for better performance
    print("Creating indexes...")
    
    # User indexes
    User.ensure_indexes()
    print("✓ User indexes created")
    
    # Dish indexes
    Dish.ensure_indexes()
    print("✓ Dish indexes created")
    
    # Recipe indexes
    Recipe.ensure_indexes()
    print("✓ Recipe indexes created")
    
    # Ingredient indexes
    Ingredient.ensure_indexes()
    print("✓ Ingredient indexes created")
    
    # Grocery list indexes
    GroceryList.ensure_indexes()
    print("✓ Grocery list indexes created")
    
    print("\nDatabase initialization complete!")


if __name__ == '__main__':
    init_database()

