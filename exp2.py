import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re

class OlympicsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.base_url = 'https://www.reddit.com'  # Changed to www.reddit.com
        
    def clean_text(self, text):
        if text:
            text = re.sub(r'[\n\r\t]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        return ''

    def get_posts(self, subreddit='sports', query='Olympics 2024', limit=25):
        posts_data = []
        url = f"{self.base_url}/r/{subreddit}/search/.json?q={query}&limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'children' in data['data']:
                    for post in data['data']['children']:
                        post_data = post['data']
                        posts_data.append({
                            'title': self.clean_text(post_data.get('title', 'No Title')),
                            'score': post_data.get('score', 0),
                            'author': post_data.get('author', '[deleted]'),
                            'url': self.base_url + post_data.get('permalink', ''),
                            'num_comments': post_data.get('num_comments', 0),
                            'created_utc': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                            'subreddit': post_data.get('subreddit', subreddit)
                        })
                    print(f"Successfully collected {len(posts_data)} posts from r/{subreddit}")
                else:
                    print(f"No posts found in r/{subreddit}")
            else:
                print(f"Failed to get data from r/{subreddit}. Status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error collecting data from r/{subreddit}: {str(e)}")
            
        return posts_data

    def analyze_engagement(self, row):
        score = int(row.get('score', 0))
        comments = int(row.get('num_comments', 0))
        
        if score > 1000 or comments > 100:
            return 'High'
        elif score > 100 or comments > 20:
            return 'Medium'
        else:
            return 'Low'

    def collect_olympics_data(self):
        # Multiple subreddits and queries for broader data collection
        subreddits = ['sports', 'olympics', 'worldnews', 'paris']
        queries = ['Olympics 2024', 'Paris Olympics', 'Olympic Games']
        
        all_posts = []
        
        # Collect data from each subreddit with each query
        for subreddit in subreddits:
            for query in queries:
                print(f"\nCollecting data from r/{subreddit} for query: {query}")
                posts = self.get_posts(subreddit=subreddit, query=query)
                all_posts.extend(posts)
                time.sleep(2)  # Respect rate limiting
        
        if not all_posts:
            print("No data collected. Please check your internet connection and try again.")
            return None
            
        # Convert to DataFrame
        df = pd.DataFrame(all_posts)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['url'])
        
        # Add engagement level
        df['engagement_level'] = df.apply(self.analyze_engagement, axis=1)
        
        # Add post categories
        def categorize_post(title):
            title = title.lower()
            categories = {
                'Ceremonies': ['opening', 'ceremony', 'closing'],
                'Swimming': ['swim', 'swimming', 'pool'],
                'Athletics': ['track', 'field', 'athletics', 'run'],
                'Event Schedule': ['schedule', 'program', 'timing'],
                'Infrastructure': ['stadium', 'venue', 'facility'],
                'Teams': ['team', 'athlete', 'qualification']
            }
            
            for category, keywords in categories.items():
                if any(keyword in title for keyword in keywords):
                    return category
            return 'General'
            
        df['category'] = df['title'].apply(categorize_post)
        
        # Save the data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"olympics_2024_data_{timestamp}.csv"
        
        # Reorder columns for better readability
        columns_order = [
            'title', 'score', 'num_comments', 'engagement_level',
            'category', 'subreddit', 'author', 'created_utc', 'url'
        ]
        df = df[columns_order]
        
        # Save to CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        # Generate and save summary
        summary = {
            'Total Posts': len(df),
            'Unique Subreddits': df['subreddit'].nunique(),
            'Average Score': df['score'].mean(),
            'Average Comments': df['num_comments'].mean(),
            'Categories Distribution': df['category'].value_counts().to_dict(),
            'Engagement Levels': df['engagement_level'].value_counts().to_dict()
        }
        
        # Save summary
        summary_filename = f"olympics_2024_summary_{timestamp}.csv"
        pd.DataFrame([summary]).to_csv(summary_filename, index=False)
        
        print(f"\nData collection complete!")
        print(f"Main data saved to: {filename}")
        print(f"Summary saved to: {summary_filename}")
        print(f"\nCollection Summary:")
        print(f"Total posts collected: {len(df)}")
        print(f"Number of subreddits: {df['subreddit'].nunique()}")
        print(f"Date range: {df['created_utc'].min()} to {df['created_utc'].max()}")
        
        return df

def main():
    scraper = OlympicsScraper()
    print("Starting data collection for 2024 Olympics...")
    olympics_data = scraper.collect_olympics_data()
    
    if olympics_data is not None and not olympics_data.empty:
        print("\nData collection successful!")
    else:
        print("\nData collection failed. Please check the error messages above.")

if __name__ == "__main__":
    main()