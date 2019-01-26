#! /usr/bin/python

import pdb

def globals(_setPDB, _setTrace):
	global setPDB
	setPDB = _setPDB
	global setTrace
	setTrace = _setTrace

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