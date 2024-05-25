import os
import re
from pytube import YouTube, Playlist

# Function to sanitize filenames by removing invalid characters
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Function to download a single song from a YouTube URL
def download_song(song_url):
    # Create a YouTube object using the pytube library
    # Get the first audio stream available
    # Download the audio stream to the 'Songs' folder in the user's Downloads folder
    # Print a message when the download is complete
    
    yt = YouTube(song_url)
    stream = yt.streams.filter(only_audio=True).first()

    if stream:
        output_path = get_songs_folder()
        filename = sanitize_filename(f"{yt.author} - {yt.title}.mp3")
        print(f"Downloading: {filename}")
        stream.download(output_path, filename=filename)
        print("Song downloaded successfully!")
    else:
        print("No suitable audio stream found.")

# Function to download all songs from a YouTube playlist URL
def download_playlist(playlist_url):
    # Create a Playlist object using the pytube library
    # Create a folder for the playlist
    # Download each video in the playlist as an audio file
    # Save the audio file in the playlist folder
    # Print a message when the download is complete

    playlist = Playlist(playlist_url)
    playlist_folder = os.path.join(get_songs_folder(), sanitize_filename(playlist.title))
    os.makedirs(playlist_folder, exist_ok=True)

    print(f"Downloading playlist: {playlist.title}")
    for video_url in playlist.video_urls:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        if stream:
            filename = sanitize_filename(f"{yt.author} - {yt.title}.mp3")
            stream.download(playlist_folder, filename=filename)
            print(f"- Downloaded: {filename}")
        else:
            print(f"- Skipped (no audio stream): {yt.author} - {yt.title}")
    print("Playlist download complete!")

# Function to get the folder path where songs will be saved
def get_songs_folder():
    # Get the user's Downloads folder
    # Create a 'Songs' folder inside the Downloads folder
    # Return the path to the 'Songs' folder
    downloads_folder = os.path.expanduser('~/Downloads')
    songs_folder = os.path.join(downloads_folder, 'Songs')
    os.makedirs(songs_folder, exist_ok=True)
    return songs_folder

# Main function to handle user input and start the download process
def main():
    url = input("Enter YouTube song or playlist URL: ")
    # Check if the URL is a playlist URL
    # If it is, download the playlist
    # If it is not, check if it is a list URL
    # If it is, ask the user if they want to download the playlist or the song
    # If it is a song URL, download the song
    if "playlist" in url:
        download_playlist(url)
    elif "list" in url:
        choice = input("Do you want to download the playlist? or the song? (playlist/song)\n")
        if choice == "playlist":
            print("Detected playlist URL, extracting playlist ID...")
            playlist_id = url.split('list=')[1]
            new_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            download_playlist(new_url)
        else:
            download_song(url)
    else:
        download_song(url)

# Entry point of the script
if __name__ == "__main__":
    main()