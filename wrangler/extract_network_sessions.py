import json


def main():
    session_user_set = set()
    with open('../data/source_target.csv', 'r') as fin:
        fin.readline()
        for line in fin:
            s, t = line.rstrip().split(',')
            session_user_set.add(s)
            session_user_set.add(t)

    print('{0} users appear in both 2218 session dataset and social network dataset'.format(len(session_user_set)))

    cnt = 0
    with open('../data/network_sessions_1764.json', 'w') as fout:
        with open('../data/full_sessions_2218.json', 'r') as fin:
            for line in fin:
                session_json = json.loads(line.rstrip())
                if session_json['owner_username'] in session_user_set:
                    fout.write(line)
                    cnt += 1
    print('{0} users post {1} sessions in the 2218 session dataset'.format(len(session_user_set), cnt))


if __name__ == '__main__':
    main()
