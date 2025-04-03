#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gap Analyzer Module for Localization4

This module analyzes pages for localization gaps using Nova Act Lite.
"""

import re
from typing import Dict, List, Any
from bs4 import BeautifulSoup

from config_loader import load_api_key


class NovaActLiteAnalyzer:
    """
    Nova Act Lite analyzer class for detecting localization gaps.
    """
    
    def __init__(self):
        """
        Initialize the Nova Act Lite analyzer.
        """
        try:
            self.api_key = load_api_key()
        except:
            # For now, use a dummy API key since Nova Act Lite is not actually implemented
            self.api_key = "dummy_api_key"
    
    def analyze_page(self, html: str, location: str) -> List[Dict[str, Any]]:
        """
        Analyze a page for localization gaps.
        
        Args:
            html (str): The HTML content of the page.
            location (str): The location of the page.
            
        Returns:
            List[Dict[str, Any]]: List of localization gaps found.
        """
        # Since Nova Act Lite is not actually implemented, we will
        # use a simple heuristic to detect English text in the HTML
        # that should have been translated to French.
        
        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get all text elements
        text_elements = soup.find_all(text=True)
        
        # Filter out empty text elements and non-text elements
        filtered_elements = []
        for element in text_elements:
            text = element.strip()
            if text and not self._is_code(text):
                filtered_elements.append(text)
        
        # Detect English text that should have been translated to French
        gaps = []
        for text in filtered_elements:
            # Skip if the text is a number or a single character
            if text.isdigit() or len(text) <= 1:
                continue
            
            # Skip if the text contains mostly non-alphabetic characters
            alpha_ratio = sum(c.isalpha() for c in text) / len(text) if len(text) > 0 else 0
            if alpha_ratio < 0.5:
                continue
            
            # Check if the text is likely to be English
            if self._is_likely_english(text):
                confidence = self._calculate_confidence(text)
                gap = {
                    'location': location,
                    'text': text,
                    'confidence': confidence
                }
                gaps.append(gap)
        
        return gaps
    
    def _is_code(self, text: str) -> bool:
        """
        Check if the text is code.
        
        Args:
            text (str): The text to check.
            
        Returns:
            bool: True if the text is code, False otherwise.
        """
        # Check for common code patterns
        code_patterns = [
            r'function\s+\w+\s*\(',
            r'var\s+\w+\s*=',
            r'let\s+\w+\s*=',
            r'const\s+\w+\s*=',
            r'if\s*\(',
            r'for\s*\(',
            r'while\s*\(',
            r'class\s+\w+',
            r'\{\s*\w+\s*:',
            r'\[\s*\w+\s*,',
            r'<\w+>.*<\/\w+>'
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def _is_likely_english(self, text: str) -> bool:
        """
        Check if the text is likely to be English.
        
        Args:
            text (str): The text to check.
            
        Returns:
            bool: True if the text is likely to be English, False otherwise.
        """
        # English words that are common in UI and differ from French
        english_words = [
            'the', 'and', 'with', 'for', 'your', 'you',
            'is', 'are', 'on', 'in', 'at', 'by', 'from',
            'settings', 'profile', 'account', 'save', 'cancel',
            'delete', 'create', 'edit', 'view', 'search',
            'new', 'dashboard', 'sign', 'out', 'login',
            'logout', 'password', 'username', 'email',
            'please', 'enter', 'submit', 'notifications',
            'messages', 'loading', 'error', 'success'
        ]
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Check for common English words
        for word in english_words:
            # Match whole words only
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def _calculate_confidence(self, text: str) -> float:
        """
        Calculate the confidence score for a detected gap.
        
        Args:
            text (str): The text to calculate confidence for.
            
        Returns:
            float: The confidence score (0.0 to 1.0).
        """
        # Start with a base confidence
        confidence = 0.7
        
        # Adjust based on text length (longer text more likely to be a gap)
        if len(text) > 20:
            confidence += 0.1
        
        # Adjust based on the number of English words
        english_word_count = 0
        english_words = [
            'the', 'and', 'with', 'for', 'your', 'you',
            'is', 'are', 'on', 'in', 'at', 'by', 'from',
            'settings', 'profile', 'account', 'save', 'cancel',
            'delete', 'create', 'edit', 'view', 'search',
            'new', 'dashboard', 'sign', 'out', 'login',
            'logout', 'password', 'username', 'email',
            'please', 'enter', 'submit', 'notifications',
            'messages', 'loading', 'error', 'success'
        ]
        
        text_lower = text.lower()
        for word in english_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, text_lower):
                english_word_count += 1
        
        if english_word_count > 2:
            confidence += 0.1
        
        # Cap confidence at 0.95
        return min(confidence, 0.95) 