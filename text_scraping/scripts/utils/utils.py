import os

def get_path():

    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    scraped_data_path = os.path.join(parent_path, 'scraped_data')

    if not os.path.exists(scraped_data_path):
        os.makedirs(scraped_data_path)

    return scraped_data_path