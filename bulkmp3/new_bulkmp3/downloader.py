import os
import shutil
from pytube import YouTube, Playlist
from pytube.exceptions import AgeRestrictedError
from utils import sanitize_filename, get_songs_folder

def download_song(song_url):
    try:
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
    except AgeRestrictedError:
        print(f"Age restricted video. Cannot download: {song_url}")

def download_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    playlist_folder = os.path.join(get_songs_folder(), sanitize_filename(playlist.title))
    os.makedirs(playlist_folder, exist_ok=True)

    print(f"Downloading playlist: {playlist.title}")
    video_count = len(playlist.video_urls)
    failed_count = 0
    downloaded_count = 0

    for video_url in playlist.video_urls:
        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(only_audio=True).first()
            if stream:
                filename = sanitize_filename(f"{yt.author} - {yt.title}.mp3")
                stream.download(playlist_folder, filename=filename)
                print(f"- Downloaded: {filename}")
                downloaded_count += 1
            else:
                print(f"- Skipped (no audio stream): {yt.author} - {yt.title}")
                failed_count += 1
        except AgeRestrictedError:
            print(f"Age restricted video. Skipping: {yt.author} - {yt.title} - {video_url}")
            failed_count += 1
    
    if failed_count == video_count:
        print(f"Playlist download incomplete. No videos downloaded. Failed: {failed_count}")
        print(f"All videos in the playlist are age-restricted. Deleting {playlist.title} folder.")
        shutil.rmtree(playlist_folder)
    else:
        print("Playlist download complete!")
        print(f"Total videos: {video_count}, Downloaded: {downloaded_count}, Failed: {failed_count}")