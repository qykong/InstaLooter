import gzip
import numpy as np


def extract_pos_one_int(text):
    return int(text.strip().split()[1])


def read_unit_gz(gz_file, grid):
    with gzip.open(gz_file, 'r') as fin:
        """
        $TYPE som
        $GRID_LAYOUT rectangular
        $GRID_TOPOLOGY planar
        $FILE_FORMAT_VERSION 1.2
        $YDIM 16
        $YDIM 16
        """
        for _ in range(6):
            fin.readline()

        """
        $POS_X 0
        $POS_Y 0
        $UNIT_ID ig_bully.remapped_(0/0)
        $QUANTERROR_UNIT 384.2991136358952
        $QUANTERROR_UNIT_AVG 76.85982272717904
        $NR_VEC_MAPPED 5
        $MAPPED_VECS
        1184
        243
        827
        1320
        2197
        $MAPPED_VECS_DIST 30.063413490832318 39.381441626586344 40.45431254958316 66.77418574041522 207.62576022847813
        """
        for _ in range(XDIM * YDIM):
            x = extract_pos_one_int(fin.readline())
            y = extract_pos_one_int(fin.readline())
            for _ in range(3):
                fin.readline()
            num_points = extract_pos_one_int(fin.readline())
            if num_points > 0:
                fin.readline()
                for _ in range(num_points):
                    grid['{0}-{1}'.format(x, y)].append(int(fin.readline().strip()))
                fin.readline()


def extract_prediction_results(file_idx):
    instance_label_dict = {}
    with open('../data/{0}_bully.cls'.format(cls_prefix), 'r') as fin:
        for _ in range(4):
            fin.readline()
        num_instances = extract_pos_one_int(fin.readline())
        for _ in range(num_instances):
            instance_id, label = fin.readline().strip().split()
            instance_label_dict[int(instance_id)] = int(label)

    train_instance_list = []
    with open('../data/{1}_data_samples/{1}_bully_train{0}.vec'.format(file_idx, cls_prefix), 'r') as fin:
        for _ in range(4):
            fin.readline()
        for line in fin:
            train_instance_list.append(int(line.rstrip().split()[-1]))
    test_instance_list = []
    with open('../data/{1}_data_samples/{1}_bully_test{0}.vec'.format(file_idx, cls_prefix), 'r') as fin:
        for _ in range(4):
            fin.readline()
        for line in fin:
            test_instance_list.append(int(line.rstrip().split()[-1]))

    # init 2D grid to store result
    grid = {'{0}-{1}'.format(x, y): [] for x in range(XDIM) for y in range(YDIM)}
    read_unit_gz('../data/{1}_output/{1}_bully{0}/{1}_bully.remapped.unit.unit.gz'.format(file_idx, cls_prefix), grid)
    read_unit_gz('../data/{1}_output/{1}_bully{0}/{1}_bully.unit.gz'.format(file_idx, cls_prefix), grid)

    # total number of points should equal to the number of instances, 2218 for IG and 970 for Vine
    print('total number of points', sum([len(v) for v in grid.values()]))

    # generate grid probability for each cell
    grid_prob = {}
    for x in range(XDIM):
        for y in range(YDIM):
            target_cell = grid['{0}-{1}'.format(x, y)]
            pos_cnt = 0
            cnt = 0
            for instance in target_cell:
                if instance in train_instance_list:
                    cnt += 1
                    pos_cnt += instance_label_dict[instance]
            if cnt > 0:
                grid_prob['{0}-{1}'.format(x, y)] = pos_cnt / cnt
            else:
                grid_prob['{0}-{1}'.format(x, y)] = None

    # print(grid_prob)

    # fix the None cell
    for x in range(XDIM):
        for y in range(YDIM):
            if grid_prob['{0}-{1}'.format(x, y)] is None:
                # corner
                if x == 0 and y == 0:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x+1, y)],
                                     grid_prob['{0}-{1}'.format(x, y+1)],
                                     grid_prob['{0}-{1}'.format(x+1, y+1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])
                elif x == XDIM-1 and y == 0:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x-1, y)],
                                     grid_prob['{0}-{1}'.format(x, y+1)],
                                     grid_prob['{0}-{1}'.format(x-1, y+1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])
                elif x == 0 and y == YDIM-1:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x+1, y)],
                                     grid_prob['{0}-{1}'.format(x, y-1)],
                                     grid_prob['{0}-{1}'.format(x+1, y-1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])
                elif x == XDIM-1 and y == YDIM-1:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x-1, y)],
                                     grid_prob['{0}-{1}'.format(x, y-1)],
                                     grid_prob['{0}-{1}'.format(x-1, y-1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])

                # border
                elif x == 0:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x, y-1)],
                                     grid_prob['{0}-{1}'.format(x, y+1)],
                                     grid_prob['{0}-{1}'.format(x+1, y-1)],
                                     grid_prob['{0}-{1}'.format(x+1, y)],
                                     grid_prob['{0}-{1}'.format(x+1, y+1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])
                elif x == XDIM-1:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x, y-1)],
                                     grid_prob['{0}-{1}'.format(x, y+1)],
                                     grid_prob['{0}-{1}'.format(x-1, y-1)],
                                     grid_prob['{0}-{1}'.format(x-1, y)],
                                     grid_prob['{0}-{1}'.format(x-1, y+1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])
                elif y == 0:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x-1, y)],
                                     grid_prob['{0}-{1}'.format(x+1, y)],
                                     grid_prob['{0}-{1}'.format(x-1, y+1)],
                                     grid_prob['{0}-{1}'.format(x, y+1)],
                                     grid_prob['{0}-{1}'.format(x+1, y+1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])
                elif y == YDIM-1:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x-1, y)],
                                     grid_prob['{0}-{1}'.format(x+1, y)],
                                     grid_prob['{0}-{1}'.format(x-1, y-1)],
                                     grid_prob['{0}-{1}'.format(x, y-1)],
                                     grid_prob['{0}-{1}'.format(x+1, y-1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])

                # middle
                else:
                    neighbor_cell = [grid_prob['{0}-{1}'.format(x-1, y-1)],
                                     grid_prob['{0}-{1}'.format(x-1, y)],
                                     grid_prob['{0}-{1}'.format(x-1, y+1)],
                                     grid_prob['{0}-{1}'.format(x, y-1)],
                                     grid_prob['{0}-{1}'.format(x, y+1)],
                                     grid_prob['{0}-{1}'.format(x+1, y-1)],
                                     grid_prob['{0}-{1}'.format(x+1, y)],
                                     grid_prob['{0}-{1}'.format(x+1, y+1)]]
                    grid_prob['{0}-{1}'.format(x, y)] = np.mean([ncell for ncell in neighbor_cell if ncell is not None])

    # generate test_id, true_label, pred_label
    with open('../data/{1}_output/{1}_bully{0}/{1}_id_true_pred.csv'.format(file_idx, cls_prefix), 'w') as fout:
        for x in range(XDIM):
            for y in range(YDIM):
                target_cell = grid['{0}-{1}'.format(x, y)]
                for instance in target_cell:
                    if instance in test_instance_list:
                        fout.write('{0},{1},{2}\n'.format(instance, instance_label_dict[instance], grid_prob['{0}-{1}'.format(x, y)]))


def main():
    for file_idx in range(1, 11):
        extract_prediction_results('{:02d}'.format(file_idx))


if __name__ == '__main__':
    XDIM = 16
    YDIM = 16
    cls_prefix = 'ig'

    main()
