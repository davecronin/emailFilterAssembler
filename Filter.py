#! /usr/bin/python

class Filter:
	def __init__(self, condition, result=None):
		self.condition=condition
		self.result=result
		self.childStatements=[]
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
		str += " with %d children." % len(self.childStatements)
		return str
		
	def addChild(self, child):
		self.childStatements.append(child)
		
	def merge(self, other):
		if not other:
			assert 0
		# This is part of the flattening process so we 
		# can discard information about children
		self.childStatements = []
		self.condition.merge(other.condition)
		self.result.overrideWith(other.result)