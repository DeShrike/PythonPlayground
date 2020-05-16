import sys
levelCount = 0

def per(number):
	global levelCount

	snumber = str(number)
	if len(snumber) == 1:
		return levelCount

	digits = [int(i) for i in str(snumber)]

	prod = 1
	for j in digits:
		prod *= j
	
	print (prod)

	levelCount += 1
	return per(prod)


arguments = len(sys.argv) - 1

if arguments == 1:
	arg = sys.argv[1]
	print (arg)
	level = per(arg)
	print ("Level %d" % (level))
else:
	print ("Usage: python mulper.py <number>")


