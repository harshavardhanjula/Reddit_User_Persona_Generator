import os
import requests
import json
from typing import Dict, Optional
from dotenv import load_dotenv

# OpenRouter API configuration
OPENROUTER_API_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "moonshotai/kimi-k2:free"

# Output directory for personas
PERSONAS_DIR = "personas"

class PersonaGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

    def generate_prompt(self, user_data: Dict) -> str:
        """Generate the prompt for persona generation"""
        # Format data for analysis
        data_str = json.dumps(user_data, indent=2)
        
        return f"""#You are an expert **social behavior analyst AI** specializing in digital personalities. Using structured Reddit user data, your task is to generate a **captivating and nuanced persona profile** that goes beyond basic facts. This profile should resemble a well-crafted character study, highlighting the essence of the user’s online identity and personality.

### **Input Data**
```
{data_str}
```

### **Persona Creation Guidelines**
1. **Narrative Focus:** Craft an engaging narrative that tells the story of the user’s online personality, habits, and behaviors.
2. **Personality Insights:** Capture their distinct traits, including tone (e.g., sarcastic, helpful) and communication style.
3. **Behavior Patterns:** Infer patterns, interests, and subreddit habits from their data, but avoid quoting or referencing specific posts.
4. **Tagline Creation:** Write a memorable one-liner that encapsulates their Reddit persona.
5. **Community Role:** Describe their typical roles in discussions (e.g., mentor, challenger, comedian).
6. **Unique Traits:** Highlight distinct patterns, hobbies, or quirks that make them stand out.
7. **Psychological Themes:** Reflect inferred tendencies such as empathy, caution, or risk-taking.
8. **Motivations & Frustrations:** Analyze what drives or annoys them in their online interactions.
9. **Fluid Style:** Maintain a smooth and engaging tone, like a thoughtful social researcher.

### **Output Requirements**
- **Persona Header:** Use the Reddit username as the header.
- **Tagline:** A concise, expressive summary of their online identity.
- **Narrative Overview:** A descriptive profile of who they are on Reddit.
- **Key Interests:** Topics and communities they frequently engage in.
- **Communication Style:** Tone, quirks, and posting/commenting behaviors.
- **Community Interactions:** Roles they play in online communities.
- **Signature Traits:** Distinctive aspects of their behavior or habits.
- **Motivations & Frustrations:** Insights into what drives or troubles them.
- **Trademark Behaviors:** Unique posting or interaction styles.

Present the profile with clear section headers and a readable structure. Aim for a compelling, human-like portrayal, while avoiding references, citations, or links to specific posts/comments.

Generate the persona profile based on the provided data.
"""

    def generate_persona(self, user_data: Dict) -> Optional[str]:
        """Generate persona using OpenRouter API"""
        if not user_data:
            print("Error: No user data available")
            return None



        # Format data for prompt
        data_str = json.dumps(user_data, indent=2)
        prompt = self.generate_prompt(user_data)

        # OpenRouter API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in Reddit persona analysis. Generate a detailed persona following the exact structure shown in the example. Use markdown formatting to maintain the visual structure. Focus on capturing the essence of the user's personality and behavior patterns without referencing specific posts or comments."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(OPENROUTER_API_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error generating persona: {str(e)}")
            return None
