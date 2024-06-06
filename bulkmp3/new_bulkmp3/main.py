from downloader import download_song, download_playlist

def main():
    url = input("Enter YouTube song or playlist URL: ")
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

if __name__ == "__main__":
    main()