""" "
YouTube Video Downloader
Download Videos or Playlists
"""

import concurrent.futures
import csv
import datetime
import os
import time

import pyinputplus as pyinput
from pytube import Playlist as PT
from pytube import YouTube as YT
from pytube.cli import on_progress
from pytube.innertube import _default_clients

f1 = time.perf_counter()

# Bypassing AgeRestrictedError
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

WORKING_DIR = os.getcwd()
PROMPT_CHOICE = """
>>> Choose what to download:
>>> 1. YouTube Video (Default)
>>> 2. YouTube Playlist
>>> """
CHOICE = pyinput.inputInt(PROMPT_CHOICE, min=1, max=2, blank=True) or 1
print(CHOICE)


class Video:
    def __init__(self, link):
        self.link = link
        self.folder = self.create_folder()

    def create_folder(self, folder="Downloads"):
        os.makedirs(folder, exist_ok=True)
        print(f'>>> Saving to folder "{folder}" at {WORKING_DIR}')
        return os.path.join(WORKING_DIR, folder)

    def get_size(self, video):
        return round(video / (1024**2), 2)

    def get_current_time(self):
        now = datetime.datetime.now()
        format = "%d/%m/%Y %H:%M:%S"
        return now.strftime(format)

    def write_to_csv(self, title):
        log = [self.get_current_time(), title, self.link]
        with open("log.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(log)

    def download_video(self, link):
        yt = YT(link, on_progress_callback=on_progress)
        stream = yt.streams.get_highest_resolution()

        print(f'>>> Downloading "{yt.title}"...')
        video_size = self.get_size(video=stream.filesize)

        print(f"Size: {video_size}MB")
        video = stream.download(output_path=self.folder)

        print(f'\n>>> Downloaded: "{yt.title}" successfully!')
        print(f'>>> Saved as "{video}"')

        self.write_to_csv(title=yt.title)


class Playlist(Video):
    def __init__(self, link):
        super().__init__(link)

    def convert_to_valid_name(self, string):
        filename = "".join(c for c in string if c.isalnum() or c in "-_. ")
        return os.path.splitext(filename)[0]

    def get_playlist_urls(self):
        video_urls = PT(self.link).video_urls
        return video_urls

    def prepare_metadata(self):
        yt_playlist = PT(self.link)
        title = yt_playlist.title
        folder = self.convert_to_valid_name(string=title)
        folder = self.create_folder(folder=folder)
        self.folder = folder
        total_video_count = len(yt_playlist.videos)
        print(f">>> Total videos in playlist: {total_video_count}")


if __name__ == "__main__":
    if CHOICE == 1:
        link = pyinput.inputURL(">>> Enter YouTube Video URL: ")
        video = Video(link=link)
        video.download_video(link=link)

    elif CHOICE == 2:
        link = pyinput.inputURL(">>> Enter YouTube Playlist URL: ")
        playlist = Playlist(link=link)
        video_urls = playlist.get_playlist_urls()

        playlist.prepare_metadata()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(playlist.download_video, video_urls)

    else:
        print("Please, choose a valid option.")

f2 = time.perf_counter()
print(f"Script finished in {round(f2-f1, 2)} second(s)")
