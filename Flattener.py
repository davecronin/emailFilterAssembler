from copy import deepcopy

class Flattener():
	'''
	Flattens a tree of Filters. Every node needs to compile to a complete independant 
	filter with the correct matchers and actions being overriden for that node to behave
	as needed. 
	For example, if we have nodes A and B, where B is a child of A, then b is a more 
	specific filter then A since it includes additional matching criteria. Therefore there
	needs to be two filters, one with As less specific criteria and respective result, and
	one with Bs more specific criteria and respective result.
	'''
	def __init__(self):
		self.finalFilters = []
		self.stack = []
		
	def genFinalFilter(self):
		'''
		Creates the filter by merging the list of filters given. In the example above
		this would be called for (A) and (A and B)
		'''
		# If the last filter, or leaf filter has no filter then there might be no point 
		# generating this filter since it will will not contain any additional actions, only
		# an extra matcher.. Should we error here? or ignore creating the extra filter?
		# leaving creating the extra filter in since it's not easy to error here nicely
		# and I don't want to drop information on the floor. 
		#if not self.stack[-1].result:
		#	return
		# We need to copy the stack so we don't modify the originals
		tmp = deepcopy(self.stack)
		result = tmp[0]
		for each in tmp[1:]:
			result.merge(each)
		self.finalFilters.append(result)

	def flatten(self, filters):
		'''
		Depth first search of the tree to and generate the filter with the stack before an 
		item is popped. With the above example that would mean creating (A and B) and then (A).
		'''
		assert isinstance(filters, list)
		for each in filters:
			self.stack.append(each)
			if each.childStatements:
				self.flatten(each.childStatements)
			else:
				self.genFinalFilter()
			self.stack.pop()
    #exception for when the very last entry is popped
		if self.stack:
			self.genFinalFilter()
		return self.finalFilters