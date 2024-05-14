""""
YouTube Video Downloader
Download Videos or Playlists
"""

import concurrent.futures
import os
import sys
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

    def create_folder(self, folder="Video_Downloads"):
        os.makedirs(folder, exist_ok=True)
        print(f'>>> Saving to folder "{folder}" at {WORKING_DIR}')
        return os.path.join(WORKING_DIR, folder)

    def get_resolutions(self, video):
        resolutions = []
        for stream in video.streams.filter(progressive=True):
            resolution = stream.resolution
            if resolution is None:
                continue
            resolutions.append(resolution)

        if resolutions:
            return sorted(set(resolutions), key=lambda x: int(x.split("p")[0]))
        return None

    def choose_resolution(self, resolutions):
        prompt = ">>> Choose a video quality: \n"
        return pyinput.inputMenu(resolutions, prompt=prompt, numbered=True, blank=True)

    def get_size(self, video):
        return round(video / (1024**2), 2)

    def download_video(self):
        yt = YT(link, on_progress_callback=on_progress)
        title = yt.title
        folder = self.create_folder()

        resolutions = self.get_resolutions(video=yt)

        if not resolutions:
            print(">>> Sorry, the downloadable format is not found.")
            sys.exit()
        resolution = self.choose_resolution(resolutions=resolutions)

        stream = yt.streams.filter(
            file_extension="mp4", resolution=resolution, progressive=True
        )
        print(f'>>> Downloading "{title}" in {resolution} quality...')

        video_size = self.get_size(video=stream.first().filesize)
        print(f"Size: {video_size}MB")
        video = stream.first().download(output_path=folder)

        print(f'\n>>> Downloaded: "{title}" successfully!')
        print(f'>>> Saved to "{video}"')


class Playlist(Video):
    def __init__(self, link, folder=None):
        super().__init__(link)
        self.folder = folder

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

    def download_playlist(self, video_url):
        yt = YT(video_url, on_progress_callback=on_progress)
        print(f">>> Downloading: {yt.title}")
        stream = yt.streams.get_highest_resolution()
        video_size = self.get_size(stream.filesize)
        print(f"Size: {video_size}MB")
        stream.download(output_path=self.folder)
        print(f'\n>>> Downloaded: "{yt.title}" successfully!')


if __name__ == "__main__":
    if CHOICE == 1:
        link = pyinput.inputURL(">>> Enter YouTube Video URL: ")
        video = Video(link=link)
        video.download_video()

    elif CHOICE == 2:
        link = pyinput.inputURL(">>> Enter YouTube Playlist URL: ")
        playlist = Playlist(link=link)
        video_urls = playlist.get_playlist_urls()

        playlist.prepare_metadata()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(playlist.download_playlist, video_urls)

    else:
        print("Please, choose a valid option.")

f2 = time.perf_counter()
print(f"Script finished in {round(f2-f1, 2)} second(s)")
