from openai import OpenAI
import os
from src.config import get_openai_api_key

import openai

def veo_prompt_stage1(creative_brief):
    client = OpenAI(api_key=get_openai_api_key())

    system_prompt = (
        "You are a creative prompt engineer for Veo v3. Your job is to turn high-level brand video ideas into concise, visually specific, cinematic prompts that will be used to generate videos with Veo. "
        "Make sure the final prompt includes a tone (e.g. upbeat, nostalgic), camera movement, lighting, setting, and style. Make it Gen-Z appealing and visually stunning."
    )

    user_prompt = f"""
    Turn the following brand creative brief into a cinematic Veo v3 prompt targeted at Gen-Z:

    {creative_brief}

    Keep it under 700 characters. The result should be visually specific and cinematic enough to pass to Veo's video model. Avoid vagueness.
    """

    response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9
        )

    return response.choices[0].message.content


def veo_prompt_stage2(creative_brief: str) -> dict:
    client = OpenAI(api_key=get_openai_api_key())

    system_prompt = """You are a world-class creative director who specializes in short-form video ads made for Gen Z — think TikTok, Reels, and YouTube Shorts.

                        Generate a **cinematic video prompt** in JSON format for **Veo v3** that **markets a local business without showing the business itself**. Instead, use storytelling, symbolism, and creator-style formats to evoke what the business feels like.

                        ---

                        **Target Audience:** Gen Z (18–25)

                        **DO NOT Include:**
                        - Any footage, images, or signs from the actual business
                        - Logos, storefronts, recognizable branding, or real-world identifiers
                        - Any specific text or visual that could be reverse image-searched

                        **If the business is a:**
                        - **Restaurant** → Emphasize the food in a way that makes it **look irresistible** (melting cheese, golden-hour plating, steamy close-ups)
                        - **Café** → Focus on visually **romanticizing the coffee** (slow-pour shots, cream swirling, mugs against sunlight)

                        ---

                        **Conceptual Formats to Use:**
                        1. **POV Voiceovers** – e.g., “POV: You stumbled into the coziest brunch spot and the playlist is all 2014 Tumblr girl vibes.”
                        2. **Narrative Hooks** – e.g., “I wasn’t going to share this place because I wanted it all to myself…”
                        3. **Skits/Characters** – e.g., “Mom at brunch: ‘This is the best toast I’ve ever had.’”
                        4. **Mood Collages** – abstract visuals like “hands holding a coffee,” “sunlight through a window,” or “shoes tapping tile”
                        5. **Ambient Soundscapes** – play café background sounds, lo-fi music, or ambient city chatter
                        6. **Conceptual Lines** – e.g., “This place feels like the inside of my comfort zone.”
                        7. **Geolocation Teases** – e.g., “Somewhere near the green door off Main Street...”
                        8. **Review-Style Reactions** – e.g., “Just tried the wildest lemonade ever — here’s what happened.”

                        ---

                        **Visual Style:**
                        - No literal footage of the business
                        - Use metaphor, symbolism, or vibe-matching visuals
                        - Style can be dreamy, surreal, punchy, or mood-heavy
                        - Golden hour, slow zooms, bokeh, or bold handheld shots welcome

                        **Audio:**
                        - **Always include spoken word** (VO, chaotic review, storytime, etc.)
                        - Capture the **essence** of the business through emotion, tone, or character — not facts
                        - Example tones: cozy overshare, sarcastic Gen Z monologue, poetic aesthetic, chaotic review

                        **Viral Checklist:**
                        - Hook in 3 seconds (gatekeep-y or emotional)
                        - Relatable tropes (social anxiety, “this is so me,” romanticizing your life)
                        - Loopable
                        - Shareable lines: “If you know, you know”

                        ---

                        **Output Format:**
                        ```json
                        {
                        "description": "...",         // Creative summary of the concept
                        "style": "...",               // Visual tone (e.g., dreamy realism, Gen Z chaos)
                        "camera": "...",              // Movement or framing
                        "lighting": "...",            // Mood and feel
                        "environment": "...",         // Abstract/generalized location (e.g., a window seat at dusk)
                        "elements": [...],            // Symbolic objects, not business imagery
                        "motion": "...",              // Scene flow and transitions
                        "audio": "...",               // Spoken VO, quirky line, skit dialogue
                        "ending": "...",              // Loop or emotional close
                        "text": "none",               // No on-screen text
                        "keywords": [...]             // Veo-style hashtags like #cozyaesthetic, #pov, #hiddenvibe
                        }
                        """

    user_prompt = f"Creative brief: {creative_brief}\n\nGenerate the cinematic video prompt now."

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        temperature=0.9,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
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
        return json.loads(cleaned)

