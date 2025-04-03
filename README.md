# Localization4 - Localization Gap Detection Tool

A lightweight, automated tool to detect localization gaps within the Guesty PMS UI by analyzing live page content. The tool flags untranslated English text in a French environment, pinpointing exact locations (pages, modals, buttons) with a confidence score.

## Features

- Automated navigation through pages and modals
- Localization gap analysis with Nova Act Lite
- Precise gap location reporting with confidence scores
- Beautiful HTML and CSV reports

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Gurgeron/Localization4.git
cd Localization4
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Configure your URLs in the `config/urls.txt` file
2. Run the tool:
```bash
python src/main.py
```
3. Log in manually to the Guesty PMS and change the language to French
4. Press Enter in the terminal to start the scanning process
5. Once completed, the HTML report will open automatically

## Configuration

The `config/urls.txt` file should contain the URLs to scan, along with descriptive names and UI element identifiers in the following format:

```
URL|Page Name|UI Element Identifier
```

Example:
```
https://example.com/dashboard|Dashboard|.modal-button
```

## Reports

Two types of reports are generated:
- HTML report (automatically opens in browser)
- CSV report (stored in the `reports` directory)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for details on all updates.

## License

This project is proprietary and confidential. 