"""
NLP processing utilities for dish name and ingredient processing
"""
import re
import string


class NLPProcessor:
    """Natural Language Processing utilities"""
    
    def __init__(self):
        # Common dish name variations and synonyms
        self.dish_synonyms = {
            'pasta': ['spaghetti', 'noodles', 'macaroni'],
            'curry': ['kari', 'kadhi'],
            'rice': ['chawal', 'bhaat'],
            'bread': ['roti', 'naan', 'chapati']
        }
    
    def normalize_text(self, text):
        """
        Normalize text: lowercase, remove extra spaces, punctuation
        
        Args:
            text: Input text string
        
        Returns:
            Normalized text
        """
        if not text:
            return ''
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', '', text)
        
        return text.strip()
    
    def tokenize(self, text):
        """
        Tokenize text into words
        
        Args:
            text: Input text string
        
        Returns:
            List of tokens
        """
        if not text:
            return []
        
        # Normalize first
        normalized = self.normalize_text(text)
        
        # Split into words
        tokens = normalized.split()
        
        return tokens
    
    def extract_keywords(self, text, max_keywords=5):
        """
        Extract keywords from text
        
        Args:
            text: Input text string
            max_keywords: Maximum number of keywords to return
        
        Returns:
            List of keywords
        """
        tokens = self.tokenize(text)
        
        # Remove common stop words (simple version)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        keywords = [token for token in tokens if token not in stop_words]
        
        return keywords[:max_keywords]
    
    def find_synonyms(self, word):
        """
        Find synonyms for a word
        
        Args:
            word: Word to find synonyms for
        
        Returns:
            List of synonyms
        """
        word = word.lower()
        
        # Check direct mapping
        if word in self.dish_synonyms:
            return self.dish_synonyms[word]
        
        # Check if word is a synonym of another
        for main_word, synonyms in self.dish_synonyms.items():
            if word in synonyms:
                return [main_word] + [s for s in synonyms if s != word]
        
        return []

