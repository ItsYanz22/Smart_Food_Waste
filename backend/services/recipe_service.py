"""
Recipe service for fetching recipes from external APIs
"""
import requests
import json
from bs4 import BeautifulSoup
from backend.config import Config
try:
    from backend.services.ingredient_extractor import IngredientExtractor
except ImportError:
    # Fallback if circular import
    IngredientExtractor = None


class RecipeService:
    """Service for fetching and parsing recipes"""
    
    def __init__(self):
        self.api_key = Config.GOOGLE_SEARCH_API_KEY
        self.search_engine_id = Config.GOOGLE_SEARCH_ENGINE_ID
        if IngredientExtractor:
            self.ingredient_extractor = IngredientExtractor()
        else:
            from backend.services.ingredient_extractor import IngredientExtractor
            self.ingredient_extractor = IngredientExtractor()
    
    def fetch_recipe(self, dish_name):
        """
        Fetch recipe from Google Search API
        
        Args:
            dish_name: Name of the dish to search for
        
        Returns:
            Dictionary containing recipe data or None if not found
        """
        try:
            # Search for recipe
            search_query = f"{dish_name} recipe"
            url = f"https://www.googleapis.com/customsearch/v1"
            
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': search_query,
                'num': 3  # Get top 3 results
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                # Fallback to Spoonacular if available
                return self._fetch_from_spoonacular(dish_name)
            
            search_results = response.json()
            
            if 'items' not in search_results or len(search_results['items']) == 0:
                return self._fetch_from_spoonacular(dish_name)
            
            # Try to parse first result
            for item in search_results['items']:
                recipe_data = self._parse_recipe_page(item.get('link', ''), dish_name)
                if recipe_data:
                    recipe_data['source_url'] = item.get('link', '')
                    recipe_data['source_type'] = 'google_search'
                    return recipe_data
            
            # If no recipe found, return None
            return None
        
        except Exception as e:
            print(f"Error fetching recipe: {str(e)}")
            return self._fetch_from_spoonacular(dish_name)
    
    def _parse_recipe_page(self, url, dish_name):
        """
        Parse recipe from a webpage
        
        Args:
            url: URL of the recipe page
            dish_name: Name of the dish
        
        Returns:
            Dictionary containing recipe data or None
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract ingredients using ingredient extractor
            ingredients = self.ingredient_extractor.extract_from_html(soup)
            
            # Extract instructions
            instructions = self._extract_instructions(soup)
            
            # Extract serving size
            servings = self._extract_servings(soup)
            
            if not ingredients:
                return None
            
            return {
                'dish_name': dish_name,
                'ingredients': ingredients,
                'instructions': instructions,
                'servings': servings,
                'raw_data': {
                    'url': url,
                    'html_preview': soup.get_text()[:500]  # First 500 chars
                }
            }
        
        except Exception as e:
            print(f"Error parsing recipe page: {str(e)}")
            return None
    
    def _extract_instructions(self, soup):
        """Extract cooking instructions from HTML"""
        instructions = []
        
        # Try common recipe instruction patterns
        instruction_selectors = [
            {'itemprop': 'recipeInstructions'},
            {'class': 'recipe-instructions'},
            {'class': 'instructions'},
            {'id': 'instructions'},
            {'class': 'recipe-steps'}
        ]
        
        for selector in instruction_selectors:
            elements = soup.find_all(attrs=selector)
            if elements:
                for elem in elements:
                    # Try to get ordered list items or paragraphs
                    steps = elem.find_all(['li', 'p', 'div'])
                    for step in steps:
                        text = step.get_text().strip()
                        if text and len(text) > 10:  # Filter out very short text
                            instructions.append(text)
                if instructions:
                    break
        
        # If no structured instructions found, try to extract from paragraphs
        if not instructions:
            paragraphs = soup.find_all('p')
            for p in paragraphs[:10]:  # Limit to first 10 paragraphs
                text = p.get_text().strip()
                if text and len(text) > 20:
                    instructions.append(text)
        
        return instructions[:20]  # Limit to 20 steps
    
    def _extract_servings(self, soup):
        """Extract serving size from HTML"""
        # Try to find serving information
        serving_selectors = [
            {'itemprop': 'recipeYield'},
            {'class': 'servings'},
            {'class': 'recipe-servings'},
            {'id': 'servings'}
        ]
        
        for selector in serving_selectors:
            elem = soup.find(attrs=selector)
            if elem:
                text = elem.get_text().strip()
                # Try to extract number
                import re
                numbers = re.findall(r'\d+', text)
                if numbers:
                    return int(numbers[0])
        
        # Default servings
        return 4
    
    def _fetch_from_spoonacular(self, dish_name):
        """Fallback to Spoonacular API if available"""
        if not Config.SPOONACULAR_API_KEY:
            return None
        
        try:
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
                'apiKey': Config.SPOONACULAR_API_KEY,
                'query': dish_name,
                'number': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    recipe_id = data['results'][0]['id']
                    # Get detailed recipe
                    detail_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                    detail_response = requests.get(
                        detail_url,
                        params={'apiKey': Config.SPOONACULAR_API_KEY},
                        timeout=10
                    )
                    
                    if detail_response.status_code == 200:
                        recipe_detail = detail_response.json()
                        ingredients = [
                            {
                                'name': ing.get('name', ''),
                                'quantity': str(ing.get('amount', '')),
                                'unit': ing.get('unit', ''),
                                'category': None
                            }
                            for ing in recipe_detail.get('extendedIngredients', [])
                        ]
                        
                        instructions = []
                        if 'analyzedInstructions' in recipe_detail:
                            for instruction in recipe_detail['analyzedInstructions']:
                                for step in instruction.get('steps', []):
                                    instructions.append(step.get('step', ''))
                        
                        return {
                            'dish_name': dish_name,
                            'ingredients': ingredients,
                            'instructions': instructions,
                            'servings': recipe_detail.get('servings', 4),
                            'source_type': 'spoonacular',
                            'source_url': recipe_detail.get('sourceUrl', '')
                        }
        
        except Exception as e:
            print(f"Error fetching from Spoonacular: {str(e)}")
        
        return None

