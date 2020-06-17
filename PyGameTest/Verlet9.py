from Graphics import Graphics, Vector2, Vector3
import random
import math


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# https://medium.com/better-programming/making-a-verlet-physics-engine-in-javascript-1dff066d7bc5

class VectorShape(object):

    # shapes contain lines (x1, y1, x2, t2)
    sample_shape = [(-4, 0, 4, 0), (0, -4, 0, 4), (-4, 0, 0, -4), (0, 4, 4, 0), (-4, 4, 4, -4) ]

    def __init__(self, shape, x, y, rotation, scale = 1):
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale = scale

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_scale(self, scale):
        self.scale = scale

    def set_rotation(self, rotation):
        self.rotation = rotation

    def render(self, g: Graphics):
        for s in self.shape:
            # angle = self.rotation * (math.pi / 2) # degrees
            angle = self.rotation # radians

            new_x1 = math.cos(angle) * (s[0]) - math.sin(angle) * (s[1])
            new_y1 = math.sin(angle) * (s[0]) + math.cos(angle) * (s[1])
            new_x1 = self.x + new_x1 * self.scale
            new_y1 = self.y + new_y1 * self.scale

            new_x2 = math.cos(angle) * (s[2]) - math.sin(angle) * (s[3])
            new_y2 = math.sin(angle) * (s[2]) + math.cos(angle) * (s[3])
            new_x2 = self.x + new_x2 * self.scale
            new_y2 = self.y + new_y2 * self.scale

            g.line(new_x1, new_y1, new_x2, new_y2, Graphics.WHITE)


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
    gravity = 0.1
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

    def current_velocity(self):
        return (self.pos - self.oldpos) * Particle.friction

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


class Verlet9(Graphics):

    def __init__(self):
        super().__init__("PyGame Verlet 9 and Vector Graphics", WINDOW_WIDTH, WINDOW_HEIGHT)
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

    def add_particle(self, x, y, ox = None, oy = None) -> Particle:
        p = Particle(f"{len(self.particles)}", Vector2(x, y), Vector2(x if ox == None else ox, y if oy == None else oy))
        self.particles.append(p)
        return p

    def add_wall(self, x, y, w, h):
        w = Wall(x, y, w, h)
        self.walls.append(w)

    def setup(self):
        border = 5
        self.add_wall(0, 0, WINDOW_WIDTH, border)
        self.add_wall(0, WINDOW_HEIGHT - border, WINDOW_WIDTH, border)

        self.add_wall(0, border, border, WINDOW_HEIGHT - 2 * border)
        self.add_wall(WINDOW_WIDTH - border, border, border, WINDOW_HEIGHT - 2 * border)

        fishshape = [
            (-4, 0, 4, 0),
            (0, -4, 0, 4),
            (-4, 0, 0, -4),
            (0, 4, 4, 0),
            (-4, 4, 4, -4)
        ]

        self.fish = VectorShape(fishshape, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 0, 1)
        self.angle2 = 0
        self.angle1 = 0
        self.angledelta1 = 0.01
        self.angledelta2 = 0.1

        self.add_particle(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2 - 5, WINDOW_HEIGHT / 2 + 10)

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
        # for w in self.walls:
        #    w.render(self)

        for p in self.particles:
            p.render(self)

        for s in self.sticks:
            s.render(self)

        self.fish.render(self)

    def update(self, timeDelta):

        self.angle1 += self.angledelta1
        self.angle2 += self.angledelta2

        self.fish.set_scale((math.sin(self.angle2) + 2) * 3)

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

        self.fish.set_position(self.particles[0].pos.x, self.particles[0].pos.y)
        self.fish.set_rotation(self.to_angle(self.particles[0].current_velocity()) + math.pi / 4)

    def to_angle(self, v: Vector2):
        vn = v.normalize()
        return math.atan2(vn.y, vn.x)

    def check_collisions(self, p: Particle):
        pass

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = Verlet9()
    app.loop()
