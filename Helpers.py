#! /usr/bin/python

import pdb

def globals(_setPDB, _setTrace):
	global setPDB
	setPDB = _setPDB
	global setTrace
	setTrace = _setTrace
	global labelWarningOccured
	labelWarningOccured = False

def goToFailure(error=None):
	if error:
		print error
	if setPDB:
		pdb.set_trace()
	exit(1)
	
def trace(str):
	if setTrace:
		print(str)
		
def handleParseError(lineNumber, line, error):
	print("Line {0}: {1} => {2}".format(lineNumber, line, error))
	goToFailure()
	
def labelWarning(label):
	global labelWarningOccured
	if labelWarningOccured:
		print("Warning, another potentially nested label '{}'\n".format(label))
	else:
		print("Warning, the label '{}' contains a '/' which you might be using to indicate"
					" nested/sub labels or folders. When uploading filters to gmail the importer"
					" treats the / as part of the label name, and creates the label as such.\n"
					"It does not create a nested label with this information. However if a nested"
					" label aleardy exists, it will use it. So please create any nested labels first"
					" manually in gmail. Regular labels will be created automatically on import.\n"
					"Sorry for the inconvenience this causes.\n".format(label))
		labelWarningOccured = True