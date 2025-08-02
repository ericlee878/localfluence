#!/usr/bin/env python3
"""
Localfluence - Simple Business to VEO3 Prompt Generator

This module provides the main entry point for generating VEO3 prompts from business information.

Usage:
    python main.py "Business Name" "Address"

Author: Localfluence Team
"""

import sys
import os
import asyncio
from typing import Optional, Dict, Any

# Add the project root to Python path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.google_maps_scraper import find_one_business
from src.config import validate_configuration
from src.utils.argument_parser import parse_and_validate_arguments
from src.utils.website_scraper import scrape_business_website_ai
from src.prompts.veo_prompt_generator import veo_prompt_stage1, veo_prompt_stage2


# python main.py "Hamiltons" "174 E Magnolia Ave, Auburn, AL 36830, USA"
def main() -> Optional[str]:
    """
    Main function to get the VEO3 prompt for a business
    """
    args = parse_and_validate_arguments()
    if not args:
        print("Invalid arguments provided.")
        return None
    
    if not validate_configuration():
        return None
    
    business_name = args['business_name']
    address = args['address']
    
    business_info = find_one_business(business_name, address)
    
    if not business_info:
        print("Business not found!")
        return None

    website_scraped_info = asyncio.run(scrape_business_website_ai(business_name, address, "ai_video"))    
    
    prompt1 = veo_prompt_stage1(website_scraped_info)
    final_prompt = veo_prompt_stage2(prompt1)

        
    print("\n" + "=" * 50)
    print("VEO3 PROMPT GENERATED!")
    print("=" * 50)
    print(final_prompt)





if __name__ == "__main__":
    result = main()
    if result is None:
        sys.exit(1) 