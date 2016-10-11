array_value_separator = ".."
setting_value_separator = "..."
setting_separator = "...."


def settings_to_directory(settings):
	global array_value_separator, setting_value_separator, setting_separator

	directory_name_parts = []
	for key, value in settings.iteritems():
		if type(value) == list:
			value_string = array_value_separator.join(str(item) for item in value)
		else:
			value_string = str(value)
		directory_name_parts.append(key + setting_value_separator + value_string)

	return setting_separator.join(str(part) for part in directory_name_parts)


def directory_to_settings(directory_name):
	global array_value_separator, setting_value_separator, setting_separator

	result = {}
	settings = directory_name.split(setting_separator)
	for setting in settings:
		setting_name, setting_value = setting.split(setting_value_separator)
		if setting_value.find(array_value_separator) != -1:
			setting_value = setting_value.split(array_value_separator)
			setting_value = ','.join(setting_value)
		result[setting_name] = setting_value

	return result
