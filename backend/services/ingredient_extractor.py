"""
Ingredient extraction service using NLP and regex
"""
import re
from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models.ingredient import Ingredient
except ImportError:
    try:
        from backend.models.ingredient import Ingredient
    except ImportError:
        Ingredient = None  # Optional import


class IngredientExtractor:
    """Service for extracting ingredients from recipe text"""
    
    def __init__(self):
        # Common ingredient patterns
        self.quantity_pattern = re.compile(
            r'(\d+[\s/]*\d*)\s*([a-zA-Z]+)?\s+(.+)',
            re.IGNORECASE
        )
        
        # Common units
        self.units = [
            'cup', 'cups', 'tbsp', 'tablespoon', 'tablespoons',
            'tsp', 'teaspoon', 'teaspoons', 'gram', 'grams', 'g',
            'kg', 'kilogram', 'kilograms', 'lb', 'lbs', 'pound', 'pounds',
            'oz', 'ounce', 'ounces', 'ml', 'milliliter', 'milliliters',
            'l', 'liter', 'liters', 'piece', 'pieces', 'clove', 'cloves',
            'bunch', 'bunches', 'can', 'cans', 'package', 'packages'
        ]
    
    def extract_from_html(self, soup):
        """
        Extract ingredients from HTML soup
        
        Args:
            soup: BeautifulSoup object
        
        Returns:
            List of ingredient dictionaries
        """
        ingredients = []
        
        # Try to find structured ingredient lists
        ingredient_selectors = [
            {'itemprop': 'recipeIngredient'},
            {'class': 'recipe-ingredient'},
            {'class': 'ingredients'},
            {'class': 'ingredient'},
            {'id': 'ingredients'},
            {'class': 'ingredient-list'}
        ]
        
        for selector in ingredient_selectors:
            elements = soup.find_all(attrs=selector)
            if elements:
                for elem in elements:
                    ingredient = self._parse_ingredient_text(elem.get_text())
                    if ingredient:
                        ingredients.append(ingredient)
                if ingredients:
                    break
        
        # If no structured list found, try to find lists
        if not ingredients:
            lists = soup.find_all(['ul', 'ol'])
            for ul in lists:
                items = ul.find_all('li')
                for item in items:
                    ingredient = self._parse_ingredient_text(item.get_text())
                    if ingredient:
                        ingredients.append(ingredient)
                if ingredients:
                    break
        
        # If still no ingredients, try to extract from paragraphs
        if not ingredients:
            paragraphs = soup.find_all('p')
            for p in paragraphs[:20]:  # Limit search
                text = p.get_text().lower()
                if 'ingredient' in text or 'recipe' in text:
                    # Try to extract from this paragraph
                    ingredient = self._parse_ingredient_text(p.get_text())
                    if ingredient:
                        ingredients.append(ingredient)
        
        return ingredients[:50]  # Limit to 50 ingredients
    
    def _parse_ingredient_text(self, text):
        """
        Parse ingredient text into structured format
        
        Args:
            text: Raw ingredient text (e.g., "2 cups flour")
        
        Returns:
            Dictionary with name, quantity, unit, category or None
        """
        if not text or len(text.strip()) < 3:
            return None
        
        text = text.strip()
        
        # Try to match quantity pattern
        match = self.quantity_pattern.match(text)
        
        if match:
            quantity = match.group(1).strip()
            unit = match.group(2).strip() if match.group(2) else ''
            ingredient_name = match.group(3).strip()
            
            # Clean up unit
            if unit.lower() in self.units:
                unit = unit.lower()
            else:
                # Unit might be part of ingredient name
                ingredient_name = f"{unit} {ingredient_name}".strip()
                unit = ''
            
            # Clean up ingredient name
            ingredient_name = self._clean_ingredient_name(ingredient_name)
            
            # Determine category
            category = self._categorize_ingredient(ingredient_name)
            
            return {
                'name': ingredient_name,
                'quantity': quantity,
                'unit': unit,
                'category': category
            }
        else:
            # No quantity found, treat entire text as ingredient name
            ingredient_name = self._clean_ingredient_name(text)
            
            if len(ingredient_name) < 2:
                return None
            
            return {
                'name': ingredient_name,
                'quantity': '1',
                'unit': '',
                'category': self._categorize_ingredient(ingredient_name)
            }
    
    def _clean_ingredient_name(self, name):
        """Clean and normalize ingredient name"""
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Remove common prefixes/suffixes
        name = re.sub(r'^(a|an|some|the)\s+', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+(to taste|as needed|optional)$', '', name, flags=re.IGNORECASE)
        
        # Capitalize first letter
        if name:
            name = name[0].upper() + name[1:].lower()
        
        return name.strip()
    
    def _categorize_ingredient(self, name):
        """Categorize ingredient based on name"""
        name_lower = name.lower()
        
        # Produce
        produce_keywords = ['tomato', 'onion', 'garlic', 'potato', 'carrot', 'lettuce',
                          'pepper', 'cucumber', 'spinach', 'broccoli', 'cauliflower']
        if any(keyword in name_lower for keyword in produce_keywords):
            return 'produce'
        
        # Dairy
        dairy_keywords = ['milk', 'cheese', 'butter', 'cream', 'yogurt', 'sour cream']
        if any(keyword in name_lower for keyword in dairy_keywords):
            return 'dairy'
        
        # Meat
        meat_keywords = ['beef', 'pork', 'lamb', 'steak', 'ground']
        if any(keyword in name_lower for keyword in meat_keywords):
            return 'meat'
        
        # Poultry
        poultry_keywords = ['chicken', 'turkey', 'duck']
        if any(keyword in name_lower for keyword in poultry_keywords):
            return 'poultry'
        
        # Seafood
        seafood_keywords = ['fish', 'salmon', 'shrimp', 'crab', 'lobster']
        if any(keyword in name_lower for keyword in seafood_keywords):
            return 'seafood'
        
        # Grains
        grain_keywords = ['rice', 'pasta', 'flour', 'bread', 'wheat']
        if any(keyword in name_lower for keyword in grain_keywords):
            return 'grains'
        
        # Spices
        spice_keywords = ['salt', 'pepper', 'cumin', 'turmeric', 'coriander', 'spice']
        if any(keyword in name_lower for keyword in spice_keywords):
            return 'spices'
        
        # Default
        return 'other'

