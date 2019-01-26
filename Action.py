#! /usr/bin/python

import re

from Helpers import handleParseError

class Action:
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
			assert(0), "Matcher must have enclosing []"
		# TODO should check for non escaped commas in future
		content = content[1:-1].split(',')
		content = [ each.lstrip() for each in content]
		self.content=content
		self.compile()
		
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
		
	def handleParseError(self, error):
		handleParseError(self.lineNumber, self.line, error)
		
	def labelIs(self, str):
		if self.label_ is None:
			self.label_ = str
		else:
			self.handleParseError("Can only set 'label' once per Matcher.")
			
	def markAsReadIs(self, str):
		if self.markAsRead_ is None:
			self.markAsRead_ = str
		else:
			self.handleParseError("Can only set 'markAsRead' once per Matcher.")
			
	def starIs(self, str):
		if self.star_ is None:
			self.star_ = str
		else:
			self.handleParseError("Can only set 'star' once per Matcher.")
			
	def deleteIs(self, str):
		if self.delete_ is None:
			self.delete_ = str
		else:
			self.handleParseError("Can only set 'delete' once per Matcher.")
			
	def archiveIs(self, str):
		if self.archive_ is None:
			self.archive_ = str
		else:
			self.handleParseError("Can only set 'archive' once per Matcher.")
			
	def neverSpamIs(self, str):
		if self.neverSpam_ is None:
			self.neverSpam_ = str
		else:
			self.handleParseError("Can only set 'neverSpam' once per Matcher.")
			
	def importantIs(self, str):
		if self.important_ is None:
			self.important_ = str
		else:
			self.handleParseError("Can only set 'important' once per Matcher.")
			
	def smartLabelIs(self, str):
		if self.smartLastrel_ is None:
			self.smartLabel_ = str
		else:
			self.handleParseError("Can only set 'smartLabel' once per Matcher.")
			
	def compile(self):
		for each in self.content:
			x = re.match(r'(.+)', each)
			if x is None:
				self.handleParseError("failed to find token".format(each))
			assert len(x.groups()) == 1
			token = x.group(1)
			
			if token == "mark as read" or token == "mark read" or token == "read":
				self.markAsReadIs("true")
				continue
			if token == "star":
				self.starIs("true")
				continue
			if token == "delete" or token == "bin" or token == "trash":
				self.deleteIs("true")
				continue
			if token == "archive":
				self.archiveIs("true")
				continue
			if token == "not spam" or token == "never spam":
				self.containsIs("true")
				continue
			if token == "mark as important" or token == "mark important" or token == "important":
				self.importantIs("true")
				continue
			
			self.handleParseError("unrecognised token '{}'".format(token))
			
	def assemble(self):
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