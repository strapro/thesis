import os
from sys import stdout


def execute_ferret(target_directory, force_overwrite=True, verbosity='silent'):
	if verbosity != 'silent':
		stdout.write("Executing ferret. Please wait.\n")

	command = 'ferret/src/ferret'

	i = 0
	directories = next(os.walk(target_directory))[1]
	for directory in directories:
		i += 1
		if verbosity != 'silent':
			stdout.write("\r"+str(i)+'/'+str(len(directories)))
			stdout.flush()

		if force_overwrite is True or os.path.exists(target_directory+"/"+directory+"/ferret_result.txt") is False:
			files = next(os.walk(target_directory + '/' + directory))[2]
			command_with_files = command + " " + target_directory + "/" + directory + "/" + files[0] + " " + target_directory + "/" + directory + "/" + files[1]
			command_with_redirects = command_with_files + " > " + target_directory + "/" + directory + "/ferret_result.txt" + " 2> /dev/null"
			os.system(command_with_redirects)

	if verbosity != 'silent':
		stdout.write("\n")


def execute_single_ferret(target_directory):
	command = 'ferret/src/ferret'
	files = next(os.walk(target_directory))[2]
	command_with_files = command + " " + target_directory + "/" + files[0] + " " + target_directory + "/" + files[1]
	command_with_redirects = command_with_files + " > " + target_directory + "/ferret_result.txt" + " 2> /dev/null"
	os.system(command_with_redirects)