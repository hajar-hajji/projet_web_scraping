def main():
    
    print("Choisissez le réseau social à scraper :")
    print("1. Instagram")
    print("2. Reddit")
    print("3. Twitter")
    print("4. YouTube")
    print()
    print()

    choix = int(input("Entrez le numéro de votre choix : "))

    if choix == 1:
        import instagram_scraper
        instagram_scraper.run()
    elif choix == 2:
        import reddit_scraper
        reddit_scraper.run()
    elif choix == 3:
        import twitter_scraper
        twitter_scraper.run()
    elif choix == 4:
        import youtube_scraper
        youtube_scraper.run()
    else:
        print("Choix invalide!! Veuillez réessayer..")

if __name__ == "__main__":
    main()