import string
import random
import itertools
import nltk

class PreProcessor:

	__settings = {}

	def __init__(self, settings):
		self.__settings = settings

	#This function returns a subset of the original words of the sentence accompanied by the corresponding part of speech tag
	def get_words_for_sentence(self, sentence):
		#Tokenize the text
		tokenizedText = nltk.word_tokenize(sentence)

		#Use part of speech tagger. We don't want to remove the stop words at this point in order to provide the tagger with all the relevant context
		tags = nltk.pos_tag(tokenizedText)

		#TODO At this step we should consider whether a reordering should happen. This place would be good for a sophisticated re ordering taking into account the grammar tree

		#Remove stopwords we do not need them for the rest of this procedure
		if self.__settings['remove_stop_words']:
			filteredTags = [(word, tag) for word, tag in tags if word not in nltk.corpus.stopwords.words('english')]
		else:
			filteredTags = tags

		#Keep the simple tag representation
		simplifiedTags = [(word, nltk.tag.map_tag('en-ptb', 'universal', tag)) for word, tag in filteredTags]

		#Keep only certain parts of speech	
		simplifiedSubSetTags = [(word, tag) for word, tag in simplifiedTags if tag in self.__settings['permitted_tags'] ]

		#Lemmatize words 
		lemmatiser = nltk.stem.WordNetLemmatizer()
		lemmatizedSubSetTags = [(lemmatiser.lemmatize(word, pos=self.__get_wordnet_pos(tag)), tag) for word, tag in simplifiedSubSetTags ]

		#At this step we should consider whether a reordering should happen. This place would be good for a simple alphanumeric sorting
		if self.__settings['perform_ordering']:
			sortedLemmatizedSubSetTags = [(str(word.lower()), tag) for word, tag in lemmatizedSubSetTags]
			sortedLemmatizedSubSetTags = list(set(sortedLemmatizedSubSetTags)) #TODO whether only the unique words should be kept should also be a setting
			sortedLemmatizedSubSetTags.sort(key=lambda tup: tup[0])

			return sortedLemmatizedSubSetTags
		else:
			return lemmatizedSubSetTags	

	#This function returns the words that are present in one sentence but not in the other
	def get_unique_words(self, tagsPerSentence1, tagsPerSentence2):
		uniqueWordsPerSentence = list(set(tagsPerSentence1) - set(tagsPerSentence2))
		
		return uniqueWordsPerSentence
	
	#This function return the similarity between the unique words of one sentence and all the words of the other sentence. Only the maximum similarity for each pair will be returned
	def get_similarities(self, uniqueWords, uniqueWordsSentence, allWords, allWordsSentence):
		maxSimilarities = []
		for word1, tag1 in uniqueWords:
			syns1 = self.__get_synset(uniqueWordsSentence, word1, tag1)
			sims = []
			for word2, tag2 in allWords:
				#We want to examine the similarity only for similar parts of speech
				if tag1 == tag2:
					syns2 = self.__get_synset(allWordsSentence, word2, tag2)
					for sense1, sense2 in itertools.product(syns1, syns2):
						#There is a chance that we do not have a synset for a word at all
						if sense1 and sense2:
							d = self.__get_similarity(sense1, sense2)
							#There is a chance that there is no similarity at all
							if d > 0.0:			
								sims.append((d, sense1, sense2, word1, word2))

			#Sims at this point holds the similarity of every word in the other sentence to a single unique word of the first sentence
			if sims:
				#Keep only the most similar word pair
				maxSimilarity = max(sims, key=lambda item:item[0])
				maxSimilarities.append((word1, maxSimilarity[4], maxSimilarity[0], maxSimilarity[1], maxSimilarity[2]))

		return maxSimilarities

	#This function returns the words after the necessary replacements have taken place
	def get_words_after_replacements(self, maxSimilarities, uniqueWordsFinalWordsSentence, allWordsFinalWordsSentence):
		for uniqueWord, word, similarity, uniqueWordSynset, wordSynset in maxSimilarities:
			if similarity > self.__settings['similaty_threshold']:
				replacement = self.__get_replacement_word(uniqueWord, word, uniqueWordSynset, wordSynset)
				uniqueWordsFinalWordsSentence = self.__replace_word(uniqueWord, replacement, uniqueWordsFinalWordsSentence)
				allWordsFinalWordsSentence = self.__replace_word(word, replacement, allWordsFinalWordsSentence)

		if self.__settings['perform_ordering']:
			uniqueWordsFinalWordsSentence.sort(key=lambda tup: tup[0])
			allWordsFinalWordsSentence.sort(key=lambda tup: tup[0])

		return (uniqueWordsFinalWordsSentence, allWordsFinalWordsSentence)

	#========================================================================================================================================

	#This function maps the simple tags to the relevant wordnet part of speech tag, in order to use the lemmatiser
	def __get_wordnet_pos(self, tag):
	    if tag.startswith('V'):
	        return nltk.corpus.wordnet.VERB
	    elif tag.startswith('N'):
	        return nltk.corpus.wordnet.NOUN
	    elif tag.startswith('ADV'):
	        return nltk.corpus.wordnet.ADV
	    else:
	        return nltk.corpus.wordnet.NOUN

	#This function returns all the synsets for a word that are the same part of speech as that tag
	def __get_synset(self, sentence, word, tag):
		#At this step we should consider whether word sense disambiguation should take place
		if self.__settings["use_word_sense"]:
			syns = [nltk.wsd.lesk(sentence, word, pos=self.__get_wordnet_pos(tag))]	
		else:
			syns = nltk.corpus.wordnet.synsets(word, pos=self.__get_wordnet_pos(tag))	

		return syns

	#This function returns the similarity betweeen twn senses
	def __get_similarity(self, sense1, sense2):
		#Possible values are "jcn", "lin", "res", "lch", "path", "wup"
		if self.__settings["similarity_measure"] == 'jcn':
			d = nltk.corpus.wordnet.jcn_similarity(sense1, sense2, nltk.corpus.wordnet_ic.ic('ic-brown.dat'))
		elif self.__settings["similarity_measure"] == 'lin':
			d = nltk.corpus.wordnet.lin_similarity(sense1, sense2, nltk.corpus.wordnet_ic.ic('ic-brown.dat'))
		elif self.__settings["similarity_measure"] == 'res':
			d = nltk.corpus.wordnet.res_similarity(sense1, sense2, nltk.corpus.wordnet_ic.ic('ic-brown.dat'))
		elif self.__settings["similarity_measure"] == 'lch':
			d = nltk.corpus.wordnet.lch_similarity(sense1, sense2)
		elif self.__settings["similarity_measure"] == 'path':
			d =nltk.corpus.wordnet.path_similarity(sense1, sense2)
		elif self.__settings["similarity_measure"] == 'wup':
			d = nltk.corpus.wordnet.wup_similarity(sense1, sense2)

		return d

	def __get_replacement_word(self, uniqueWord, word, uniqueWordSynset, wordSynset):
		#Possible values are "random", "keep_unique", "keep_other" TODO use something more sophisticated like common hypernym
		if self.__settings["type_of_replacement"] == 'random':
			replacement = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
		elif self.__settings["type_of_replacement"] == 'keep_unique':
			replacement = uniqueWord
		elif self.__settings["type_of_replacement"] == 'keep_other':
			replacement = word

		return replacement

	#This function replaces all occurences of a word in a list of tuples
	def __replace_word(self, oldWord, newWord, listOfWords):
		out = [(newWord, tpl[1]) if tpl[0] == oldWord else tpl for tpl in listOfWords]
		
		return out
