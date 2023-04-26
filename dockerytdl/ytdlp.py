from pathlib import Path
from yt_dlp import YoutubeDL


BASE_PATH = Path("/data")

with open("format.txt", "r") as f:
	FORMAT = f.readline()


ytdl_config = {
	# "simulate": True,
	"verbose": True,
	"format": FORMAT,
	"download_archive": BASE_PATH / "archive.log",
	"outtmpl": "/data/%(uploader)s - %(upload_date)s - %(title)s [%(id)s].%(ext)s",
	"writeinfojson": True,
	"continuedl": False,
	"overwrites": False,
	"merge_output_format": "mkv",
	"concurrent_fragment_downloads": 5,
	"throttledratelimit": 100_000,

}

URLS = ['https://www.youtube.com/watch?v=4IJCsxeCJ6o']
with YoutubeDL(ytdl_config) as ydl:
    ydl.download(URLS)