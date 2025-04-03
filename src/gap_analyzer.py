#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gap Analyzer Module for Localization4

This module analyzes pages for localization gaps using AWS Comprehend.
"""

import re
import boto3
from typing import Dict, List, Any
from bs4 import BeautifulSoup

from config_loader import load_aws_credentials


class NovaActLiteAnalyzer:
    """
    Nova Act Lite analyzer class for detecting localization gaps using AWS Comprehend.
    """
    
    def __init__(self):
        """
        Initialize the AWS Comprehend client for language detection.
        """
        # Load AWS credentials
        try:
            aws_credentials = load_aws_credentials()
            self.aws_access_key_id = aws_credentials['AWS_ACCESS_KEY_ID']
            self.aws_secret_access_key = aws_credentials['AWS_SECRET_ACCESS_KEY']
            self.aws_region = aws_credentials['AWS_REGION']
            
            # Initialize AWS Comprehend client
            self.comprehend = boto3.client(
                'comprehend',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region
            )
            self.initialized = True
            
        except Exception as e:
            print(f"Warning: Failed to initialize AWS Comprehend: {str(e)}")
            self.initialized = False
    
    def analyze_page(self, html: str, location: str) -> List[Dict[str, Any]]:
        """
        Analyze a page for localization gaps using AWS Comprehend.
        
        Args:
            html (str): The HTML content of the page.
            location (str): The location of the page.
            
        Returns:
            List[Dict[str, Any]]: List of localization gaps found.
        """
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
        
        # Detect language for each text element
        gaps = []
        batch_size = 25  # AWS Comprehend has limits on batch size
        
        for i in range(0, len(filtered_elements), batch_size):
            batch = filtered_elements[i:i+batch_size]
            
            # Skip single character texts and numbers
            valid_batch = [text for text in batch if len(text) > 1 and not text.isdigit()]
            
            if not valid_batch:
                continue
                
            if self.initialized:
                # Use AWS Comprehend to detect language
                try:
                    response = self.comprehend.batch_detect_dominant_language(
                        TextList=valid_batch
                    )
                    
                    for j, result in enumerate(response['ResultList']):
                        text = valid_batch[j]
                        
                        # Get the dominant language with the highest score
                        languages = result['Languages']
                        dominant_lang = max(languages, key=lambda x: x['Score'])
                        
                        # If the dominant language is English (and we're in a French UI)
                        if dominant_lang['LanguageCode'] == 'en' and dominant_lang['Score'] > 0.7:
                            confidence = dominant_lang['Score']
                            gap = {
                                'location': location,
                                'text': text,
                                'confidence': confidence
                            }
                            gaps.append(gap)
                            
                except Exception as e:
                    print(f"Warning: AWS Comprehend error: {str(e)}")
                    # Fall back to heuristic method for this batch
                    gaps.extend(self._analyze_with_heuristic(valid_batch, location))
            else:
                # If AWS is not initialized, use heuristic method
                gaps.extend(self._analyze_with_heuristic(valid_batch, location))
        
        return gaps
    
    def _analyze_with_heuristic(self, texts: List[str], location: str) -> List[Dict[str, Any]]:
        """
        Analyze texts using heuristic method as a fallback.
        
        Args:
            texts (List[str]): List of text elements to analyze.
            location (str): The location of the texts.
            
        Returns:
            List[Dict[str, Any]]: List of gaps found.
        """
        gaps = []
        for text in texts:
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
        Check if the text is likely to be English using heuristics.
        
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