import time
from timeit import default_timer as timer

def num_multi1(max):
    result = 0
    for num in range(0, max):
        if (num % 3 == 0 or num % 5 == 0):
            result += num

    print("Sum is %d " % result)

def DoIt():
    num_multi1(10000000)

start = time.time()
DoIt()
end = time.time()
ellapsed = end - start
print(f"Ellapsed: {ellapsed:.5f} seconds")


start = timer()
DoIt()
end = timer()
ellapsed = end - start
print(f"Ellapsed: {ellapsed:.5f} seconds")


start = time.process_time()
DoIt()
end = time.process_time()
ellapsed = end - start
print(f"Ellapsed: {ellapsed:.5f} seconds")

