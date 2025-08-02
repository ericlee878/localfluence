#!/usr/bin/env python3
"""
Command Line Interface Utilities Module

This module contains functions for handling command line arguments and
CLI-related functionality for the Localfluence application.

Author: Localfluence Team
"""

import argparse
from typing import Optional, Dict, Any


def parse_and_validate_arguments() -> Optional[Dict[str, Any]]:
    """Parse and validate command line arguments, returning them as a dictionary."""
    try:
        parser = argparse.ArgumentParser(
            description="Localfluence - Simple Business to VEO3 Prompt Generator",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
        Examples:
        python main.py "Hamilton's" "174 E Magnolia Ave, Auburn, AL 36830, USA"
        python main.py "Starbucks" "123 Main St, New York, NY 10001"
            """
        )
        
        parser.add_argument("business_name", help="Name of the business")
        parser.add_argument("address", help="Address of the business")
        
        args = parser.parse_args()
        
        # Validate arguments
        if not args.business_name or not args.address:
            print("Missing required arguments: business_name and address")
            return None
        
        return {
            "business_name": args.business_name,
            "address": args.address
        }
        
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        return None 