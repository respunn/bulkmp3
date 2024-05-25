# YouTube Music Downloader
This script allows you to download songs and playlists from YouTube. The audio files are saved in a designated folder in your Downloads directory.

## Features
+ Download individual songs from YouTube.
+ Download all songs from a YouTube playlist.
+ Automatically sanitizes filenames to remove invalid characters.

## Releases
+ Initial beta release
+ Added functionality to download individual songs and playlists
+ Filename sanitization to remove invalid characters
+ Saves audio files in the user's Downloads directory
+ Download from [here](https://github.com/respunn/bulkmp3/releases)

### The following operations are for those who want to deal with the source code.

## Requirements
+ Python 3.x
+ pytube library
## Installation
1. Clone the repository or download the script file.
```
git clone https://github.com/respunn/bulkmp3.git
cd bulkmp3
```
2. Install the required Python library.
```
pip install pytube
```
## Usage
1. Run the script.
```
python main.py
```
2. Enter the YouTube song or playlist URL when prompted.

## Functions
### sanitize_filename(filename)
Removes invalid characters from filenames.

### download_song(song_url)
Downloads a single song from a YouTube URL.

### download_playlist(playlist_url)
Downloads all songs from a YouTube playlist URL.

### get_songs_folder()
Returns the folder path where songs will be saved. Creates the folder if it doesn't exist.

### main()
Handles user input and starts the download process.

## Example
To download a song or playlist, run the script and provide the YouTube URL when prompted. The downloaded audio files will be saved in the Songs folder in your Downloads directory.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
