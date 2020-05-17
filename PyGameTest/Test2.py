# http://programarcadegames.com/index.php?lang=nl&chapter=introduction_to_animation
# http://programarcadegames.com/index.php?lang=nl&chapter=controllers_and_graphics

from Graphics import Graphics, Vector2, Vector3
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class Point():
    def __init__(self, pos, dx, dy):
        self.pos = pos
        self.dx = dx
        self.dy = dy

class Test2(Graphics):

    def __init__(self):
        super().__init__("PyGame Test 2", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)

    def setup(self):
        self.points = []
        for i in range(10):
            x = random.randint(5, WINDOW_WIDTH - 5)
            y = random.randint(5, WINDOW_HEIGHT - 5)
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            p = Point(Vector2(x, y), dx, dy)
            self.points.append(p)

    def cleanup(self):
        # print("Done")
        pass

    def draw(self):
        for p1 in self.points:
            for p2 in self.points:
                self.line(p1.pos.x, p1.pos.y, p2.pos.x, p2.pos.y, Graphics.WHITE)

    def update(self, timeDelta):
        for p in self.points:
            p.pos.x += p.dx
            if p.pos.x <= 5 or p.pos.x >= WINDOW_WIDTH - 5:
                p.dx *= -1
            p.pos.y += p.dy
            if p.pos.y <= 5 or p.pos.y >= WINDOW_HEIGHT - 5:
                p.dy *= -1

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = Test2()
    app.loop()
