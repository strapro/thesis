import os
import csv
from sys import stdout


def split_corpus(verbosity='silent'):
	if verbosity != 'silent':
		stdout.write("Splitting corpus. Please wait\n")
	i = 0
	with open('MSRParaphraseCorpus/msr_paraphrase_train.txt', 'r') as f:
		next(f)
		reader = csv.reader(f, delimiter='\t')
		for result, id1, id2, string1, string2 in reader:
			i += 1

			directory = 'splitted_files/'+str(i)
			if not os.path.exists(directory):
				os.makedirs(directory)

			target1 = open(directory+'/'+id1+'.txt', 'w')
			target1.truncate()
			target1.write(string1)
			target1.close()

			target2 = open(directory+'/'+id2+'.txt', 'w')
			target2.truncate()
			target2.write(string2)
			target2.close()
