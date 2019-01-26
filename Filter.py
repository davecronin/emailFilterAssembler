#! /usr/bin/python

class Filter:
	def __init__(self, condition, result=None):
		self.condition=condition
		self.result=result
		self.xmlLines = [
			"<category term='filter'></category>",
			"<title>Mail Filter</title>",
			"<id>tag:mail.google.com,2008:filter:4366218717592519022</id>"
		]
		
	def assemble(self):
		xml = [each for each in self.xmlLines]
		xml += self.condition.assemble()
		if self.result is not None:
			xml += self.result.assemble()
		return xml
	
	def __str__(self):
		return self.__repr__()
		
	def __repr__(self):
		str = "Filter: condition is %s" % self.condition 
		if self.result:
			str += " and result is %s" % self.result
		return str