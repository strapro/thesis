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