# Download YouTube videos from CLI

## Description
Supports both YouTube videos and playlists. Automatically chooses the highest resolution available for videos and playlists.
Uses threading to speed up downloads. Also adds history to the log.csv file.


## Installation
1. Clone this repository:
   
   ------------
         git clone https://github.com/HBarotov/yt-downloader.git
  
2. Create a new virtual environment and activate it:

   Use ```venv``` (Python 3.3+):
   
   ------------
         python -m venv .venv

   Activate on Windows:

   ------------
         .venv\Scripts\Activate.ps1

   Activate on Linux/macOS:

   ------------
         source .venv/bin/activate
4. Install the required packages:

   ------------
         pip install -r requirements.txt

5. Run the downloader.py
