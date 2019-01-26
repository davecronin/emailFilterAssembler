#! /usr/bin/python

class XmlHelper:
	def __init__(self):
		self.xml = "<?xml version='1.0' encoding='UTF-8'?><feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>\n"
		self.addLine(1, "<title>Mail Filters</title>")
		self.addLine(1, "<id>tag:mail.google.com,2008:filters:4366218717592519022</id>")
		
	def addLine(self, indent, line ):
		assert self.xml[-1:] == "\n"
		for i in range(0, indent):
			self.xml += '\t'
		self.xml += line
		self.xml += '\n'
		
	def formatEntryLine(self, input):
		return "<apps:property name='{0}' value='{1}'/>".format(input[0], input[1])
		
	def addEntry(self, entryLines):
		assert isinstance(entryLines, list)
		self.addLine(1, "<entry>")
		for each in entryLines:
			if isinstance(each, str):
				self.addLine(2, each)
			elif isinstance(each, tuple):
				assert len(each) == 2
				self.addLine(2, self.formatEntryLine(each))
			else:
				assert 0, "invalid type for entry line"	
		self.addLine(1, "</entry>")
		
	def ending(self):
		return "</feed>"
		
	def __str__(self):
		return self.xml + self.ending()
		
	def __repr__(self):
		return self.xml + self.ending()
		
