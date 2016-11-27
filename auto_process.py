from scripts.settings_helper import *
from scripts.corpus_pre_processor import pre_process_corpus
from scripts.ferret_executer import execute_ferret
from scripts.result_generator import generate_result
from scripts.accuracy_calculator import calculate_accuracy
from itertools import combinations
import csv
import shutil
import multiprocessing
import os
import time
import hashlib


def float_range(x, y, jump):
	while x <= y:
		yield x
		x += jump


def execute(settings_to_execute, executing_i):
	verbosity = 'silent'
	force_overwrite = False
	total = 2526

	print "Executing " + str(executing_i) + "/" + str(total)

	new_directory_name = settings_to_directory(settings_to_execute)
	pre_process_corpus(settings_to_execute, 'splitted_parsed_files/' + new_directory_name, force_overwrite, verbosity)
	execute_ferret('splitted_parsed_files/' + new_directory_name, force_overwrite, verbosity)
	return executing_i, new_directory_name, settings_to_execute


def log_auto_process_result(result):
	(logging_i, directory_name_to_log, settings_to_log) = result

	total = 2526
	print "Calculating " + str(logging_i) + "/" + str(total)
	jaccard_threshold_array = list(float_range(0.1, 1, 0.2))

	result_file = open('auto_result.csv', 'a', 0)
	result_file_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for jaccard_threshold in jaccard_threshold_array:
		try:
			generate_result('splitted_parsed_files/' + directory_name_to_log, jaccard_threshold)
			accuracy = calculate_accuracy('splitted_parsed_files/' + directory_name_to_log)

			result_file_writer.writerow([
				str(settings_to_log['remove_stop_words']),
				" ".join(settings_to_log['permitted_tags']),
				str(settings_to_log['perform_ordering']),
				str(settings_to_log['use_word_sense']),
				str(settings_to_log['similarity_measure']),
				str(settings_to_log['similarity_threshold']),
				str(settings_to_log['type_of_replacement']),
				str(jaccard_threshold),
				str(accuracy['accuracy']),
				str(accuracy['recall']),
				str(accuracy['precision']),
				str(accuracy['f_measure']),
			])
			result_file.flush()
		except Exception, e:
			os.fsync(result_file.fileno())
			result_file.close()
			time.sleep(5)

			print str(e)

			return True
			# print 'Error. Executing ferret and retrying '
			# execute_single_ferret(str(e))
			# log_auto_process_result(directory_name, jaccard_threshold, result_file_writer)

	os.fsync(result_file.fileno())
	result_file.close()

	print "Removing " + str(logging_i) + "/" + str(total)
	os.system('tar -cf' + ' splitted_parsed_files/' + directory_name_to_log + '.tar' + ' splitted_parsed_files/' + directory_name_to_log)
	shutil.rmtree('splitted_parsed_files/'+directory_name_to_log, ignore_errors=True)


def get_already_processed():
	result_file = open('auto_result.csv', 'r')
	csv.register_dialect('test', delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	reader = csv.DictReader(result_file, dialect='test')

	hashes = []
	for row in reader:
		processed_settings = {
			"remove_stop_words": row["remove_stop_words"],
			"permitted_tags": row["permitted_tags"].split(' '),
			"perform_ordering": row["perform_ordering"],
			"use_word_sense": row["use_word_sense"],
			"similarity_measure": row["similarity_measure"],
			"similarity_threshold": row["similarity_threshold"],
			"type_of_replacement": row["type_of_replacement"],
		}
		parsed_directory_name = settings_to_directory(processed_settings)
		hashes.append(hashlib.md5(parsed_directory_name).hexdigest())

	result_file.close()

	return hashes

if __name__ == '__main__':
	i = 0
	total = 2526

	existing_hashes = get_already_processed()

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
	i = 0
	p = multiprocessing.Pool(4)
	for remove_stop_words in settings_possible_values['remove_stop_words']:
		for permitted_tags in settings_possible_values['permitted_tags']:
			for perform_ordering in settings_possible_values['perform_ordering']:
				for use_word_sense in settings_possible_values['use_word_sense']:
					for similarity_measure in settings_possible_values['similarity_measure']:
						for similarity_threshold in settings_possible_values['similarity_threshold']:
							for type_of_replacement in settings_possible_values['type_of_replacement']:
								i += 1

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
								hash_to_check = hashlib.md5(directory_name).hexdigest()

								if hash_to_check in existing_hashes:
									print "Skipping " + str(i) + "/" + str(total)
								else:
									p.apply_async(execute, args=(settings, i,), callback=log_auto_process_result)

	p.close()
	p.join()

