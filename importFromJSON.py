import json

# https://tohigherground.wistia.com/projects/khrbkvjqnh
# ebujold@guidepostmontessori.com
# Temp29966

with open("media.json") as read_file:
    data = json.load(read_file)

for each in data['media_groups']:
    # print(each['name'])
    print("Group: ", each['media_count'], each['name'])

    for video in data['medias']:
        if video['media_group_id'] == each['id']:
            print("Video: ", video['id'], video['hashed_id'], video['name'])
        

