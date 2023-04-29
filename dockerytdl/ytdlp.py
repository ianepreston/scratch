from pathlib import Path
from yt_dlp import YoutubeDL


with open("format.txt", "r") as f:
    FORMAT = f.readline()


def download_playlist(playlist: str, channel_folder: bool = True, delete_removed: bool = False) -> None:
    """Download a playlist."""
    base_path = "/data"
    file_str: str = "%(channel)s - %(upload_date)s - %(title)s [%(id)s].%(ext)s"
    if channel_folder:
        folder_str = f"{base_path}/%(channel)s/%(playlist_title)s"
    else:
        folder_str = f"{base_path}/%(playlist_title)s"
    ytdl_config = {
        # "simulate": True,
        "verbose": True,
        "format": FORMAT,
        # "download_archive": f"{folder_str}/archive.log",
        "outtmpl": f"{folder_str}/{file_str}",
        "writeinfojson": True,
        "continuedl": False,
        "overwrites": False,
        "merge_output_format": "mkv",
        "concurrent_fragment_downloads": 5,
        "throttledratelimit": 100_000,
    }
    with YoutubeDL(ytdl_config) as ydl:
        ydl.download(playlist)


if __name__ == "__main__":
    # apaird CNC playlist
    url = "https://www.youtube.com/watch?v=akjSc2-bZpY&list=PLZcFwaChdgSqyJ2bLlg0hyQ0vf83pPpcY"
    download_playlist(url, channel_folder=True, delete_removed=False)
    url = "https://www.youtube.com/watch?v=-plesrt8ZCs&list=PLQMVnqe4XbifORmvspB_Oun47H0tkbW-C"
    download_playlist(url, channel_folder=False, delete_removed=True)