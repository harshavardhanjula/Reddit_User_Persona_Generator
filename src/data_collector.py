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
            print(f"\n=== User Details for {username} ===")
            user_details = self.get_user_details(username)
            print(f"Created: {datetime.fromtimestamp(self.reddit.redditor(username).created_utc)}")
            print(f"Link Karma: {user_details['karma']['link_karma']}")
            print(f"Comment Karma: {user_details['karma']['comment_karma']}")
            print(f"Total Karma: {user_details['karma']['total_karma']}")
            print(f"Has Verified Email: {user_details['has_verified_email']}")
            print("=== End of User Details ===\n")

            print("\n=== Posts ===")
            posts = self.get_posts(username)
            for post in posts:
                print(f"Post Title: {post['title']}")
                print(f"Subreddit: r/{post['subreddit']}")
                print(f"Score: {post['score']} (Positive: {post['score'] >= 0})")
                print(f"Date: {post['created_utc']}")
                print("---")
            print("=== End of Posts ===\n")

            print("\n=== Comments ===")
            comments = self.get_comments(username)
            for comment in comments:
                print(f"Comment Text: {comment['text'][:100]}...")
                print(f"Subreddit: r/{comment['subreddit']}")
                print(f"Score: {comment['score']}")
                print(f"Date: {comment['created_utc']}")
                print("---")
            print("=== End of Comments ===\n")

            return {
                'username': username,
                'posts': posts,
                'comments': comments,
                'user_details': user_details
            }

        except Exception as e:
            print(f"Error fetching user data: {str(e)}")
            return None
