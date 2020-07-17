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
        self.value = perlin_noise(self.nx, self.ny, nz)
        cv = (self.value + 1) / 2.0
        self.color = (int(cv * 255), int(cv * 255), int(cv * 255))


class MarchingSquares(Graphics):

    square_size = 20

    def __init__(self):
        super().__init__("MarchingSquares Demo", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.lines = []
        self.dots = []
        self.frames = 0
        self.noise_scale = 10
        self.noisez = 0.01
        self.noisez_delta = 0.02
        self.squares_x = int(WINDOW_WIDTH / self.square_size + 1)
        self.squares_y = int(WINDOW_HEIGHT / self.square_size + 1)

    def add_dot(self, sx, sy, nx, ny):
        w = Dot(sx, sy, nx, ny)
        self.dots.append(w)

    def setup(self):
        for yy in range(self.squares_y):
            row = []
            y = yy * self.square_size
            py = y / WINDOW_HEIGHT 
            ny = py * self.noise_scale
            for xx in range(self.squares_x):
                x = xx * self.square_size
                px = x / WINDOW_WIDTH
                nx = px * self.noise_scale
                
                w = Dot(x, y, nx, ny)
                row.append(w)

            self.dots.append(row)

    def cleanup(self):
        pass

    def draw(self):
        self.frames += 1

        for l in self.lines:
            l.render(self)

        #for row in self.dots:
        #    for col in row:
        #        col.render(self)

    def update(self, timeDelta):
        self.noisez += self.noisez_delta
        for row in self.dots:
            for col in row:
                col.update(self.noisez)

        self.lines.clear()
        halfsize = self.square_size / 2
        for y in range(self.squares_y - 1):
            for x in range(self.squares_x - 1):
                msq = self.getMsq(x, y)
                xx = x * self.square_size
                yy = y * self.square_size
                if msq == 1:
                    line = Line(xx + halfsize, yy, xx, yy + halfsize)
                    self.lines.append(line)
                elif msq == 2:
                    line = Line(xx + halfsize, yy, xx + self.square_size, yy + halfsize)
                    self.lines.append(line)
                elif msq == 3:
                    line = Line(xx, yy + halfsize, xx + self.square_size, yy + halfsize)
                    self.lines.append(line)
                elif msq == 4:
                    line = Line(xx + halfsize, yy + self.square_size, xx + self.square_size, yy + halfsize)
                    self.lines.append(line)
                elif msq == 5:
                    line = Line(xx, yy + halfsize, xx + halfsize, yy + self.square_size)
                    self.lines.append(line)
                    line = Line(xx + halfsize, yy, xx + self.square_size, yy + halfsize)
                    self.lines.append(line)
                elif msq == 6:
                    line = Line(xx + halfsize, yy, xx + halfsize, yy + self.square_size)
                    self.lines.append(line)
                elif msq == 7:
                    line = Line(xx, yy + halfsize, xx + halfsize, yy + self.square_size)
                    self.lines.append(line)
                elif msq == 8:
                    line = Line(xx, yy + halfsize, xx + halfsize, yy + self.square_size)
                    self.lines.append(line)
                elif msq == 9:
                    line = Line(xx + halfsize, yy, xx + halfsize, yy + self.square_size)
                    self.lines.append(line)
                elif msq == 10:
                    line = Line(xx, yy + halfsize, xx + halfsize, yy)
                    self.lines.append(line)
                    line = Line(xx + halfsize, yy + self.square_size, xx + self.square_size, yy + halfsize)
                    self.lines.append(line)
                elif msq == 11:
                    line = Line(xx + halfsize, yy + self.square_size, xx + self.square_size, yy + halfsize)
                    self.lines.append(line)
                elif msq == 12:
                    line = Line(xx, yy + halfsize, xx + self.square_size, yy + halfsize)
                    self.lines.append(line)
                elif msq == 13:
                    line = Line(xx + halfsize, yy, xx + self.square_size, yy + halfsize)
                    self.lines.append(line)
                elif msq == 14:
                    line = Line(xx, yy + halfsize, xx + halfsize, yy)
                    self.lines.append(line)

    def getMsq(self, x, y):
        a = math.ceil(self.dots[y][x].value)
        b = math.ceil(self.dots[y][x + 1].value)
        c = math.ceil(self.dots[y + 1][x + 1].value)
        d = math.ceil(self.dots[y + 1][x].value)
        return d * 8 + c * 4 + b * 2 + a

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
