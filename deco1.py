import time


def func(value):
    def wrapper():
        print("Started")
        print(value)
        print("Ended")

    return wrapper

x = func("Hello")
print(x)
x()


def my_decorator(f):
    def wrapper(*args, **kwargs):
        print("Started")
        rv = f(*args, **kwargs)
        print("Ended")
        return rv

    return wrapper

def func2():
    print("I am func2")

def func3():
    print("I am func3")

def func4():
    print("I am func4")

@my_decorator
def func5():
    print("I am func 5")

x = my_decorator(func2)
print(x)
x()

x = my_decorator(func3)
print(x)
x()

func4 = my_decorator(func4)
func4()


func5()


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        rv = func()
        total = time.time() - start
        print("Time: ", total)
        return rv

    return wrapper


@timer
def test():
    for _ in range(10000):
         pass

test()

