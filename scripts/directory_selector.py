import os


def select_directory():
	original_or_parse = raw_input("Do you want to check the [o]riginal or the [p]arsed files?")

	if original_or_parse == 'o':
		target_directory = 'splitted_files'
	else:
		target_directory_candidates = []
		i = 0
		for parsedDirectory in next(os.walk('splitted_parsed_files'))[1]:
			print "["+str(i)+"] "+parsedDirectory
			i += 1
			target_directory_candidates.append(parsedDirectory)
		target_directory_candidate_index = raw_input("Which parsed files?")
		target_directory = 'splitted_parsed_files/'+target_directory_candidates[int(target_directory_candidate_index)]

	return target_directory
