# http://programarcadegames.com/index.php?lang=nl&chapter=introduction_to_animation
# http://programarcadegames.com/index.php?lang=nl&chapter=controllers_and_graphics

from Graphics import Graphics
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class Point():
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

class Test1(Graphics):

    def __init__(self):
        super().__init__("PyGame Test 1", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)

    def setup(self):
        self.points = []
        for i in range(50):
            x = random.randint(5, WINDOW_WIDTH - 5)
            y = random.randint(5, WINDOW_HEIGHT - 5)
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            p = Point(x, y, dx, dy)
            self.points.append(p)

    def cleanup(self):
        # print("Done")
        pass

    def draw(self):
        for p in self.points:
            self.circle(p.x, p.y, 30, Graphics.RED)
            self.circle(p.x, p.y, 20, Graphics.GREEN)
            # self.filled_circle(p.x, p.y, 10, Graphics.BLUE)
            # self.line(100, 100, self.x, self.y, Graphics.RED)
            # self.line(self.x, self.y, 200, 100, Graphics.RED)
            # self.rectangle(100, 100, 150, 150, Graphics.RED)
        self.line(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, Graphics.WHITE)
        self.line(WINDOW_WIDTH, 0, 0, WINDOW_HEIGHT, Graphics.WHITE)

    def update(self, timeDelta):
        for p in self.points:
            p.x += p.dx
            if p.x <= 5 or p.x >= WINDOW_WIDTH - 5:
                p.dx *= -1
            p.y += p.dy
            if p.y <= 5 or p.y >= WINDOW_HEIGHT - 5:
                p.dy *= -1

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = Test1()
    app.loop()
