import os

def Exists(oldFunc):
	def inside(filename):
		if os.path.exists(filename):
			oldFunc(filename)
		else:
			print("File not found")
	return inside

@Exists
def outputLine(infile):
	with open(infile) as f:
		print(f.readlines())

outputLine("Test.py")
outputLine("Deco.py")
