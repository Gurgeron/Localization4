# How to Run Localization4

This document provides detailed instructions on how to run the Localization4 tool for detecting localization gaps in the Guesty PMS UI.

## Prerequisites

1. Python 3.8 or higher
2. Google Chrome browser
3. Valid Guesty PMS credentials
4. AWS account with access to Amazon Comprehend service
5. Proper IAM permissions for AWS Comprehend API access

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

3. Configure your AWS credentials:
   - Open API_KEYS.md
   - Verify that your AWS credentials are correctly entered:
   ```
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   AWS_REGION=your_aws_region
   ```
   - Ensure the IAM user has permissions for `comprehend:BatchDetectDominantLanguage`

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
   - Analyze each page for localization gaps using AWS Comprehend
   - Generate HTML and CSV reports

6. When the process is complete, the HTML report will open automatically in your default browser.

## AWS Comprehend Details

The tool uses AWS Comprehend to detect the dominant language of text elements on web pages. When a text element is detected as English in a French UI context, it's flagged as a localization gap.

If AWS Comprehend is unavailable or encounters an error, the tool will automatically fall back to using heuristic detection methods.

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
3. Verify that your AWS credentials are correct and have the necessary permissions
4. Check the AWS service quotas and limits for Comprehend

## AWS Permission Requirements

The IAM user needs the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "comprehend:BatchDetectDominantLanguage"
            ],
            "Resource": "*"
        }
    ]
}
```

## Support

For support, please contact gur.geron@gmail.com 