from Graphics import Graphics, Vector2, Vector3
import random
import math


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# https://medium.com/better-programming/making-a-verlet-physics-engine-in-javascript-1dff066d7bc5

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


class Verlet6(Graphics):

    def __init__(self):
        super().__init__("PyGame Verlet 6", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.particles = []
        self.sticks = []
        self.frames = 0
        self.angle1 = 0
        self.anglespeed1 = 0.05
        self.angle2 = 0
        self.anglespeed2 = 0.15

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
        self.add_particle(100, 100)
        self.add_particle(150, 100)
        self.add_particle(200, 100)
        self.add_particle(250, 100)
        self.add_particle(300, 100)

        self.add_particle(350, 100) # 5
        self.add_particle(400, 50)
        self.add_particle(400, 150)
        self.add_particle(450, 100)

        self.add_particle(500, 100)
        self.add_particle(550, 100)
        self.add_particle(600, 100)
        self.add_particle(650, 100)
        self.add_particle(700, 100)

        self.find_particle("0").pinned = True
        self.find_particle(f"{len(self.particles) - 1}").pinned = True

        self.add_stick(5, 6)
        self.add_stick(6, 8)
        self.add_stick(8, 7)
        self.add_stick(7, 5)
        self.add_stick(6, 7).hidden = True

        self.add_stick(0, 1)
        self.add_stick(1, 2)
        self.add_stick(2, 3)
        self.add_stick(3, 4)
        self.add_stick(4, 5)

        self.add_stick(8, 9)
        self.add_stick(9, 10)
        self.add_stick(10, 11)
        self.add_stick(11, 12)
        self.add_stick(12, 13)

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
        x = math.cos(self.angle1) * 50 + 700
        y = math.sin(self.angle1) * 50 + WINDOW_HEIGHT / 2
        self.particles[0].pos.x = x
        self.particles[0].pos.y = y
        self.angle1 += self.anglespeed1

        x = math.cos(self.angle2) * 50 + 100
        y = math.sin(self.angle2) * 50 + WINDOW_HEIGHT / 2
        self.particles[len(self.particles) - 1].pos.x = x
        self.particles[len(self.particles) - 1].pos.y = y
        self.angle2 += self.anglespeed2

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
    app = Verlet6()
    app.loop()
