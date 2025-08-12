from openai import OpenAI
import os
from src.config import get_openai_api_key
from src.prompts.gpt_prompts import (
    GPT_MODEL, 
    GPT_TEMPERATURE,
    STAGE1_SYSTEM_PROMPT,
    STAGE2_SYSTEM_PROMPT,
    get_stage1_user_prompt,
    get_stage2_user_prompt
)

import openai

def veo_prompt_stage1(creative_brief):
    client = OpenAI(api_key=get_openai_api_key())

    response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": STAGE1_SYSTEM_PROMPT},
                {"role": "user", "content": get_stage1_user_prompt(creative_brief)}
            ],
            temperature=GPT_TEMPERATURE
        )

    return response.choices[0].message.content


def veo_prompt_stage2(creative_brief: str) -> dict:
    client = OpenAI(api_key=get_openai_api_key())

    response = client.chat.completions.create(
        model=GPT_MODEL,
        temperature=GPT_TEMPERATURE,
        messages=[
            {"role": "system", "content": STAGE2_SYSTEM_PROMPT},
            {"role": "user", "content": get_stage2_user_prompt(creative_brief)}
        ]
    )

    # Extract and parse response
    reply = response.choices[0].message.content

    try:
        import json
        return json.loads(reply)
    except json.JSONDecodeError:
        # If it's not valid JSON (e.g., Markdown code block), try cleaning
        cleaned = reply.strip().strip("```json").strip("```")
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Raise an exception if JSON parsing fails
            raise ValueError(f"Failed to parse JSON response from GPT API. Response: {reply}")

