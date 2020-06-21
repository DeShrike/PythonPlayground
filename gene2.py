import sys



def gen(n):
    for i in range(n):
        yield i ** 2

x = [i ** 2 for i in range(10_000)]
g = gen(10_000)

print(sys.getsizeof(x))
print(sys.getsizeof(g))



# for i in gen(1_000):
#    print(i)


