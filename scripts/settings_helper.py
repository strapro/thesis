def settings_to_directory(settings):
	directory_name_parts = []
	for key, value in settings.iteritems():
		if type(value) == list:
			value_string = "".join(str(item) for item in value)
		else:
			value_string = str(value)
		directory_name_parts.append(key + "=" + value_string)

	return "splitted_parsed_files/" + "_".join(str(part) for part in directory_name_parts)
