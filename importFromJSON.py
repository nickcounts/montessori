import json
from os import getcwd, path, makedirs
from subprocess import Popen
from sanitize_filename import sanitize

# https://tohigherground.wistia.com/projects/khrbkvjqnh
# ebujold@guidepostmontessori.com
# Temp29966

# tohigherground.wistia.com/medias/y94h3dv4vp
BASE_MEDIA_URL = "https://tohigherground.wistia.com/medias/"

INDEX_FILE = "higher_ground_media_list.json"

media_folder_name = "downloads"
path_test_root = getcwd()

START_NUMBER = 1
STOP_NUMBER = 0




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




with open(INDEX_FILE) as read_file:
    data = json.load(read_file, )


target_group_ids = [9318021, 9318023]


path_media_root = initFolder(path_test_root, media_folder_name)
print(path_media_root)

GROUP_NUM = 0
DOWNLOAD_COUNTER = 0

for each in data['media_groups']:
    GROUP_NUM += 1
    # print(each['name'])
    this_group_id = each['id']

    if this_group_id not in target_group_ids:
        continue

    print("Group: ", each['media_count'], each['name'])

    media_group_title = sanitize(each['name'])
    path_this_group = initFolder(path_media_root, media_group_title)

    PLAYLIST_VID_NUM = 0
    for video in data['medias']:
        this_video_group_id = video['media_group_id']
        
        if this_video_group_id != this_group_id:
            continue

        PLAYLIST_VID_NUM += 1
        
        this_video_url = f"{BASE_MEDIA_URL}{video['hashed_id']}"
        this_video_filename = sanitize(video['name'])
        this_video_fullpath = path.join(path_this_group, this_video_filename)

        ytdl_output_str = f"{this_video_fullpath}.%(ext)s"

        # formatArgument = "'bestvideo[ext=mp4][height<=720]+bestaudio/best[height<=720]'"
        # formatArgument = "'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'"
        formatArgument = "md_mp4-540p/hd_mp4-720p/hd_mp4-1080p"

        print("Video: ", video['id'], video['hashed_id'], video['name'])
        with Popen(['yt-dlp', '-o', ytdl_output_str, '-f', formatArgument, this_video_url]) as sp:
            print("\t\t\tDownload in progress...")

        DOWNLOAD_COUNTER += 1

        if STOP_NUMBER:
            if DOWNLOAD_COUNTER >= STOP_NUMBER:
                print(f"\nVIDEO {DOWNLOAD_COUNTER} REACHED : Halting Download\n\n")
                quit()

        
        

print(f"\n\nFinished downloading {DOWNLOAD_COUNTER} videos\n")