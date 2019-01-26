#! /usr/bin/python

import re

from Matcher import Matcher
from Action import Action
from Filter import Filter
from Helpers import handleParseError, goToFailure

class Parser():
	def __init__(self):
		self.matchers = {}
		self.actions = {}
		self.filters = []
		
	def parseVariable(self, keyword, value, line, lineNumber):
		if value[0] != '=':
			handleParseError(lineNumber, line, 
			                 "Assignment operator '=' not found.")
		value = value[1:].lstrip()
		if value[0] == '{':
			if value[-1] == '}':
				self.matchers[keyword] = Matcher(value, line, lineNumber)
			else:
				handleParseError(lineNumber, line, "failed to find closing }")
		elif value[0] == '[':
			if value[-1] == ']':
				self.actions[keyword] = Action(value, line, lineNumber)
			else:
				handleParseError(lineNumber, line, "failed to find closing ]")
		else:
			handleParseError(lineNumber, line, "failed to find opening brace ({ or [)")

	def parseStatement(self, statement, lineNumber):
		# filter out the 'if; from the start
		tmp = statement[3:].split('->')
		if len(tmp) != 2:
			handleParseError(lineNumber, statement, "Missing '->'.")
		condition = tmp[0].lstrip().rstrip()
		result = tmp[1].lstrip().rstrip()
		if condition in self.matchers:
			condition = self.matchers[condition]
		else:
			condition = Matcher(condition, statement, lineNumber)
		if result in self.actions:
			result = self.actions[result]
		else:
			result = Action(result, statement, lineNumber)
		filter = Filter(condition, result)
		self.filters.append(filter)
	
	def parse(self, fileContents):
		lines = fileContents.split('\n')
		for lineNumber, line in enumerate(lines):
			if not len(line) or line[0] == '#':
			#skip over empty lines and comments,
				continue
			keyword = re.search(r'[a-zA-Z0-9]+', line)
			if keyword is None:
				handleParseError(lineNumber, line, "Can't find opening valid token")
			keyword = keyword.group(0)
			if keyword == 'if':
				self.parseStatement(line, lineNumber)
				continue
			else:
				self.parseVariable(keyword, line[len(keyword):].lstrip(), line, lineNumber)
				continue
		return self.filters
		
