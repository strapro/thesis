import os
from sys import stdout


def execute_ferret(target_directory, force_overwrite=True, verbosity='silent', progress_bar=None):
	if verbosity != 'silent':
		stdout.write("Executing ferret. Please wait.\n")

	command = 'ferret/src/ferret'

	if progress_bar is not None:
		progress_bar.set_text("Executing ferret")
		progress_bar.set_fraction(0)

	i = 0
	directories = next(os.walk(target_directory))[1]
	directories_len = len(directories)
	for directory in directories:
		i += 1
		if verbosity != 'silent':
			stdout.write("\r"+str(i)+'/'+str(directories_len))
			stdout.flush()

		if progress_bar is not None:
			progress_bar.pulse()
			fraction = i/float(directories_len)
			progress_bar.set_fraction(fraction)

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