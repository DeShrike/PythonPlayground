from Graphics import Graphics, Vector2, Vector3
import random
import math


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# https://medium.com/better-programming/making-a-verlet-physics-engine-in-javascript-1dff066d7bc5

class Particle(object):

    bounce = 0.9
    gravity = 0.5
    friction = 0.999

    def __init__(self, pos: Vector2, oldpos: Vector2, pinned: bool = False):
        self.pos = pos
        self.oldpos = oldpos
        self.pinned = pinned
        self.velocity = None

    def update(self, delta):
        self.velocity = (self.pos - self.oldpos) * Particle.friction
        self.oldpos = Vector2(self.pos)
        self.pos += self.velocity

    def constrain_points(self, width, height):
        if self.pos.x > width:
            self.pos.x = width
            self.oldpos.x = self.pos.x + self.velocity.x * Particle.bounce
        elif self.pos.x < 0:
            self.pos.x = 0
            self.oldpos.x = self.pos.x + self.velocity.x * Particle.bounce

        if self.pos.y > height:
            self.pos.y = height
            self.oldpos.y = self.pos.y + self.velocity.y * Particle.bounce
        elif self.pos.y < 0:
            self.pos.y = 0
            self.oldpos.y = self.pos.y + self.velocity.y * Particle.bounce

    def apply_gravity(self):
        self.pos.y += Particle.gravity

    def distance_to(self, other: "Particle"):
        return self.pos.distance_to(other.pos)

class Stick(object):

    def __init__(self, pointa: Particle, pointb: Particle, lenght: int, hidden: bool = False):
        self.p0 = pointa
        self.p1 = pointb
        self.lenght = lenght
        self.hidden = hidden

    def update(self, delta):
        dx = self.p1.pos.x - self.p0.pos.x
        dy = self.p1.pos.y - self.p0.pos.y
        distance = math.sqrt(dx * dx + dy * dy)
        difference = self.lenght - distance
        percent = difference / distance / 2
        offset_x = dx * percent
        offset_y = dy * percent
        self.p0.pos.x -= offset_x
        self.p0.pos.y -= offset_y
        self.p1.pos.x += offset_x
        self.p1.pos.y += offset_y


class Verlet1(Graphics):

    def __init__(self):
        super().__init__("PyGame Verlet 1", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.particles = []
        self.sticks = []

    def setup(self):
        p = Particle(Vector2(100, 100), Vector2(95, 95))
        self.particles.append(p)
        p = Particle(Vector2(200, 100), Vector2(150, 100))
        self.particles.append(p)
        p = Particle(Vector2(200, 200), Vector2(200, 200))
        self.particles.append(p)
        p = Particle(Vector2(100, 200), Vector2(100, 200))
        self.particles.append(p)

        a = self.particles[0]
        b = self.particles[1]
        s = Stick(a, b, a.distance_to(b))
        self.sticks.append(s)

        a = self.particles[1]
        b = self.particles[2]
        s = Stick(a, b, a.distance_to(b))
        self.sticks.append(s)

        a = self.particles[2]
        b = self.particles[3]
        s = Stick(a, b, a.distance_to(b))
        self.sticks.append(s)

        a = self.particles[3]
        b = self.particles[0]
        s = Stick(a, b, a.distance_to(b))
        self.sticks.append(s)

        a = self.particles[0]
        b = self.particles[2]
        s = Stick(a, b, a.distance_to(b), True)
        self.sticks.append(s)

    def cleanup(self):
        pass

    def draw(self):
        for p in self.particles:
            self.filled_circle(p.pos.x, p.pos.y, 5, Graphics.WHITE)

        for s in self.sticks:
            if s.hidden:
                continue
            self.line(s.p0.pos.x, s.p0.pos.y, s.p1.pos.x, s.p1.pos.y, Graphics.WHITE)

    def update(self, timeDelta):
        for p in self.particles:
            p.update(timeDelta)

        for p in self.particles:
            p.apply_gravity()

        for _ in range(2):
            for s in self.sticks:
                s.update(timeDelta)
            for p in self.particles:
                p.constrain_points(WINDOW_WIDTH, WINDOW_HEIGHT)

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = Verlet1()
    app.loop()
