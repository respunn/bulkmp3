import os
import re

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def get_songs_folder():
    downloads_folder = os.path.expanduser('~/Downloads')
    songs_folder = os.path.join(downloads_folder, 'Songs')
    os.makedirs(songs_folder, exist_ok=True)
    return songs_folder