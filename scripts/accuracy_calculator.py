import csv
from sklearn.metrics import precision_recall_fscore_support


def calculate_accuracy(target_directory):
    y_true = []
    y_pred = []
    with open(target_directory+'/results.csv', 'r') as f:
        next(f)
        reader = csv.reader(f, delimiter=';')
        for row_number, actual_result, ferret_result, coefficient in reader:
            actual_result_label = 'true' if actual_result == '1' else 'false'
            ferret_result_label = 'true' if ferret_result == '1' else 'false'
            y_true.append(actual_result_label)
            y_pred.append(ferret_result_label)

    result = precision_recall_fscore_support(y_true, y_pred, average='binary', pos_label=None)

    return result
