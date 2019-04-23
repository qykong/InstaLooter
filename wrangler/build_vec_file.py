import json

line_cnt = 1
with open('../data/bully.vec', 'w') as fout:
    fout.write('$TYPE vec\n')
    fout.write('$XDIM 4601\n')
    fout.write('$YDIM 1\n')
    fout.write('$VEC_DIM 57\n')
    with open('../data/full_sessions_pos_2218.json', 'r') as fin:
        for line in fin:
            session_json = json.loads(line.rstrip())
            semantic_features = session_json['semantic_features']
            line_cnt += 1