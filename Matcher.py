#! /usr/bin/python

import re

from Helpers import handleParseError

class Matcher:
	def __init__(self, content, line, lineNumber):
		self.line = line
		self.lineNumber = lineNumber
		self.from_ = None
		self.to_ = None
		self.subject_ = None
		self.contains_ = None
		self.notContains_ = None
		self.hasAttachment_ = None # Not supported yet
		self.excludeChats_ = None # Not supported yet
		
		if content[0]!='{' or content[-1] != '}':
			assert(0), "Matcher should have enclosing {} checked by caller."
		# TODO should check for non escaped commas
		content = content[1:-1].split(',')
		content = [ each.lstrip() for each in content]
		self.input=content
		self.compile()
		
	def __str__(self):
		return self.__repr__()
		
	def __repr__(self):
		str = "Matcher:"
		if self.from_:
			str += " from '%s'" % self.from_  
		if self.to_:
			str += " to '%s'" % self.to_  
		if self.subject_:
			str += " with subject '%s'" % self.subject_  
		if self.contains_:
			str += " containing '%s'" % self.hasWord_  
		if self.notContains_:
			str += " not containing '%s'" % self.hasWord_  
		return str
		
	def handleParseError(self, error):
		handleParseError(self.lineNumber, self.line, error)
		
	def fromIs(self, str):
		if self.from_ is None:
			self.from_ = str
		else:
			self.handleParseError("Can only set 'from' once per Matcher.")
			
	def toIs(self, str):
		if self.to_ is None:
			self.to_ = str
		else:
			self.handleParseError("Can only set 'to' once per Matcher.")
		
	def subjectIs(self, str):
		if self.subject_ is None:
			self.subject_ = str
		else:
			print self.handleParseError("Can only set'subject' once per Matcher.")
		
	def containsIs(self, str):
		if self.contains_ is None:
			self.contains_ = str
		else:
			print self.handleParseError("Can only set 'contain' once per Matcher.")
	
	def notContainsIs(self, str):
		if self.notContains_ is None:
			self.notContains_ = str
		else:
			print self.handleParseError("Can only set 'notContain' once per Matcher.")	
		
	def compile(self):
		for each in self.input:
			x = re.match(r'([a-zA-Z0-9]+) "(.+)"', each)
			if x is None:
				self.handleParseError("Failed to find pattern 'token \"Matcher\"' in '{}'.".format(each))
			token = x.group(1)
			matcher = x.group(2)
			
			if token == "from":
				self.fromIs(matcher)
				continue
			if token == "to":
				self.toIs(matcher)
				continue
			if token == "subject":
				self.subjectIs(matcher)
				continue
			if token == "contains":
				self.containsIs(matcher)
				continue
				
			if token == "notContains":
				self.containsIs(matcher)
				continue
			
			self.handleParseError("unrecognised token '{}'".format(token))
			
		
	def assemble(self):
		lines = []
		if self.from_ is not None:
			lines.append(("from", self.from_))
		if self.to_ is not None:
			lines.append(("to", self.to_))
		if self.subject_ is not None:
			lines.append(("subject", self.subject_))
		if self.contains_ is not None:
			lines.append(("hasTheWord", self.contains_))
		if self.hasAttachment_ is not None:
			lines.append(("hasAttachment", self.hasAttachment_))
		if self.excludeChats_ is not None:
			lines.append(("excludeChats", self.excludeChats_))
		return lines
