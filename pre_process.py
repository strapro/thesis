from scripts.accuracy_calculator import calculate_accuracy
from scripts.corpus_pre_processor import pre_process_corpus
from scripts.corpus_splitter import split_corpus
from scripts.ferret_executer import execute_ferret
from scripts.result_generator import generate_result
from scripts.settings_helper import *

import os
import time


class Table:
	def __init__(self, headers, rows):
		self.headers = headers
		self.rows = rows
		self.n_rows = len(self.rows)
		self.field_len = []

		n_cols = len(headers)

		for i in range(n_cols):
			max = 0
			for j in rows:
				if len(str(j[i])) > max:
					max = len(str(j[i]))
			self.field_len.append(max)

		for i in range(len(headers)):
			if len(str(headers[i])) > self.field_len[i]:
				self.field_len[i] = len(str(headers[i]))

		self.width = sum(self.field_len) + (n_cols - 1) * 3 + 4

	def __str__(self):
		bar = "-" * self.width
		out = []
		header = ""
		for i in range(len(self.headers)):
			header += "| %s" % (str(self.headers[i])) + " " * (self.field_len[i] - len(str(self.headers[i]))) + " "
		header += "|"
		out.append(header)
		out.append(bar)
		for i in self.rows:
			line = ""
			for j in range(len(i)):
				line += "| %s" % (str(i[j])) + " " * (self.field_len[j] - len(str(i[j]))) + " "
			out.append(line+"|")

		out.append(bar)
		return "\r\n".join(out)


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
	print("\033c")

	return menu_input


def select_directory():
	original_or_parse = raw_input("Do you want to check the [o]riginal or the [p]arsed files: ")

	if original_or_parse == 'o':
		target_directory = 'splitted_files'
	else:
		target_directory_candidates = []
		i = 0
		header = values = []
		for parsedDirectory in next(os.walk('splitted_parsed_files'))[1]:
			extracted_settings = directory_to_settings(parsedDirectory)
			if i == 0:
				header = ['# '] + ['date'] + list(extracted_settings.keys())
			directory_time = os.stat('splitted_parsed_files/'+parsedDirectory).st_mtime
			directory_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(directory_time))
			values.append(['['+str(i)+']'] + [directory_date] + list(extracted_settings.values()))

			target_directory_candidates.append(parsedDirectory)
		print Table(header, values)
		target_directory_candidate_index = raw_input("Which parsed files: ")
		target_directory = 'splitted_parsed_files/'+target_directory_candidates[int(target_directory_candidate_index)]

	return target_directory


# TODO This settings should inserted by the user either through a GUI or by command line
# The settings to be used
settings = {
	"remove_stop_words": True,
	"permitted_tags": ['NOUN', 'VERB', 'ADV', 'PRON'],
	"perform_ordering": True,
	"use_word_sense": True,
	"similarity_measure": "wup",  # Possible values are "jcn", "lin", "res", "lch", "path", "wup"
	"similarity_threshold": 0.5,
	"type_of_replacement": "keep_unique",  # Possible values are "random", "keep_unique", "keep_other"
	# TODO use something more sophisticated like common_hypernym or most_abstract
}

verbosity = 'verbose'
loop = True
while loop:
	selection = display_menu()
	if selection == '1':  # Split corpus
		split_corpus(verbosity)
		execute_ferret('splitted_files', verbosity)
		raw_input("Corpus splitted successfully \n(Press any key to continue)")
	elif selection == '2':  # Pre process corpus
		directory_name = settings_to_directory(settings)
		pre_process_corpus(settings, 'splitted_parsed_files/'+directory_name, verbosity)
		execute_ferret('splitted_parsed_files/'+directory_name, verbosity)
		raw_input("Corpus pre processed successfully \n(Press any key to continue)")
	elif selection == '3':  # Calculate accuracy
		directory_name = select_directory()
		threshold = raw_input("Please input threshold: ")
		generate_result(directory_name, threshold)
		result = calculate_accuracy(directory_name)
		print Table(result.keys(), [[round(x, 4) for x in result.values()]])
		raw_input("(Press any key to continue)")
	elif selection == '4':  # Calculate accuracy
		loop = False
