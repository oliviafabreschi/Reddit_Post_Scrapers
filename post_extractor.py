# developed to extract reddit posts
# By Olivia Fabreschi Aug 2024
import praw
import csv
import json

import openai

# Load configuration from file
with open('config.json') as config_file:
    config = json.load(config_file)

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
    # for post in subreddit.top(limit=limit, time_filter='all'):
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
post_limit = 10  #limit of Number of posts to scrape

# Convert dates to UNIX timestamps
# calling authentication function
reddit = authenticate_reddit()
csv_filename = 'reddit_results.csv'  #CSV file to write the posts
# calling posts function
posts = fetch_subreddit_posts(reddit, subreddit_name, post_limit)
# calling csv function
write_posts_to_csv(posts, csv_filename)


print(f"Data written to {csv_filename}")










