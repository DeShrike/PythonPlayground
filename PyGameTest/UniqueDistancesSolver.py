import itertools
import random
import math

PEGGS = 7

class Pegg():
    def __init__(self, pos):
        self.pos = pos
        self.y = pos // PEGGS
        self.x = pos % PEGGS

    def advance(self):
        if self.pos < (PEGGS * PEGGS) - 1:
            self.pos += 1
            self.y = self.pos // PEGGS
            self.x = self.pos % PEGGS
            return True
        else:
            return False


class UniqueDistancesSolver():

    def __init__(self):
        self.positions = [x for x in range(PEGGS * PEGGS)]
        self.stack = []
        self.peggs = []

    def distance(self, a, b):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def measure(self):
        measures = {}
        for i, a in enumerate(self.peggs):
            for j, b in enumerate(self.peggs):
                if j > i:
                    continue
                if a == b:
                    continue
                d = self.distance(a, b)
                dd = f"{d:.4f}"
                if dd in measures:
                    measures[dd] += 1
                    # print("Measures: ", measures)
                    return False
                else:
                    measures[dd] = 1

        return True

    def createPegg(self, position):
        p = Pegg(position)
        self.peggs.append(p)

    def printPositions(self):
        pp = [x.pos for x in self.peggs]
        print("Positions", pp)

    def run(self):
        print(f"Solving {PEGGS} x {PEGGS}")
        self.createPegg(0)
        self.createPegg(1)
        popped = False
        count = 0
        while True:
            count += 1
            if popped == False and self.measure():
                popped = False
                if len(self.peggs) == PEGGS:
                    print(f"Found in {count} steps !")
                    self.printPositions()
                    break
                else:
                    last = self.peggs[-1]
                    if last.pos + 1 < PEGGS * PEGGS:
                        self.createPegg(last.pos + 1)
                    else:
                        if len(self.peggs) == 0:
                            print("No Solution !")
                            break
                        self.peggs.pop()
                        popped = True

            else:
                popped = False
                last = self.peggs[-1]
                if last.advance():
                    pass
                else:
                    if len(self.peggs) == 0:
                        print("No Solution !")
                        break
                    self.peggs.pop()
                    popped = True

            if count % 100000 == 0:
                self.printPositions()


if __name__ == "__main__":
    app = UniqueDistancesSolver()
    app.run()

