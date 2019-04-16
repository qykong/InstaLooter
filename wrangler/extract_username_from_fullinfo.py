#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Extract seed username from UserFullInfo.json.
"""

import os, json


def main():
    fout = open('../data/fullinfo_username.txt', 'w')
    session_username_set = set()
    visited_username_set = set()
    written_username_set = set()

    with open('../data/session_username.txt', 'r') as fin:
        for line in fin:
            session_username_set.add(line.rstrip())

    network_edge_file = open('../data/source_target.csv', 'w')
    network_edge_file.write('Source,Target\n')

    for dir_path in ['../data/FormattedCommonUserFullInfo', '../data/FormattedNormalUserFullInfo']:
        for subdir, _, files in os.walk(dir_path):
            for f in files:
                line_cnt = 0
                with open(os.path.join(subdir, f), 'r') as fin:
                    for line in fin:
                        user_obj = json.loads(line.rstrip())
                        username = user_obj['user_name']
                        line_cnt += 1
                        if username not in visited_username_set:
                            fout.write('{0}\n'.format(username))
                            visited_username_set.add(username)

                        if username in session_username_set and username not in written_username_set:
                            # time to write to network relation file
                            print('find {1} common user {0}'.format(username, len(written_username_set) + 1))
                            follows = user_obj['follows']
                            for target_username in follows:
                                if target_username in session_username_set:
                                    network_edge_file.write('{0},{1}\n'.format(username, target_username))
                            followed_by = user_obj['followed_by']
                            for source_username in followed_by:
                                if source_username in session_username_set:
                                    network_edge_file.write('{0},{1}\n'.format(source_username, username))
                            written_username_set.add(username)
                print('{0} lines in {1}'.format(line_cnt, f))

    fout.close()
    network_edge_file.close()


if __name__ == '__main__':
    main()
