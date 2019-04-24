#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Convert session csv to json.

Json format:
{unit_id: int,
 question1: string,  ## 0 - noneAgg, 1 - aggression
 question1_conf: float,
 question2: string,  ## 0 - noneBll, 1 - bullying
 question2_conf: float,
 comments: [(commenting_username: string, comment_text: string, comment_timestamp: string)],
 total_comments: int,
 post_timestamp: string,
 img_url: string,
 total_likes: int,
 owner_comment: string,
 owner_username: string,
 owner_num_posts: int,
 owner_num_followers: int,
 owner_num_follows: int,
 cyberaggression: int,
 cyberbullying: int
"""

import re, json
import pandas as pd


def extract_comment_triplet(block):
    if pd.isna(block) or block == 'empty' or 'font color' not in block or 'created_at' not in block:
        return None
    comment_text = block[block.find('</font>') + 9: block.find('(created')]
    # remove http url
    comment_text = re.sub(r'http\S+', '', comment_text).strip()
    return (block[block.find('>') + 1: block.find('</font>')],
            remove_decorator(comment_text),
            block[block.find('(created') + 12: -8])


def remove_decorator(text):
    return re.sub('<.*?>', '', text).strip()


def main():
    output_path = '../data/vine_full_sessions_970.json'
    session_filenames = ['../data/vine_labeled_cyberbullying_data.csv']

    with open(output_path, 'w') as fout:
        for filename in session_filenames:
            data_f = pd.read_csv(filename, encoding='latin-1')
            print(list(data_f))

            for row_idx, row in data_f.iterrows():
                unit_id = int(row['_unit_id'])
                question1 = row['question1'] == 'aggression'
                question1_conf = float(row['question1:confidence'])
                question2 = row['question2'] == 'bullying'
                question2_conf = float(row['question2:confidence'])

                comments_list = []
                for i in range(1, 661):
                    comment_triplet = extract_comment_triplet(row['column{0}'.format(i)])
                    if comment_triplet is not None:
                        comments_list.append(comment_triplet)
                total_comments = len(comments_list)

                if 'media posted' in row['creationtime'].lower():
                    post_timestamp = row['creationtime'][-26: -7].strip()
                else:
                    post_timestamp = None
                video_url = row['videolink'].strip()
                total_likes = int(row['likecount'])

                if pd.isna(row['mediacaption']):
                    owner_comment = ''
                else:
                    owner_comment = row['mediacaption']
                    # remove http url
                    owner_comment = re.sub(r'http\S+', '', owner_comment)

                owner_username = remove_decorator(row['username'])

                to_write = {'unit_id': unit_id,
                            'question1': question1, 'question1_conf': question1_conf,
                            'question2': question2, 'question2_conf': question2_conf,
                            'comments_list': comments_list, 'total_comments': total_comments,
                            'post_timestamp': post_timestamp, 'video_url': video_url, 'total_likes': total_likes,
                            'owner_comment': owner_comment,
                            'owner_username': owner_username
                            }

                fout.write('{0}\n'.format(json.dumps(to_write)))


if __name__ == '__main__':
    main()

