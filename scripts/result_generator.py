import csv
import os


def generate_result(target_directory, threshold, progress_bar=None):

	if progress_bar is not None:
		progress_bar.set_text("Calculating accuracy")
		progress_bar.set_fraction(0)

	result_file = open(target_directory+'/results.csv', 'w')
	result_file.truncate()
	result_file_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	result_file_writer.writerow([
		'Row #',
		'Actual Result',
		'Ferret Result (threshold = ' + str(threshold) + ')',
		'Jaccard Coefficient'
	])
	i = 0
	with open('MSRParaphraseCorpus/msr_paraphrase_train.txt', 'r') as f:
		next(f)  # skip headers
		reader = csv.reader(f, delimiter='\t')

		directories_len = len(list(reader))
		f.seek(0)
		next(f)  # skip headers
		for result, id1, id2, string1, string2 in reader:
			i += 1
			if progress_bar is not None:
				progress_bar.pulse()
				fraction = i / float(directories_len)
				progress_bar.set_fraction(fraction)

			try:
				with open(target_directory + '/' + str(i) + '/ferret_result.txt', 'r') as ferret_output:
					ferret_output_reader = csv.reader(ferret_output, delimiter=';')
					ferret_result_row = next((x for j, x in enumerate(ferret_output_reader) if j == 2), None)
					if ferret_result_row is None:
						raise Exception(target_directory+'/'+str(i))
					ferret_jaccard_coefficient = ferret_result_row[5].strip()
					result_file_writer.writerow([
						str(i),
						result,
						1 if float(ferret_jaccard_coefficient) > float(threshold) else 0,
						ferret_jaccard_coefficient,
					])
			except Exception:
				raise Exception(target_directory + '/' + str(i))

	result_file.close()


def generate_list_rows(target_directory, threshold):
	rows = []
	i = 0
	with open('MSRParaphraseCorpus/msr_paraphrase_train.txt', 'r') as f:
		next(f)  # skip headers
		reader = csv.reader(f, delimiter='\t')

		for result, id1, id2, string1, string2 in reader:
			i += 1

			with open(target_directory + '/' + str(i) + '/ferret_result.txt', 'r') as ferret_output:
				ferret_output_reader = csv.reader(ferret_output, delimiter=';')
				ferret_result_row = next((x for j, x in enumerate(ferret_output_reader) if j == 2), None)
				ferret_jaccard_coefficient = ferret_result_row[5].strip()

			with open(target_directory + '/' + str(i) + '/' + id1 + '.txt', 'r') as my_file:
				string1_parsed = my_file.read().replace('\n', '')
			with open(target_directory + '/' + str(i) + '/' + id2 + '.txt', 'r') as my_file:
				string2_parsed = my_file.read().replace('\n', '')

			result = True if result == '1' else False
			prediction = float(ferret_jaccard_coefficient) > float(threshold)
			correctly_identified = result == prediction
			rows.append([string1, string2, correctly_identified, result, prediction, string1_parsed, string2_parsed])

	return rows
