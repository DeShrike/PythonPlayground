from typing import List, Optional, Union, Dict
import time
import random


class Link(object):

    def __init__(self, a: "Node", b: "Node", cost: int = 0):
        self.cost = cost
        self.a = a
        self.b = b


class Node(object):

    def __init__(self, id: any, name: str, x: int, y: int, userdata: any = None):
        self.userdata = userdata
        self.name = name
        self.id = id
        self.links: List[Link] = []
        self.g_score = 999_999_999
        self.f_score = 999_999_999
        self.h_score = self.g_score + self.f_score
        self.came_from = None
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Node({self.id}, {self.name}, {self.x}, {self.y})"

    def get_neighbours(self):
        n = []
        for l in self.links:
            if l.a != self:
                if l.a not in n:
                    n.append(l.a)
            if l.b != self:
                if l.b not in n:
                    n.append(l.b)
        return n

    def weight_to(self, to) -> float:
        for l in self.links:
            if l.a == to or l.b == to:
                return l.cost
        return None


class Graph(object):

    def __init__(self):
        self.nodes: Dict[Node] = {}

    def add_node(self, id: any, name: str, x: int, y: int, userdata: any = None):
        n = Node(id, name, x, y, userdata)
        self.nodes[id] = n

    def add_link(self, ida: any, idb: Node, cost: int = 0):
        a = self.nodes[ida]
        b = self.nodes[idb]
        l = Link(a, b, cost)
        a.links.append(l)
        b.links.append(l)

    def print_info(self):
        for key, n in self.nodes.items():
            print(f"Node {n.name}", n.id)
            for l in n.links:
                print(f"  Link - Cost {l.cost} - From {l.a.name} To {l.b.name}")                
            # aaaa = input()

    @staticmethod
    def generate_from_grid(grid, allow_diagonals: bool) -> "Graph":
        g = Graph()
        height = len(grid)
        width = len(grid[0])

        for y in range(height):
            for x in range(width):
                if grid[y][x] != 0:
                    continue
                g.add_node((x, y), f"NODE:{x},{y}", x, y)

        for y in range(height):
            for x in range(width):
                if grid[y][x] != 0:
                    continue
                a = (x, y)
                if x < width - 1:
                    if grid[y][x + 1] == 0:
                        b = (x + 1, y)
                        g.add_link(a, b, 1)
                if y < height - 1:
                    if grid[y + 1][x] == 0:
                        b = (x, y + 1)
                        g.add_link(a, b, 1)
                if allow_diagonals:
                    if y < height - 1 and x < width - 1:
                        if grid[y + 1][x + 1] == 0 and grid[y + 1][x] == 0 and grid[y][x + 1] == 0:
                            b = (x + 1, y + 1)
                            g.add_link(a, b, 1.41)
                    if y < height - 1 and x > 0:
                        if grid[y + 1][x - 1] == 0 and grid[y + 1][x] == 0 and grid[y][x - 1] == 0:
                            b = (x - 1, y + 1)
                            g.add_link(a, b, 1.41)

        return g


class Astar(object):

    def __init__(self, graph: Graph):
        self.graph = graph

    # def equal(self, current: Noode, end: noode) -> bool:
    #    return current.x == end.x and current.y == end.y

    def heuristic(self, current: Node, other: Node) -> int:
        return (current.x - other.x) ** 2 + (current.y - other.y) ** 2

    def reconstruct_path(self, came_from, current: Node):
        path = []
        while current.came_from != None:
            path.append(current)
            current = current.came_from

        return path

    def find_lowest_f_score_node(self, openset):
        lowest_f_score = 999_999_999
        node = None
        for n in openset:
            if n.f_score < lowest_f_score:
                node = n
                lowest_f_score = n.f_score
        return node

    def get_path(self, start: any, goal: any) -> List[Node]:
        # see https://en.wikipedia.org/wiki/A*_search_algorithm
        print(f"Path from {start} to {goal}")
        start_node = self.graph.nodes[start]
        goal_node = self.graph.nodes[goal]

        openset = [start_node]
        came_from = []

        start_node.g_score = 0
        start_node.f_score = self.heuristic(start_node, goal_node)

        while len(openset) > 0:
            current = self.find_lowest_f_score_node(openset)
            # print(f"Current: {current.id}")
            if current.id == goal:
                return self.reconstruct_path(came_from, current)

            openset.remove(current)

            neighbours = current.get_neighbours()
            # print(neighbours)
            for neighbor in neighbours:
                # d(current,neighbor) is the weight of the edge from current to neighbor
                # tentative_gScore is the distance from start to the neighbor through current
                tentative_g_score = current.g_score + current.weight_to(neighbor)
                # print(f"if {tentative_g_score} < {neighbor.g_score}")
                if tentative_g_score < neighbor.g_score:
                    # This path to neighbor is better than any previous one. Record it!
                    neighbor.came_from = current
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = neighbor.g_score + self.heuristic(neighbor, goal_node)
                    if neighbor not in openset:
                        openset.append(neighbor)                

        return None

########################################################
########################################################
########################################################

def print_grid(grid):
    for line in grid:
        for col in line:
            if col == 0:
                print(".", end = "")
            if col == 1:
                print("#", end = "")
            if col == 2:
                print("o", end = "")
        print("")

def Main():
    gridsizex = 40
    gridsizey = 20

    grid = [[0 for x in range(gridsizex)] for y in range(gridsizey)]

    for y in range(0, gridsizey - 5):
        grid[y][5] = 1
    grid[gridsizey // 2][6] = 1
    grid[gridsizey // 2][4] = 1

    for y in range(5, gridsizey):
        grid[y][10] = 1
    grid[gridsizey // 2][11] = 1
    grid[gridsizey // 2][9] = 1

    for y in range(0, gridsizey - 5):
        grid[y][15] = 1
    grid[gridsizey // 2][16] = 1
    grid[gridsizey // 2][14] = 1

    for y in range(5, gridsizey):
        grid[y][20] = 1
    grid[gridsizey // 2][21] = 1
    grid[gridsizey // 2][19] = 1

    for y in range(0, gridsizey - 5):
        grid[y][25] = 1
    grid[gridsizey // 2][26] = 1
    grid[gridsizey // 2][24] = 1

    for y in range(5, gridsizey):
        grid[y][30] = 1
    grid[gridsizey // 2][31] = 1
    grid[gridsizey // 2][29] = 1

    for y in range(0, gridsizey - 5):
        grid[y][35] = 1
    grid[gridsizey // 2][36] = 1
    grid[gridsizey // 2][37] = 1
    grid[gridsizey // 2][34] = 1

    print_grid(grid)

    g = Graph.generate_from_grid(grid, True)
    # g.print_info()

    astar = Astar(g)
    p = astar.get_path((1, gridsizey // 3), (gridsizex - 3, 3))
    # print("Result Path:")
    # print(p)

    for node in p:
        grid[node.y][node.x] = 2

    print_grid(grid)


if __name__ == "__main__":
    Main()

