# Localfluence

A professional business website scraping and AI marketing video prompt generation tool powered by AI.

## Features

- **Business Discovery**: Find businesses using Google Places API
- **Website Scraping**: Extract structured data from business websites
- **AI-Powered Video Content**: Generate Google Veo 3 video prompts from business data
- **Professional Configuration**: Secure API key management
- **Multiple LLM Support**: Groq, OpenAI, and Anthropic integration
- **Concurrent Processing**: Scrape multiple businesses simultaneously
- **Copy-Paste Ready**: Generate prompts ready for Flow.google and other Veo 3 tools

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Configuration

Create a configuration file with your API keys:

```bash
python config.py --create-template
```

This creates a `.env` file template. Edit it with your API keys:

```env
# Google Places API (Required for business search)
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here

# LLM API Keys (Required for AI-powered content extraction)
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Validate Configuration

```bash
python config.py --validate
```

### 4. Run Examples

```bash
# Run the simple test
python test_simple.py

# Run the main scraping script
python main.py "Business Name" "Address"

# Generate AI video prompts
python main.py "Business Name" "Address" ai_video

# See example Veo 3 prompts (no API required)
python example_veo3.py

# Test the return functionality
python test_main_return.py
```

## Configuration

The configuration system supports multiple ways to set API keys:

### Environment Variables (Recommended)
```bash
export GOOGLE_PLACES_API_KEY="your_key_here"
export GROQ_API_KEY="your_key_here"
```

### Configuration File
Create a `.env` file in your project directory:
```env
GOOGLE_PLACES_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

### Configuration Locations
The system looks for configuration files in this order:
1. `.env` (current directory)
2. `config.env` (current directory)
3. `localfluence.env` (current directory)
4. `~/.localfluence/config.env`
5. `~/.config/localfluence/config.env`

## API Keys Required

### Google Places API
- **Purpose**: Business search and discovery
- **Get it from**: [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- **Required**: Yes

### LLM API (Choose one)
- **Purpose**: AI-powered content extraction
- **Options**:
  - **Groq** (Recommended): Fast, free tier available
    - Get it from: [Groq Console](https://console.groq.com/)
  - **OpenAI**: GPT models
    - Get it from: [OpenAI Platform](https://platform.openai.com/api-keys)
  - **Anthropic**: Claude models
    - Get it from: [Anthropic Console](https://console.anthropic.com/)
- **Required**: Yes (at least one)

## Usage Examples

### Basic Business Search

```python
from business_scraper import findOneBusiness

# Find a business
business = findOneBusiness("Hamilton's", "174 E Magnolia Ave, Auburn, AL 36830, USA")
print(f"Found: {business['name']}")
print(f"Website: {business.get('website')}")
```

### Raw Website Scraping

```python
from business_scraper import scrapeBusinessWebsiteRaw

# Scrape raw website data
rawData = scrapeBusinessWebsiteRaw(business)
print(f"Text length: {rawData['rawWebsiteData']['textLength']} characters")
```

### AI-Powered Video Content Generation

```python
from website_scraper import scrape_business_website_ai, generate_google_veo3_prompts

# Extract AI video content and generate Veo 3 prompts
result = await scrape_business_website_ai(
    "Hamilton's", 
    "174 E Magnolia Ave, Auburn, AL 36830, USA",
    "ai_video"
)

if result and result.get('websiteData'):
    data = result['websiteData']
    
    # Generate Google Veo 3 prompts
    prompts = generate_google_veo3_prompts(data)
    
    for i, prompt in enumerate(prompts, 1):
        print(f"Video Concept {i}: {prompt.get('description', '')[:100]}...")
        print(f"Style: {prompt.get('style')}")
        print(f"Keywords: {prompt.get('keywords')}")
```

### Programmatic Access to Veo 3 Prompts

```python
from main import get_veo3_prompts

# Get Veo 3 prompts programmatically
result = get_veo3_prompts("Hamilton's", "174 E Magnolia Ave, Auburn, AL 36830, USA")

if result and result.get('success'):
    # Access individual prompts
    prompts = result['veo3_prompts']
    formatted_prompts = result['formatted_prompts']
    
    # Get business info
    business_name = result['business_info']['name']
    
    # Get workflow instructions
    instructions = result['workflow_instructions']
    
    # Use individual prompt elements
    for prompt in prompts:
        description = prompt['description']
        style = prompt['style']
        keywords = prompt['keywords']
        
    # Get copy-paste ready prompts for Flow.google
    for formatted_prompt in formatted_prompts:
        # formatted_prompt is ready to paste into Flow.google
        print(formatted_prompt)
```

### Command Line Usage

```bash
# Generate AI video prompts (default)
python main.py "Business Name" "Address"

# Generate AI video prompts explicitly
python main.py "Business Name" "Address" ai_video

# Extract full business data
python main.py "Business Name" "Address" full

# Extract influencer content (legacy)
python main.py "Business Name" "Address" influencer
```

### Multiple Business Processing

```python
from website_scraper import scrape_multiple_businesses

businesses = [
    {"name": "Business 1", "address": "Address 1"},
    {"name": "Business 2", "address": "Address 2"},
]

results = await scrape_multiple_businesses(businesses, "ai_video")
```

## Google Veo 3 Integration

Localfluence generates copy-paste ready prompts for Google Veo 3 video generation. The workflow is simple:

1. **Extract Business Data**: Use Localfluence to analyze a business website
2. **Generate Prompts**: Get multiple video concept prompts optimized for Veo 3
3. **Create Videos**: Copy prompts to Flow.google or other Veo 3 tools
4. **Download & Use**: Generate professional marketing videos instantly

### Supported Veo 3 Tools

- **Flow.google** (Official): https://flow.google
- **Freepik Sebtips**: http://www.freepik.sebtips.com
- **Higgsfield AI**: https://goto.higgsfield.ai/seb

### Prompt Format

Each generated prompt includes:
- **Description**: Detailed scene description
- **Style**: Visual style (cinematic, photorealistic, etc.)
- **Camera**: Camera movement and positioning
- **Lighting**: Lighting setup and mood
- **Elements**: Key visual elements to include
- **Motion**: Movement and animation description
- **Keywords**: Optimized keywords for AI generation

### Example Output

```json
{
  "description": "Cinematic shot of a sunlit kitchen...",
  "style": "cinematic, photorealistic",
  "camera": "slow orbital shot from low angle",
  "lighting": "morning sunlight streaming through curtains",
  "elements": ["product", "props", "environment"],
  "motion": "smooth camera movement with product focus",
  "ending": "beautifully arranged final scene",
  "text": "none",
  "keywords": ["16:9", "brand", "cinematic", "no text"]
}
```

## Configuration Options

### Web Scraping Settings
```env
DEFAULT_TIMEOUT=30
MAX_RETRIES=3
HEADLESS_MODE=true
VERBOSE_LOGGING=false
```

### Business Search Settings
```env
DEFAULT_SEARCH_RADIUS=4000
```

## Project Structure

```
localfluence/
├── config.py              # Configuration management
├── business_scraper.py    # Google Places API and basic scraping
├── website_scraper.py     # AI-powered scraping with crawl4ai
├── main.py               # Main entry point with CLI
├── test_simple.py        # Simple test script
├── test_main_return.py   # Test script for return functionality
├── example_veo3.py       # Google Veo 3 prompt example
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── .env                  # Your API keys (not in git)
```

## Security Notes

- **Never commit API keys to version control**
- The `.env` file is automatically ignored by git
- Use environment variables for production deployments
- Rotate API keys regularly

## Troubleshooting

### Configuration Issues
```bash
# Check configuration status
python config.py

# Create new template
python config.py --create-template

# Validate configuration
python config.py --validate
```

### Common Errors

**"Google Places API key not found"**
- Set `GOOGLE_PLACES_API_KEY` in your `.env` file
- Get a key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

**"No LLM API key available"**
- Set at least one LLM API key (`GROQ_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`)
- Groq is recommended for its free tier and speed

**"Failed to scrape website"**
- Check if the business has a website
- Some websites may block automated access
- Try adjusting timeout settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 