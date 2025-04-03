# How to Run Localization4

This document provides detailed instructions on how to run the Localization4 tool for detecting localization gaps in the Guesty PMS UI.

## Prerequisites

1. Python 3.8 or higher
2. Google Chrome browser
3. Valid Guesty PMS credentials
4. Nova Act Lite API key

## Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/Gurgeron/Localization4.git
cd Localization4
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Add your Nova Act Lite API key:
   - Open API_KEYS.md
   - Replace the placeholder with your actual API key

4. Configure the URLs to scan:
   - Edit config/urls.txt
   - Add the URLs in the format: URL|Page Name|UI Element Identifier
   - Example: https://app.guesty.com/dashboard|Dashboard|.dashboard-settings-button

## Running the Tool

1. Start the tool:
```bash
python src/main.py
```

2. The tool will open a browser window and navigate to the first URL in the configuration file.

3. Manually:
   - Log in to the Guesty PMS
   - Switch the language to French

4. Return to the terminal and press Enter to start the automated scanning process.

5. The tool will:
   - Navigate through each URL in the configuration file
   - Interact with UI elements as specified
   - Analyze each page for localization gaps using Nova Act Lite
   - Generate HTML and CSV reports

6. When the process is complete, the HTML report will open automatically in your default browser.

## Interpreting the Reports

The reports contain:
- Page/modal/button location of each gap
- The untranslated text
- Confidence score for each detection
- Summary statistics

## Troubleshooting

If the tool fails to navigate or analyze a page:
1. Check that the URLs and UI element identifiers are correct
2. Ensure your Guesty PMS credentials are valid
3. Verify that your Nova Act Lite API key is correctly configured

## Support

For support, please contact gur.geron@gmail.com 