from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.utils import get_path
import csv
import os


# Introducing youtube video categories
video_domains = {
    '1': 'Film & Animation',
    '2': 'Autos & Vehicles',
    '10': 'Music',
    '15': 'Pets & Animals',
    '17': 'Sports',
    '18': 'Short Movies',
    '19': 'Travel & Events',
    '20': 'Gaming',
    '21': 'Videoblogging',
    '22': 'People & Blogs',
    '23': 'Comedy',
    '24': 'Entertainment',
    '25': 'News & Politics',
    '26': 'Howto & Style',
    '27': 'Education',
    '28': 'Science & Technology',
    '29': 'Nonprofits & Activism',
    '30': 'Movies',
    '31': 'Anime/Animation',
    '32': 'Action/Adventure',
    '33': 'Classics',
    '34': 'Comedy',
    '35': 'Documentary',
    '36': 'Drama',
    '37': 'Family',
    '38': 'Foreign',
    '39': 'Horror',
    '40': 'Sci-Fi/Fantasy',
    '41': 'Thriller',
    '42': 'Shorts',
    '43': 'Shows',
    '44': 'Trailers'
}

def scrap_ytb(youtube, searched_word, path, occurrences_to_find, scrap_titles=True, scrap_comments=False, video_categories=None, print_results=True, store_results=False):

    if scrap_titles and scrap_comments:
        raise ValueError("Both scrap_titles and scrap_comments cannot be activated at the same time!!")
    
    # Scraping youtube video titles
    if scrap_titles:
        if video_categories is None:
            # Fetch videos containing the searched word in their titles (without category filter)
            search_response = youtube.search().list(
                q=searched_word,
                part='snippet',
                type='video',
                maxResults=occurrences_to_find
            ).execute()
        else:
            # Fetch videos containing the searched word in their titles within specified categories
            all_search_results = []
            stored_categories = []
            for category_id in video_categories:
                category_search_response = youtube.search().list(
                    q=searched_word,
                    part='snippet',
                    type='video',
                    maxResults=occurrences_to_find//2,
                    videoCategoryId=str(category_id)
                ).execute()
                stored_categories.append(str(category_id))
                
                all_search_results.extend(category_search_response.get('items', []))

            search_response = {'items': all_search_results}

        results_to_print = []
        for i, search_result in enumerate(search_response.get('items', [])):
            snippet = search_result['snippet']
            title = snippet['title']
            published_at = snippet['publishedAt']
            category_name = video_domains.get(stored_categories[i], 'Unknown Category') if video_categories is not None and i < len(stored_categories) else 'NaN'
            video_id = search_result['id']['videoId']
            video_link = f"https://www.youtube.com/watch?v={video_id}"

            result = {
                "Title": title.encode('utf-8', errors='ignore').decode('utf-8'),
                "Category": category_name,
                "Published At": published_at,
                "Video ID": video_id,
                "Video Link": video_link
            }

            if 'regionCode' in snippet:
                result["Country"] = snippet['regionCode']

            results_to_print.append(result)

        if print_results:
            print(f"Top {occurrences_to_find} videos with '{searched_word}' in title:")
            for result in results_to_print:
                for key, value in result.items():
                    print(f"{key}: {value}")
                print("------")

        if store_results:
            file_name = f"{searched_word}_videos_all_results.csv" if video_categories is None else f"{searched_word}_videos_filtered_results.csv"
            with open(os.path.join(path, file_name), mode='w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ["Title", "Category", "Published At", "Video ID", "Video Link", "Country"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results_to_print)

    # Scraping youtube comments
    if scrap_comments:
        found_occurrences = 0
        comments_to_print = []

        for video_domain in video_categories:
            if found_occurrences >= occurrences_to_find:
                break

            category_name = video_domains.get(str(video_domain), 'Unknown Category')
            print(f"Searching in category: {category_name}")

            next_page_token = None
            while found_occurrences < occurrences_to_find:
                videos_response = youtube.search().list(
                    part='id',
                    type='video',
                    maxResults=10,
                    pageToken=next_page_token if next_page_token else '',
                    videoCategoryId=str(video_domain)
                ).execute()

                video_ids = [item['id']['videoId'] for item in videos_response.get('items', [])]

                for video_id in video_ids:
                    try:
                        comments_response = youtube.commentThreads().list(
                            part='snippet',
                            videoId=video_id,
                            textFormat='plainText'
                        ).execute()

                        for comment in comments_response.get('items', []):
                            comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                            if searched_word.lower() in comment_text.lower():
                                found_occurrences += 1
                                video_link = f"https://www.youtube.com/watch?v={video_id}"
                                comment_info = {
                                    "Comment": comment_text.encode('utf-8', errors='ignore').decode('utf-8'),
                                    "Video ID": video_id,
                                    "Link": video_link,
                                    "Category": category_name}

                                comments_to_print.append(comment_info)

                                if found_occurrences >= occurrences_to_find:
                                    break

                        if found_occurrences >= occurrences_to_find:
                            break

                    except HttpError as e:
                        if e.resp.status == 403:
                            continue

                next_page_token = videos_response.get('nextPageToken')
                if not next_page_token:
                    break

        if print_results:
            for comment_info in comments_to_print:
                for key, value in comment_info.items():
                    print(f"{key}: {value}")
                print("\n")

        if store_results:
            file_name = f"{searched_word}_ytb_comments.csv"
            with open(os.path.join(path, file_name), mode='w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ["Comment", "Video ID", "Link", "Category"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(comments_to_print)


# searched_word = 'cobalt'
# occurrences_to_find = 5
# video_categories = [27,28]
#scrap_ytb(searched_word, occurrences_to_find, scrap_titles=True, scrap_comments=False, video_categories=None, print_results=True, store_results=True)
#scrap_ytb(searched_word, occurrences_to_find, scrap_titles=True, scrap_comments=False, video_categories=video_categories, print_results=True, store_results=True)
#scrap_ytb(searched_word, occurrences_to_find, scrap_titles=False, scrap_comments=True, video_categories=video_categories, print_results=True, store_results=True)

def run():
    api_key = input("Entrez votre clé API pour YouTube : ")
    youtube = build('youtube', 'v3', developerKey=api_key)

    searched_word = input("Entrez le mot-clé pour la recherche sur YouTube : ")
    while True:
        try:
            occurrences_to_find = int(input("Combien de vidéos souhaitez-vous récupérer ? "))
            if occurrences_to_find > 0:
                break
            else:
                print("Le nombre doit être supérieur à 0 !!")
        except ValueError:
            print("Veuillez entrer un nombre valide !")

    print("Vous pouvez soit scraper les données à partir des titres des vidéos OU bien les commentaires, choisir une à la fois !!")
    while True:
        scrap_titles_input = input("Voulez-vous scraper les titres ? (Y/N) ")
        scrap_comments_input = input("Voulez-vous scraper les commentaires ? (Y/N) ")

        if scrap_titles_input.upper() in ['Y', 'N'] and scrap_comments_input.upper() in ['Y', 'N']:
            scrap_titles = scrap_titles_input == "Y"
            scrap_comments = scrap_comments_input == "Y"
            if scrap_titles != scrap_comments:
                break
            else:
                print("Vous ne pouvez pas choisir à la fois les titres et les commentaires !!")
        else:
            print("Veuillez répondre par 'Y' ou 'N'")
    print()
    print("Catégories de vidéos disponibles :")
    for key, value in video_domains.items():
        print(f"{key}: {value}")
    
    categories_input = input("Parmi les domaines cités en haut, entrez les numéros de vos catégories séparés par des virgules (ex: 1,2,10), ou 'None' pour aucune catégorie: ")
    if categories_input.lower() in ['none', '']:
        video_categories = None
    else:
        video_categories = [int(category.strip()) for category in categories_input.split(',') if category.strip().isdigit()]

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

    print_results = input("Voulez-vous afficher les résultats ? (Y/N) ").upper() == "Y"
    store_results = input("Voulez-vous enregistrer les résultats ? (Y/N) ").upper() == "Y"

    scrap_ytb(youtube, searched_word, path, occurrences_to_find, scrap_titles, scrap_comments, video_categories, print_results, store_results)

if __name__ == "__main__":
    run()