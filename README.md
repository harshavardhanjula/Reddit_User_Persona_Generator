# Reddit User Persona Generator

A Python-based tool that generates detailed, professional personas for Reddit users based on their activity patterns, interests, and communication style.

## Features

- Extracts user data from Reddit API
- Analyzes posts, comments, and user behavior
- Generates detailed, human-like personas
- Focuses on positive, well-received content
- No references to specific posts or citations

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd reddit-persona-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your Reddit API credentials:
  - Go to https://www.reddit.com/prefs/apps
  - Create a new script app
  - Add `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` to your `.env` file
- Add your OpenRouter API key:
  - Sign up at https://openrouter.ai
  - Add `OPENROUTER_API_KEY` to your `.env` file

## Usage

Run the script with a Reddit profile URL:
```bash
python main.py "https://www.reddit.com/user/username/"
```

The generated persona will be saved in the `personas` directory with the format `username_persona.txt`.

## Project Structure

```
reddit-persona-generator/
├── .env                    # Environment variables (copy from .env.example)
├── main.py                 # Main script
├── personas/               # Generated personas
├── requirements.txt        # Python dependencies
├── src/
│   ├── data_collector.py  # Reddit data extraction
│   └── persona_generator.py # Persona generation using OpenRouter API
└── README.md              # This file
```

## Dependencies

- praw
- openrouter
- python-dotenv

