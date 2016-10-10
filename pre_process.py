from scripts.accuracy_calculator import calculate_accuracy
from scripts.corpus_pre_processor import pre_process_corpus
from scripts.corpus_splitter import split_corpus
from scripts.directory_selector import select_directory
from scripts.ferret_executer import execute_ferret
from scripts.result_generator import generate_result
from scripts.settings_helper import settings_to_directory


# TODO This settings should inserted by the user either through a GUI or by command line
# The settings to be used
settings = {
	"remove_stop_words": True,
	"permitted_tags": ['NOUN', 'VERB', 'ADV', 'PRON'],
	"perform_ordering": True,
	"use_word_sense": True,
	"similarity_measure": "wup", # Possible values are "jcn", "lin", "res", "lch", "path", "wup"
	"similarity_threshold": 0.5,
	"type_of_replacement": "keep_unique",
	# Possible values are "random", "keep_unique", "keep_other"
	# TODO use something more sophisticated like common_hypernym or most_abstract
}


def display_menu():
	print("\033c")
	menu_input = raw_input((
		"Commands: \n"
		"[1] Split corpus \n"
		"[2] Pre process corpus \n"
		"[3] Calculate accuracy \n"
		"[4] Quit \n"
		"Please input command: "
	))

	return menu_input

verbosity = 'verbose'
loop = True
while loop:
	selection = display_menu()
	if selection == '1':
		split_corpus(verbosity)
		execute_ferret('splitted_files', verbosity)
		raw_input("Corpus splitted successfully \n(Press any key to continue)")
	elif selection == '2':
		directory_name = settings_to_directory(settings)
		pre_process_corpus(settings, directory_name, verbosity)
		execute_ferret(directory_name, 'verbose')
		raw_input("Corpus pre processed successfully \n(Press any key to continue)")
	elif selection == '3':
		directory_name = select_directory()
		threshold = raw_input("Please input threshold: ")
		generate_result(directory_name, threshold)
		result = calculate_accuracy(directory_name)
		print result
		raw_input("(Press any key to continue)")
	elif selection == '4':
		loop = False
	else:
		raise Exception("Unknown selection")
