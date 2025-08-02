"""
Configuration Module for Localfluence

This module manages API keys and configuration settings for the Localfluence
application. It provides secure loading of environment variables and validation
of required configuration.

Author: Localfluence Team
"""

import os
from typing import Optional
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# API Keys
GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_PLACES_API_KEY")
GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")


def validate_configuration() -> bool:
    """
    Validate that all required API keys are present and properly configured.
    
    Returns:
        True if all required configuration is valid, False otherwise
        
    Note:
        This function will print helpful error messages if configuration
        is missing or invalid.
    """
    if not GOOGLE_API_KEY:
        print("❌ Google Places API key not found!")
        print("Please set GOOGLE_PLACES_API_KEY in your .env file")
        return False
    
    if not GROQ_API_KEY:
        print("⚠️  Groq API key not found - AI scraping will not work")
        print("Get a free key from: https://console.groq.com/")
        return False

    if not OPENAI_API_KEY:
        print("⚠️  Open AI API key not found - AI prompt create will not work")
        print("Get a free key from: https://platform.openai.com/")
        return False
    
    return True


def get_google_api_key() -> str:
    """
    Get the Google Places API key.
    
    Returns:
        The Google Places API key
        
    Raises:
        ValueError: If the API key is not configured
    """
    if not GOOGLE_API_KEY:
        raise ValueError("Google Places API key not configured")
    return GOOGLE_API_KEY


def get_groq_api_key() -> str:
    """
    Get the Groq API key.
    
    Returns:
        The Groq API key
        
    Raises:
        ValueError: If the API key is not configured
    """
    if not GROQ_API_KEY:
        raise ValueError("Groq API key not configured")
    return GROQ_API_KEY 

def get_openai_api_key() -> str:
    """
    Get the Open AI API key.
    
    Returns:
        The Open AI API key
        
    Raises:
        ValueError: If the API key is not configured
    """
    if not OPENAI_API_KEY:
        raise ValueError("Open AI API key not configured")
    return OPENAI_API_KEY 