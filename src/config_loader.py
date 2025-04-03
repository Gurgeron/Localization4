#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration Loader Module for Localization4

This module loads the URLs and configurations from the config file.
"""

import os
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


def load_api_key(key_file: str = 'API_KEYS.md') -> str:
    """
    Load the Nova Act Lite API key from the API_KEYS.md file.
    
    Args:
        key_file (str): Path to the API keys file.
        
    Returns:
        str: The Nova Act Lite API key.
        
    Raises:
        FileNotFoundError: If the API keys file does not exist.
        ValueError: If the API key is not found in the file.
    """
    # Check if the API keys file exists
    if not os.path.exists(key_file):
        raise FileNotFoundError(f"API keys file not found: {key_file}")
    
    # Read the API keys file
    with open(key_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('NOVA_ACT_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                if api_key and api_key != 'your_nova_act_api_key_here':
                    return api_key
    
    # If we get here, the API key was not found
    raise ValueError("Nova Act Lite API key not found in the API keys file.") 