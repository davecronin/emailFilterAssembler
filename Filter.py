#! /usr/bin/python

class Filter:
	'''Class representing a filter or an entry in the XML. This contains a Matcher object
	for any conditions of the filter and a result object for the Actions. The result can be
	None, which is can be then allowed in nested filters where the top level filter might
	not specify a result.'''
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
		'''
		Create a list of XML values from the Filter. Returns None if there is no result
		for the Filter which needs to be handled by the caller.
		'''
		xml = [each for each in self.xmlLines]
		xml += self.condition.assemble()
		if self.result is not None:
			xml += self.result.assemble()
			return xml
		else:
			return None
		
	def addChild(self, child):
		self.childStatements.append(child)
		
	def merge(self, other):
		'''
		Merges the Filter with another such that the Matchers and ANDed or ORed and the
		Actions are overriden to be more specific.
		 '''
		if not other:
			assert 0
		# This is part of the flattening process so we 
		# can discard information about children
		self.childStatements = []
		self.condition.merge(other.condition)
		self.result.overrideWith(other.result)
			
	def __str__(self):
		return self.__repr__()
		
	def __repr__(self):
		str = "Filter: condition is %s" % self.condition 
		if self.result:
			str += " and result is %s" % self.result
		str += " with %d children." % len(self.childStatements)
		return str