import os
import string
import random
import itertools
import nltk
import shutil
from sys import stdout

class PreProcessor:
	__settings = {}

	def __init__(self, settings):
		self.__settings = settings

	# This does all the work
	def pre_process(self, first_sentence, second_sentence):
		final_words_first_sentence = self.__get_words_for_sentence(first_sentence)
		final_words_second_sentence = self.__get_words_for_sentence(second_sentence)

		unique_words_first_sentence = self.__get_unique_words(final_words_first_sentence, final_words_second_sentence)
		max_similarities_first_sentence = self.__get_similarities(
			unique_words_first_sentence,
			first_sentence,
			final_words_second_sentence,
			second_sentence
		)
		(final_words_first_sentence, final_words_second_sentence) = self.__get_words_after_replacements(
			max_similarities_first_sentence,
			final_words_first_sentence,
			final_words_second_sentence
		)

		unique_words_second_sentence = self.__get_unique_words(final_words_second_sentence, final_words_first_sentence)
		max_similarities_second_sentence = self.__get_similarities(
			unique_words_second_sentence,
			second_sentence,
			final_words_first_sentence,
			first_sentence
		)
		(final_words_second_sentence, final_words_first_sentence) = self.__get_words_after_replacements(
			max_similarities_second_sentence,
			final_words_second_sentence,
			final_words_first_sentence
		)

		return final_words_second_sentence, final_words_first_sentence

	# ==================================================================================================================

	# This function returns a subset of the original words of the sentence
	# accompanied by the corresponding part of speech tag. The words are also lemmatized
	def __get_words_for_sentence(self, sentence):
		# Tokenize the text
		tokenized_text = nltk.word_tokenize(sentence)

		# Use part of speech tagger. We don't want to remove the stop words at this point
		# in order to provide the tagger with all the relevant context
		tags = nltk.pos_tag(tokenized_text)

		# Remove stopwords we do not need them for the rest of this procedure
		if self.__settings['remove_stop_words']:
			filtered_tags = [(word, tag) for word, tag in tags if word not in nltk.corpus.stopwords.words('english')]
		else:
			filtered_tags = tags

		# Keep the simple tag representation
		filtered_tags = [(word.decode('utf-8'), nltk.tag.map_tag('en-ptb', 'universal', tag)) for word, tag in filtered_tags]

		# Keep only certain parts of speech
		sub_set_tags = [(word, tag) for word, tag in filtered_tags if tag in self.__settings['permitted_tags']]

		# Lemmatize words
		lemmatizer = nltk.stem.WordNetLemmatizer()
		lemmatized_tags = [(lemmatizer.lemmatize(word, pos=self.__get_wordnet_pos(tag)), tag) for word, tag in sub_set_tags]
		lemmatized_tags = [(word.lower(), tag) for word, tag in lemmatized_tags]

		return lemmatized_tags

	# This function returns the words that are present in one sentence but not in the other
	def __get_unique_words(self, tags_per_sentence1, tags_per_sentence2):
		unique_words_per_sentence = list(set(tags_per_sentence1) - set(tags_per_sentence2))

		return unique_words_per_sentence

	# This function return the similarity between the unique words of one sentence and
	# all the words of the other sentence. Only the maximum similarity for each pair will be returned
	def __get_similarities(self, unique_words, unique_words_sentence, all_words, all_words_sentence):
		max_similarities = []
		for word1, tag1 in unique_words:
			syns_1 = self.__get_synset(unique_words_sentence, word1, tag1)
			sims = []
			for word2, tag2 in all_words:
				# We want to examine the similarity only for similar parts of speech
				if tag1 == tag2:
					syns_2 = self.__get_synset(all_words_sentence, word2, tag2)
					for sense1, sense2 in itertools.product(syns_1, syns_2):
						# There is a chance that we do not have a synset for a word at all
						if sense1 and sense2:
							d = self.__get_similarity(sense1, sense2)
							# There is a chance that there is no similarity at all
							if d > 0.0:
								sims.append((d, sense1, sense2, word1, word2))

			# Sims at this point holds the similarity of every word in the other sentence
			# to a single unique word of the first sentence
			if sims:
				# Keep only the most similar word pair
				max_similarity = max(sims, key=lambda item: item[0])
				max_similarities.append((word1, max_similarity[4], max_similarity[0], max_similarity[1], max_similarity[2]))

		return max_similarities

	# This function returns the words after the necessary replacements have taken place
	def __get_words_after_replacements(self, max_similarities, first_sentence, second_sentence):
		for uniqueWord, word, similarity, uniqueWordSynset, wordSynset in max_similarities:
			if similarity > self.__settings['similarity_threshold']:
				replacement = self.__get_replacement_word(uniqueWord, word, uniqueWordSynset, wordSynset)
				first_sentence = self.__replace_word(uniqueWord, replacement, first_sentence)
				second_sentence = self.__replace_word(word, replacement, second_sentence)

		# TODO At this step we should consider whether a reordering should happen.
		# This place would be good for a sophisticated re ordering taking into account the grammar tree
		if self.__settings['perform_ordering']:
			first_sentence.sort(key=lambda tup: tup[0])
			second_sentence.sort(key=lambda tup: tup[0])

		return first_sentence, second_sentence

	# This function maps the simple tags to the relevant wordnet part of speech tag, in order to use the lemmatizer
	def __get_wordnet_pos(self, tag):
		if tag.startswith('V'):
			return nltk.corpus.wordnet.VERB
		elif tag.startswith('N'):
			return nltk.corpus.wordnet.NOUN
		elif tag.startswith('ADV'):
			return nltk.corpus.wordnet.ADV
		else:
			return nltk.corpus.wordnet.NOUN

	# This function returns all the synsets for a word that are the same part of speech as that tag
	def __get_synset(self, sentence, word, tag):
		# At this step we should consider whether word sense disambiguation should take place
		if self.__settings["use_word_sense"]:
			syns = [nltk.wsd.lesk(sentence, word, pos=self.__get_wordnet_pos(tag))]
		else:
			syns = nltk.corpus.wordnet.synsets(word, pos=self.__get_wordnet_pos(tag))

		return syns

	# This function returns the similarity between twn senses
	def __get_similarity(self, sense1, sense2):
		# Possible values are "jcn", "lin", "res", "lch", "path", "wup"
		if self.__settings["similarity_measure"] == 'jcn':
			d = nltk.corpus.wordnet.jcn_similarity(sense1, sense2, nltk.corpus.wordnet_ic.ic('ic-brown.dat'))
		elif self.__settings["similarity_measure"] == 'lin':
			d = nltk.corpus.wordnet.lin_similarity(sense1, sense2, nltk.corpus.wordnet_ic.ic('ic-brown.dat'))
		elif self.__settings["similarity_measure"] == 'res':
			d = nltk.corpus.wordnet.res_similarity(sense1, sense2, nltk.corpus.wordnet_ic.ic('ic-brown.dat'))
		elif self.__settings["similarity_measure"] == 'lch':
			d = nltk.corpus.wordnet.lch_similarity(sense1, sense2)
		elif self.__settings["similarity_measure"] == 'path':
			d = nltk.corpus.wordnet.path_similarity(sense1, sense2)
		elif self.__settings["similarity_measure"] == 'wup':
			d = nltk.corpus.wordnet.wup_similarity(sense1, sense2)
		else:
			raise Exception('Unknown similarity measure')

		return d

	def __get_replacement_word(self, unique_word, word, unique_word_synset, word_synset):
		# Possible values are "random", "keep_unique", "keep_other"
		# TODO use something more sophisticated like common hypernym
		if self.__settings["type_of_replacement"] == 'random':
			replacement = ''.join(
				random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
		elif self.__settings["type_of_replacement"] == 'keep_unique':
			replacement = unique_word
		elif self.__settings["type_of_replacement"] == 'keep_other':
			replacement = word
		else:
			raise Exception('Unknown replacement type')

		return replacement

	# This function replaces all occurrences of a word in a list of tuples
	def __replace_word(self, old_word, new_word, list_of_words):
		out = [(new_word, tpl[1]) if tpl[0] == old_word else tpl for tpl in list_of_words]

		return out


def pre_process_corpus(settings, parsed_directory_name, verbosity='silent'):
	if verbosity != 'silent':
		stdout.write("Executing pre processing. Please wait\n")

	if os.path.exists(parsed_directory_name):
		shutil.rmtree(parsed_directory_name, ignore_errors=True)

	os.makedirs(parsed_directory_name)

	i = 0
	directories = next(os.walk('splitted_files'))[1]
	for directory in directories:
		i += 1
		if verbosity != 'silent':
			stdout.write("\r" + str(i) + '/' + str(len(directories)))
			stdout.flush()

		files = next(os.walk('splitted_files/'+directory))[2]
		first_sentence = False
		second_sentence = False
		file_name1 = 'undefined1'
		file_name2 = 'undefined2'
		if files[0] != "ferret_result.txt":
			file_name1 = files[0]
			with open('splitted_files/'+directory+'/'+files[0], 'r') as my_file:
				first_sentence = my_file.read().replace('\n', '')
		if files[1] != "ferret_result.txt":
			file_name2 = files[1]
			with open('splitted_files/'+directory+'/'+files[1], 'r') as my_file:
				second_sentence = my_file.read().replace('\n', '')
		if first_sentence is False:
			file_name1 = files[2]
			with open('splitted_files/' + directory + '/' + files[2], 'r') as my_file:
				first_sentence = my_file.read().replace('\n', '')
		if second_sentence is False:
			file_name2 = files[2]
			with open('splitted_files/' + directory + '/' + files[2], 'r') as my_file:
				second_sentence = my_file.read().replace('\n', '')

		pre_processor = PreProcessor(settings)
		(final_words_first_sentence, final_words_second_sentence) = pre_processor.pre_process(first_sentence, second_sentence)

		os.makedirs(parsed_directory_name+'/'+directory)

		target1 = open(parsed_directory_name+'/'+directory+'/'+file_name1, 'w')
		target1.truncate()
		target1.write(" ".join(word.encode('utf8') for word, pos in final_words_first_sentence))
		target1.close()

		target2 = open(parsed_directory_name+'/'+directory+'/'+file_name2, 'w')
		target2.truncate()
		target2.write(" ".join(word.encode('utf8') for word, pos in final_words_second_sentence))
		target2.close()

	if verbosity != 'silent':
		stdout.write("\n")