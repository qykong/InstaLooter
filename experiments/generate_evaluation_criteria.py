# precision (neg), recall (neg), f1 (neg), precision (pos), recall (pos), f1 (pos), accuracy, auc
import numpy as np
from sklearn.metrics import roc_auc_score


def generate_table(file_idx):
    true_list = []
    pred_list = []
    pred_prob_list = []

    with open('../data/{1}_output/{1}_bully{0}/{1}_id_true_pred.csv'.format(file_idx, cls_prefix), 'r') as fin:
        for line in fin:
            _, true, pred = line.rstrip().split(',')
            true = int(true)
            pred_prob = float(pred)
            pred = int(pred_prob >= 0.5)

            true_list.append(true)
            pred_list.append(pred)
            pred_prob_list.append(pred_prob)

    true_list = np.array(true_list)
    pred_list = np.array(pred_list)
    pred_prob_list = np.array(pred_prob_list)

    # precision (neg)
    prec_neg = 1 - sum(true_list[pred_list == 0]) / sum(pred_list == 0)
    # print('prec neg: {0:.4f}'.format(prec_neg))

    # recall (neg)
    recall_neg = 1 - sum(pred_list[true_list == 0]) / sum(true_list == 0)
    # print('recall neg: {0:.4f}'.format(recall_neg))

    # f1 (neg)
    f1_neg = 2 * prec_neg * recall_neg / (prec_neg + recall_neg)
    # print('f1 neg: {0:.4f}'.format(f1_neg))

    # precision (pos)
    prec_pos = sum(true_list[pred_list == 1]) / sum(pred_list == 1)
    # print('prec pos: {0:.4f}'.format(prec_pos))

    # recall (pos)
    recall_pos = sum(pred_list[true_list == 1]) / sum(true_list == 1)
    # print('recall pos: {0:.4f}'.format(recall_pos))

    # f1 (pos)
    f1_pos = 2 * prec_pos * recall_pos / (prec_pos + recall_pos)
    # print('f1 pos: {0:.4f}'.format(f1_pos))

    # accuracy
    accuracy = (sum(true_list[pred_list == 1]) + len(true_list[pred_list == 0]) - sum(true_list[pred_list == 0])) / len(true_list)
    # print('accuracy: {0:.4f}'.format(accuracy))

    # auc
    auc = roc_auc_score(true_list, pred_prob_list)
    # print('auc: {0:.4f}'.format(auc))

    return prec_neg, recall_neg, f1_neg, prec_pos, recall_pos, f1_pos, accuracy, auc


def main():
    prec_neg_list = []
    recall_neg_list = []
    f1_neg_list = []
    prec_pos_list = []
    recall_pos_list = []
    f1_pos_list = []
    accuracy_list = []
    auc_list = []

    for file_idx in range(1, 11):
        prec_neg, recall_neg, f1_neg, prec_pos, recall_pos, f1_pos, accuracy, auc = generate_table('{:02d}'.format(file_idx))
        prec_neg_list.append(prec_neg)
        recall_neg_list.append(recall_neg)
        f1_neg_list.append(f1_neg)
        prec_pos_list.append(prec_pos)
        recall_pos_list.append(recall_pos)
        f1_pos_list.append(f1_pos)
        accuracy_list.append(accuracy)
        auc_list.append(auc)

    print('prec neg: {0:.4f} +- {1:.4f}'.format(np.mean(prec_neg_list), np.std(prec_neg_list)))
    print('recall neg: {0:.4f} +- {1:.4f}'.format(np.mean(recall_neg_list), np.std(recall_neg_list)))
    print('f1 neg: {0:.4f} +- {1:.4f}'.format(np.mean(f1_neg_list), np.std(f1_neg_list)))
    print('prec pos: {0:.4f} +- {1:.4f}'.format(np.mean(prec_pos_list), np.std(prec_pos_list)))
    print('recall pos: {0:.4f} +- {1:.4f}'.format(np.mean(recall_pos_list), np.std(recall_pos_list)))
    print('f1 pos: {0:.4f} +- {1:.4f}'.format(np.mean(f1_pos_list), np.std(f1_pos_list)))
    print('accuracy: {0:.4f} +- {1:.4f}'.format(np.mean(accuracy_list), np.std(accuracy_list)))
    print('auc: {0:.4f} +- {1:.4f}'.format(np.mean(auc_list), np.std(auc_list)))


if __name__ == '__main__':
    cls_prefix = 'vine'
    if cls_prefix == 'ig':
        print('Experimental results for Instagram')
    elif cls_prefix == 'vine':
        print('Experimental results for Vine')


    main()
