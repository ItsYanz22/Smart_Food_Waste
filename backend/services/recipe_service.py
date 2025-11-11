"""
Recipe service for fetching recipes from external APIs
"""
import requests
import json
from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import Config
try:
    from config import Config
except ImportError:
    try:
        from backend.config import Config
    except ImportError:
        Config = None

# Try to import IngredientExtractor
_ingredient_extractor_class = None
try:
    from services.ingredient_extractor import IngredientExtractor
    _ingredient_extractor_class = IngredientExtractor
except ImportError:
    try:
        from backend.services.ingredient_extractor import IngredientExtractor
        _ingredient_extractor_class = IngredientExtractor
    except ImportError:
        _ingredient_extractor_class = None

# Try to import NLPProcessor
_nlp_processor_class = None
try:
    import sys
    import os
    # Add project root for ai_module
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from ai_module.nlp_processor import NLPProcessor
    _nlp_processor_class = NLPProcessor
except ImportError:
    try:
        from backend.ai_module.nlp_processor import NLPProcessor
        _nlp_processor_class = NLPProcessor
    except ImportError:
        _nlp_processor_class = None


class RecipeService:
    """Service for fetching and parsing recipes"""
    
    def __init__(self):
        # Get API keys
        if Config:
            self.api_key = Config.GOOGLE_SEARCH_API_KEY
            self.search_engine_id = Config.GOOGLE_SEARCH_ENGINE_ID
        else:
            from dotenv import load_dotenv
            load_dotenv()
            self.api_key = os.getenv('GOOGLE_SEARCH_API_KEY', '')
            self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')
        
        # Initialize ingredient extractor
        if _ingredient_extractor_class:
            try:
                self.ingredient_extractor = _ingredient_extractor_class()
            except Exception as e:
                print(f"Warning: Could not initialize IngredientExtractor: {e}")
                self.ingredient_extractor = None
        else:
            print("Warning: IngredientExtractor not available - recipe parsing may be limited")
            self.ingredient_extractor = None
        
        # Initialize NLP processor
        if _nlp_processor_class:
            try:
                self.nlp_processor = _nlp_processor_class()
            except Exception as e:
                print(f"Warning: Could not initialize NLPProcessor: {e}")
                self.nlp_processor = None
        else:
            print("Warning: NLPProcessor not available - NLP processing will be skipped")
            self.nlp_processor = None
    
    def fetch_recipe(self, dish_name):
        """
        Fetch recipe from Spoonacular API (primary) or Google Search (fallback)
        
        Args:
            dish_name: Name of the dish to search for
        
        Returns:
            Dictionary containing recipe data or None if not found
        """
        # Try Spoonacular API first (more reliable, structured data)
        recipe_data = self._fetch_from_spoonacular(dish_name)
        if recipe_data:
            return recipe_data
        
        # Fallback to Google Search + web scraping only if Spoonacular fails
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
                return None
            
            search_results = response.json()
            
            if 'items' not in search_results or len(search_results['items']) == 0:
                return None
            
            # Try to parse first result
            for item in search_results['items']:
                recipe_data = self._parse_recipe_page(item.get('link', ''), dish_name)
                if recipe_data:
                    recipe_data['source_url'] = item.get('link', '')
                    recipe_data['source_type'] = 'google_search'
                    return recipe_data
            
            return None
        
        except Exception as e:
            print(f"Error fetching recipe: {str(e)}")
            return None
    
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
            
            # Get raw HTML content for NLP processing
            raw_html_content = str(soup)
            raw_text_content = soup.get_text(separator='\n', strip=True)
            
            # Process with NLP model if available
            nlp_processed = None
            if self.nlp_processor:
                try:
                    # Use HTML content for better structure extraction
                    nlp_processed = self.nlp_processor.process_recipe_text(raw_html_content)
                except Exception as e:
                    print(f"Warning: NLP processing failed: {e}")
                    # Fallback to text content
                    try:
                        nlp_processed = self.nlp_processor.process_recipe_text(raw_text_content)
                    except Exception as e2:
                        print(f"Warning: NLP processing with text also failed: {e2}")
            
            # Extract ingredients - prefer NLP processed, fallback to extractor
            if nlp_processed and nlp_processed.get('ingredients'):
                ingredients = nlp_processed['ingredients']
            elif self.ingredient_extractor:
                ingredients = self.ingredient_extractor.extract_from_html(soup)
            else:
                # Fallback: basic ingredient extraction
                ingredients = self._basic_ingredient_extraction(soup)
            
            # Extract instructions - prefer NLP processed, fallback to extractor
            if nlp_processed and nlp_processed.get('steps'):
                instructions = nlp_processed['steps']
            else:
                instructions = self._extract_instructions(soup)
            
            # Extract serving size
            servings = self._extract_servings(soup)
            
            # Use NLP title if available, otherwise use dish_name
            recipe_title = dish_name
            if nlp_processed and nlp_processed.get('title'):
                recipe_title = nlp_processed['title']
            
            if not ingredients:
                return None
            
            result = {
                'dish_name': recipe_title or dish_name,
                'ingredients': ingredients,
                'instructions': instructions,
                'servings': servings,
                'raw_data': {
                    'url': url,
                    'html_preview': soup.get_text()[:500],  # First 500 chars
                    'nlp_processed': nlp_processed  # Store NLP processed data
                }
            }
            
            # Add summary if available from NLP
            if nlp_processed and nlp_processed.get('summary'):
                result['summary'] = nlp_processed['summary']
            
            return result
        
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
        """Fetch recipe from Spoonacular API (primary method)"""
        spoonacular_key = ''
        if Config:
            spoonacular_key = Config.SPOONACULAR_API_KEY
        else:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            spoonacular_key = os.getenv('SPOONACULAR_API_KEY', '')
        
        if not spoonacular_key:
            print("Warning: SPOONACULAR_API_KEY not set. Please add it to your .env file.")
            return None
        
        try:
            # Search for recipes
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
                'apiKey': spoonacular_key,
                'query': dish_name,
                'number': 1,
                'addRecipeInformation': 'true'  # Get basic info in search
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    recipe_id = data['results'][0]['id']
                    
                    # Get detailed recipe information
                    detail_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                    detail_params = {
                        'apiKey': spoonacular_key,
                        'includeNutrition': 'false'
                    }
                    detail_response = requests.get(detail_url, params=detail_params, timeout=15)
                    
                    if detail_response.status_code == 200:
                        recipe_detail = detail_response.json()
                        
                        # Extract ingredients (structured data from API)
                        ingredients = []
                        for ing in recipe_detail.get('extendedIngredients', []):
                            ingredients.append({
                                'name': ing.get('name', '').strip(),
                                'quantity': str(ing.get('amount', '1')),
                                'unit': ing.get('unit', '').strip(),
                                'category': self._categorize_ingredient(ing.get('name', ''))
                            })
                        
                        # Extract instructions (structured steps)
                        instructions = []
                        if 'analyzedInstructions' in recipe_detail and recipe_detail['analyzedInstructions']:
                            for instruction_group in recipe_detail['analyzedInstructions']:
                                for step in instruction_group.get('steps', []):
                                    step_text = step.get('step', '').strip()
                                    if step_text:
                                        instructions.append(step_text)
                        
                        # If no analyzed instructions, try summary
                        if not instructions and recipe_detail.get('instructions'):
                            # Parse HTML instructions if available
                            from bs4 import BeautifulSoup
                            soup = BeautifulSoup(recipe_detail.get('instructions', ''), 'html.parser')
                            for p in soup.find_all(['p', 'li']):
                                text = p.get_text().strip()
                                if text and len(text) > 10:
                                    instructions.append(text)
                        
                        # Get title
                        title = recipe_detail.get('title', dish_name)
                        
                        # Generate summary
                        summary = recipe_detail.get('summary', '')
                        if summary:
                            from bs4 import BeautifulSoup
                            soup = BeautifulSoup(summary, 'html.parser')
                            summary = soup.get_text().strip()[:300]  # Limit to 300 chars
                        
                        return {
                            'dish_name': title or dish_name,
                            'ingredients': ingredients,
                            'instructions': instructions,
                            'servings': recipe_detail.get('servings', 4),
                            'prep_time': recipe_detail.get('preparationMinutes'),
                            'cook_time': recipe_detail.get('cookingMinutes'),
                            'total_time': recipe_detail.get('readyInMinutes'),
                            'summary': summary,
                            'title': title,
                            'source_type': 'spoonacular',
                            'source_url': recipe_detail.get('sourceUrl', recipe_detail.get('spoonacularSourceUrl', ''))
                        }
            elif response.status_code == 402:
                print("Warning: Spoonacular API quota exceeded. Please check your API key or upgrade plan.")
            else:
                print(f"Warning: Spoonacular API returned status {response.status_code}")
        
        except requests.exceptions.Timeout:
            print("Error: Spoonacular API request timed out")
        except Exception as e:
            print(f"Error fetching from Spoonacular: {str(e)}")
        
        return None
    
    def _categorize_ingredient(self, ingredient_name):
        """Categorize ingredient based on name"""
        if not ingredient_name:
            return 'other'
        
        name_lower = ingredient_name.lower()
        
        # Produce
        if any(kw in name_lower for kw in ['tomato', 'onion', 'garlic', 'potato', 'carrot', 'lettuce', 'pepper', 'cucumber', 'spinach', 'broccoli', 'cauliflower', 'celery', 'mushroom']):
            return 'produce'
        
        # Dairy
        if any(kw in name_lower for kw in ['milk', 'cheese', 'butter', 'cream', 'yogurt', 'sour cream', 'yoghurt']):
            return 'dairy'
        
        # Meat
        if any(kw in name_lower for kw in ['beef', 'pork', 'lamb', 'steak', 'ground beef', 'ground pork']):
            return 'meat'
        
        # Poultry
        if any(kw in name_lower for kw in ['chicken', 'turkey', 'duck']):
            return 'poultry'
        
        # Seafood
        if any(kw in name_lower for kw in ['fish', 'salmon', 'shrimp', 'crab', 'lobster', 'tuna', 'cod']):
            return 'seafood'
        
        # Grains
        if any(kw in name_lower for kw in ['rice', 'pasta', 'flour', 'bread', 'wheat', 'noodle', 'quinoa']):
            return 'grains'
        
        # Spices
        if any(kw in name_lower for kw in ['salt', 'pepper', 'cumin', 'turmeric', 'coriander', 'spice', 'paprika', 'cinnamon']):
            return 'spices'
        
        return 'other'
    
    def _basic_ingredient_extraction(self, soup):
        """Basic ingredient extraction fallback when IngredientExtractor is not available"""
        ingredients = []
        
        # Try to find ingredient lists
        ingredient_selectors = [
            {'itemprop': 'recipeIngredient'},
            {'class': 'recipe-ingredient'},
            {'class': 'ingredients'},
            {'id': 'ingredients'}
        ]
        
        for selector in ingredient_selectors:
            elements = soup.find_all(attrs=selector)
            if elements:
                for elem in elements:
                    text = elem.get_text().strip()
                    if text and len(text) > 3:
                        # Simple parsing - just extract text
                        ingredients.append({
                            'name': text,
                            'quantity': '1',
                            'unit': '',
                            'category': 'other'
                        })
                if ingredients:
                    break
        
        # If no structured list, try lists
        if not ingredients:
            lists = soup.find_all(['ul', 'ol'])
            for ul in lists[:3]:  # Limit to first 3 lists
                items = ul.find_all('li')
                for item in items[:20]:  # Limit to 20 items
                    text = item.get_text().strip()
                    if text and len(text) > 3:
                        ingredients.append({
                            'name': text,
                            'quantity': '1',
                            'unit': '',
                            'category': 'other'
                        })
                if ingredients:
                    break
        
        return ingredients[:50]  # Limit to 50 ingredients

