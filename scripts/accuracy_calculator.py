import csv
from sklearn.metrics import *


def calculate_accuracy(target_directory):
	y_true = []
	y_pred = []

	with open(target_directory+'/results.csv', 'r') as f:
		next(f)

		reader = csv.reader(f, delimiter=';')
		for row_number, actual_result, ferret_result, coefficient in reader:
			actual_result_label = True if actual_result == '1' else False
			ferret_result_label = True if ferret_result == '1' else False
			y_true.append(actual_result_label)
			y_pred.append(ferret_result_label)

	accuracy = accuracy_score(y_true, y_pred)
	precision = precision_score(y_true, y_pred)
	recall = recall_score(y_true, y_pred)
	f_measure = f1_score(y_true, y_pred)

	return {
		'accuracy': accuracy,
		'precision': precision,
		'recall': recall,
		'f_measure': f_measure
	}
