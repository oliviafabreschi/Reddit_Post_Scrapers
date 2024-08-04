# developed to extract reddit posts
# By Olivia Fabreschi Aug 2024
from datetime import time, datetime

import praw
import csv
import json

import openai

# Load configuration from file
with open('config.json') as config_file:
    config = json.load(config_file)


def fetch_posts_within_timeframe(subreddit_name, start_time, end_time, limit):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for submission in subreddit.submissions(start=start_time, end=end_time):
        # Check if the post's creation time is within the specified timeframe
        if start_time <= submission.created_utc <= end_time:
            posts.append({
                'title': submission.title,
                'score': submission.score,
                'url': submission.url,
                'id': submission.id,
                'subreddit': submission.subreddit.display_name,
                'selftext': submission.selftext,
                'created': submission.created_utc
            })
        if len(posts) >= limit:
            break

    return posts

def date_to_timestamp(date_string):
    # Convert a date string (e.g., 'YYYY-MM-DD') to UNIX timestamp
    dt = datetime.strptime(date_string, '%Y-%m-%d')
    # Convert datetime object to UNIX timestamp
    return int(dt.timestamp())

def authenticate_reddit():
    reddit = praw.Reddit(
        user_agent='True', # not important
        client_id=config.get('client_id'),  # client ID from reddit.com app, in config file
        client_secret=config.get("client_secret")  # client secret, in config file
    )
    return reddit

def fetch_subreddit_posts(reddit, subreddit_name, limit):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.top(limit=limit):
        posts.append({
            'title': post.title,
            'score': post.score,
            'url': post.url,
            'id': post.id,
            'subreddit': post.subreddit.display_name,
            'selftext': post.selftext,
            'created': post.created
        })
    return posts

# searching for keyword
def search_keyword(posts, keyword):
    keyword = keyword.lower()
    results = []

    for post in posts:
        title_contains = keyword in post['title'].lower()
        body_contains = keyword in post['selftext'].lower() if post['selftext'] else False

        if title_contains or body_contains:
            results.append(post)

    return results

# open a file for writing in CSV format
def write_posts_to_csv(posts, filename):
    # Extract the keys from the first post to use as headers
    headers = posts[0].keys()

    # Open the file in append mode
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header only if the file is new
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the post data
        for post in posts:
            writer.writerow(post)

# main calling all functions
subreddit_name = 'Scams'  #subreddit to scrape
post_limit = 100000000000  #Number of posts to scrape
start_date = '2021-01-01'  # Start date in 'YYYY-MM-DD' format
end_date = '2024-08-04'    # End date in 'YYYY-MM-DD' format

# Convert dates to UNIX timestamps
start_timestamp = date_to_timestamp(start_date)
end_timestamp = date_to_timestamp(end_date)
keyword = "elon musk"
# calling authentication function
reddit = authenticate_reddit()
csv_filename = 'reddit_results.csv'  #CSV file to write the posts
# calling posts function
posts = fetch_subreddit_posts(reddit, subreddit_name, post_limit)
# calling csv function
write_posts_to_csv(posts, csv_filename)
# Search for keyword
matching_posts = search_keyword(posts, keyword)

print(f"Data written to {csv_filename}")
# Display matching posts
for post in matching_posts:
    print(f"Title: {post['title']}")
    print(f"URL: {post['url']}")
    print(f"Score: {post['score']}")
    print(f"Created: {post['created']}")
    print()










