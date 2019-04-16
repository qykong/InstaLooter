#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Extract seed username from sessions_metadata.csv.
"""

import re
import pandas as pd


def remove_decorator(text):
    return re.sub('<.*?>', '', text).strip()


def main():
    username_set = set()

    session_filenames = ['../data/sessions_0plus_to_10_metadata.csv', '../data/sessions_10plus_to_40_metadata.csv',
                         '../data/sessions_40plus_metadata.csv']
    for filename in session_filenames:
        data = pd.read_csv(filename, encoding='latin-1')
        data_usernames = set(map(remove_decorator, list(data['owner_id'].values)))
        username_set.update(data_usernames)

    with open('../data/session_username.txt', 'w') as fout:
        for username in username_set:
            fout.write('{0}\n'.format(username))


if __name__ == '__main__':
    main()

