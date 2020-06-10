from Graphics import Graphics, Vector2, Vector3
from QuadTree import QuadTree, QuadTreePoint, RectangleRange, CircleRange
import itertools
import random
import math

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

class Pegg():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MattParkerPuzzleManual(Graphics):

    # PEGGS = 3
    # SOLUTION = [0, 1, 5]

    # PEGGS = 4
    # SOLUTION = [0, 1, 6, 12]

    # PEGGS = 5
    # SOLUTION = [0, 1, 4, 11, 23]

    # PEGGS = 6
    # SOLUTION = [0, 1, 9, 23, 32, 35]

    # PEGGS = 7
    # SOLUTION = [0, 2, 9, 20, 21, 40, 48]

    PEGGS = 8
    SOLUTION = [0, 2, 9, 20, 21, 40, 48, 63]

    SIZE = WINDOW_WIDTH / PEGGS
    RADIUS = SIZE * 0.3

    def __init__(self):
        super().__init__("MattParkerPuzzle", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.showFps(False)
        self.selectedx = 0
        self.selectedy = 0
        self.selectedpegg = None

    def setup(self):
        self.peggs = []
        for i in range(self.PEGGS):
            p = Pegg(i, 0)
            self.peggs.append(p)

        self.setPeggs(self.SOLUTION)

    def setPeggs(self, positions):
        for ix, p in enumerate(positions):
            y = p // self.PEGGS
            x = p % self.PEGGS
            self.peggs[ix].x = x
            self.peggs[ix].y = y

    def cleanup(self):
        pass

    def draw(self):
        for i in range(self.PEGGS):
            self.line(0, i * self.SIZE, WINDOW_WIDTH, i * self.SIZE, Graphics.WHITE, 3)
        for i in range(self.PEGGS):
            self.line(i * self.SIZE, 0, i * self.SIZE, WINDOW_HEIGHT, Graphics.WHITE, 3)

        for pegg in self.peggs:
            self.filled_circle(self.SIZE * pegg.x + self.SIZE / 2, self.SIZE * pegg.y +self.SIZE / 2, int(self.RADIUS), Graphics.RED)

        for i, a in enumerate(self.peggs):
            for j, b in enumerate(self.peggs):
                if a == b:
                    continue
                d = self.distance(a, b)
                # print(f"From {i} to {j}: {d:.3f}")
        # aaa = input()

    def update(self, timeDelta):
        pass

    def distance(self, a, b):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def mouseEvent(self, x, y):
        print(f"mouseCallback: {x} {y}")
        gridx = int(x // self.SIZE)
        gridy = int(y // self.SIZE)
        print(f"{gridx} {gridy}")
        found = False
        for p in self.peggs:
            if p.x == gridx and p.y == gridy:
                found = True
                self.selectedx = gridx
                self.selectedy = gridy
                self.selectedpegg = p
                break

        if found == False:
            self.selectedpegg.x = gridx
            self.selectedpegg.y = gridy

        self.showResults()

    def showResults(self):
            print("Measuring")
            measures = {}
            perfect = True
            for i, a in enumerate(self.peggs):
                for j, b in enumerate(self.peggs):
                    if j > i:
                        continue
                    if a == b:
                        continue
                    d = self.distance(a, b)
                    dd = f"{d:.4f}"
                    if dd in measures:
                        perfect = False
                        measures[dd] += 1
                    else:
                        measures[dd] = 1
                    # print(f"From {i} to {j}: {d:.3f}")
            print(measures)
            if perfect:
                print("FOUND IT !!!!")

    def keyEvent(self, key):
        print(f"keyCallback: {key}")
        if key == "M":
            self.showResults()


class MattParkerPuzzle(Graphics):

    PEGGS = 5
    SIZE = WINDOW_WIDTH / PEGGS
    RADIUS = SIZE * 0.3

    def __init__(self):
        super().__init__("MattParkerPuzzle", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setClearColor(Graphics.BLACK)
        self.setTargetFps(60)
        self.positions = [x for x in range(self.PEGGS * self.PEGGS)]

    def setup(self):
        self.peggs = []
        for i in range(self.PEGGS):
            p = Pegg(i, 0)
            self.peggs.append(p)

        self.iter = enumerate(itertools.permutations(self.positions, self.PEGGS))
        ix, p = self.iter.__next__()
        self.setPeggs(p)

    def setPeggs(self, positions):
        for ix, p in enumerate(positions):
            y = p // self.PEGGS
            x = p % self.PEGGS
            self.peggs[ix].x = x
            self.peggs[ix].y = y

    def cleanup(self):
        pass

    def draw(self):
        for i in range(self.PEGGS):
            self.line(0, i * self.SIZE, WINDOW_WIDTH, i * self.SIZE, Graphics.WHITE, 3)
        for i in range(self.PEGGS):
            self.line(i * self.SIZE, 0, i * self.SIZE, WINDOW_HEIGHT, Graphics.WHITE, 3)

        for pegg in self.peggs:
            self.filled_circle(self.SIZE * pegg.x + self.SIZE / 2, self.SIZE * pegg.y + self.SIZE / 2, int(self.RADIUS), Graphics.RED)

    def update(self, timeDelta):
        ix, p = self.iter.__next__()
        self.setPeggs(p)

    def distance(self, a, b):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def showResults(self):
        print("Measuring")
        measures = {}
        perfect = True
        for i, a in enumerate(self.peggs):
            for j, b in enumerate(self.peggs):
                if j > i:
                    continue
                if a == b:
                    continue
                d = self.distance(a, b)
                dd = f"{d:.4f}"
                if dd in measures:
                    perfect = False
                    measures[dd] += 1
                else:
                    measures[dd] = 1
                # print(f"From {i} to {j}: {d:.3f}")
        print(measures)
        if perfect:
            print("FOUND IT !!!!")
            return True
        return False

    def mouseEvent(self, x, y):
        pass

    def keyEvent(self, key):
        print(f"keyCallback: {key}")
        if key == "M":
            self.showResults()

class Solve():

    PEGGS = 7

    def __init__(self):
        self.positions = [x for x in range(self.PEGGS * self.PEGGS)]

        self.peggs = []
        for i in range(self.PEGGS):
            p = Pegg(i, 0)
            self.peggs.append(p)

        self.iter = enumerate(itertools.permutations(self.positions, self.PEGGS))
        ix, p = self.iter.__next__()
        self.setPeggs(p)
        self.checks = 0

    def setPeggs(self, positions):
        for ix, p in enumerate(positions):
            y = p // self.PEGGS
            x = p % self.PEGGS
            self.peggs[ix].x = x
            self.peggs[ix].y = y

    def distance(self, a, b):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def measure(self):
        measures = {}
        self.checks += 1
        for i, a in enumerate(self.peggs):
            for j, b in enumerate(self.peggs):
                if j > i:
                    continue
                if a == b:
                    continue
                d = self.distance(a, b)
                dd = f"{d:.4f}"
                if dd in measures:
                    return False
                else:
                    measures[dd] = 1

        # print(measures)
        print("FOUND IT !!!!")
        print(f"{self.checks} measures")
        return True

    def goodOrder(self, p):
        for i in range(len(p) - 1):
            if p[i+1] < p[i]:
                return False
        return True

    def run(self):
        while True:
            ix, p = self.iter.__next__()
            if self.goodOrder(p) == False:
                continue
            self.setPeggs(p)
            if self.measure():
                print(p)
                break
            if ix % 10000 == 0:
                print(ix, p)

if __name__ == "__main__":
    app = MattParkerPuzzleManual()
    app.loop()

    # app = MattParkerPuzzle()
    # app.loop()

    # app = Solve()
    # app.run()

