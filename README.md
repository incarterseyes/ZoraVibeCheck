# Zora Collection Vibe Analyzer

This tool analyzes your Zora art collection using gpt-4o-mini to give you insights about your collecting style and preferences.

## Setup

### Prerequisites
- Python 3.11 or higher
- Chrome installed
- OpenAI API key with gpt-4o-mini access

### Installation

1. Clone or download this repository

2. Set up a Python virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Mac/Linux:
```bash
source venv/bin/activate
```

4. Install required packages:
```bash
pip install openai Pillow requests selenium
```

5. Install ChromeDriver:
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Make sure the version matches your Chrome browser
   - Extract the chromedriver executable to your project directory

### Usage

1. Open the `analyzer_run.py` file

2. Replace:
   - `"your-api-key-here"` with your OpenAI API key
   - `"username"` with the Zora username you want to analyze

3. Run the script:
```bash
python analyzer_run.py
```

The tool will:
- Scrape the user's Zora collection using Chrome
- Analyze each artwork using gpt-4o-mini
- Generate a summary of the collection's style and themes

### Cost Considerations
- The tool uses gpt-4o-mini which has associated API costs
- Images are optimized to minimize token usage
- Start with a small number of items (5-10) to test
- Use the `max_items` parameter to control how many pieces are analyzed

### Rate Limits
The tool respects OpenAI's rate limits for gpt-4o-mini:
- 500 requests per minute
- 200,000 tokens per minute
- Built-in delays prevent hitting rate limits

## Files
- `analyzer.py`: Main analysis logic using OpenAI's API
- `analyzer_run.py`: Runs `scraper.py` then `analyzer.py`and gives results
- `scraper.py`: Web scraping functionality for Zora
- `scraper_test.py`: Example usage script

## Troubleshooting
- If you get ChromeDriver errors, make sure you have the correct version installed
- API errors might indicate rate limiting or incorrect API key
- Image processing errors usually mean the URL is invalid or inaccessible

## Notes
- This tool is for educational purposes
- Be mindful of OpenAI's API costs and rate limits
- The analysis quality depends on gpt-4's understanding of art
