#! /usr/bin/python

import re

from Helpers import handleParseError, labelWarning

class Action:
	'''
	Class to represent the possible actions of a filter. It is responsible
	for parsing the contents between [] to compile its attributes, merging with other 
	Actions and producing values for the XML representation of itself.
	'''
	def __init__(self, content, line, lineNumber):
		self.line = line
		self.lineNumber = lineNumber		
		self.label_ = None # Not supported yet
		self.markAsRead_ = None
		self.star_ = None
		self.delete_ = None
		self.archive_ = None
		self.neverSpam_ = None
		self.important_ = None
		self.smartLabel_ = None # Not supported yet
		
		if content[0]!='[' or content[-1] != ']':
			assert 0, "Matcher must have enclosing []"
		# TODO should check for non escaped commas in future
		content = content[1:-1].split(',')
		content = [ each.lstrip() for each in content]
		self.content=content
		self.compile()
		
	def overrideWith(self, other):
		'''Overriding this Matcher with another, preferring the values of the other '''
		if not other:
			assert 0
		if other.label_:
			self.label_ = other.label_
		if other.markAsRead_:
			self.markAsRead_ = other.markAsRead_
		if other.star_:
			self.star_ = other.star_
		if other.delete_:
			self.delete_ = other.delete_
		if other.archive_:
			self.archive_ = other.archive_
		if other.neverSpam_:
			self.neverSpam_ = other.neverSpam_
		if other.important_:
			self.important_ = other.important_
		if other.smartLabel_:
			self.smartLabel_ = other.smartLabel_
	
	def handleParseError(self, error):
		handleParseError(self.lineNumber, self.line, error)
		
	def set(self, attr, str):
		'''Generic setter for attrs only allowing them to be set once.'''
		if getattr(self, attr + '_') is None:
			setattr(self, attr + '_', str)
		else:
			self.handleParseError("Can only set '{}' once per Action.".format(attr))
		if 'label' == attr and '/' in str:
			labelWarning(self.label_)
						
	def compile(self):
		'''
		Parse the contents between [] to assign values to self. Each attribute can only
		be set once. 
		'''
		for each in self.content:
			x = re.match(r'(.+)', each)
			if x is None:
				self.handleParseError("failed to find token".format(each))
			assert len(x.groups()) == 1
			token = x.group(1)
			
			if token == "mark as read" or token == "mark read" or token == "read":
				self.set("markAsRead", "true")
				continue
			if token == "star":
				self.set("star", "true")
				continue
			if token == "delete" or token == "bin" or token == "trash":
				self.set("delete", "true")
				continue
			if token == "archive":
				self.set("archive", "true")
				continue
			if token == "not spam" or token == "never spam":
				self.set("neverSpam", "true")
				continue
			if token == "mark as important" or token == "mark important" or token == "important":
				self.set("important", "true")
				continue
			
			x = re.match(r'label "(.+)"', each)
			if x:
				self.set('label', x.group(1))
				continue
				
			self.handleParseError("unrecognised token '{}'".format(token))
			
	def assemble(self):
		'''Produces a list of values to represent self in XML'''
		lines = []
		if self.label_ is not None:
			lines.append(("label", self.label_))
		if self.markAsRead_ is not None:
			lines.append(("shouldMarkAsRead", self.markAsRead_))
		if self.star_ is not None:
			lines.append(("shouldStar", self.star_))
		if self.delete_ is not None:
			lines.append(("shouldTrash", self.delete_))
		if self.archive_ is not None:
			lines.append(("shouldArchive", self.archive_))
		if self.neverSpam_ is not None:
			lines.append(("shouldNeverSpam", self.neverSpam_))
		if self.important_ is not None:
			lines.append(("shouldAlwaysMarkAsImportant", self.important_))
		if self.smartLabel_ is not None:
			lines.append(("smartLabelToApply", self.smartLabel_))
		return lines	
				
	def __str__(self):
		return self.__repr__()
		
	def __repr__(self):
		str = "Action:"
		if self.label_:
			str += " apply label '%s'" % self.label_  
		if self.markAsRead_:
			str += " mark as read,"
		if self.star_:
			str += " star,"
		if self.delete_:
			str += " delete,"
		if self.archive_:
			str += " archive,"
		if self.neverSpam_:
			str += " don't treat as spam,"
		if self.important_:
			str += " mark as important,"
		if self.smartLabel_:
			str += " apply smark label '%s'" % self.smartLabel_  
		return str[:-1]