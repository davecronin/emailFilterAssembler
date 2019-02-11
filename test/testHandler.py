#! /usr/bin/python

import glob
import subprocess


def runTests():
	tests = glob.glob("./test/*.xmf")
	for test in tests:
		# change xmf to xml
		outFile = test[:-4]	
		cmd = ["python", "main.py", test, outFile+".xml" ]
		if 'STDOUT' in test:
			res = subprocess.check_output(cmd + ["--ignoreParseErrors"])
			with open(outFile+".txt", "r") as expectedOutput:
				if res != expectedOutput.read():
					assert False, "Failed test case %s" % test
		elif 'XML' in test:
			res = subprocess.check_output(cmd)
			with open(outFile+".xml", "r") as output:
				with open(outFile+".expected.xml", "r") as expectedOutput:
					if output.read() != expectedOutput.read():
						assert False, "Failed test case %s" % test
			
if __name__ == "__main__":
	runTests()