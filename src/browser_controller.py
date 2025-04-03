#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Browser Controller Module for Localization4

This module handles browser automation using Selenium.
"""

import os
import time
import platform
import subprocess
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class BrowserController:
    """
    Browser controller class for automating browser interactions.
    """
    
    def __init__(self, headless: bool = False):
        """
        Initialize the browser controller.
        
        Args:
            headless (bool): Whether to run in headless mode.
        """
        # Set up Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        
        # Initialize the Chrome driver with platform-specific settings
        try:
            # Download the driver first
            driver_path = ChromeDriverManager().install()
            
            # Handle permission issues on macOS
            if platform.system() == 'Darwin':
                # Ensure the ChromeDriver is executable
                try:
                    subprocess.run(['chmod', '+x', driver_path], check=True)
                    print(f"Fixed permissions for ChromeDriver at: {driver_path}")
                except subprocess.SubprocessError as e:
                    print(f"Warning: Could not set executable permissions: {e}")
            
            # Initialize the driver
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            
            # Set default timeouts
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 10)
            
        except Exception as e:
            # More detailed error reporting
            print(f"Error initializing Chrome driver: {str(e)}")
            print(f"Platform: {platform.system()}, Machine: {platform.machine()}")
            raise
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a URL.
        
        Args:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)
        
        # Wait for the page to load
        time.sleep(2)
    
    def click_element(self, selector: str) -> bool:
        """
        Click an element on the page.
        
        Args:
            selector (str): CSS selector for the element.
            
        Returns:
            bool: True if the element was clicked, False otherwise.
        """
        try:
            # First, try to find the element by CSS selector
            element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            element.click()
            return True
        except:
            try:
                # If that fails, try XPath
                element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                return True
            except:
                # If both fail, return False
                return False
    
    def get_page_source(self) -> str:
        """
        Get the page source.
        
        Returns:
            str: The page source.
        """
        return self.driver.page_source
    
    def close(self) -> None:
        """
        Close the browser.
        """
        if self.driver:
            self.driver.quit() 