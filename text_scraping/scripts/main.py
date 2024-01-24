def main():
    
    print("Choose the social media platform to scrape:")
    print("1. Instagram")
    print("2. Reddit")
    print("3. Twitter")
    print("4. YouTube")
    print()
    print()

    choice = int(input("Enter the number of your choice: "))

    if choice == 1:
        import instagram_scraper
        instagram_scraper.run()
    elif choice == 2:
        import reddit_scraper
        reddit_scraper.run()
    elif choice == 3:
        import twitter_scraper
        twitter_scraper.run()
    elif choice == 4:
        import youtube_scraper
        youtube_scraper.run()
    else:
        print("Invalid choice!! Please try again.")

if __name__ == "__main__":
    main()