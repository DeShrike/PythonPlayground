def move(f, t):
	global moveCount
	# print("Move from {} to {}".format(f, t))
	moveCount += 1

def hanoi(n, f, via, t):
	if n == 0:
		pass
	else:
		hanoi(n-1, f, t, via)
		move(f, t)
		hanoi(n-1, via, f, t)

for i in range(0, 22):
	moveCount = 0
	disks = i

	hanoi(disks, "A", "B", "C")

	print("Hanoi with {} disks takes {} moves".format(disks, moveCount))

