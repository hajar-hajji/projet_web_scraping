import praw
from utils.utils import get_path
import datetime as dt
import csv
import os


def scrap_reddit(reddit, searched_word, path, num_posts=2, print_results=True, store_results=False):

    # Access the subreddit 'all'
    no_subreddit = reddit.subreddit('all')
    
    # Get the posts related to the searched word
    results = no_subreddit.search(searched_word, limit=num_posts)
    
    comments_to_print = []
    
    # Extract information from each post
    for post in results:
        comment_info = {
            "Title": post.title, # Title of the post
            "Content": post.selftext,  # Content of the post
            "Publication Date": dt.datetime.fromtimestamp(post.created),  # Date of post creation
            "Number of Comments": post.num_comments,  # Number of comments on the post
            "URL": post.url }  # URL of the post
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
        file_name = f"{searched_word}_reddit.csv"
        with open(os.path.join(path, file_name), mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ["Title", "Content", "Publication Date", "Number of Comments", "URL"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(comments_to_print)

def run():
    client_id = input("Entrez votre client ID pour Reddit : ")
    client_secret = input("Entrez votre client secret pour Reddit : ")

    # Initialize API key
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='projet_web_scraping')

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