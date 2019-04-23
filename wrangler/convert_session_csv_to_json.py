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
    if block == 'empety':
        return None
    comment_text = block[block.find('</font>') + 7: block.find('(created')]
    # remove http url
    comment_text = re.sub(r'http\S+', '', comment_text).strip()
    return (block[block.find('>') + 1: block.find('</font>')],
            remove_decorator(comment_text),
            block[block.find('(created') + 12: -1])


def remove_decorator(text):
    return re.sub('<.*?>', '', text).strip()


def main():
    output_path = '../data/full_sessions_2218.json'
    session_filenames = ['../data/sessions_0plus_to_10_metadata.csv', '../data/sessions_10plus_to_40_metadata.csv',
                         '../data/sessions_40plus_metadata.csv']

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
                for i in range(1, 196):
                    comment_triplet = extract_comment_triplet(row['clmn{0}'.format(i)])
                    if comment_triplet is not None:
                        comments_list.append(comment_triplet)
                total_comments = len(comments_list)

                post_timestamp = row['cptn_time'][-19:].strip()
                if post_timestamp[0] == ' ':
                    post_timestamp = '2' + post_timestamp[1:]
                img_url = row['img_url'].strip()
                total_likes = int(row['likes'].split()[0])

                if pd.isna(row['owner_cmnt']):
                    owner_comment = ''
                else:
                    owner_comment = remove_decorator(row['owner_cmnt'])
                    if owner_comment.startswith('Media posted at'):
                        owner_comment = ''
                    # remove http url
                    owner_comment = re.sub(r'http\S+', '', owner_comment)
                    if len(owner_comment) > 0 and owner_comment[-1] == '"':
                        owner_comment = owner_comment[: -1]

                owner_username = remove_decorator(row['owner_id'])
                owner_num_posts = int(row['shared media'])
                owner_num_followers = int(row['followed_by'])
                owner_num_follows = int(row['follows'])
                cyberaggression = int(row['cyberaggression'])
                cyberbullying = int(row['cyberbullying'])

                to_write = {'unit_id': unit_id,
                            'question1': question1, 'question1_conf': question1_conf,
                            'question2': question2, 'question2_conf': question2_conf,
                            'comments_list': comments_list, 'total_comments': total_comments,
                            'post_timestamp': post_timestamp, 'img_url': img_url, 'total_likes': total_likes,
                            'owner_comment': owner_comment,
                            'owner_username': owner_username, 'owner_num_posts': owner_num_posts,
                            'owner_num_followers': owner_num_followers, 'owner_num_follows': owner_num_follows,
                            'cyberaggression': cyberaggression, 'cyberbullying': cyberbullying,
                            }

                fout.write('{0}\n'.format(json.dumps(to_write)))


if __name__ == '__main__':
    main()

