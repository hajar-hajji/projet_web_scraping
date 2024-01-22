import os

def get_path(file_path, file_name):
    directory_path = os.path.dirname(file_path)
    return os.path.join(directory_path, file_name)