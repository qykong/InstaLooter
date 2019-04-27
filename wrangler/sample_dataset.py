# sample 80% data into train, 20% into test
import os
import numpy as np


def extract_pos_one_int(text):
    return int(text.strip().split()[1])


def main():
    data_prefix = '../data'
    num_splits = 10
    input_filename = 'vine_bully.vec'

    header = []
    content = []
    with open(os.path.join(data_prefix, input_filename), 'r') as fin:
        header.append(fin.readline())
        xdim = extract_pos_one_int(fin.readline())
        num_train = int(0.8 * xdim)
        num_test = xdim - num_train
        header.append(fin.readline())
        header.append(fin.readline())

        for line in fin:
            content.append(line)

    for idx in range(1, 1 + num_splits):
        train_fout = open(os.path.join(data_prefix, 'vine_data_samples', 'vine_bully_train{:02d}.vec'.format(idx)), 'w')
        test_fout = open(os.path.join(data_prefix, 'vine_data_samples', 'vine_bully_test{:02d}.vec'.format(idx)), 'w')
        train_fout.write(header[0])
        test_fout.write(header[0])
        train_fout.write('$XDIM {0}\n'.format(num_train))
        test_fout.write('$XDIM {0}\n'.format(num_test))
        train_fout.write(header[1])
        test_fout.write(header[1])
        train_fout.write(header[2])
        test_fout.write(header[2])

        np.random.seed(idx)
        np.random.shuffle(content)
        content_train = content[: num_train]
        content_test = content[num_train:]
        for line in content_train:
            train_fout.write(line)
        for line in content_test:
            test_fout.write(line)


if __name__ == '__main__':
    main()
