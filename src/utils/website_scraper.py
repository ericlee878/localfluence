"""
Website Scraper Module

This module provides AI-powered website scraping functionality using crawl4ai.
It extracts structured business information and influencer marketing content
from business websites.

Author: Localfluence Team
"""

import json
import asyncio
from typing import List, Dict, Optional, Any

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
    LLMConfig,
)

from src.utils.google_maps_scraper import find_one_business
from src.config import get_groq_api_key


def get_browser_config() -> BrowserConfig:
    """
    Get the browser configuration for the web crawler.
    
    Returns:
        BrowserConfig: Configuration settings for the browser
    """
    return BrowserConfig(
        browser_type="chromium",
        headless=True,
        verbose=False,
    )


def get_business_extraction_strategy() -> LLMExtractionStrategy:
    """
    Get the LLM extraction strategy for general business information.
    
    Returns:
        LLMExtractionStrategy: Configuration for extracting business data
        
    Raises:
        ValueError: If GROQ_API_KEY is not configured
    """
    try:
        groq_api_key = get_groq_api_key()
    except ValueError:
        raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")
    
    return LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="groq/deepseek-r1-distill-llama-70b",
            api_token=groq_api_key,
        ),
        schema={
            "type": "object",
            "properties": {
                "business_name": {
                    "type": "string", 
                    "description": "Full business name"
                },
                "description": {
                    "type": "string", 
                    "description": "Brief description of the business"
                },
                "keywords": {
                    "type": "array", 
                    "items": {"type": "string"}, 
                    "description": "Relevant keywords for SEO and business categorization"
                },
                "services_offered": {
                    "type": "array", 
                    "items": {"type": "string"}, 
                    "description": "List of services or products offered"
                },
                "business_hours": {
                    "type": "string", 
                    "description": "Operating hours if found"
                },
                "contact_information": {
                    "type": "object",
                    "properties": {
                        "phone": {"type": "array", "items": {"type": "string"}},
                        "email": {"type": "array", "items": {"type": "string"}},
                        "address": {"type": "string"}
                    }
                },
                "social_media": {
                    "type": "object",
                    "properties": {
                        "facebook": {"type": "string"},
                        "twitter": {"type": "string"},
                        "instagram": {"type": "string"},
                        "linkedin": {"type": "string"},
                        "youtube": {"type": "string"}
                    }
                },
                "special_features": {
                    "type": "array", 
                    "items": {"type": "string"}, 
                    "description": "Special features, amenities, or unique selling points"
                },
                "target_audience": {
                    "type": "string", 
                    "description": "Who this business serves"
                },
                "price_range": {
                    "type": "string", 
                    "description": "Price range if mentioned (e.g., $, $$, $$$)"
                },
                "business_type": {
                    "type": "string", 
                    "description": "Type of business (restaurant, retail, service, etc.)"
                },
                "location_features": {
                    "type": "array", 
                    "items": {"type": "string"}, 
                    "description": "Location-specific features (parking, accessibility, etc.)"
                },
                "additional_notes": {
                    "type": "string", 
                    "description": "Any other relevant information"
                }
            },
            "required": ["business_name", "description", "keywords"]
        },
        extraction_type="schema",
        instruction=(
            "Extract comprehensive business information from this website. Focus on identifying "
            "keywords that would be useful for SEO, local search, and business categorization. "
            "Include all relevant services, features, and contact information. Be thorough but "
            "accurate in your extraction."
        ),
        input_format="markdown",
        verbose=False,
    )


def get_ai_video_content_strategy() -> LLMExtractionStrategy:
    """
    Get the LLM extraction strategy for AI marketing video content.
    
    Returns:
        LLMExtractionStrategy: Configuration for extracting data to create Google Veo 3 video prompts
        
    Raises:
        ValueError: If GROQ_API_KEY is not configured
    """
    try:
        groq_api_key = get_groq_api_key()
    except ValueError:
        raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")
    
    return LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="groq/deepseek-r1-distill-llama-70b",
            api_token=groq_api_key,
        ),
        schema={
            "type": "object",
            "properties": {
                "business_identity": {
                    "type": "object",
                    "properties": {
                        "brand_name": {"type": "string", "description": "Business/brand name"},
                        "brand_story": {"type": "string", "description": "Compelling brand story and mission"},
                        "unique_selling_points": {"type": "array", "items": {"type": "string"}, "description": "What makes this business unique"},
                        "brand_values": {"type": "array", "items": {"type": "string"}, "description": "Core brand values and personality"}
                    },
                    "description": "Core business identity and brand information"
                },
                "visual_elements": {
                    "type": "object",
                    "properties": {
                        "primary_products": {"type": "array", "items": {"type": "string"}, "description": "Main products or services to feature"},
                        "visual_style": {"type": "string", "description": "Desired visual aesthetic (e.g., modern, rustic, luxury, minimalist)"},
                        "color_palette": {"type": "array", "items": {"type": "string"}, "description": "Brand colors and visual themes"},
                        "environmental_elements": {"type": "array", "items": {"type": "string"}, "description": "Physical environment elements (interior, exterior, props)"},
                        "texture_materials": {"type": "array", "items": {"type": "string"}, "description": "Materials and textures to feature"}
                    },
                    "description": "Visual elements for video creation"
                },
                "target_audience": {
                    "type": "object",
                    "properties": {
                        "demographics": {"type": "array", "items": {"type": "string"}},
                        "interests": {"type": "array", "items": {"type": "string"}},
                        "lifestyle": {"type": "array", "items": {"type": "string"}},
                        "emotional_triggers": {"type": "array", "items": {"type": "string"}, "description": "Emotions to evoke in the audience"}
                    },
                    "description": "Target audience insights for video messaging"
                },
                "video_concepts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "concept_name": {"type": "string", "description": "Name of the video concept"},
                            "description": {"type": "string", "description": "Detailed description of the video scene"},
                            "style": {"type": "string", "description": "Visual style (cinematic, photorealistic, etc.)"},
                            "camera": {"type": "string", "description": "Camera movement and positioning"},
                            "lighting": {"type": "string", "description": "Lighting setup and mood"},
                            "environment": {"type": "string", "description": "Setting and location"},
                            "elements": {"type": "array", "items": {"type": "string"}, "description": "Key visual elements to include"},
                            "motion": {"type": "string", "description": "Movement and animation description"},
                            "ending": {"type": "string", "description": "How the video should conclude"},
                            "text": {"type": "string", "description": "Text overlays or call-to-action"},
                            "keywords": {"type": "array", "items": {"type": "string"}, "description": "Keywords for AI video generation"}
                        }
                    },
                    "description": "Multiple video concept ideas for Google Veo 3"
                },
                "brand_assets": {
                    "type": "object",
                    "properties": {
                        "logo_description": {"type": "string", "description": "How to incorporate the brand logo"},
                        "tagline": {"type": "string", "description": "Brand tagline or slogan"},
                        "signature_elements": {"type": "array", "items": {"type": "string"}, "description": "Signature brand elements to feature"}
                    },
                    "description": "Brand assets to incorporate in videos"
                },
                "call_to_action": {
                    "type": "object",
                    "properties": {
                        "primary_cta": {"type": "string", "description": "Main call-to-action message"},
                        "secondary_cta": {"type": "string", "description": "Secondary call-to-action options"},
                        "contact_info": {"type": "string", "description": "How to display contact information"}
                    },
                    "description": "Call-to-action elements for video"
                },
                "technical_specs": {
                    "type": "object",
                    "properties": {
                        "aspect_ratio": {"type": "string", "description": "Video aspect ratio (16:9, 9:16, etc.)"},
                        "duration": {"type": "string", "description": "Target video duration"},
                        "quality": {"type": "string", "description": "Desired video quality level"}
                    },
                    "description": "Technical specifications for video generation"
                }
            },
            "required": ["business_identity", "visual_elements", "target_audience", "video_concepts"]
        },
        extraction_type="schema",
        instruction=(
            "Extract comprehensive business information to create AI marketing video prompts for Google Veo 3. "
            "Focus on identifying visual elements, brand identity, target audience, and creating multiple video concepts. "
            "Each video concept should be detailed enough to generate a complete Google Veo 3 prompt with description, "
            "style, camera, lighting, elements, motion, and keywords. Be creative and thorough in identifying "
            "all potential video angles and opportunities that showcase the business effectively."
        ),
        input_format="markdown",
        verbose=False,
    )


async def scrape_business_website_ai(
    business_name: str, 
    business_address: str,
    extraction_type: str = "ai_video"
) -> Optional[Dict[str, Any]]:
    """
    Scrape a business website using AI to extract structured information.
    
    Args:
        business_name: Name of the business
        business_address: Address of the business
        extraction_type: Type of extraction - "full" for complete business info, "influencer" for influencer content, "ai_video" for AI video prompts
        
    Returns:
        Dictionary containing extracted business information or None if failed
        
    Raises:
        ValueError: If extraction_type is invalid
        Exception: If scraping process fails
    """
    if extraction_type not in ["full", "influencer", "ai_video"]:
        raise ValueError("extraction_type must be 'full', 'influencer', or 'ai_video'")
    
    try:
        # Find the business using Google Places API
        print(f"Finding business: {business_name}")
        business = find_one_business(business_name, business_address)
        
        if not business:
            print(f"Business not found: {business_name}")
            return None
        
        website = business.get('website')
        if not website:
            print(f"No website found for {business_name}")
            return {
                'businessInfo': business,
                'websiteData': None,
                'error': 'No website available'
            }
        
        print(f"Found website: {website}")
        
        # Initialize the crawler
        crawler = AsyncWebCrawler()
        
        # Choose extraction strategy based on type
        if extraction_type == "influencer":
            strategy = get_ai_video_content_strategy()
        elif extraction_type == "ai_video":
            strategy = get_ai_video_content_strategy()
        else:
            strategy = get_business_extraction_strategy()
        
        # Scrape the website
        result = await crawler.arun(
            url=website,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=strategy,
                session_id=f"business_{business_name.replace(' ', '_')}",
            ),
        )
        
        if not result.success:
            print(f"Failed to scrape website: {result.error_message}")
            return {
                'businessInfo': business,
                'websiteData': None,
                'error': result.error_message
            }
        
        if not result.extracted_content:
            print("No content extracted from website")
            return {
                'businessInfo': business,
                'websiteData': None,
                'error': 'No content extracted'
            }
        
        # Parse the extracted content
        try:
            extracted_data = json.loads(result.extracted_content)
        except json.JSONDecodeError as e:
            print(f"Failed to parse extracted content: {e}")
            return {
                'businessInfo': business,
                'websiteData': None,
                'error': f'JSON parsing error: {str(e)}',
                'rawContent': result.extracted_content
            }
        
        return {
            'businessInfo': business,
            'websiteData': extracted_data,
            'rawHtml': result.cleaned_html,
            'extractionType': extraction_type
        }
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return {
            'businessInfo': business if 'business' in locals() else None,
            'websiteData': None,
            'error': str(e)
        }
