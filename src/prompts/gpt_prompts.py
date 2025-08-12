#!/usr/bin/env python3
"""
GPT Prompts and Call Settings Module

This module loads prompts and settings from JSON files for GPT API calls used in the VEO3 prompt generation.

Author: Localfluence Team
"""

import json
import os
from typing import Dict, Any, List

def load_prompts() -> Dict[str, Any]:
    """Load prompts from the JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_file = os.path.join(current_dir, "prompts.json")
    
    with open(prompts_file, 'r') as f:
        return json.load(f)

# Load prompts from JSON
PROMPTS_DATA = load_prompts()

# GPT Model Settings
GPT_MODEL = PROMPTS_DATA["gpt_settings"]["model"]
GPT_TEMPERATURE = PROMPTS_DATA["gpt_settings"]["temperature"]

# Stage 1 Prompt - Creative Brief to Cinematic Prompt
STAGE1_SYSTEM_PROMPT = PROMPTS_DATA["stage1"]["system_prompt"]

def get_stage1_user_prompt(creative_brief: str) -> str:
    """Generate the user prompt for stage 1."""
    template = PROMPTS_DATA["stage1"]["user_prompt_template"]
    return template.format(creative_brief=creative_brief)

# Stage 2 Prompt - Cinematic Prompt to JSON Structure
STAGE2_SYSTEM_PROMPT = PROMPTS_DATA["stage2"]["system_prompt"]

def get_stage2_user_prompt(creative_brief: str) -> str:
    """Generate the user prompt for stage 2."""
    template = PROMPTS_DATA["stage2"]["user_prompt_template"]
    return template.format(creative_brief=creative_brief) 