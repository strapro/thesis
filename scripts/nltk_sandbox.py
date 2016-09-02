import pprint
import os
import shutil
import pre_processing

pp = pprint.PrettyPrinter(indent=4)

#TODO This settings should inserted by the user either through a GUI or by command line
#The settings to be used
settings = {
	"remove_stop_words": True,
	"permitted_tags": ['NOUN', 'VERB', 'ADV', 'PRON'],
	"perform_ordering": True,
	"use_word_sense": True,
	"similarity_measure": "wup", #Possible values are "jcn", "lin", "res", "lch", "path", "wup"
	"similaty_threshold": 0.5,
	"type_of_replacement": "keep_unique", #Possible values are "random", "keep_unique", "keep_other" TODO use something more sophisticated like common_hypernym or most_abstract
}

parsedDirectoryNameParts = []
for key, value in settings.iteritems():
	if type(value) == list:
		valueString = "".join(str(item) for item in value)
	else:
		valueString = str(value)	
	parsedDirectoryNameParts.append(key+"="+valueString)

parsedDirectoryName = "splitted_parsed_files/"+"_".join(str(part) for part in parsedDirectoryNameParts)

if os.path.exists(parsedDirectoryName):
	shutil.rmtree(parsedDirectoryName, ignore_errors=True)

os.makedirs(parsedDirectoryName)

pre = pre_processing.PreProcessor(settings)

for directory in next(os.walk('splitted_files'))[1]:
	print directory
	files = next(os.walk('splitted_files/'+directory))[2]
	firstSentence = False
	secondSentence = False
	fileName1 = 'undefined1'
	fileName2 = 'undefined2'
	if files[0] != "ferret_result.txt":
		fileName1 = files[0]
		with open('splitted_files/'+directory+'/'+files[0], 'r') as myfile:
			firstSentence = myfile.read().replace('\n', '')
	if files[1] != "ferret_result.txt":
		fileName2 = files[1]
		with open('splitted_files/'+directory+'/'+files[1], 'r') as myfile:
			secondSentence = myfile.read().replace('\n', '')
	if firstSentence == False:
		fileName1 = files[2]
		with open('splitted_files/' + directory + '/' + files[2], 'r') as myfile:
			firstSentence = myfile.read().replace('\n', '')
	if secondSentence == False:
		fileName2 = files[2]
		with open('splitted_files/' + directory + '/' + files[2], 'r') as myfile:
			secondSentence = myfile.read().replace('\n', '')

	finalWordsFirstSentence = pre.get_words_for_sentence(firstSentence)
	finalWordsSecondSentence = pre.get_words_for_sentence(secondSentence)

	uniqueWordsFirstSentence = pre.get_unique_words(finalWordsFirstSentence, finalWordsSecondSentence)
	maxSimilaritiesFirstSentence = pre.get_similarities(uniqueWordsFirstSentence, firstSentence, finalWordsSecondSentence, secondSentence)
	(finalWordsFirstSentence, finalWordsSecondSentence) = pre.get_words_after_replacements(maxSimilaritiesFirstSentence, finalWordsFirstSentence, finalWordsSecondSentence)

	uniqueWordsSecondSentence = pre.get_unique_words(finalWordsSecondSentence, finalWordsFirstSentence)
	maxSimilaritiesSecondSentence = pre.get_similarities(uniqueWordsSecondSentence, secondSentence, finalWordsFirstSentence, firstSentence)
	(finalWordsSecondSentence, finalWordsFirstSentence) = pre.get_words_after_replacements(maxSimilaritiesSecondSentence, finalWordsSecondSentence, finalWordsFirstSentence)

	os.makedirs(parsedDirectoryName+'/'+directory)

	target1 = open(parsedDirectoryName+'/'+directory+'/'+fileName1, 'w')
	target1.truncate()
	target1.write(" ".join(word.encode('utf8') for word, pos in finalWordsFirstSentence))
	target1.close()

	target2 = open(parsedDirectoryName+'/'+directory+'/'+fileName2, 'w')
	target2.truncate()
	target2.write(" ".join(word.encode('utf8') for word, pos in finalWordsSecondSentence))
	target2.close()    
