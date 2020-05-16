import math

def is_valid(vat):
	rest = vat % 100
	dit = 97 - (math.floor(vat / 100) % 97)
	return rest == dit

def hasDigits(s, d):
	cc = [0 for _ in range(10)]
	for c in s:
		ic = int(c)
		cc[ic] += 1
	count = 0
	for c in cc:
		if c > 0:
			count += 1
	if count <= d:
		return True
	return False

# 0413059454
for i in range(100000070, 999999999, 99):
	if i % 1000000 == 0:
		print("Testing", i)
	if is_valid(i):
		if hasDigits(str(i), 2):
			print(i)


# print(is_valid(413059454))
# print(is_valid(882704849))
# print(is_valid(898373319))
# print(is_valid(887685503))
# print(is_valid(123456789))

# 0413059454
# 0100000100

# BE0251111125

