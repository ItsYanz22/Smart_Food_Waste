"""
Recipe model for MongoDB
"""
from datetime import datetime
from mongoengine import Document, StringField, ListField, DictField, IntField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField


class IngredientItem(EmbeddedDocument):
    """Embedded document for recipe ingredients"""
    name = StringField(required=True)
    quantity = StringField(required=True)  # Store as string to handle fractions
    unit = StringField()  # e.g., 'cups', 'grams', 'tbsp'
    category = StringField()  # e.g., 'produce', 'dairy', 'meat'


class Recipe(Document):
    """Recipe model for storing recipe information"""
    dish_name = StringField(required=True, max_length=200)
    source_url = StringField()  # URL where recipe was fetched from
    source_type = StringField(choices=['google_search', 'spoonacular', 'edamam', 'manual'], default='google_search')
    
    # Recipe details
    servings = IntField(default=4)
    prep_time = IntField()  # in minutes
    cook_time = IntField()  # in minutes
    total_time = IntField()  # in minutes
    
    # Ingredients
    ingredients = ListField(EmbeddedDocumentField(IngredientItem), default=list)
    
    # Instructions (stored as list of strings)
    instructions = ListField(StringField(), default=list)
    
    # NLP processed fields
    summary = StringField()  # Recipe summary from NLP processing
    title = StringField()  # Recipe title from NLP processing
    
    # Raw recipe data (for debugging/reprocessing)
    raw_data = DictField()
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    times_accessed = IntField(default=0)
    
    meta = {
        'collection': 'recipes',
        'indexes': ['dish_name', 'source_url']
    }
    
    def to_dict(self):
        """Convert recipe to dictionary"""
        result = {
            'id': str(self.id),
            'dish_name': self.dish_name,
            'source_url': self.source_url,
            'source_type': self.source_type,
            'servings': self.servings,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'total_time': self.total_time,
            'ingredients': [
                {
                    'name': ing.name,
                    'quantity': ing.quantity,
                    'unit': ing.unit,
                    'category': ing.category
                }
                for ing in self.ingredients
            ],
            'instructions': self.instructions,
            'created_at': self.created_at.isoformat(),
            'times_accessed': self.times_accessed
        }
        
        # Add NLP fields if available (backward compatible)
        if self.summary:
            result['summary'] = self.summary
        if self.title:
            result['title'] = self.title
        
        return result


