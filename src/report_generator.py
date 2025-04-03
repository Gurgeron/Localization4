#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report Generator Module for Localization4

This module generates HTML and CSV reports for localization gaps.
"""

import os
import csv
from datetime import datetime
from typing import Dict, List, Any


def generate_html_report(gaps: List[Dict[str, Any]], output_file: str) -> None:
    """
    Generate an HTML report for localization gaps.
    
    Args:
        gaps (List[Dict[str, Any]]): List of localization gaps.
        output_file (str): Path to the output file.
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Count gaps by location and confidence
    location_counts = {}
    confidence_ranges = {
        '90-100%': 0,
        '80-90%': 0,
        '70-80%': 0,
        '<70%': 0
    }
    
    for gap in gaps:
        location = gap['location']
        confidence = gap['confidence']
        
        # Update location counts
        if location not in location_counts:
            location_counts[location] = 0
        location_counts[location] += 1
        
        # Update confidence ranges
        if confidence >= 0.9:
            confidence_ranges['90-100%'] += 1
        elif confidence >= 0.8:
            confidence_ranges['80-90%'] += 1
        elif confidence >= 0.7:
            confidence_ranges['70-80%'] += 1
        else:
            confidence_ranges['<70%'] += 1
    
    # Generate the HTML report
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Localization Gap Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #1e5631;
                color: white;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
            }}
            .summary {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
            }}
            .summary-box {{
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                padding: 15px;
                flex: 1;
                margin: 0 10px;
            }}
            .summary-box h3 {{
                margin-top: 0;
                color: #1e5631;
            }}
            .chart {{
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                padding: 15px;
                margin-bottom: 20px;
            }}
            .chart h3 {{
                margin-top: 0;
                color: #1e5631;
            }}
            .table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .table th {{
                background-color: #1e5631;
                color: white;
                padding: 12px 15px;
                text-align: left;
            }}
            .table td {{
                padding: 12px 15px;
                border-bottom: 1px solid #ddd;
            }}
            .table tr:last-child td {{
                border-bottom: none;
            }}
            .table tr:hover {{
                background-color: #f5f5f5;
            }}
            .confidence {{
                padding: 5px 10px;
                border-radius: 20px;
                font-weight: bold;
                color: white;
                display: inline-block;
                width: 60px;
                text-align: center;
            }}
            .high {{
                background-color: #1e5631;
            }}
            .medium {{
                background-color: #4d8c57;
            }}
            .low {{
                background-color: #84bf8e;
            }}
            .very-low {{
                background-color: #ff9800;
            }}
            .pagination {{
                display: flex;
                justify-content: center;
                margin-top: 20px;
            }}
            .pagination button {{
                background-color: #1e5631;
                color: white;
                border: none;
                padding: 8px 16px;
                margin: 0 5px;
                border-radius: 5px;
                cursor: pointer;
            }}
            .pagination button:hover {{
                background-color: #4d8c57;
            }}
            .pagination button:disabled {{
                background-color: #ccc;
                cursor: not-allowed;
            }}
            .page-info {{
                margin: 0 10px;
                line-height: 32px;
            }}
            .donut-chart {{
                width: 200px;
                height: 200px;
                margin: 0 auto;
                position: relative;
            }}
            .bar-chart {{
                display: flex;
                align-items: flex-end;
                height: 200px;
                justify-content: space-around;
                padding: 0 20px;
            }}
            .bar {{
                width: 40px;
                background-color: #84bf8e;
                margin: 0 10px;
                position: relative;
            }}
            .bar-label {{
                position: absolute;
                bottom: -25px;
                text-align: center;
                width: 100%;
                font-size: 12px;
            }}
            .bar-value {{
                position: absolute;
                top: -20px;
                text-align: center;
                width: 100%;
            }}
            footer {{
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                color: #666;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Localization Gap Report</h1>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <div class="summary-box">
                    <h3>Total Gaps</h3>
                    <p style="font-size: 2em; text-align: center;">{len(gaps)}</p>
                </div>
                <div class="summary-box">
                    <h3>Pages Scanned</h3>
                    <p style="font-size: 2em; text-align: center;">{len(location_counts)}</p>
                </div>
                <div class="summary-box">
                    <h3>High Confidence Gaps</h3>
                    <p style="font-size: 2em; text-align: center;">{confidence_ranges['90-100%'] + confidence_ranges['80-90%']}</p>
                </div>
                <div class="summary-box">
                    <h3>Time Stamp</h3>
                    <p style="font-size: 1.5em; text-align: center;">{datetime.now().strftime('%H:%M:%S')}</p>
                </div>
            </div>
            
            <div class="chart">
                <h3>Gaps by Confidence</h3>
                <div class="bar-chart">
                    <div class="bar" style="height: {confidence_ranges['90-100%'] / max(1, max(confidence_ranges.values())) * 100}%;">
                        <div class="bar-value">{confidence_ranges['90-100%']}</div>
                        <div class="bar-label">90-100%</div>
                    </div>
                    <div class="bar" style="height: {confidence_ranges['80-90%'] / max(1, max(confidence_ranges.values())) * 100}%;">
                        <div class="bar-value">{confidence_ranges['80-90%']}</div>
                        <div class="bar-label">80-90%</div>
                    </div>
                    <div class="bar" style="height: {confidence_ranges['70-80%'] / max(1, max(confidence_ranges.values())) * 100}%;">
                        <div class="bar-value">{confidence_ranges['70-80%']}</div>
                        <div class="bar-label">70-80%</div>
                    </div>
                    <div class="bar" style="height: {confidence_ranges['<70%'] / max(1, max(confidence_ranges.values())) * 100}%;">
                        <div class="bar-value">{confidence_ranges['<70%']}</div>
                        <div class="bar-label">&lt;70%</div>
                    </div>
                </div>
            </div>
            
            <div class="chart">
                <h3>Gaps by Location</h3>
                <div class="bar-chart">
                    {
                    ''.join([
                        f'''<div class="bar" style="height: {count / max(1, max(location_counts.values())) * 100}%;">
                            <div class="bar-value">{count}</div>
                            <div class="bar-label">{location[:10] + ('...' if len(location) > 10 else '')}</div>
                        </div>'''
                        for location, count in list(location_counts.items())[:5]
                    ])
                    }
                </div>
            </div>
            
            <table class="table">
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>Text</th>
                        <th>Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    {
                    ''.join([
                        f'''<tr>
                            <td>{gap['location']}</td>
                            <td>{gap['text']}</td>
                            <td>
                                <span class="confidence {'high' if gap['confidence'] >= 0.9 else 'medium' if gap['confidence'] >= 0.8 else 'low' if gap['confidence'] >= 0.7 else 'very-low'}">
                                    {int(gap['confidence'] * 100)}%
                                </span>
                            </td>
                        </tr>'''
                        for gap in sorted(gaps, key=lambda x: x['confidence'], reverse=True)
                    ])
                    }
                </tbody>
            </table>
            
            <footer>
                <p>Localization4 - Localization Gap Detection Tool</p>
                <p>Generated using Nova Act Lite</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    # Write the HTML report to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_csv_report(gaps: List[Dict[str, Any]], output_file: str) -> None:
    """
    Generate a CSV report for localization gaps.
    
    Args:
        gaps (List[Dict[str, Any]]): List of localization gaps.
        output_file (str): Path to the output file.
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Sort gaps by confidence
    sorted_gaps = sorted(gaps, key=lambda x: x['confidence'], reverse=True)
    
    # Write the CSV report
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Location', 'Text', 'Confidence'])
        for gap in sorted_gaps:
            writer.writerow([gap['location'], gap['text'], f"{int(gap['confidence'] * 100)}%"]) 