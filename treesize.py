import os

sizes = []
initial = {}
initialFile = "treesize.txt"
diffFile = "treesize.diff.txt"
rootfolder = "c:\\"
# rootfolder = "C:\\TFSProjects\\Playground\\Python"
diffs = []

def listdir_fullpath(d):
	return [os.path.join(d, f) for f in os.listdir(d)]

def CreateInitial():
	global sizes
	errorcount = 0
	dircount = 0
	# d = listdir_fullpath(".")

	for dirname, dirnames, filenames in os.walk(rootfolder):
		# print path to all subdirectories first.
		# for subdirname in dirnames:
		#    print(os.path.join(dirname, subdirname))
		dircount += 1
		size = 0
		# print path to all filenames.
		# print(dirname)
		for filename in filenames:
			# print(os.path.join(dirname, filename))
			file = os.path.join(dirname, filename)
			try:
				size += os.path.getsize(file)
			except Exception as e:
				# print("ERROR")
				errorcount += 1
			else:
				pass
			finally:
				pass
		sizes.append([dirname, size])

		# Advanced usage:
		# editing the 'dirnames' list will stop os.walk() from recursing into there.
		if '.git' in dirnames:
			# don't go into any .git directories.
			dirnames.remove('.git')

		if dircount % 123 == 0:
			print(f"{dircount:,} Directories - {errorcount} Errors", end = "\r")

	print("")
	print("Sorting")

	sizes.sort(key = lambda x: x[1], reverse = True)

	print("Saving")

	f = open(initialFile, "w+")
	for item in sizes:
		f.write("%d\t%s\n" % (item[1], item[0]))
	f.close()

def CheckDifferences():
	dircount = 0
	errorcount = 0
	difference = 0
	for dirname, dirnames, filenames in os.walk(rootfolder):
		# print path to all subdirectories first.
		# for subdirname in dirnames:
		#    print(os.path.join(dirname, subdirname))

		size = 0
		dircount += 1

		# print path to all filenames.
		# print(dirname)
		for filename in filenames:
			# print(os.path.join(dirname, filename))
			file = os.path.join(dirname, filename)
			try:
				size += os.path.getsize(file)
			except Exception as e:
				# print("ERROR")
				errorcount += 1
			else:
				pass
			finally:
				pass

		if dirname in initial:
			ini = initial[dirname]
		else:
			ini = 0

		diff = size - ini
		difference += diff
		if abs(diff) > 1024:
			diffs.append([dirname, diff])
		
		# Advanced usage:
		# editing the 'dirnames' list will stop os.walk() from recursing into there.
		if '.git' in dirnames:
			# don't go into any .git directories.
			dirnames.remove('.git')
		
		if dircount % 123 == 0:
			print(f"{dircount:,} Directories - {errorcount} Errors", end = "\r")

	print("")
	print("Sorting")

	diffs.sort(key = lambda x: x[1], reverse = True)

	print("Saving")

	f = open(diffFile, "w+")
	for item in diffs:
		f.write("%s\t%s\n" % ("{:,}".format(item[1]), item[0]))
	sign = "+" if difference > 0 else ""
	kb = difference // 1024
	mb = difference // (1024 * 1024)
	f.write(f"Overall Difference: {sign}{difference:,} bytes / {kb:,} Kb / {mb:,} Mb")
	f.close()

def LoadInitial():
	initial.clear()
	file = open(initialFile, "r")
	for line in file:
		l = line.rstrip("\n")
		parts = l.split("\t")
		initial[parts[1]] = int(parts[0])

		# print(l)
		# print(initial[parts[1]])		
		# input("....")

	file.close()

if __name__ == "__main__":
	if os.path.exists(initialFile) == False:
		CreateInitial()
	else:
		LoadInitial()
		CheckDifferences()

