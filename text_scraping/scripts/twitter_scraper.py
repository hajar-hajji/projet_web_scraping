import tweepy
from utils.utils import get_path
import csv
import os
import getpass


def scrap_twitter(consumer_key, consumer_secret, access_token, access_token_secret, keyword, numb_tweets, path, print_data=True, store_data=True):

    # Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creating the API object
    api = tweepy.API(auth)
    query = f"{keyword} OR {keyword.upper()} OR {keyword.capitalize()} -filter:links"

    # Search tweets containing the specific word
    # tweets = tweepy.Cursor(api.search_tweets, q=query, count=num_tweets)
    tweets = tweepy.Cursor(api.search_tweets, q=query, count=numb_tweets).items(numb_tweets)

    # File name for storing data
    file_name = f"{keyword}_twitter.csv"

    with open(os.path.join(path, file_name), 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Tweet', 'Published at', 'Country'])

        # Extracting information from tweets
        for tweet in tweets:
            tweet_text = tweet.text
            tweet_date = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
            tweet_country = tweet.place.country if tweet.place else "Undefined"

            # Printing tweet details
            if print_data:
                print(f"Tweet: {tweet_text}")
                print(f"Published at: {tweet_date}")
                print(f"Country: {tweet_country}")
                print("------")

            # Storing tweet details
            if store_data:
                csv_writer.writerow([tweet_text, tweet_date, tweet_country])

# keyword = "cobalt"
# scrap_twitter(consumer_key, consumer_secret, access_token, access_token_secret, keyword, 2, default_path, print_data=True, store_data=True)

def run():
    consumer_key = input("Entrez votre consumer key pour Twitter : ")
    consumer_secret = input("Entrez votre consumer secret pour Twitter : ")
    access_token = input("Entrez votre access token pour Twitter : ")
    access_token_secret = getpass.getpass("Entrez votre access token secret pour Twitter : ")

    keyword = input("Entrez le mot-clé pour la recherche sur Twitter : ")

    while True:
        try:
            numb_tweets = int(input("Combien de tweets souhaitez-vous récupérer ? "))
            if numb_tweets > 0:
                break
            else:
                print("Le nombre doit être supérieur à 0 !!")
        except ValueError:
            print("Veuillez entrer un nombre valide !")

    print_results = input("Voulez-vous afficher les données ? (Y/N) ").upper() == "Y"
    store_results = input("Voulez-vous enregistrer les données ? (Y/N) ").upper() == "Y"

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

    scrap_twitter(consumer_key, consumer_secret, access_token, access_token_secret, keyword, numb_tweets, path, print_results, store_results)

if __name__ == "__main__":
    run()