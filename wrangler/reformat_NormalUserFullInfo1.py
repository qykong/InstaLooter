#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Reformat NormalUserFullInfo1.
"""

import json


def main():
    input_filepath = '../data/NormalUserFullInfo1.txt'
    output_filepath = '../data/NormalUserFullInfo1.json'

    user_field_cnt = 8
    media_field_cnt = 5
    user_json_obj = None
    media_json_obj = None

    with open(output_filepath, 'w', encoding='utf-8') as fout:
        with open(input_filepath, 'r', encoding='utf-8') as fin:
            for line in fin:
                text = line.rstrip().lower()
                if text:
                    # if we are about to start a new user object, extract instagram user id and user name
                    if user_field_cnt == 8 and media_field_cnt == 5 and RAW_USER_FIELD_NAMES[0] in text:
                        # append last media object if not None
                        if media_json_obj is not None:
                            user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]].append(media_json_obj)
                        # write last user object if not None
                        if user_json_obj is not None:
                            fout.write('{0}\n'.format(json.dumps(user_json_obj)))

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
                    elif user_field_cnt == 8:
                        # go into the media object
                        if media_field_cnt == 5 and RAW_MEDIA_FIELD_NAMES[0] in text:
                            # append last media object if not None
                            if media_json_obj is not None:
                                user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]].append(media_json_obj)

                            # reset media pointer
                            media_field_cnt = 0

                            # init a new media object
                            media_json_obj = {}
                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = ''
                            media_field_cnt += 1

                        elif media_field_cnt == 1:
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
                                comment_json_obj = {'commenting_user_id': commenting_user_id.strip(),
                                                    'commenting_user_name': commenting_user_name.strip(),
                                                    'comment_text': comment_text.strip()}
                                media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]].append(comment_json_obj)
                            else:
                                media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt]] = []
                                media_field_cnt += 1
                        elif media_field_cnt == 5:
                            text = text.replace('userid:', '$').replace('username:', '$')
                            _, liked_user_id, liked_user_name = text.split('$', 2)
                            liked_json_obj = {'liked_user_id': liked_user_id.strip(),
                                              'liked_user_name': liked_user_name.strip()}
                            media_json_obj[NEW_MEDIA_FIELD_NAMES[media_field_cnt - 1]].append(liked_json_obj)

        # append last media object if not None
        if media_json_obj is not None:
            user_json_obj[NEW_USER_FIELD_NAMES[user_field_cnt - 1]].append(media_json_obj)
        # write last user object if not None
        if user_json_obj is not None:
            fout.write('{0}\n'.format(json.dumps(user_json_obj)))


if __name__ == '__main__':
    RAW_USER_FIELD_NAMES = ['instagram user id:', 'user name:', 'askfmid:', 'follows:', 'followed by:',
                            'totallikes', 'totalcomments',
                            'medias']
    RAW_MEDIA_FIELD_NAMES = ['media id:', 'number of likes for this media:', 'number of comments for this media:',
                             'comments for this media:', 'likes for this media:']

    NEW_USER_FIELD_NAMES = ['user_id', 'user_name', 'askfm_id', 'follows', 'followed by',
                            'total_likes', 'total_comments',
                            'medias']
    NEW_MEDIA_FIELD_NAMES = ['media_id', 'num_likes', 'num_comments',
                             'comments', 'liked_users']

    main()
