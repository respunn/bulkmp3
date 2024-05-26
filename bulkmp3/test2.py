import os
import re
import subprocess
from pytube import YouTube, Playlist
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.console import Console

# Function to sanitize filenames by removing invalid characters
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Function to download a single song from a YouTube URL
def download_song(song_url, output_path, progress, task_id):
    yt = YouTube(song_url)
    stream = yt.streams.filter(only_audio=True).first()

    if stream:
        filename = sanitize_filename(f"{yt.author} - {yt.title}.mp3")
        print(f"Downloading: {filename}")
        stream.download(output_path, filename=filename)
        progress.update(task_id, advance=1, description=f"")
    else:
        print("No suitable audio stream found.")

# Function to download all songs from a YouTube playlist URL
def download_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    playlist_folder = os.path.join(get_songs_folder(), sanitize_filename(playlist.title))
    os.makedirs(playlist_folder, exist_ok=True)

    console = Console()
    progress = Progress(
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    )
    
    with progress:
        task_id = progress.add_task(f"Downloading playlist: {playlist.title}", total=len(playlist.video_urls))
        
        for video_url in playlist.video_urls:
            download_song(video_url, playlist_folder, progress, task_id)

    console.print("Playlist download complete!")

# Function to download a song from a Spotify URL using spotdl
def download_spotify_song(spotify_url):
    output_path = get_songs_folder()
    command = ["spotdl", "--output", output_path, spotify_url]
    subprocess.run(command)
    print("Spotify song downloaded successfully!")

# Function to download all songs from a Spotify playlist URL using spotdl
def download_spotify_playlist(spotify_playlist_url):
    output_path = get_songs_folder()
    playlist_id = spotify_playlist_url.split('/')[-1].split('?')[0]  # Extract the playlist ID
    playlist_folder = os.path.join(output_path, playlist_id)
    os.makedirs(playlist_folder, exist_ok=True)
    command = ["spotdl", "--output", playlist_folder, spotify_playlist_url]
    subprocess.run(command)
    print(f"Spotify playlist downloaded successfully in folder: {playlist_folder}")

# Function to get the folder path where songs will be saved
def get_songs_folder():
    downloads_folder = os.path.expanduser('~/Downloads')
    songs_folder = os.path.join(downloads_folder, 'Songs')
    os.makedirs(songs_folder, exist_ok=True)
    return songs_folder

# Main function to handle user input and start the download process
def main():
    url = input("Enter YouTube/Spotify song or playlist URL: ")
    if "spotify" in url:
        if "playlist" in url:
            download_spotify_playlist(url)
        else:
            download_spotify_song(url)
    elif "playlist" in url:
        download_playlist(url)
    else:
        # For individual YouTube song
        console = Console()
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        )

        with progress:
            task_id = progress.add_task(f"Downloading song: {url}", total=1)
            download_song(url, get_songs_folder(), progress, task_id)

# Entry point of the script
if __name__ == "__main__":
    main()
