import hashlib

input = "3.141592653"

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def countSame(value):
	first = value[-1]
	for i in range(2, len(value)):
		if value[-i] != first:
			return i
	return 0


for i in range(1, 9999999999):
	if i % 100000000 == 0:
		print(i)
	plain = input + str(i)
	sha_signature = encrypt_string(plain)
	c = countSame(sha_signature) 
	if c > 7:
		print(plain, sha_signature, c)

