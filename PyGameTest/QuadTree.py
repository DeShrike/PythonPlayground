import random
import math


def CircleRectIntersects(circle, rect):

    cx = circle.x
    cy = circle.y
    radius = circle.r
    rx = rect.cx - rect.w
    ry = rect.cy - rect.h
    rw = rect.w * 2
    rh = rect.h * 2

    # temporary variables to set edges for testing
    testX = cx;
    testY = cy;

    # which edge is closest?
    if cx < rx:
        testX = rx      # test left edge
    elif cx > rx + rw:
        testX = rx + rw    # right edge
  
    if cy < ry:         
        testY = ry      # top edge
    elif cy > ry + rh:
        testY = ry + rh   #bottom edge

    # get distance from closest edges
    distX = cx - testX;
    distY = cy - testY;
    distance = math.sqrt( (distX * distX) + (distY * distY) )

    # if the distance is less than the radius, collision!
    if distance <= radius:
        return True
  
    return False


class QuadTreePoint():

    def __init__(self, x, y, userdata = None):
        self.x = x
        self.y = y
        self.userdata = userdata

    def __repr__(self):
        return f"QuadTreePoint({self.x}, {self.y})"


class CircleRange():

    def __init__(self, x: int, y: int, r: int):
        self.x = x
        self.y = y
        self.r = r

    def __repr__(self):
        return f"CircleRange({self.x}, {self.y}, {self.r})"

    def contains(self, point: QuadTreePoint) -> bool:
        dist = math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
        return dist <= self.r

    def intersectsRectangle(self, rect: "RectangleRange") -> bool:
        return CircleRectIntersects(self, rect)

    def intersectsCircle(self, circle: "CircleRange") -> bool:
        dist = math.sqrt((self.x - circle.x) ** 2 + (self.y - circle.y) ** 2)
        return dist <= self.r + circle.r


class RectangleRange():

    def __init__(self, cx: int, cy: int, w: int, h: int):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h

    def __repr__(self):
        return f"RectangleRange({self.cx}, {self.cy}, {self.w}, {self.h})"

    def contains(self, point: QuadTreePoint) -> bool:
        return (point.x >= self.cx - self.w and
            point.x <= self.cx + self.w and
            point.y >= self.cy - self.h and 
            point.y <= self.cy + self.h)

    def intersectsRectangle(self, range: "RectangleRange") -> bool:
        return not(range.cx - range.w > self.cx + self.w or
           range.cx + range.w < self.cx - self.w or
           range.cy - range.h > self.cy + self.h or
           range.cy + range.h < self.cy - self.h)

    def intersectsCircle(self, circle: "CircleRange") -> bool:
        return CircleRectIntersects(circle, self)


class QuadTree():

    CAPACITY = 5

    def __init__(self, boundary: RectangleRange, level = 0):
        self.boundary = boundary
        self.points = []
        self.ne = None
        self.nw = None
        self.se = None
        self.sw = None
        self.level = level

    def __str__(self):
        indent = "    " * self.level
        value = indent + f"QuadTree Level {self.level} \n"

        for p in self.points:
            value = value + indent + f"  Point {p.x}, {p.y} \n"

        if self.ne != None:
            value += str(self.ne)
        if self.nw != None:
            value += str(self.nw)
        if self.se != None:
            value += str(self.se)
        if self.sw != None:
            value += str(self.sw)

        return value

    def subdivide(self):
        if self.ne != None:
            return

        x = self.boundary.cx
        y = self.boundary.cy
        w = self.boundary.w
        h = self.boundary.h

        bne = RectangleRange(x + w // 2, y - h // 2, w // 2, h // 2)
        bnw = RectangleRange(x - w // 2, y - h // 2, w // 2, h // 2)
        bse = RectangleRange(x + w // 2, y + h // 2, w // 2, h // 2)
        bsw = RectangleRange(x - w // 2, y + h // 2, w // 2, h // 2)
        self.ne = QuadTree(bne, self.level + 1)
        self.nw = QuadTree(bnw, self.level + 1)
        self.se = QuadTree(bse, self.level + 1)
        self.sw = QuadTree(bsw, self.level + 1)


    def insert(self, point: QuadTreePoint) -> bool:
        # self.points.append(point)
        # return True

        if self.boundary.contains(point) == False:
            return False

        if len(self.points) < self.CAPACITY or self.level > 5:
            self.points.append(point)
            return True
        else:
            self.subdivide()               
            if self.ne.insert(point):
                return True
            if self.se.insert(point):
                return True
            if self.nw.insert(point):
                return True
            if self.sw.insert(point):
                return True

            return False

    def all(self):
        found = [] + self.points
        if self.ne != None:
            found += self.ne.all()
            found += self.se.all()
            found += self.nw.all()
            found += self.sw.all()
        return found

    def queryRectangle(self, range: RectangleRange):
        found = []
        if self.boundary.intersectsRectangle(range) == False:
            return found
        for p in self.points:
            if range.contains(p):
                found.append(p)

        if self.ne != None:
            found += self.ne.queryRectangle(range)
            found += self.se.queryRectangle(range)
            found += self.nw.queryRectangle(range)
            found += self.sw.queryRectangle(range)

        return found

    def queryCircle(self, range: CircleRange):
        found = []
        if self.boundary.intersectsCircle(range) == False:
            return found
        for p in self.points:
            if range.contains(p):
                found.append(p)

        if self.ne != None:
            found += self.ne.queryCircle(range)
            found += self.se.queryCircle(range)
            found += self.nw.queryCircle(range)
            found += self.sw.queryCircle(range)

        return found
