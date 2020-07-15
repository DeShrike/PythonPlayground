from Graphics import Graphics, Vector2, Vector3
from PerlinNoise import perlin_noise
import random
import math


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

class Line():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def render(self, g: Graphics):
        g.line(self.x1, self.y1, self.x2, self.y2, Graphics.WHITE)


class Dot():
    def __init__(self, sx, sy, nx, ny):
        self.sx = sx
        self.sy = sy
        self.r = 5
        self.nx = nx
        self.ny = ny
        self.update(0)

    def render(self, g: Graphics):
        g.filled_circle(self.sx, self.sy, self.r, self.color)

    def update(self, nz):
        self.value = (perlin_noise(self.nx, self.ny, nz) + 1) / 2.0
        self.color = (int(self.value * 255), int(self.value * 255), int(self.value * 255))


class MarchingSquares(Graphics):

    square_size = 20
    squares = 30

    def __init__(self):
        super().__init__("MarchingSquares Demo", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.lines = []
        self.dots = []
        self.frames = 0
        self.noise_scale = 5
        self.noisez = 0.01
        self.noisez_delta = 0.05

    def add_dot(self, sx, sy, nx, ny):
        w = Dot(sx, sy, nx, ny)
        self.dots.append(w)

    def setup(self):
        for yy in range(self.squares):
            y = yy * self.square_size
            py = y / WINDOW_HEIGHT 
            ny = py * self.noise_scale
            for xx in range(self.squares):
                x = xx * self.square_size
                px = x / WINDOW_WIDTH
                nx = px * self.noise_scale
                self.add_dot(x, y, nx, ny)

    def cleanup(self):
        pass

    def draw(self):
        self.frames += 1

        for l in self.lines:
            l.render(self)

        for d in self.dots:
            d.render(self)

    def update(self, timeDelta):
        self.noisez += self.noisez_delta
        for dot in self.dots:
            dot.update(self.noisez)

    def to_angle(self, v: Vector2):
        vn = v.normalize()
        return math.atan2(vn.y, vn.x)

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")


if __name__ == "__main__":
    app = MarchingSquares()
    app.loop()
