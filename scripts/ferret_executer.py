import multiprocessing
import os
from sys import stdout


my_progress_bar = None


def execute_command(command, i, directories_len, verbosity):
	os.system(command)
	return i, directories_len, verbosity


def log_ferret_result(result):
	(i, directories_len, verbosity) = result
	if verbosity != 'silent':
		stdout.write("\r" + str(i) + '/' + str(directories_len))
		stdout.flush()

	global my_progress_bar

	if my_progress_bar is not None:
		my_progress_bar.pulse()
		fraction = 1 / float(directories_len)
		new_fraction = my_progress_bar.get_fraction() + fraction
		if new_fraction <= 1:
			my_progress_bar.set_fraction(new_fraction)


def execute_ferret(target_directory, force_overwrite=True, verbosity='silent', progress_bar=None):
	global my_progress_bar

	my_progress_bar = progress_bar

	p = multiprocessing.Pool(4)
	if verbosity != 'silent':
		stdout.write("Executing ferret. Please wait.\n")

	command = '/bin/ferret'

	if progress_bar is not None:
		progress_bar.set_text("Executing ferret")
		progress_bar.set_fraction(0)

	i = 0
	directories = next(os.walk(target_directory))[1]
	directories_len = len(directories)
	for directory in directories:
		i += 1

		if force_overwrite is True or os.path.exists(target_directory+"/"+directory+"/ferret_result.txt") is False:
			files = next(os.walk(target_directory + '/' + directory))[2]
			command_with_files = command + " " + target_directory + "/" + directory + "/" + files[0] + " " + target_directory + "/" + directory + "/" + files[1]
			command_with_redirects = command_with_files + " > " + target_directory + "/" + directory + "/ferret_result.txt" + " 2> /dev/null"
			p.apply_async(execute_command, args=(command_with_redirects, i, directories_len, verbosity, ), callback=log_ferret_result)

	p.close()
	p.join()

	if verbosity != 'silent':
		stdout.write("\n")


def execute_single_ferret(target_directory):
	command = 'bin/ferret'
	files = next(os.walk(target_directory))[2]
	command_with_files = command + " " + target_directory + "/" + files[0] + " " + target_directory + "/" + files[1]
	command_with_redirects = command_with_files + " > " + target_directory + "/ferret_result.txt" + " 2> /dev/null"
	os.system(command_with_redirects)