# http://programarcadegames.com/index.php?lang=nl&chapter=introduction_to_animation
# http://programarcadegames.com/index.php?lang=nl&chapter=controllers_and_graphics

from Graphics import Graphics, Vector2, Vector3
import random
import math

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def limitVector2(v, maxsize):
    if v.magnitude() > maxsize:
        v.scale_to_length(maxsize)


class Rotator():

    def __init__(self, angle, speed, radiusx, radiusy):
        self.angle = angle
        self.speed = speed
        self.radiusx = radiusx
        self.radiusy = radiusy
        self.pos = Vector2(0, 0)

    def update(self):
        self.angle += self.speed
        tx = math.sin(self.angle) * self.radiusx + (WINDOW_WIDTH / 2)
        ty = math.cos(self.angle) * self.radiusy + (WINDOW_HEIGHT / 2)
        self.pos.update(tx, ty)


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

class Test3(Graphics):

    def __init__(self):
        super().__init__("PyGame Test 3", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)

    def setup(self):
        self.points = []
        for i in range(500):
            px = random.randint(5, WINDOW_WIDTH - 5)
            py = random.randint(5, WINDOW_HEIGHT - 5)
            p = Vehicle(Vector2(px, py), Vector2(0, 0))
            self.points.append(p)

        self.targets = []
        t = Rotator(0, 0.05, (WINDOW_WIDTH - 100) / 2, (WINDOW_HEIGHT - 100) / 2)
        self.targets.append(t)
        t = Rotator(0.1, 0.04, (WINDOW_WIDTH - 350) / 2, (WINDOW_HEIGHT - 150) / 2)
        self.targets.append(t)
        t = Rotator(0.2, 0.03, (WINDOW_WIDTH - 300) / 2, (WINDOW_HEIGHT - 150) / 2)
        self.targets.append(t)

        self.repulsors = []
        t = Rotator(0, 0.05, (WINDOW_WIDTH - 300) / 2, (WINDOW_HEIGHT - 200) / 2)
        self.repulsors.append(t)
        t = Rotator(0.2, -0.045, (WINDOW_WIDTH - 200) / 2, (WINDOW_HEIGHT - 300) / 2)
        self.repulsors.append(t)
        t = Rotator(0.4, 0.04, (WINDOW_WIDTH - 110) / 2, (WINDOW_HEIGHT - 100) / 2)
        self.repulsors.append(t)
        t = Rotator(0.6, 0.035, (WINDOW_WIDTH - 110) / 2, (WINDOW_HEIGHT - 200) / 2)
        self.repulsors.append(t)

    def cleanup(self):
        pass

    def draw(self):
        for p in self.points:
            self.circle(p.pos.x, p.pos.y, 11, Graphics.WHITE)
        
        for t in self.targets:
            self.circle(t.pos.x, t.pos.y, 7, Graphics.GREEN)
            self.filled_circle(t.pos.x, t.pos.y, 7, Graphics.GREEN)

        for r in self.repulsors:
            self.circle(r.pos.x, r.pos.y, 7, Graphics.RED)
            self.filled_circle(r.pos.x, r.pos.y, 7, Graphics.RED)

    def update(self, timeDelta):

        for t in self.targets:
            t.update()

        for r in self.repulsors:
            r.update()

        for p in self.points:
            closest = None
            dist = 10000
            for t in self.targets:
                d = p.pos.distance_to(t.pos)
                if d < dist:
                    dist = d
                    closest = t

            p.arrive(closest.pos)

            for r in self.repulsors:
                p.flee(r.pos)

            for pp in self.points:
                if p == pp:
                    continue
                d = p.pos.distance_to(pp.pos)
                if d < 30:
                    p.flee(pp.pos)

        for p in self.points:
            p.update()

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = Test3()
    app.loop()
