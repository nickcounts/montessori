from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib import request
from os import path
from os import getcwd
from os import makedirs
from subprocess import PIPE, Popen
import sys
from sanitize_filename import sanitize


# run `pipenv install` to set up dependencies

# https://tohigherground.wistia.com/projects/khrbkvjqnh
# ebujold@guidepostmontessori.com
# Temp29966

# Constants 

url = "media_divs.html"
media_folder_name = "downloads"
path_test_root = getcwd()

START_NUMBER = 1
STOP_NUMBER = 0
VIDEO_NUMBER = 0
PLAYLIST_NUM = 1

if len(sys.argv) >= 2:
    START_NUMBER = int(sys.argv[1])
    print(f"Starting download at video number {START_NUMBER}")

if len(sys.argv) >= 3:
    STOP_NUMBER = int(sys.argv[2])
    print(f"Stopping download at video number {STOP_NUMBER}")



def initFolder(root, folder):
    # Create root folder to download media
    newFolder = path.join(root, folder)
    if not (path.exists(newFolder) & path.isdir(newFolder)):
        if not path.exists(newFolder):
            makedirs(newFolder)
        else:
            print(f"{newFolder} is not a directory.")
            quit()
    return newFolder




path_media_root = initFolder(path_test_root, media_folder_name)
print(path_media_root)

with open(url) as read_file:
    data = read_file.read()
    soup = BeautifulSoup(data, 'html.parser')


mydivs = soup.find_all("div", {"class": "media_group open"})
for div in mydivs:
    headDiv = div.find("span", {"class": "media_group_name"})
    media_group_title = sanitize(headDiv.text.strip())
    print(f"NEW GROUP:\t{media_group_title}")

    path_this_group = initFolder(path_media_root, media_group_title)

    PLAYLIST_NUM = 0

    for media in div.find_all("div", {"class": "media" }):
        VIDEO_NUMBER+=1
        PLAYLIST_NUM+=1

        if START_NUMBER > VIDEO_NUMBER:
            print(f"\tSKIPPING video {VIDEO_NUMBER}")
            continue


        media_title = sanitize(media.find("span", {"class": "editable"}).text.strip())
        ytdl_output_pattern = f"{PLAYLIST_NUM:03} {media_title}.%(ext)s"
        ytdl_output_str = path.join(path_this_group, ytdl_output_pattern)

        media_link  = media.find("a", {"class": "media_link"}).get('href')
        
        p = urlparse( media.find("img", {"class": "media_thumb"}).get('src'))
        media_thumb_url = f"{p.scheme}://{p.netloc}/{p.path}"
        media_thumb_name = f"{PLAYLIST_NUM:03} {media_title}.jpg"
        media_thumb_file = path.join(path_this_group, media_thumb_name)

        print(f"\t{media_title}")
        print(f"\t\tDownloading thumbnail as {media_thumb_name}")
        request.urlretrieve(media_thumb_url, media_thumb_file)

        print(f"\t\tDownloading video as {media_title}")

        formatArgument = "'bestvideo[height<=720]+bestaudio/best[height<=720]'"
        formatArgument = "'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'"
        formatArgument = "md_mp4-540p/hd_mp4-720p/hd_mp4-1080p"

        with Popen(['youtube-dl', '-o', ytdl_output_str, '-f', formatArgument, media_link]) as sp:
            print("\t\t\tDownload in progress...")
            # for line in sp.stdout:
            #     print(line)

        if STOP_NUMBER:
            if VIDEO_NUMBER >= STOP_NUMBER:
                print(f"\nVIDEO {VIDEO_NUMBER} REACHED : Halting Download\n\n")
                quit()

