#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Convert UserFullInfo txt to json.

Usage: change input_dir_path, output_dir_path, and is_common_user
TODO: if it's a contaminated user/media object, discard current user/media.

Json format:
{user_id: int,
 user_name: string,
 askfm_id: string,
 follows: [user_name, user_name, ...],
 followed_by: [user_name, user_name, ...],
 total_likes: int,
 total_comments: int,
 medias: [{media_id: string, num_likes: int, num_comments: int,
            comments: [{commenting_user_id: int, commenting_user_name: string, comment_text: string}],
            liked_users: [{liked_user_id: int, liked_user_name: string}]}]}
"""


import sys, os, json, time
from datetime import timedelta


def write_to_file(media_json_obj, user_json_obj, output_handler, user_field_cnt=8, n_upper=5):
    # append last media object if not None
    if media_json_obj is not None:
        if n_upper == 3:
            media_json_obj['num_likes'] = len(media_json_obj['liked_users'])
            media_json_obj['num_comments'] = len(media_json_obj['comments'])
        user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]].append(media_json_obj)
    # write last user object if not None
    if user_json_obj is not None:
        output_handler.write('{0}\n'.format(json.dumps(user_json_obj)))


def convert_to_json(input_filepath, output_filepath):
    print('>>> Converting {0} to {1}...'.format(input_filepath, output_filepath))
    inner_start_time = time.time()

    m_upper = len(RAW_USER_FIELD_NAMES)
    n_upper = len(RAW_MEDIA_FIELD_NAMES)

    user_field_cnt = len(RAW_USER_FIELD_NAMES)
    media_field_cnt = len(RAW_MEDIA_FIELD_NAMES)
    user_json_obj = None
    media_json_obj = None

    with open(output_filepath, 'w', encoding='utf-8') as fout:
        with open(input_filepath, 'r', encoding='utf-8') as fin:
            for line in fin:
                text = line.rstrip().lower()
                if text:
                    try:
                        # if we are about to start a new user object, extract instagram user id and user name
                        if user_field_cnt == m_upper and media_field_cnt == n_upper and RAW_USER_FIELD_NAMES[0] in text:
                            # output stream
                            write_to_file(media_json_obj, user_json_obj, fout, user_field_cnt, n_upper)

                            # reset user pointer
                            user_field_cnt = 0

                            # init a new user object
                            user_json_obj = {}
                            # instagram user id
                            instagram_user_id = int(text.split(RAW_USER_FIELD_NAMES[user_field_cnt])[1].split()[0])
                            user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt]] = instagram_user_id
                            user_field_cnt += 1
                            # instgram user name
                            instagram_user_name = text.split(RAW_USER_FIELD_NAMES[user_field_cnt])[1]
                            user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt]] = instagram_user_name
                            user_field_cnt += 1
                        elif user_field_cnt == 2:
                            # askfm id
                            askfm_id = text.split(RAW_USER_FIELD_NAMES[user_field_cnt])[1]
                            user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt]] = askfm_id
                            user_field_cnt += 1
                        elif user_field_cnt == 3:
                            # init the list of 'Follows:'
                            user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt]] = []
                            user_field_cnt += 1
                        elif user_field_cnt == 4:
                            if RAW_USER_FIELD_NAMES[user_field_cnt] not in text:
                                # retrieve the follower user name
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]].append(text)
                            else:
                                # init the list of 'Followed BY:'
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt]] = []
                                user_field_cnt += 1
                        elif user_field_cnt == 5:
                            if RAW_USER_FIELD_NAMES[user_field_cnt] not in text:
                                # retrieve the followed by user name
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]].append(text)
                            else:
                                # init 'total_likes'
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt]] = 0
                                user_field_cnt += 1
                        elif user_field_cnt == 6:
                            if RAW_USER_FIELD_NAMES[user_field_cnt] not in text:
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]] = int(text)
                            else:
                                # init 'total_comments'
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt]] = 0
                                user_field_cnt += 1
                        elif user_field_cnt == 7:
                            if RAW_USER_FIELD_NAMES[user_field_cnt] not in text:
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]] = int(text)
                            else:
                                # init the list of 'media:'
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt]] = []
                                user_field_cnt += 1
                        elif user_field_cnt == m_upper:
                            # go into the media object
                            if media_field_cnt == n_upper and RAW_MEDIA_FIELD_NAMES[0] in text:
                                # append last media object if not None
                                if media_json_obj is not None:
                                    if n_upper == 3:
                                        media_json_obj['num_likes'] = len(media_json_obj['liked_users'])
                                        media_json_obj['num_comments'] = len(media_json_obj['comments'])
                                    user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]].append(media_json_obj)

                                # reset media pointer
                                media_field_cnt = 0

                                # init a new media object
                                media_json_obj = {}
                                media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = ''
                                media_field_cnt += 1

                            else:
                                if n_upper == 5:
                                    if media_field_cnt == 1:
                                        if RAW_MEDIA_FIELD_NAMES[media_field_cnt] not in text:
                                            # add media id
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]] = text
                                        else:
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = 0
                                            media_field_cnt += 1
                                    elif media_field_cnt == 2:
                                        if RAW_MEDIA_FIELD_NAMES[media_field_cnt] not in text:
                                            # add media number of likes
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]] = int(text)
                                        else:
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = 0
                                            media_field_cnt += 1
                                    elif media_field_cnt == 3:
                                        if RAW_MEDIA_FIELD_NAMES[media_field_cnt] not in text:
                                            # add media number of comments
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]] = int(text)
                                        else:
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = []
                                            media_field_cnt += 1
                                    elif media_field_cnt == 4:
                                        if RAW_MEDIA_FIELD_NAMES[media_field_cnt] not in text:
                                            text = text.replace('userid:', '$').replace('username:', '$').replace('commenttext:', '$')
                                            try:
                                                _, commenting_user_id, commenting_user_name, comment_text = text.split('$', 3)
                                            except:
                                                continue
                                            comment_tuple = (commenting_user_id.strip(), commenting_user_name.strip(), comment_text.strip())
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]].append(comment_tuple)
                                        else:
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = []
                                            media_field_cnt += 1
                                    elif media_field_cnt == 5:
                                        text = text.replace('userid:', '$').replace('username:', '$')
                                        _, liked_user_id, liked_user_name = text.split('$', 2)
                                        liked_tuple = (liked_user_id.strip(), liked_user_name.strip())
                                        media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]].append(liked_tuple)
                                elif n_upper == 3:
                                    if media_field_cnt == 1:
                                        if RAW_MEDIA_FIELD_NAMES[media_field_cnt] not in text:
                                            # add media id
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]] = text
                                        else:
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = []
                                            media_field_cnt += 1
                                    elif media_field_cnt == 2:
                                        if RAW_MEDIA_FIELD_NAMES[media_field_cnt] not in text:
                                            text = text.replace('userid:', '$').replace('username:', '$').replace('commenttext:', '$')
                                            try:
                                                _, commenting_user_id, commenting_user_name, comment_text = text.split('$', 3)
                                            except:
                                                continue
                                            comment_tuple = (commenting_user_id.strip(), commenting_user_name.strip(), comment_text.strip())
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]].append(comment_tuple)
                                        else:
                                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = []
                                            media_field_cnt += 1
                                    elif media_field_cnt == n_upper:
                                        text = text.replace('userid:', '$').replace('username:', '$')
                                        _, liked_user_id, liked_user_name = text.split('$', 2)
                                        liked_tuple = (liked_user_id.strip(), liked_user_name.strip())
                                        media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]].append(liked_tuple)
                    except:
                        user_field_cnt = len(RAW_USER_FIELD_NAMES)
                        media_field_cnt = len(RAW_MEDIA_FIELD_NAMES)
                        user_json_obj = None
                        media_json_obj = None
                        continue

        # output stream
        write_to_file(media_json_obj, user_json_obj, fout, user_field_cnt, n_upper)

        print('>>> Elapsed time: {0}\n'.format(str(timedelta(seconds=time.time() - inner_start_time))[:-3]))


def main():
    input_dir_path = '../data/NormalUserFullInfo'
    output_dir_path = '../data/FormattedNormalUserFullInfo'

    if not os.path.exists(input_dir_path):
        print('>>> No input dir! Exit...')
        sys.exit(1)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    total_start_time = time.time()
    for subdir, _, files in os.walk(input_dir_path):
        for f in files:
            input_filepath = os.path.join(subdir, f)
            output_filepath = os.path.join(output_dir_path, os.path.splitext(f)[0]+'.json')

            convert_to_json(input_filepath, output_filepath)
    print('>>> Total elapsed time: {0}\n'.format(str(timedelta(seconds=time.time() - total_start_time))[:-3]))


if __name__ == '__main__':
    is_common_user = False

    RAW_USER_FIELD_NAMES = ['instagram user id:', 'user name:', 'askfmid:', 'follows:', 'followed by:',
                            'totallikes', 'totalcomments', 'medias']
    NORMAL_RAW_MEDIA_FIELD_NAMES = ['media id:',
                                    'number of likes for this media:', 'number of comments for this media:',
                                    'comments for this media:', 'likes for this media:']
    COMMON_RAW_MEDIA_FIELD_NAMES = ['media id:', 'comments for this media:', 'likes for this media:']
    RAW_MEDIA_FIELD_NAMES = [NORMAL_RAW_MEDIA_FIELD_NAMES, COMMON_RAW_MEDIA_FIELD_NAMES][is_common_user]

    NEW_USER_FIELD_NAMES = ['user_id', 'user_name', 'askfm_id', 'follows', 'followed_by',
                            'total_likes', 'total_comments', 'medias']
    NORMAL_NEW_MEDIA_FIELD_NAMES = ['media_id', 'num_likes', 'num_comments', 'comments', 'liked_users']
    COMMON_NEW_MEDIA_FIELD_NAMES = ['media_id', 'comments', 'liked_users']
    NEW_MEDIA_FIELD_NAMES = [NORMAL_NEW_MEDIA_FIELD_NAMES, COMMON_NEW_MEDIA_FIELD_NAMES][is_common_user]

    main()
