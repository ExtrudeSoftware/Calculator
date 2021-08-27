"""
calculator.py

Main file for calculator project
"""

import token
from tokentype import TokenTypes
from tokenizer import Tokenizer
from parser_ import Parser
from astprinter import AstPrinter
from interpreter import Interpreter

from sys import argv, exit as sys_exit
from os import system
from platform import system as os_type

print_tokens = False
print_ast = False

def parse_argv():
	global print_tokens, print_ast

	for arg in argv:
		if arg in ("-t", "--tokens"):
			print_tokens = True

		elif arg in ("-a", "--ast"):
			print_ast = True

def prompt_commands(command):
	# prompt commands doesn't get parser, tokenized, interpreted
	if command == "help":
		print(
"""
Commands

help			shows this page
exit			exits from program
clear			clears prompt
""")

	elif command == "exit":
		sys_exit(0)
	
	elif command == "clear":
		if os_type() == "Windows":
			system("cls")
		
		else:
			system("clear")
	
	else:
		return False # command not found
	
	return True # command executed

def main():
	parse_argv()

	print("Calculator v0.0.1\nType \"help\" for more information.")

	try:
		while True:
			i = input("> ")

			if not i:
				continue

			if prompt_commands(i.strip()):
				continue

			""" Tokenizing """
			
			tokenizer = Tokenizer("stdin", i)
			tokens = tokenizer.getTokens()

			if tokenizer.hadError:
				continue
			
			if tokens and print_tokens:
				for token in tokens:
					print(token)
				
				print()

			""" Parsing """
			
			parser = Parser("stdin", i, tokens)
			ast = parser.parse()

			if parser.hadError:
				continue

			if ast and print_ast:
				AstPrinter().pretty_print(ast)

			""" Evaluating """
			
			interpreter = Interpreter("stdin", i, ast)
			result = interpreter.interpret()

			if interpreter.hadError:
				continue

			if result == 0 or result:
				print(result)
	
	except KeyboardInterrupt:
		sys_exit(0)

if __name__ == "__main__":
	main()