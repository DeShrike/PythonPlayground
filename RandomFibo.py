import itertools
import functools

pattern_length = 7

theset = ['+' for _ in range(pattern_length)] + ['-' for _ in range(pattern_length)]
print(theset)

perms = []
total = 0
for x in itertools.permutations(theset, pattern_length):
	total = total +1
	if x not in perms:
		perms.append(x)

print(f"length: {pattern_length}")
print(f"total: {total}")
print(f"unique: {len(perms)}")

hi = 0
lo = 0

@functools.lru_cache(maxsize=128)
def Fibo(n, pattern):
	if n == 1 or n == 2:
		return 1
	operator = pattern[n % len(pattern)]
	if operator == '-':
		return Fibo(n - 1, pattern) - Fibo(n - 2, pattern)
	return Fibo(n - 1, pattern) + Fibo(n - 2, pattern)

def rand_fibo(pattern):
	global hi, lo
	hi = 0
	lo = 0
	print(f"RANDOM FIBONACI with {pattern}")

	for i in range(100):
		val = Fibo(i + 1, pattern)
		if val < lo:
			lo = val
		if val > hi:
			hi = val	
	print(f"Pattern: {pattern}", end = "")
	print(f"Low: {lo}  High: {hi}")
	

for perm in perms:
	rand_fibo(perm)

