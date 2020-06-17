from Graphics import Graphics, Vector2, Vector3
import random
import math


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# https://medium.com/better-programming/making-a-verlet-physics-engine-in-javascript-1dff066d7bc5

class Wall(object):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def render(self, g: Graphics):
        g.rectangle(self.x, self.y, self.x + self.w, self.y + self.h, Graphics.GREEN, 0)

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

    def render(self, g: Graphics):
        g.filled_circle(self.pos.x, self.pos.y, 3, Graphics.WHITE)


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

    def render(self, g: Graphics):
        if self.hidden:
            return
        g.line(self.p0.pos.x, self.p0.pos.y, self.p1.pos.x, self.p1.pos.y, Graphics.WHITE)


class Verlet8(Graphics):

    def __init__(self):
        super().__init__("PyGame Verlet 8", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.particles = []
        self.sticks = []
        self.walls = []
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

    def add_wall(self, x, y, w, h):
        w = Wall(x, y, w, h)
        self.walls.append(w)

    def setup(self):
        border = 20
        self.add_wall(0, 0, WINDOW_WIDTH, border)
        # self.add_wall(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)

        self.add_wall(0, border, border, WINDOW_HEIGHT - 2 * border)
        self.add_wall(WINDOW_WIDTH - border, border, border, WINDOW_HEIGHT - 2 * border)

        self.add_particle(100, 100)
        self.add_particle(200, 50)
        self.add_particle(300, 100)
        self.add_particle(400, 50)
        self.add_particle(500, 100)
        self.add_particle(600, 150)
        self.add_particle(700, 200)
        self.add_stick(0, 1)
        self.add_stick(1, 2)
        self.add_stick(2, 3)
        self.add_stick(3, 4)
        self.add_stick(4, 5)
        self.add_stick(5, 6)

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
        for w in self.walls:
            w.render(self)

        for p in self.particles:
            p.render(self)

        for s in self.sticks:
            s.render(self)

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
                self.check_collisions(p)
                p.constrain_points(WINDOW_WIDTH, WINDOW_HEIGHT)

    def check_collisions(self, p: Particle):
        pass

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = Verlet8()
    app.loop()
