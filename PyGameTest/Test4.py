from Graphics import Graphics, Vector2, Vector3
from QuadTree import QuadTree, QuadTreePoint, RectangleRange, CircleRange
import random
import math

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def limitVector2(v, maxsize):
    if v.magnitude() > maxsize:
        v.scale_to_length(maxsize)

class Vehicle():

    maxspeed = 10
    maxforce = 1

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.acc = Vector2(0, 0)

    def update(self):
        self.vel += self.acc
        limitVector2(self.vel, self.maxspeed)
        self.pos += self.vel
        self.acc.update(0, 0)

    def applyForce(self, force):
        self.acc += force

    def seek(self, target):
        desired = target - self.pos
        desired.normalize_ip()
        desired *= self.maxspeed
        steer = desired - self.vel
        limitVector2(steer, self.maxforce)
        self.applyForce(steer)

    def flee(self, target):
        desired = target - self.pos
        distance = desired.magnitude()
        if distance > 100:
            return
        desired.normalize_ip()
        desired *= -self.maxspeed
        steer = desired - self.vel
        limitVector2(steer, self.maxforce)
        self.applyForce(steer)

    def arrive(self, target):
        desired = target - self.pos
        distance = desired.magnitude()
        desired.normalize_ip()
        if distance < 100:
            desired *= distance / 10
        else:
            desired *= self.maxspeed

        steer = desired - self.vel
        limitVector2(steer, self.maxforce)
        self.applyForce(steer)

class Test4(Graphics):

    def __init__(self):
        super().__init__("PyGame Test 4", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)

    def setup(self):

        boundary = RectangleRange(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.qt = QuadTree(boundary)

        for i in range(2000):
            px = random.randint(5, WINDOW_WIDTH - 5)
            py = random.randint(50, WINDOW_HEIGHT - 5)
            v = Vehicle(Vector2(px, py), Vector2(0, 0))
            p = QuadTreePoint(px, py, v)
            self.qt.insert(p)

        self.r1 = RectangleRange(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 200, 100)
        self.r2 = CircleRange(WINDOW_WIDTH // 2 + 220, WINDOW_HEIGHT // 2 - 100, 90)

        self.r1dx = 1
        self.r1dy = 2

        self.r2dx = 2
        self.r2dy = 1

        print(self.qt)

    def cleanup(self):
        pass

    def draw(self):
        for p in self.qt.all():
            self.filled_circle(p.userdata.pos.x, p.userdata.pos.y, 3, Graphics.WHITE)

        self.rectangle(self.r1.cx - self.r1.w, 
            self.r1.cy - self.r1.h, 
            self.r1.cx + self.r1.w, 
            self.r1.cy + self.r1.h, Graphics.RED)

        self.circle(self.r2.x, self.r2.y, self.r2.r, Graphics.GREEN)

        for p in self.qt.queryRectangle(self.r1):
            self.filled_circle(p.userdata.pos.x, p.userdata.pos.y, 3, Graphics.RED)

        for p in self.qt.queryCircle(self.r2):
            self.filled_circle(p.userdata.pos.x, p.userdata.pos.y, 3, Graphics.GREEN)

    def update(self, timeDelta):

        self.r1.cx += self.r1dx
        self.r1.cy += self.r1dy 
        if self.r1.cx + self.r1.w >= WINDOW_WIDTH:
            self.r1dx *= -1
        if self.r1.cx - self.r1.w <= 0:
            self.r1dx *= -1
        if self.r1.cy + self.r1.h >= WINDOW_HEIGHT:
            self.r1dy *= -1
        if self.r1.cy - self.r1.h <= 0:
            self.r1dy *= -1

        self.r2.x += self.r2dx
        self.r2.y += self.r2dy 
        if self.r2.x + self.r2.r >= WINDOW_WIDTH:
            self.r2dx *= -1
        if self.r2.x - self.r2.r <= 0:
            self.r2dx *= -1
        if self.r2.y + self.r2.r >= WINDOW_HEIGHT:
            self.r2dy *= -1
        if self.r2.y - self.r2.r <= 0:
            self.r2dy *= -1
        # for p in self.points:
        #    p.update()

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = Test4()
    app.loop()
