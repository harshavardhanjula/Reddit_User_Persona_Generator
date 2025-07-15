import praw
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List, Optional

# Reddit API configuration
REDDIT_API_CONFIG = {
    "client_id": "REDDIT_CLIENT_ID",
    "client_secret": "REDDIT_CLIENT_SECRET",
    "user_agent": "Reddit Persona Generator v1.0"
}

# Data limits
POST_LIMIT = 100
COMMENT_LIMIT = 100

class RedditDataCollector:
    def __init__(self):
        load_dotenv()
        self.reddit = praw.Reddit(
            client_id=os.getenv(REDDIT_API_CONFIG["client_id"]),
            client_secret=os.getenv(REDDIT_API_CONFIG["client_secret"]),
            user_agent=REDDIT_API_CONFIG["user_agent"]
        )

    def extract_username(self, url: str) -> str:
        """Extract username from Reddit profile URL"""
        return url.split('/')[-2]

    def get_user_details(self, username: str) -> Dict:
        """Get essential user information"""
        redditor = self.reddit.redditor(username)
        return {
            'karma': {
                'link_karma': redditor.link_karma,
                'comment_karma': redditor.comment_karma,
                'total_karma': redditor.link_karma + redditor.comment_karma
            },
            'account_age': datetime.fromtimestamp(redditor.created_utc).isoformat(),
            'has_verified_email': redditor.has_verified_email
        }

    def get_posts(self, username: str, limit: int = POST_LIMIT) -> List[Dict]:
        """Get essential post information, filtering out negatively scored posts"""
        posts = []
        redditor = self.reddit.redditor(username)
        
        for submission in redditor.submissions.new(limit=limit):
            if submission.score >= 0:  # Only include posts with non-negative score
                posts.append({
                    'title': submission.title,
                    'text': submission.selftext,
                    'subreddit': submission.subreddit.display_name,
                    'score': submission.score,
                    'created_utc': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'url': f'https://reddit.com{submission.permalink}'
                })
        
        return posts

    def get_comments(self, username: str, limit: int = COMMENT_LIMIT) -> List[Dict]:
        """Get user's comments"""
        comments = []
        redditor = self.reddit.redditor(username)
        
        for comment in redditor.comments.new(limit=limit):
            comments.append({
                'text': comment.body,
                'subreddit': comment.subreddit.display_name,
                'score': comment.score,
                'created_utc': datetime.fromtimestamp(comment.created_utc).isoformat(),
                'url': f'https://reddit.com{comment.permalink}'
            })
        
        return comments

    def scrape_user_data(self, username: str) -> Optional[Dict]:
        """Scrape user's data from Reddit"""
        try:
            user_details = self.get_user_details(username)
            posts = self.get_posts(username)
            comments = self.get_comments(username)
            
            return {
                'username': username,
                'posts': posts,
                'comments': comments,
                'user_details': user_details
            }

        except Exception as e:
            print("Error fetching user data")
            return None
