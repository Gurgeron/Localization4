#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration Loader Module for Localization4

This module loads the URLs and configurations from the config file.
"""

import os
import re
from typing import List, Dict, Any


def load_urls(config_file: str) -> List[Dict[str, Any]]:
    """
    Load URLs and configurations from the config file.
    
    Args:
        config_file (str): Path to the configuration file.
        
    Returns:
        List[Dict[str, Any]]: List of URL configurations.
        
    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If the config file is malformed.
    """
    # Check if the config file exists
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    # Read the config file
    urls = []
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments
                
            # Parse the line (URL|Page Name|UI Element)
            parts = line.split('|')
            if len(parts) < 2:
                raise ValueError(f"Invalid line in config file: {line}")
            
            url = parts[0].strip()
            name = parts[1].strip() if len(parts) > 1 else url
            ui_element = parts[2].strip() if len(parts) > 2 else None
            
            # Add to the list of URLs
            urls.append({
                'url': url,
                'name': name,
                'ui_element': ui_element
            })
    
    # Check if any URLs were loaded
    if not urls:
        raise ValueError("No URLs found in the config file.")
    
    return urls


def load_aws_credentials(key_file: str = 'API_KEYS.md') -> Dict[str, str]:
    """
    Load AWS credentials from the API_KEYS.md file for Nova Act Lite.
    
    Args:
        key_file (str): Path to the API keys file.
        
    Returns:
        Dict[str, str]: The AWS credentials.
        
    Raises:
        FileNotFoundError: If the API keys file does not exist.
        ValueError: If required AWS credentials are not found in the file.
    """
    # Check if the API keys file exists
    if not os.path.exists(key_file):
        raise FileNotFoundError(f"API keys file not found: {key_file}")
    
    # AWS credential keys we need to find
    required_keys = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_REGION'
    ]
    
    # Dictionary to store the found credentials
    aws_credentials = {}
    
    # Read the API keys file
    with open(key_file, 'r') as f:
        content = f.read()
        
        # Look for each credential in the file
        for key in required_keys:
            match = re.search(f"{key}=([^\n]+)", content)
            if match:
                aws_credentials[key] = match.group(1).strip()
    
    # Check if all required credentials were found
    missing_keys = [key for key in required_keys if key not in aws_credentials]
    if missing_keys:
        raise ValueError(f"Missing AWS credentials in the API keys file: {', '.join(missing_keys)}")
    
    return aws_credentials 