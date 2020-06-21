class Meta(type):
    def __new__(self, class_name, bases, attrs):
        print(f"Class Name: {class_name}")
        print("Bases: ", bases)
        print("Attributes: ", attrs)

        a = {}
        for name, value in attrs.items():
            if name.startswith("__"):
                a[name] = value
            else:
                a[name.upper()] = value

        print("Moddified Attributes: ", a)

        return type(class_name, bases, a)

class Dog(metaclass = Meta):
    x = 5
    y = 8
    def __init__(self):
        pass
    def show(self):
        print(f"X: {self.X}  Y: {self.Y}")


class Cat(Dog, metaclass = Meta):
    def show(self):
        print("I am a cat")

d = Dog()
d.SHOW()

c = Cat()
c.SHOW()

