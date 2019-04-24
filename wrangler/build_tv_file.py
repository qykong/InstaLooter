with open('../data/ig_bully.tv', 'w') as fout:
    fout.write('$TYPE template\n')
    fout.write('$XDIM 2\n')
    fout.write('$YDIM 2218\n')
    fout.write('$VEC_DIM 3810\n')

    with open('../data/ig_non_zero_tags.txt', 'r') as fin:
        for line in fin:
            fout.write(line)

with open('../data/vine_bully.tv', 'w') as fout:
    fout.write('$TYPE template\n')
    fout.write('$XDIM 2\n')
    fout.write('$YDIM 970\n')
    fout.write('$VEC_DIM 2845\n')

    with open('../data/vine_non_zero_tags.txt', 'r') as fin:
        for line in fin:
            fout.write(line)
