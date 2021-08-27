from os import stat


# Pretty Error Messenger

class Error:
	
	@staticmethod
	def pretty_error(filename, source, line, column, message):
		space = " " * ((len(str(line)) + 2) + column)

		print(
f"""
In file <{filename}> at line {line}, column {column}

{line}| {source}
{space}^-- Here

{message}
""")

	@staticmethod
	def error(filename, source, line, message):
		# this function is for runtime errors
		print(
f"""
In file <{filename}> at line {line}

{line}| {source}

{message}
""")