allowed = ['2', '3', '4', '7', '8', '9' ]
minima = [0, 0, 0, 0, 0, 1]
maxima = [30, 30, 30, 30, 30, 30]

currentPosition = []
for i in range(0, len(minima)):
	currentPosition.append(minima[i])

currentNumber = []
levelCount = 0
countChecked = 0
showEvery = 100000			# 100000
showMinimumScore = 11	# 11

totaalToDo = 1
for i in range(0, len(allowed)):
	totaalToDo *= maxima[i]	- minima[i] + 1

print ("Total: %d" % (totaalToDo))

def per(number):
	global levelCount

	snumber = str(number)
	if len(snumber) == 1:
		return levelCount

	digits = [int(i) for i in str(snumber)]

	prod = 1
	for j in digits:
		prod *= j
	
	levelCount += 1
	return per(prod)

def process():
	global levelCount
	global countChecked
	levelCount = 0
	num = ""
	for i in range(0, len(currentNumber)):
		num = num + str(currentNumber[i])
	levels = per(int(num))
	countChecked += 1
	if levels >= showMinimumScore or countChecked % showEvery == 0:
		percDone = (float(countChecked) / float(totaalToDo)) * 100.0
		print ("L: %d - %s - %.3f%%" % (levels, num, percDone))
		writeLine(levels, num, percDone, countChecked, totaalToDo)

def writeLine(steps, number, perc, count, total):
	f = open("mulper.txt", "a+")
	f.write("%d steps : %d / %d = %.3f %% : %s\r\n" % (steps, count, total, perc, number))
	f.close()

def incrementPosition():
	global currentNumber
	global currentPosition
	p = 0
	while currentPosition[p] >= maxima[p]:
		p += 1
		if p >= len(currentPosition):
			return False

	currentPosition[p] += 1
	for i in range(0, p):
		currentPosition[i] = minima[i]

	# print (currentPosition)
	return True

def showNumber():
	num = ""
	for i in range(0, len(currentNumber)):
		num = num + currentNumber[i]

	print(num)


def buildNumber():
	global currentNumber
	global currentPosition
	currentNumber = []
	for i in range(0, len(currentPosition)):
		for c in range(1, currentPosition[i] + 1):
			currentNumber.append(allowed[i])

	# print (currentNumber)

def my_range(start, end, step):
	while start <= end:
		yield start
		start += step


#################################################################""


while (True):
	buildNumber()
	# showNumber()
	process()

	if incrementPosition() == False:
		break
	

print("Done")

