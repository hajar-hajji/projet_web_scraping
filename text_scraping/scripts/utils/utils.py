import os

def get_path():
    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    scraped_data_path = os.path.join(parent_path, "scraped_data")
    scraped_data_path = os.path.normpath(scraped_data_path)
    if not os.path.exists(scraped_data_path):
        os.makedirs(scraped_data_path)
    return scraped_data_path

def get_data_path(file_name):
    current_path = os.getcwd()
    data_path = os.path.join(current_path, "text_scraping", "scraped_data", file_name)
    return data_path