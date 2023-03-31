from pytube import Playlist, YouTube
import os

# Set the default resolution to "720p"
DEFAULT_RESOLUTION = "720p"

def download_video(video_url, folder_name):
    # Define a progress function for pytube
    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = bytes_downloaded / total_size * 100
        print(f"\r{progress:.2f}% downloaded", end='', flush=True)

    # Create a YouTube object and pass it the video URL and progress function
    yt = YouTube(video_url, on_progress_callback=on_progress)
    # Truncate the title to 50 characters (adjust as needed)
    title = yt.title[:100]
    # If the default resolution is set to "HIGHEST", download the video with the highest resolution
    if DEFAULT_RESOLUTION == "HIGHEST":
        video = yt.streams.get_highest_resolution()
    # If the default resolution is set to "LOWEST", download the video with the lowest resolution
    elif DEFAULT_RESOLUTION == "LOWEST":
        video = yt.streams.get_lowest_resolution()
    # Otherwise, try to download the video with the default resolution, and if it's not available, fall back to the next highest resolution
    else:
        video = yt.streams.filter(progressive=True, res=DEFAULT_RESOLUTION).first()
        if video is None:
            video = yt.streams.filter(progressive=True).order_by('resolution').desc().first()

    # Create the directory for the downloads if it doesn't exist
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Check if a file with the same name already exists in the specified folder
    file_path = os.path.join(folder_name, title+".mp4")
    if os.path.exists(file_path):
        print(f"'{title}' already exists in '{folder_name}'")
        return

    # Start downloading the video and print a message to the console
    print(f"Starting to download '{yt.title}'")
    video.download(output_path=folder_name, filename_prefix=yt.title)
    print(f"\n'{yt.title}' downloaded")


def download_playlist(playlist_url, folder_name):
    # Create a Playlist object and pass it the playlist URL
    playlist = Playlist(playlist_url)

    # Iterate through the video URLs in the playlist and download each one
    for video_url in playlist.video_urls:
        try:
            download_video(video_url, folder_name)
        except Exception as e:
            print(f"\nFailed to download '{video_url}': {str(e)}\n")
            continue

def is_playlist(link):
    # Check if the link contains the word "playlist"
    return 'playlist' in link

def download(link):
    # Prompt the user to enter a folder name for the downloads
    folder_name = input("Enter folder name: ")

    # If the link is to a playlist, download the whole playlist
    if is_playlist(link):
        download_playlist(link, folder_name)
    # If the link is to a single video, download that video
    else:
        download_video(link, folder_name)

# Prompt the user to enter a video or playlist URL and call the appropriate function to download it
link = input("Enter video or playlist URL: ")
download(link)
