#! /usr/bin/python

import re

from Helpers import handleParseError

class Matcher:
	'''
	Class to represent the possible matching criteria a filter can posses. It is responsible
	for parsing the contents between {} to compile its attributes, merging with other 
	Matchers and values for the XML representation of itself.
	'''
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
		
	def merge(self, other):
		'''Merge the matching criteria of this Matcher with another, using OR/AND operators'''
		if not other:
			assert 0
			
		if other.from_: # This probably doesn't make sense in the syntax
			if self.from_:
				self.from_ += " || " + other.from_
			else:
				self.from_ = other.from_
				
		if other.to_:
			if self.to_:
				self.to_ += " & " + other.to_
			else:
				self.to_ = other.to_
				
		if other.subject_:
			if self.subject_:
				self.subject_ += " & " + other.subject_
			else:
				self.subject_ = other.subject_
			
		if other.contains_:
			if self.contains_:
				self.contains_ += " & " + other.contains_
			else:
				self.contains_ = other.contains_
				
		if other.notContains_:
			if self.notContains_:
				self.notContains_ += " & " + other.notContains_
			else:
				self.notContains_ = other.notContains_
				
		if other.hasAttachment_:
			self.hasAttachment_ = other.hasAttachment_
			
		if other.excludeChats_:
			self.excludeChats_ = other.excludeChats_

	def handleParseError(self, error):
		handleParseError(self.lineNumber, self.line, error)
		
	def set(self, attr, str):
		'''Generic setter for criteria only allowing them to be set once.'''
		if getattr(self, attr + '_') is None:
			setattr(self, attr + '_', str)
		else:
			self.handleParseError("Can only set '{}' once per Matcher.".format(attr))
		
	def compile(self):
		'''
		Parse the contents between {} to assign values to self. Each attribute can only
		be set once. 
		'''
		for each in self.input:
			x = re.match(r'([a-zA-Z0-9]+) "(.+)"', each)
			if x is None:
				return self.handleParseError("Failed to find pattern 'token \"Matcher\"' in '{}'.".format(each))
			token = x.group(1)
			matcher = x.group(2)
			
			if token == "from":
				self.set("from", matcher)
				continue
			if token == "to":
				self.set("to", matcher)
				continue
			if token == "subject":
				self.set("subject", matcher)
				continue
			if token == "contains":
				self.set("contains", matcher)
				continue
			if token == "notContains":
				self.set("notContains", matcher)
				continue
			
			self.handleParseError("unrecognised token '{}'".format(token))			
		
	def assemble(self):
		'''Produces a list of values to represent self in XML'''
		lines = []
		if self.from_ is not None:
			lines.append(("from", self.from_))
		if self.to_ is not None:
			lines.append(("to", self.to_))
		if self.subject_ is not None:
			lines.append(("subject", self.subject_))
		if self.contains_ is not None:
			lines.append(("hasTheWord", self.contains_))
		if self.notContains_ is not None:
			lines.append(("doesNotHaveTheWord", self.notContains_))
		if self.hasAttachment_ is not None:
			lines.append(("hasAttachment", self.hasAttachment_))
		if self.excludeChats_ is not None:
			lines.append(("excludeChats", self.excludeChats_))
		return lines

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
			str += " containing '%s'" % self.contains_  
		if self.notContains_:
			str += " not containing '%s'" % self.notContains_  
		return str