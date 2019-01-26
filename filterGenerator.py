#! /usr/bin/python

import argparse
import os

from Parser import Parser
from XmlHelper import XmlHelper
from Helpers import globals, goToFailure, trace


def assemble(filters):
	assert isinstance(filters, list)
	xml = XmlHelper()
	
	for filter in filters:
		xml.addEntry(filter.assemble())
	return str(xml)

	
def main(inFile, outFile):
	contents = inFile.read()
	parser = Parser()
	filters = parser.parse(contents)

	xml = assemble(filters) 

	trace("The generated xml output is as follows:\n%s" % xml)

	outFile.write(xml)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate XML for email filters.')
	parser.add_argument( 'input_file', help="The file containing the rules to generate filters.")
	parser.add_argument( 'output_file', help="The file to output the filter in XML")
	parser.add_argument('-t', '--trace', action='store_true', help='Add tracing')
	parser.add_argument('--pdb', action='store_true', help='Catch failures in pdb.')
	args = parser.parse_args()
	
	globals(args.pdb, args.trace)
	
	trace("Tracing is turned on for this run.")
	
	try:
		inFile = open(args.input_file, "r")
	except:
		goToFailure("The input file '{}' does not exits.".format(args.output_file))
	
	try:	
		outFile = open(args.output_file, 'w+')
	except:
		goToFailure("Cannot open the output file '{}'".format(args.output_file))
	
	main(inFile, outFile)
	
	trace("Finished, closing files.")
	inFile.close()
	outFile.close()