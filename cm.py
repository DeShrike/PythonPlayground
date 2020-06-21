class File:
    def __init__(self, filename, method):
        self.file = open(filename, method)

    def __enter__(self):
        print("In __enter__")
        return self.file

    def __exit__(self, type, value, traceback):
        print("In __exit__")
        print(type)
        print(value)
        print(traceback)
        self.file.close()
        if type == Exception:
            # handle this exception
            return False
        return True  # exception handled

with File("file.txt", "w") as f:
     print("Middle")
     f.write("Hello")
     raise Exception()
