from scripts.settings_helper import *
from scripts.corpus_pre_processor import pre_process_corpus
from scripts.ferret_executer import execute_ferret
from itertools import combinations

def float_range(x, y, jump):
	while x <= y:
		yield x
		x += jump

tags = ['VERB', 'NOUN', 'ADJ', 'ADV', 'PRON', 'ADP', 'CONJ']
settings_possible_values = {
	"remove_stop_words": [True, False],
	"permitted_tags": sum([map(list, combinations(tags, i)) for i in range(3, len(tags) + 1)], []),
	"perform_ordering": [True, False],
	"use_word_sense": [True],  # [True, False]
	"similarity_measure": ["jcn", "res", "lch", "lin", "path", "wup"],
	"similarity_threshold": list(float_range(0.1, 1, 0.2)),
	"type_of_replacement": ["keep_unique"]  # ["random", "keep_unique", "keep_other"]
}

i = 0
total = 11880
verbosity = 'verbose'
for remove_stop_words in settings_possible_values['remove_stop_words']:
	for permitted_tags in settings_possible_values['permitted_tags']:
		for perform_ordering in settings_possible_values['perform_ordering']:
			for use_word_sense in settings_possible_values['use_word_sense']:
				for similarity_measure in settings_possible_values['similarity_measure']:
					for similarity_threshold in settings_possible_values['similarity_threshold']:
						for type_of_replacement in settings_possible_values['type_of_replacement']:
							i += 1

							print("\033c")
							print str(i) + "/" + str(total)

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
							pre_process_corpus(settings, 'splitted_parsed_files/' + directory_name, verbosity)
							execute_ferret('splitted_parsed_files/' + directory_name, verbosity)
