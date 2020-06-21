# Metaclasses
# (don't use ??)

def hello():
    class Hi:
       pass

    return Hi


class Test:
     pass


print(Test)
print(Test())
print(type(Test()))
print(type(2))
print(type(hello))
print(type(Test))


class Foo:
    def show(self):
        print("Hi")

def add_attribute(self):
    self.z = 9

# name, bases, attributes
Test2 = type("Test", (Foo,), { "x": 5, "add_attribute": add_attribute })

t = Test2()

print(t.x)
t.show()
t.add_attribute()
print(t.z)


