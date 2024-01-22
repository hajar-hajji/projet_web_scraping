import requests
from bs4 import BeautifulSoup
import schedule
import time
import csv
from datetime import datetime
import os

target = "pmi_us"
location = "United_States"
url = "https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173"

filename = f"{target}.csv"

def scrap(url, filename):

    # Construct the file path in the current directory
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the element containing the PMI value
    target_element = soup.find("div", class_="arial_14 redFont")

    # Check if the file already exists
    file_exists = os.path.exists(file_path)

    # Open the file for appending; write headers if the file does not exist
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file, delimiter=',') 
        if not file_exists:
            writer.writerow(["Location", "PMI", "Date", "Time"])

        # If the target element is found, extract and write the data
        if target_element:
            t = target_element.text.strip()
            date = datetime.now().strftime("%Y-%m-%d")
            timestamp = datetime.now().strftime("%H:%M:%S")
            writer.writerow([location, t, date, timestamp])
            print(f"Le {target} est de {t}% à {date} {timestamp}")
        else:
            print(f"Le {target} n'a pas été trouvé !!")

scrap(url, filename)

def scrap_monthly(url, filename):
    today = datetime.date.today()
    if today.day == 1:
        scrap(url, filename)

# Schedule the scraping task to run monthly
schedule.every().day.at("12:00").do(scrap_monthly, url, filename)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)