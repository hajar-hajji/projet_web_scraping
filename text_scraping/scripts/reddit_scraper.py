import praw
import os
import csv
import datetime as dt
from utils.nlp import *
from utils.utils import *

def scrap_reddit(reddit, searched_words, path, num_posts=2, print_results=True, store_results=False, type_data='posts'):
    # Access the subreddit 'all'
    subreddit = reddit.subreddit('all')
    # Get the posts or comments related to the searched word
    searched_words = [term.strip() for term in searched_words.split(',')]
    results = subreddit.search(' AND '.join(searched_words), limit=num_posts)
    data_to_print = []
    # Extract information from each post or comment
    for post in results:
        if type_data == 'posts':
            title = post.title  # Title of the post
            content = post.selftext  # Content of the post
            combined = title + ' ' + content
            sentiment_label, n_stars = analyze_sentiment(combined[:512]) # Sentiment detection (post)
            data_info = {
                "Title": title, 
                "Content": content,  
                "Publication Date": dt.datetime.fromtimestamp(post.created),  # Date of post creation
                "Number of Comments": post.num_comments,  # Number of comments on the post
                "URL": post.url,  # URL of the post
                "Sentiment": sentiment_label,
                "N_stars": n_stars }
        elif type_data == 'comments':
            post.comments.replace_more(limit=None)  # Load all comments
            for comment in post.comments.list():
                # Check if the comment contains all the specified keywords
                if all(keyword.lower() in comment.body.lower() for keyword in searched_words):
                    co = comment.body
                    sentiment_label, n_stars = analyze_sentiment(co[:512]) # Sentiment detection (comment)
                    data_info = {
                        "Author": comment.author.name if comment.author else "[deleted]",
                        "Comment": co,
                        "Upvotes": comment.score,
                        "Publication Date": dt.datetime.fromtimestamp(comment.created),
                        "Subreddit": comment.subreddit.display_name,
                        "Sentiment": sentiment_label,
                        "N_stars": n_stars }
        data_to_print.append(data_info)
    # If print_results is True, print post or comment information
    if print_results:
        for data_info in data_to_print:
            for key, value in data_info.items():
                print(f"{key}: {str(value).encode('ascii', 'ignore').decode('ascii')}")
            print("\n")
            print("-" * 60)
            print("\n")
    # If store_results is True, save post or comment information to a CSV file
    if store_results:
        searched_word = '_'.join(searched_words)
        file_name = f"{searched_word}_{type_data}_reddit.csv"
        with open(os.path.join(path, file_name), mode='w', newline='', encoding='utf-8') as csv_file:
            if type_data == 'posts':
                fieldnames = ["Title", "Content", "Publication Date", "Number of Comments", "URL", "Sentiment", "N_stars"]
            elif type_data == 'comments':
                fieldnames = ["Author", "Comment", "Upvotes", "Publication Date", "Subreddit", "Sentiment", "N_stars"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_to_print)

def run():
    try:
        # Get user input for Reddit API credentials
        print("Please start by getting your Reddit API credentials, check https://www.reddit.com/wiki/api/ for guidance.")
        print()
        client_id = input("Enter your Reddit client ID: ")
        client_secret = input("Enter your Reddit client secret: ")
        # Initialize API key
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent="web_scraping_project")
        # Get user input for other parameters
        searched_word = input("Enter the keywords to search on Reddit (separated by commas): ")
        while True:
            try:
                num_posts = int(input("How many posts do you want to retrieve? "))
                if num_posts > 0:
                    break
                else:
                    print("The number must be greater than 0!")
            except ValueError:
                print("Please enter a valid number!")
        while True:
            print_results = input("Do you want to display the results? (Y/N) ").upper()
            if print_results in ['Y', 'N']:
                break
            else:
                print("Unrecognized response. Please answer with 'Y' or 'N'.")
        while True:
            store_results = input("Do you want to save the results? (Y/N) ").upper()
            if store_results in ['Y', 'N']:
                break
            else:
                print("Unrecognized response. Please answer with 'Y' or 'N'.")
        default_path = get_path()
        path = default_path
        if store_results == 'Y':
            while True:
                path_choice = input("Do you want to use the default path to save the data? (Y/N) ").upper()
                if path_choice == 'Y':
                    break
                elif path_choice == 'N':
                    path = input("Enter your custom path to save the results: ")
                    break
                else:
                    print("Unrecognized response, using the default path.")
        while True:
            data_type = input("Do you want to retrieve 'posts' or 'comments'? ").lower()
            if data_type in ['posts', 'comments']:
                break
            else:
                print("Unsupported data type. Please choose between 'posts' or 'comments'.")
        if data_type in ['posts', 'comments']:
            scrap_reddit(reddit, searched_word, path, num_posts, print_results, store_results, type_data=data_type)
        else:
            print("Unsupported data type. Please choose between 'posts' or 'comments'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    run()