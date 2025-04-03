#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Localization4 - Localization Gap Detection Tool

This script is the main entry point for the Localization4 tool,
which detects localization gaps in the Guesty PMS UI.
"""

import os
import sys
import time
import webbrowser
from datetime import datetime

from colorama import Fore, Style, init

from browser_controller import BrowserController
from config_loader import load_urls
from gap_analyzer import NovaActLiteAnalyzer
from report_generator import generate_html_report, generate_csv_report

# Initialize colorama for colored terminal output
init()

def print_banner():
    """
    Print a welcome banner for the tool.
    """
    banner = f"""
    {Fore.LIGHTGREEN_EX}╔═══════════════════════════════════════════════╗
    ║ {Fore.LIGHTBLUE_EX}Localization4 - Localization Gap Detection Tool{Fore.LIGHTGREEN_EX} ║
    ╚═══════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)
    print(f"{Fore.WHITE}Welcome to the Localization4 tool!")
    print(f"This tool will help you detect localization gaps in the Guesty PMS UI.")
    print(f"Follow the instructions below to get started.{Style.RESET_ALL}\n")

def main():
    """
    Main function to run the Localization4 tool.
    """
    print_banner()
    
    # Load URLs from configuration file
    try:
        print(f"{Fore.LIGHTBLUE_EX}Loading URLs from configuration file...{Style.RESET_ALL}")
        urls = load_urls('config/urls.txt')
        print(f"{Fore.GREEN}✓ Loaded {len(urls)} URLs from configuration file.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error loading URLs: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
    
    # Initialize the browser controller
    try:
        print(f"{Fore.LIGHTBLUE_EX}Initializing browser controller...{Style.RESET_ALL}")
        browser = BrowserController()
        print(f"{Fore.GREEN}✓ Browser controller initialized.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error initializing browser controller: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Troubleshooting tips:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Make sure Chrome is installed{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Try running 'python3 -m pip install webdriver-manager --upgrade'{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. If on macOS, ensure Xcode command line tools are installed{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Check if you have the correct permissions to execute the ChromeDriver{Style.RESET_ALL}")
        sys.exit(1)
    
    # Initialize the Nova Act Lite analyzer
    try:
        print(f"{Fore.LIGHTBLUE_EX}Initializing Nova Act Lite analyzer...{Style.RESET_ALL}")
        analyzer = NovaActLiteAnalyzer()
        print(f"{Fore.GREEN}✓ Nova Act Lite analyzer initialized.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error initializing Nova Act Lite analyzer: {str(e)}{Style.RESET_ALL}")
        browser.close()
        sys.exit(1)
    
    # Prompt the user to log in and change language manually
    print(f"\n{Fore.LIGHTYELLOW_EX}Please log in to the Guesty PMS manually and change the language to French.{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}Once you're done, press Enter to start the scanning process.{Style.RESET_ALL}")
    
    # Open the first URL
    if urls:
        first_url = urls[0]['url']
        try:
            print(f"{Fore.LIGHTBLUE_EX}Opening the first URL: {first_url}{Style.RESET_ALL}")
            browser.navigate_to(first_url)
            print(f"{Fore.GREEN}✓ Browser opened to the first URL.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error opening the first URL: {str(e)}{Style.RESET_ALL}")
            browser.close()
            sys.exit(1)
    
    # Wait for user input
    input(f"\n{Fore.WHITE}Press Enter to start scanning...{Style.RESET_ALL}")
    
    # Scan each URL for localization gaps
    all_gaps = []
    for i, url_item in enumerate(urls, 1):
        url = url_item['url']
        page_name = url_item['name']
        ui_element = url_item['ui_element']
        
        print(f"\n{Fore.LIGHTBLUE_EX}[{i}/{len(urls)}] Scanning {page_name} ({url}){Style.RESET_ALL}")
        
        try:
            # Navigate to the URL
            browser.navigate_to(url)
            time.sleep(2)  # Wait for page to load
            
            # Analyze the main page
            print(f"{Fore.WHITE}Analyzing main page...{Style.RESET_ALL}")
            main_page_gaps = analyzer.analyze_page(browser.get_page_source(), f"{page_name}")
            all_gaps.extend(main_page_gaps)
            
            # Click the UI element if specified
            if ui_element:
                print(f"{Fore.WHITE}Clicking UI element: {ui_element}{Style.RESET_ALL}")
                browser.click_element(ui_element)
                time.sleep(2)  # Wait for modal to open
                
                # Analyze the modal
                print(f"{Fore.WHITE}Analyzing modal...{Style.RESET_ALL}")
                modal_gaps = analyzer.analyze_page(browser.get_page_source(), f"{page_name} > Modal")
                all_gaps.extend(modal_gaps)
            
            print(f"{Fore.GREEN}✓ Finished scanning {page_name}.{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Error scanning {page_name}: {str(e)}{Style.RESET_ALL}")
            continue
    
    # Close the browser
    browser.close()
    
    # Generate timestamp for report filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate HTML report
    html_report_path = f"reports/localization_report_{timestamp}.html"
    try:
        print(f"\n{Fore.LIGHTBLUE_EX}Generating HTML report...{Style.RESET_ALL}")
        generate_html_report(all_gaps, html_report_path)
        print(f"{Fore.GREEN}✓ HTML report generated: {html_report_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error generating HTML report: {str(e)}{Style.RESET_ALL}")
    
    # Generate CSV report
    csv_report_path = f"reports/localization_report_{timestamp}.csv"
    try:
        print(f"\n{Fore.LIGHTBLUE_EX}Generating CSV report...{Style.RESET_ALL}")
        generate_csv_report(all_gaps, csv_report_path)
        print(f"{Fore.GREEN}✓ CSV report generated: {csv_report_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error generating CSV report: {str(e)}{Style.RESET_ALL}")
    
    # Open the HTML report
    try:
        print(f"\n{Fore.LIGHTBLUE_EX}Opening HTML report...{Style.RESET_ALL}")
        webbrowser.open('file://' + os.path.abspath(html_report_path))
        print(f"{Fore.GREEN}✓ HTML report opened in browser.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error opening HTML report: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.LIGHTGREEN_EX}Localization gap detection completed!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Found {len(all_gaps)} potential localization gaps.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Check the HTML and CSV reports for details.{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 