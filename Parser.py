#! /usr/bin/python

import re

from Matcher import Matcher
from Action import Action
from Filter import Filter
from Helpers import handleParseError, goToFailure

class Parser():
	'''
	Takes in the contents of a file and parses it, checking for syntax errors and creating
	the specified variables, Actions and Matchers, and creating the Filter tree specified 
	using	these.
	'''
	def __init__(self):
		self.matchers = {}
		self.actions = {}
		self.filters = []
		
		
	def parseVariable(self, keyword, value, line, lineNumber):
		'''Parses variable lines. eg x = [|{ content }|]'''
		if value[0] != '=':
			return handleParseError(lineNumber, line, 
			                 "Assignment operator '=' not found.")
		value = value[1:].lstrip().rstrip()
		if value[0] == '{':
			if value[-1] == '}':
				self.matchers[keyword] = Matcher(value, line, lineNumber)
			else:
				return handleParseError(lineNumber, line, "failed to find closing }")
		elif value[0] == '[':
			if value[-1] == ']':
				self.actions[keyword] = Action(value, line, lineNumber)
			else:
				return handleParseError(lineNumber, line, "failed to find closing ]")
		else:
			return handleParseError(lineNumber, line, "failed to find opening brace: { or [")


	def parseStatement(self, statement, lineNumber, indentation):
		'''
		Parses statement lines. eg if matcher -> action. Also tracks indentation to create
		nested statements.
		'''
		# filter out the 'if; from the start
		tmp = statement[3:].split('->')
		if len(tmp) != 2:
			return handleParseError(lineNumber, statement, "Missing '->'.")
		
		condition = tmp[0].lstrip().rstrip()
		result = tmp[1].lstrip().rstrip()
		
		if not condition:
			return handleParseError(lineNumber, statement, "Missing Matcher before ->.")
		if condition in self.matchers:
			condition = self.matchers[condition]
		elif condition[0] == '{' and condition[-1] == '}':
			condition = Matcher(condition, statement, lineNumber)
		else:
			return handleParseError(lineNumber, statement, "Unknown Matcher or missing {} before ->.")
		
		# need to handle there not being a specified result	
		if not result:
			filter = Filter(condition)
		else:
			if result in self.actions:
				result = self.actions[result]
			elif result[0] == '[' and result[-1] == ']':
				result = Action(result, statement, lineNumber)
			else:
				return handleParseError(lineNumber, statement, "Unknown Action or missing [] after ->.")
			filter = Filter(condition, result)
		
		if indentation == 0:
			self.filters.append(filter)
			return
		
		if not self.filters:
			return handleParseError(lineNumber, statement, "Invalid indentation, this line has no parent")
		
		parentFilter = self.filters[-1]
		indentation -= 1
		
		while (indentation > 0):
			if not parentFilter.childStatements:
				handleParseError(lineNumber, statement, "Invalid indentation, this line has no parent")
			parentFilter = parentFilter.childStatements[-1]
			indentation -= 1
		parentFilter.addChild(filter)
	
	def parse(self, fileContents):
		'''
		Main parsing function that splits file into lines and checks if they're variables
		or statements. Keeps track of indentation. Note that variables and statements must
		be on a single line.
		'''
		lines = fileContents.split('\n')
		for lineNumber, line in enumerate(lines):
			lineNumber += 1 # since it starts at 0
			tmp = line.lstrip()
			if not len(tmp) or tmp[0] == '#':
			# skip over empty lines and comments,
				continue
			# get indentation
			indentation = line.count('\t')
			line = line.lstrip()
			indentation -= line.count('\t')
			
			keyword = re.search(r'^[a-zA-Z0-9]+', line)
			if keyword is None:
				handleParseError(lineNumber, line, "Can't find opening valid token")
				continue
			keyword = keyword.group(0)
			if keyword == 'if':
				self.parseStatement(line, lineNumber, indentation)
			else:
				if indentation > 0:
					handleParseError(lineNumber, line, "Variables shouldn't be indented")
					continue
				self.parseVariable(keyword, line[len(keyword):].lstrip(), line, lineNumber)
				continue
		return self.filters
		
