#! /usr/bin/python

import glob
import subprocess


def runTests():
	tests = glob.glob("./test/*.xmf")
	for test in tests:
		# change xmf to xml
		outFile = test[:-1] + 'l'	
		cmd = ["python", "main.py", test, outFile ]
		if 'FAIL' in test:
			res = subprocess.check_output(cmd + ["--ignoreParseErrors"])
			with open(test+".expected", "r") as expectedOutput:
				if res != expectedOutput.read():
					assert False, "Failed test case %s" % test
		else:
			res = subprocess.check_output(cmd)
			with open(outFile, "r") as output:
				with open(outFile+".expected", "r") as expectedOutput:
					if output.read() != expectedOutput.read():
						assert False, "Failed test case %s" % test
			
if __name__ == "__main__":
	runTests()