import os
import sys
# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collector import RedditDataCollector
from src.persona_generator import PersonaGenerator

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <reddit_profile_url>")
        sys.exit(1)

    url = sys.argv[1]
    
    try:
        # Initialize components
        data_collector = RedditDataCollector()
        persona_generator = PersonaGenerator()
        
        # Extract username
        username = data_collector.extract_username(url)
        
        # Collect user data
        user_data = data_collector.scrape_user_data(username)
        
        # Generate persona
        persona = persona_generator.generate_persona(user_data)

        if persona:
            # Create personas directory if it doesn't exist
            os.makedirs('personas', exist_ok=True)
            
            # Save persona to file
            persona_file = os.path.join('personas', f'{username}_persona.txt')
            with open(persona_file, 'w', encoding='utf-8') as f:
                f.write(persona)
            
            print(f"Persona generated and saved to {persona_file}")
            return True
        else:
            print("Failed to generate persona")
            return False
    except Exception as e:
        print(f"Error generating persona: {str(e)}")
        return False

if __name__ == "__main__":
    main()
