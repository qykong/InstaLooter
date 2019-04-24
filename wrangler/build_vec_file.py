import json

line_cnt = 1
with open('../data/ig_full_sessions_pos_2218.json', 'r') as fin:
    fout1 = open('../data/ig_bully.vec', 'w')
    fout1.write('$TYPE vec\n')
    fout1.write('$XDIM 2218\n')
    fout1.write('$YDIM 1\n')
    fout1.write('$VEC_DIM 3810\n')

    fout2 = open('../data/ig_bully.cls', 'w')
    fout2.write('$TYPE class_information\n')
    fout2.write('$NUM_CLASSES 2\n')
    fout2.write('$CLASS_NAMES NBully Bully\n')
    fout2.write('$XDIM 2\n')
    fout2.write('$YDIM 2218\n')

    for line in fin:
        session_json = json.loads(line.rstrip())
        semantic_features = session_json['semantic_features']
        semantic_features.append(line_cnt)
        question2 = session_json['question2']
        cyberbullying = 1 if question2 else 0
        fout1.write('{0}\n'.format(' '.join(map(str, semantic_features))))
        fout2.write('{0} {1}\n'.format(line_cnt, cyberbullying))
        line_cnt += 1

    fout1.close()
    fout2.close()

line_cnt = 1
with open('../data/vine_full_sessions_pos_970.json', 'r') as fin:
    fout1 = open('../data/vine_bully.vec', 'w')
    fout1.write('$TYPE vec\n')
    fout1.write('$XDIM 970\n')
    fout1.write('$YDIM 1\n')
    fout1.write('$VEC_DIM 2845\n')

    fout2 = open('../data/vine_bully.cls', 'w')
    fout2.write('$TYPE class_information\n')
    fout2.write('$NUM_CLASSES 2\n')
    fout2.write('$CLASS_NAMES NBully Bully\n')
    fout2.write('$XDIM 2\n')
    fout2.write('$YDIM 970\n')

    for line in fin:
        session_json = json.loads(line.rstrip())
        semantic_features = session_json['semantic_features']
        semantic_features.append(line_cnt)
        question2 = session_json['question2']
        cyberbullying = 1 if question2 else 0
        fout1.write('{0}\n'.format(' '.join(map(str, semantic_features))))
        fout2.write('{0} {1}\n'.format(line_cnt, cyberbullying))
        line_cnt += 1

    fout1.close()
    fout2.close()
