import instaloader
from utils.utils import get_path
import csv
import os
import re
import getpass


def scrap_instagram(loader, hashtag, numb_posts, path, print_data=True, store_data=True):

    # Create a reproducible iterator for recent posts with the given hashtag
    post_iterator = instaloader.NodeIterator(
        loader.context, "9b498c08113f1e09617a1703c22b2f32",
        lambda d: d['data']['hashtag']['edge_hashtag_to_media'],
        lambda n: instaloader.Post(loader.context, n),
        {'tag_name': hashtag},
        f"https://www.instagram.com/explore/tags/{hashtag}/")
    
    post_count = 0

    # Define the file name for storing scraped data
    file_name = f"{hashtag}_instagram.csv"
    with open(os.path.join(path, file_name), 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        # Write the header row in the CSV file
        csv_writer.writerow(['URL', 'Caption', 'Date']) 

        # Iterate over each post in the iterator
        for post in post_iterator:
            # Check if the post has a caption
            if post.caption is not None:
                # Extract hashtags from the caption
                hash_words = re.findall(r'(?<!\w)#\w+\b', post.caption.lower())
                post_without_hashtags = post.caption.lower()
                # Remove hashtags from the caption
                for hash_word in hash_words:
                    post_without_hashtags = post_without_hashtags.replace(hash_word, "")     
                # Filter posts containing specific words
                if "cobalt" in post_without_hashtags and "metal" in post_without_hashtags:
                    # Extract post details: URL, caption, and date
                    url = post.url
                    caption = post.caption.encode('ascii', 'ignore').decode('ascii') if post.caption else ""
                    date = post.date.strftime('%Y-%m-%d %H:%M:%S') if post.date else ""
                    post_count += 1 
                    # Break the loop if the number of posts exceeds the limit
                    if post_count > numb_posts:
                        break

                    # Print post details if print_data is True
                    if print_data:
                        print("Url:", url)
                        print("Caption:", caption)
                        print("Date:", date)
                        print("\n")
                        print("-"*100)
                        print("\n")

                    # Store post details in the CSV file if store_data is True
                    if store_data:
                        csv_writer.writerow([url, caption, date])
            else:
                continue

# scrap_instagram("cobalt", 10)

def run():
    username = input("Entrez votre nom d'utilisateur Instagram : ")
    password = getpass.getpass("Entrez votre mot de passe Instagram : ")

    loader = instaloader.Instaloader()
    loader.login(username, password)

    hashtag = input("Entrez le hashtag pour la recherche sur Instagram : ")

    while True:
        try:
            numb_posts = int(input("Combien de publications souhaitez-vous récupérer ? "))
            if numb_posts > 0:
                break
            else:
                print("Le nombre doit être supérieur à 0 !!")
        except ValueError:
            print("Veuillez entrer un nombre valide !")

    print_data = input("Voulez-vous afficher les résultats ? (Y/N) ").upper() == "Y"
    store_data = input("Voulez-vous enregistrer les résultats ? (Y/N) ").upper() == "Y"

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

    scrap_instagram(loader, hashtag, numb_posts, path, print_data, store_data)

if __name__ == "__main__":
    run()