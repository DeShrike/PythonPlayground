from Graphics import Graphics, Vector2, Vector3
import random
import math


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# https://medium.com/better-programming/making-a-verlet-physics-engine-in-javascript-1dff066d7bc5

class VectorShape(object):

    # shapes contain lines (x1, y1, x2, t2)
    sample_shape = [(0, 0, 10, 0), (10, 10, 0, 10)]

    def __init__(self, shape, x, y, rotation, scale = 1):
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale = scale

    def render(self):
        for s in self.shape:
            angle = self.rotation * (math.pi / 2)

            new_x1 = math.cos(angle) * (s[0]) - math.sin(angle) * (s[1])
            new_y1 = math.sin(angle) * (s[0]) + math.cos(angle) * (s[1])
            new_x1 = self.x + new_x1 * self.scale
            new_y1 = self.y + new_y1 * self.scale

            new_x2 = math.cos(angle) * (s[2]) - math.sin(angle) * (s[3])
            new_y2 = math.sin(angle) * (s[2]) + math.cos(angle) * (s[3])
            new_x2 = self.x + new_x2 * self.scale
            new_y2 = self.y + new_y2 * self.scale

            # line(new_x1, new_y1, new_x2, new_y2)

class Particle(object):

    bounce = 1
    gravity = 0.9
    friction = 0.999

    def __init__(self, name: str, pos: Vector2, oldpos: Vector2, pinned: bool = False):
        self.name = name
        self.pos = pos
        self.oldpos = oldpos
        self.pinned = pinned
        self.velocity = None

    def update(self, delta):
        if self.pinned:
            return
        self.velocity = (self.pos - self.oldpos) * Particle.friction
        self.oldpos = Vector2(self.pos)
        self.pos += self.velocity

    def constrain_points(self, width, height):
        if self.pinned:
            return
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
        if self.pinned:
            return
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
        if self.p0.pinned == False:
            self.p0.pos.x -= offset_x
            self.p0.pos.y -= offset_y
        if self.p1.pinned == False:
            self.p1.pos.x += offset_x
            self.p1.pos.y += offset_y


class Verlet7(Graphics):

    def __init__(self):
        super().__init__("PyGame Verlet 7", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.particles = []
        self.sticks = []
        self.frames = 0

    def add_stick(self, pa, pb) -> Stick:
        a = self.find_particle(f"{pa}")
        b = self.find_particle(f"{pb}")
        s = Stick(a, b, a.distance_to(b))
        self.sticks.append(s)        
        return s

    def add_particle(self, x, y) -> Particle:
        p = Particle(f"{len(self.particles)}", Vector2(x, y), Vector2(x, y))
        self.particles.append(p)
        return p

    def setup(self):
        self.add_particle(50, 100)
        self.add_particle(200, 50)
        self.add_stick(0, 1)

    def find_particle(self, name):
        for p in self.particles:
            if p.name == name:
                return p
        print(name)
        return None

    def cleanup(self):
        pass

    def draw(self):
        self.frames += 1
        for p in self.particles:
            self.filled_circle(p.pos.x, p.pos.y, 3, Graphics.WHITE)

        for s in self.sticks:
            if s.hidden:
                continue
            self.line(s.p0.pos.x, s.p0.pos.y, s.p1.pos.x, s.p1.pos.y, Graphics.WHITE)

    def updateX(self, timeDelta):
        pass

    def update(self, timeDelta):
        for p in self.particles:
            p.update(timeDelta)

        for p in self.particles:
            p.apply_gravity()

        for _ in range(5):
            for s in self.sticks:
                s.update(timeDelta)
            for p in self.particles:
                p.constrain_points(WINDOW_WIDTH, WINDOW_HEIGHT)

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = Verlet7()
    app.loop()
