import json
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def text_preprocess(text):
    # removing whitespaces, punctuations, stopwords, and stemming words
    intermediate = re.sub(r'[^a-zA-Z1-9#@ ]+', '', text).split()
    stop = stopwords.words('english')
    intermediate = [i for i in intermediate if i not in stop]
    snowball = SnowballStemmer('english')
    intermediate = [snowball.stem(i) for i in intermediate]
    return ' '.join(intermediate)


def main():
    with open('../data/texts_for_tagging.tsv', 'w', encoding='utf-8') as fout:
        with open('../data/full_sessions_2218.json', 'r', encoding='utf-8') as fin:
            for line in fin:
                session_json = json.loads(line.rstrip())
                unit_id = session_json['unit_id']
                total_comments = int(session_json['total_comments'])
                comments_list = session_json['comments_list']
                owner_comment = session_json['owner_comment']
                owner_comment = text_preprocess(owner_comment)
                if not owner_comment == '':
                    fout.write('{0}\t{1}\n'.format(unit_id, owner_comment))
                for cmt_idx in range(total_comments):
                    comment_text = comments_list[cmt_idx][1]
                    comment_text = text_preprocess(comment_text)
                    if not comment_text == '':
                        fout.write('{0}_{1}\t{2}\n'.format(unit_id, cmt_idx, comment_text))


if __name__ == '__main__':
    main()
