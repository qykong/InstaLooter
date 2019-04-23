import json, itertools
import numpy as np
from collections import Counter


def flatten(x):
    ret = ''
    for xx in x:
        ret += xx
    return ret


def main():
    with open('../data/full_sessions_pos_2218.json', 'w') as fout:
        pos_tag_stat = []
        unit_id_set = set()

        with open('../data/pos_tag_results.tsv', 'r') as fin1:
            for line in fin1:
                processed_text, pos, conf, id, _ = line.rstrip().split('\t')
                pos_tag_stat.extend(pos.split())
                if '_' in id:
                    id = int(id.split('_')[0])
                else:
                    id = int(id)
                unit_id_set.add(id)

        print('usage of each POS')
        print(Counter(pos_tag_stat))

        # remove infrequent POS: {'Z': 198, 'X': 131, '~': 83, ',': 19, 'S': 8, 'U': 1, 'Y': 1}
        infrequent_tags = ['Z', 'X', '~', ',', 'S', 'U', 'Y']
        pos_tag_list = [x for x in Counter(pos_tag_stat).keys() if x not in infrequent_tags]
        print('number of POS tag', len(pos_tag_list))
        print(pos_tag_list)

        bigram_tags = [flatten(p) for p in itertools.product(pos_tag_list, repeat=2)]
        print(bigram_tags[:10])
        trigram_tags = [flatten(p) for p in itertools.product(pos_tag_list, repeat=3)]
        print(trigram_tags[:10])
        all_tags = bigram_tags + trigram_tags
        all_tags_idx_dict = {tag: idx for idx, tag in enumerate(all_tags)}
        print('len of semantic feature space (bigram+trigram)', len(all_tags))

        unit_id_semantic_features = {id: [0] * len(all_tags) for id in unit_id_set}
        with open('../data/pos_tag_results.tsv', 'r') as fin1:
            for line in fin1:
                processed_text, pos, conf, id, _ = line.rstrip().split('\t')
                if '_' in id:
                    id = int(id.split('_')[0])
                else:
                    id = int(id)
                pos = pos.split()
                len_pos = len(pos)
                if len_pos >= 2:
                    # bigram
                    for i in range(len_pos-1):
                        ft = pos[i] + pos[i+1]
                        if ft in all_tags:
                            unit_id_semantic_features[id][all_tags_idx_dict[ft]] += 1
                if len_pos >= 3:
                    # trigram
                    for i in range(len_pos-2):
                        ft = pos[i] + pos[i+1] + pos[i+2]
                        if ft in all_tags:
                            unit_id_semantic_features[id][all_tags_idx_dict[ft]] += 1

        # convert to numpy matrix to see if any column contains 0 only
        zero_col_idx = []
        feature_mat = np.array(list(unit_id_semantic_features.values())).reshape(len(unit_id_semantic_features), len(all_tags))
        for col_idx in range(len(all_tags)):
            if not np.any(feature_mat[:, col_idx]):
                zero_col_idx.append(col_idx)

        non_zero_tags = [tag for idx, tag in enumerate(all_tags) if idx not in zero_col_idx]
        with open('../data/non_zero_tags.txt', 'w') as fout2:
            for row_idx, tag in enumerate(non_zero_tags):
                fout2.write('{0} {1}\n'.format(row_idx, tag))
        non_zero_tags_idx_dict = {tag: idx for idx, tag in enumerate(non_zero_tags)}
        print('len of non-zero semantic feature space (bigram+trigram)', len(non_zero_tags))

        # reload the feature space because it's faster
        unit_id_semantic_features = {id: [0] * len(non_zero_tags) for id in unit_id_set}
        with open('../data/pos_tag_results.tsv', 'r') as fin1:
            for line in fin1:
                processed_text, pos, conf, id, _ = line.rstrip().split('\t')
                if '_' in id:
                    id = int(id.split('_')[0])
                else:
                    id = int(id)
                pos = pos.split()
                len_pos = len(pos)
                if len_pos >= 2:
                    # bigram
                    for i in range(len_pos - 1):
                        ft = pos[i] + pos[i + 1]
                        if ft in non_zero_tags:
                            unit_id_semantic_features[id][non_zero_tags_idx_dict[ft]] += 1
                if len_pos >= 3:
                    # trigram
                    for i in range(len_pos - 2):
                        ft = pos[i] + pos[i + 1] + pos[i + 2]
                        if ft in non_zero_tags:
                            unit_id_semantic_features[id][non_zero_tags_idx_dict[ft]] += 1

        with open('../data/full_sessions_2218.json', 'r') as fin2:
            for line in fin2:
                session_json = json.loads(line.rstrip())
                unit_id = int(session_json['unit_id'])
                session_json['semantic_features'] = unit_id_semantic_features[unit_id]
                fout.write('{0}\n'.format(json.dumps(session_json)))


if __name__ == '__main__':
    main()
