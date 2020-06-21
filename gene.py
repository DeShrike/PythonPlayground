# x = [i**2 for i in range(1_000_000_000)]

class Gen(objet):
    def __init__(self, n):
        self.n = n
        self.last = 0

    def __next__(self):
        return self.next()

    def next(self):
        if self.last == self.n:
            rasie StopIteration()
        rv = self.last ** 2
        self.last += 1
        return rv

g = Gen(1_000_000_000_000)
while True:
    try:
        print(next(g))
    except StopIteration:
        break





# for el in x:
#     print(el)

