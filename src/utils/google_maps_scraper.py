"""
Business Scraper Module

This module provides functionality for searching and scraping business information
using Google Places API and website scraping capabilities.

Author: Localfluence Team
"""

import googlemaps
import requests
from typing import Dict, List, Optional, Any
from src.config import GOOGLE_API_KEY


# Initialize Google Maps client
if not GOOGLE_API_KEY:
    raise ValueError(
        "Google Places API key not found. Please set GOOGLE_PLACES_API_KEY in your config."
    )

gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

def get_business_details(place_id: str) -> Dict[str, Any]:
    """
    Get detailed information for a business by place ID.
    
    Args:
        place_id: Google Places place ID
        
    Returns:
        Dictionary containing business details
        
    Raises:
        requests.RequestException: If API request fails
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "key": GOOGLE_API_KEY,
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,types,icon_background_color,opening_hours"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["result"]





def find_one_business(name: str, address: str) -> Optional[Dict[str, Any]]:
    """
    Find a specific business by name and address.
    
    Args:
        name: Business name
        address: Business address
        
    Returns:
        Business details dictionary or None if not found
        
    Raises:
        requests.RequestException: If API request fails
        KeyError: If no candidates found in response
    """
    search_text = f"{name}, {address}"
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": search_text,
        "inputtype": "textquery",
        "fields": "place_id,name,formatted_address",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    
    result = response.json()
    if not result.get('candidates'):
        print("No matching place found.")
        return None
    
    place_id = result['candidates'][0]['place_id']
    if not place_id:
        print("No matching place found.")
        return None
    
    return get_business_details(place_id)





if __name__ == "__main__":
    # Example usage of Google Places API functions
    coordinates = "32.6099,-85.4808"
    business = find_one_business("Hamilton's", "174 E Magnolia Ave, Auburn, AL 36830, USA")
    
    if business:
        print("Found business details:")
        print(f"Name: {business.get('name')}")
        print(f"Address: {business.get('formatted_address')}")
        print(f"Website: {business.get('website')}")
        print(f"Phone: {business.get('formatted_phone_number')}")
        print(f"Rating: {business.get('rating')}")
        print(f"Types: {business.get('types')}")
    else:
        print("No business found.")

