import contextlib

@contextlib.contextmanager
def file(filename, method):
    print("Opening")
    file = open(filename, method)
    yield file
    print("Closing")
    file.close()


with file("text.txt", "w") as f:
    print("Middle")
    f.write("Hello World")

print("DOne")

