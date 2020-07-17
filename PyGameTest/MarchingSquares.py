from Graphics import Graphics, Vector2, Vector3
from PerlinNoise import perlin_noise
import random
import math


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


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
        #cv = (self.value + 1) / 2.0
        #self.color = (int(cv * 255), int(cv * 255), int(cv * 255))


class MarchingSquares(Graphics):

    square_size = 20
    smoothing = False

    def __init__(self):
        super().__init__("MarchingSquares Demo", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.dots = []
        self.frames = 0
        self.noise_scale = 10
        self.noisez = 0.01
        self.noisez_delta = 0.02
        self.squares_x = int(WINDOW_WIDTH / self.square_size + 1)
        self.squares_y = int(WINDOW_HEIGHT / self.square_size + 1)
        self.halfsize = self.square_size / 2

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

    def draw_line(self, point1, point2):
        self.line(point1[0], point1[1], point2[0], point2[1], Graphics.WHITE)

    def draw(self):
        self.frames += 1

        #for row in self.dots:
        #    for col in row:
        #        col.render(self)

        for y in range(self.squares_y - 1):
            for x in range(self.squares_x - 1):
                xx = x * self.square_size
                yy = y * self.square_size
                msq, ab, bc, ad, dc = self.get_msq(x, y, xx, yy)
                if msq == 1:
                    self.draw_line(ab, ad)
                elif msq == 2:
                    self.draw_line(ab, bc)
                elif msq == 3:
                    self.draw_line(ad, bc)
                elif msq == 4:
                    self.draw_line(bc, dc)
                elif msq == 5:
                    self.draw_line(ad, dc)
                    self.draw_line(ab, bc)
                elif msq == 6:
                    self.draw_line(ab, dc)
                elif msq == 7:
                    self.draw_line(ad, dc)
                elif msq == 8:
                    self.draw_line(ad, dc)
                elif msq == 9:
                    self.draw_line(ab, dc)
                elif msq == 10:
                    self.draw_line(ad, ab)
                    self.draw_line(dc, bc)
                elif msq == 11:
                    self.draw_line(dc, bc)
                elif msq == 12:
                    self.draw_line(ad, bc)
                elif msq == 13:
                    self.draw_line(ab, bc)
                elif msq == 14:
                    self.draw_line(ad, ab)

    def update(self, timeDelta):
        self.noisez += self.noisez_delta
        for row in self.dots:
            for col in row:
                col.update(self.noisez)

    def get_msq(self, x, y, screen_x, screen_y):
        aa = self.dots[y][x].value
        bb = self.dots[y][x + 1].value
        cc = self.dots[y + 1][x + 1].value
        dd = self.dots[y + 1][x].value
        a = math.ceil(aa)
        b = math.ceil(bb)
        c = math.ceil(cc)
        d = math.ceil(dd)
        if self.smoothing:
            ab = (screen_x + self.interpolate(aa, bb), screen_y)
            bc = (screen_x + self.square_size, screen_y + self.interpolate(bb, cc))
            ad = (screen_x, screen_y + self.interpolate(aa, dd))
            dc = (screen_x + self.interpolate(dd, cc), screen_y + self.square_size)
        else:
            ab = (screen_x + self.halfsize, screen_y)
            bc = (screen_x + self.square_size, screen_y + self.halfsize)
            ad = (screen_x, screen_y + self.halfsize)
            dc = (screen_x + self.halfsize, screen_y + self.square_size)
        return (d * 8 + c * 4 + b * 2 + a, ab, bc, ad, dc)

    def interpolate(self, i, j):
        return self.halfsize + ((j - i) * self.square_size )

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
