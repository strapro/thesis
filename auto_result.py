from scripts.settings_helper import *
from itertools import combinations
from scripts.result_generator import generate_result
from scripts.accuracy_calculator import calculate_accuracy
from scripts.ferret_executer import execute_single_ferret
import csv


def float_range(x, y, jump):
	while x <= y:
		yield x
		x += jump


def get_row(directory_name, jaccard_threshold, result_file_writer):
	try:
		generate_result('splitted_parsed_files/' + directory_name, jaccard_threshold)
		accuracy = calculate_accuracy('splitted_parsed_files/' + directory_name)

		result_file_writer.writerow([
			str(remove_stop_words),
			" ".join(permitted_tags),
			str(perform_ordering),
			str(use_word_sense),
			str(similarity_measure),
			str(similarity_threshold),
			str(type_of_replacement),
			str(jaccard_threshold),
			str(accuracy['accuracy']),
			str(accuracy['recall']),
			str(accuracy['precision']),
			str(accuracy['f_measure']),
		])
	except Exception, e:
		print 'Error. Executing ferret and retrying '
		execute_single_ferret(str(e))
		get_row(directory_name, jaccard_threshold, result_file_writer)


tags = ['VERB', 'NOUN', 'ADJ', 'ADV', 'ADP', 'CONJ']
settings_possible_values = {
	"remove_stop_words": [True],
	"permitted_tags": sum([map(list, combinations(tags, i)) for i in range(3, len(tags) + 1)], []),
	"perform_ordering": [True, False],
	"use_word_sense": [True],  # [True, False]
	"similarity_measure": ["jcn", "res", "lch", "lin", "path", "wup"],
	"similarity_threshold": list(float_range(0.1, 1, 0.2)),
	"type_of_replacement": ["keep_unique"]  # ["random", "keep_unique", "keep_other"]
}

if __name__ == '__main__':
	result_file = open('auto_result.csv', 'w')
	result_file.truncate()
	result_file_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	result_file_writer.writerow([
		'remove_stop_words',
		'permitted_tags',
		'perform_ordering',
		'use_word_sense',
		'similarity_measure',
		'similarity_threshold',
		'type_of_replacement',
		'jaccard_threshold',
		'accuracy',
		'recall',
		'precision',
		'f_measure'
	])

	i = 0
	jaccard_threshold_array = list(float_range(0.1, 1, 0.2))
	total = 2520 * len(jaccard_threshold_array)
	for remove_stop_words in settings_possible_values['remove_stop_words']:
		for permitted_tags in settings_possible_values['permitted_tags']:
			for perform_ordering in settings_possible_values['perform_ordering']:
				for use_word_sense in settings_possible_values['use_word_sense']:
					for similarity_measure in settings_possible_values['similarity_measure']:
						for similarity_threshold in settings_possible_values['similarity_threshold']:
							for type_of_replacement in settings_possible_values['type_of_replacement']:
								settings = {
									"remove_stop_words": remove_stop_words,
									"permitted_tags": permitted_tags,
									"perform_ordering": perform_ordering,
									"use_word_sense": use_word_sense,
									"similarity_measure": similarity_measure,
									"similarity_threshold": similarity_threshold,
									"type_of_replacement": type_of_replacement,
								}

								directory_name = settings_to_directory(settings)
								for jaccard_threshold in jaccard_threshold_array:
									i += 1
									print str(i) + "/" + str(total)
									get_row(directory_name, jaccard_threshold, result_file_writer)

	result_file.close()
