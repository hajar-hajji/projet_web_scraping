import praw
from transformers import pipeline
from utils.utils import *
from utils.preprocess import *
import datetime as dt
import csv
import os


def scrap_reddit(reddit, searched_words, path, num_posts=2, print_results=True, store_results=False):

    classifier = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

    # Access the subreddit 'all'
    subreddit = reddit.subreddit('all')
    
    # Get the posts related to the searched word
    searched_words = [term.strip() for term in searched_words.split(',')]
    results = subreddit.search(' AND '.join(searched_words), limit=num_posts)
    
    comments_to_print = []
    
    # Extract information from each post
    for post in results:
        title = post.title  # Title of the post
        content = post.selftext  # Content of the post
        sentiment_result = classifier(preprocess_text(title) + ' ' + preprocess_text(content))[0]
        n_stars = int(sentiment_result['label'].split(' ')[0])
        sentiment_label = 'Positive' if n_stars >= 4 else ('Negative' if n_stars <= 2 else 'Neutral')
        comment_info = {
            "Title": title, 
            "Content": content,  
            "Publication Date": dt.datetime.fromtimestamp(post.created),  # Date of post creation
            "Number of Comments": post.num_comments,  # Number of comments on the post
            "URL": post.url,  # URL of the post
            "Sentiment": sentiment_label,
            "N_stars": n_stars
            } 
        comments_to_print.append(comment_info)

    # If print_results is True, print post information
    if print_results:
        for comment_info in comments_to_print:
            for key, value in comment_info.items():
                print(f"{key}: {str(value).encode('ascii', 'ignore').decode('ascii')}")
            print("\n")
            print("-"*60)
            print("\n")
    
    # If store_results is True, save post information to a CSV file
    if store_results:
        searched_word = '_'.join(searched_words)
        file_name = f"{searched_word}_reddit.csv"
        with open(os.path.join(path, file_name), mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ["Title", "Content", "Publication Date", "Number of Comments", "URL", "Sentiment", "N_stars"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(comments_to_print)

def run():
    client_id = input("Entrez votre client ID pour Reddit : ")
    client_secret = input("Entrez votre client secret pour Reddit : ")

    # Initialize API key
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent="projet_web_scraping")

    searched_word = input("Entrez le mot-clé à chercher sur Reddit : ")
    while True:
        try:
            num_posts = int(input("Combien de publications souhaitez-vous récupérer ? "))
            if num_posts > 0:
                break
            else:
                print("Le nombre doit être supérieur à 0 !!")
        except ValueError:
            print("Veuillez entrer un nombre valide !")

    print_results = input("Voulez-vous afficher les résultats ? (Y/N) ").upper() == "Y"
    store_results = input("Voulez-vous enregistrer les résultats ? (Y/N) ").upper() == "Y"

    default_path = get_path()
    while True:
        path_choice = input("Voulez-vous utiliser le chemin par défaut pour sauvegarder les données ? (Y/N) ")
        if path_choice.upper() == "Y":
            path = default_path
            break
        elif path_choice.upper() == "N":
            path = input("Entrez votre chemin personnalisé pour sauvegarder les résultats : ")
            break
        else:
            print("Réponse non reconnue, Utilisation du chemin par défaut.")
            path = default_path

    scrap_reddit(reddit, searched_word, path, num_posts, print_results, store_results)

if __name__ == "__main__":
    run()