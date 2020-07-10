"""The Toucan Game Engine."""

from abc import ABC, abstractmethod
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

try:
    import pygame
    import pygame.gfxdraw
except ImportError:
    print("pygame not available")
    pygame = None
    quit()


class Vector2(pygame.Vector2):
    """A 2D Vector."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        

    def limit(self, maxsize):
        if self.magnitude > maxsize:
            self.scale_to_length(maxsize)


class Vector3(pygame.Vector3):
    """A 3D Vector."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        


# pylint: disable=too-many-instance-attributes
class Component():

    def __init__(self, name: str):
        self.active: bool = True
        self.name: str = name
        self.parent: Node = None

    @abstractmethod
    def update(self, time_delta: float):
        """Update this component."""
        pass

    @abstractmethod
    def draw(self):
        """Do drawing in the method."""
        pass

    def set_active(self, flag: bool):
        """Set this component active or inactive."""
        self.active = flag

    def is_active(self) -> bool:
        """Gets a boolean value indicating wether this component is active or inactive."""
        return self.active


# pylint: disable=too-many-instance-attributes
class Node():

    def __init__(self, name: str):
        self.position: Vector3 = Vector3(0, 0, 0)
        self.rotation: float = 0.0
        self.scale: Vector3 = Vector3(0, 0, 0)
        self.active: bool = True
        self.name: str = name

        self.tag = None
        self.parent = None
        self.children = []
        self.components = []

    def add_node(self, new_node: "Node"):
        """Add a childnode to this node."""
        self.children.append(new_node)
        new_node.parent = self

    def add_componenet(self, new_component: Component):
        """Add a component to this node."""
        for component in self.components:
            if type(component) == type(new_component):
                print(f"Component type {str(type(component))} already exists")
                return

        self.components.append(new_component)
        new_component.parent = self

    def get_component_by_name(self, component_name: str):
        """Find a component on the current node with the given name."""
        for component in self.components:
            if component.name == component_name:
                return component

        return None

    def get_component_by_type(self, component_type: type):
        """Find a component on the current node with the given type."""
        for component in self.components:
            if type(component) == component_type:
                return component

        return None

    def set_active(self, flag: bool):
        """Set this node active or inactive."""
        self.active = flag

    def is_active(self) -> bool:
        """Gets a boolean value indicating wether this node is active or inactive."""
        return self.active


class Toucan():
    """The Toucan Game Engine main Class."""
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    GRAY = [200, 200, 200]

    current = None

    def __init__(self, title: str, width: int, height: int):
        """Initialize the game engine."""
        if self.current is not None:
            print("You can oly have 1 instance of class Toucan")
            quit()

        Toucan.current = self

        self.root: Node = Node("root")
        self.screen = None
        self.clock = None
        self.text_print = None
        self.disabled = True
        self.key_callback = None
        self.mouse_callback = None
        self.done = False
        self.time_delta = 0
        self.clear_color = Toucan.BLACK
        self.target_fps = 60
        self.render_fps = True

        self.init(title, width, height)


    def init(self, title: str, width: int, height: int):
        if pygame is None:
            return

        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        # self.textPrint = TextPrint()
        self.disabled = False

        self.set_mouse_callback(self.mouse_event)
        self.set_key_callback(self.key_event)

    def set_clear_color(self, color):
        """Sets the color that will be used as the background."""
        self.clear_color = color

    def set_target_fps(self, fps: int):
        """Set the target FPS."""
        self.target_fps = fps

    def add_componenet(self, component: Component):
        """Add a component to the root node."""
        self.root.add_componenet(component)

    def add_node(self, node: Node):
        """Add a child node to the root node."""
        self.root.add_node(node)

    def mouse_event(self, x: int, y: int):
        pass

    def key_event(self, key: str):
        pass

    def update(self, node: Node, time_delta: float):
        """Update all nodes / components."""
        for component in node.components:
            component.update(time_delta)
        for node in node.children:
            self.update(node, time_delta)

    def draw(self, node: Node):
        """Draw all nodes / components."""
        for component in node.components:
            component.draw()
        for node in node.children:
            self.draw(node)

    def loop(self):
        """The game loop. The will run during the entire game."""
        self.setup()

        # Loop until the user clicks the close button.
        while not self.done:

            self.done = self.query_events()

            # Set the screen background
            self.fill(self.clear_color)

            # Show FPS in top left corner
            if self.render_fps:
                self.print(f"{self.fps():.2f}")

            # Do physics
            self.update(self.root, self.time_delta)

            # Draw everything
            self.draw(self.root)

            # Update screen
            self.flip()

        self.cleanup()

        # Exit
        self.quit()

    def setup(self):
        pass

    def cleanup(self):
        pass

    def run(self):
        self.loop()

    def set_key_callback(self, cb):
        self.keyCallback = cb

    def set_mouse_callback(self, cb):
        self.mouseCallback = cb 

    def quit(self):
        if pygame is None or self.disabled:
            return
        pygame.quit()

    def fill(self, color):
        if pygame is None or self.disabled:
            return
        self.screen.fill(color)

    def flip(self):
        if pygame is None or self.disabled:
            return
        pygame.display.flip()
        self.timeDelta = self.clock.tick(self.target_fps)
        self.timeDelta /= 1000 # Convert milliseconds to seconds
        # ICI self.textPrint.reset()

    def fps(self):
        if pygame is None or self.disabled:
            return 0
        return self.clock.get_fps()
    
    def print(self, value: str):
        if pygame is None or self.disabled:
            return
        # ICI self.textPrint.print(self.screen, value, Toucan.WHITE)

    def print_centered(self, x, y, value):
        if pygame is None or self.disabled:
            return
        # ICI self.textPrint.printCentered(self.screen, x, y, value)

    def circle_no_aa(self, x, y, r, color, line_width = 1):
        if pygame is None or self.disabled:
            return
        pygame.draw.circle(self.screen, color, [int(x), int(y)], int(r), line_width)

    def circle(self, x, y, r, color):
        if pygame is None or self.disabled:
            return
        pygame.gfxdraw.aacircle(self.screen, int(x), int(y), r, color)

    def filled_circle(self, x, y, r, color):
        if pygame is None or self.disabled:
            return

        pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), r, color)

    def line(self, x1, y1, x2, y2, color, line_width = 1):
        if pygame is None or self.disabled:
            return

        pygame.draw.aaline(self.screen, color, [x1, y1], [x2, y2], line_width)

    def rectangle(self, x1, y1, x2, y2, color, line_width = 1):
        if pygame is None or self.disabled:
            return

        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)		
        pygame.draw.rect(self.screen, color, rect, line_width)

    def load_image(self, filename: str):
        img = pygame.image.load(filename)
        return img

    def draw_image(self, image, x, y, rect = None):
        self.screen.blit(image, (x, y), rect)

        # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit
        # blit(source, dest, area=None, special_flags=0) -> Rect

    def process_keys(self, key):
        return {
            pygame.K_a: lambda: "A",
            pygame.K_b: lambda: "B",
            pygame.K_c: lambda: "C",
            pygame.K_d: lambda: "D",
            pygame.K_e: lambda: "E",
            pygame.K_f: lambda: "F",
            pygame.K_g: lambda: "G",
            pygame.K_h: lambda: "H",
            pygame.K_i: lambda: "I",
            pygame.K_j: lambda: "J",
            pygame.K_k: lambda: "K",
            pygame.K_l: lambda: "L",
            pygame.K_m: lambda: "M",
            pygame.K_n: lambda: "N",
            pygame.K_o: lambda: "O",
            pygame.K_p: lambda: "P",
            pygame.K_q: lambda: "Q",
            pygame.K_r: lambda: "R",
            pygame.K_s: lambda: "S",
            pygame.K_t: lambda: "T",
            pygame.K_u: lambda: "U",
            pygame.K_v: lambda: "V",
            pygame.K_w: lambda: "W",
            pygame.K_x: lambda: "X",
            pygame.K_y: lambda: "Y",
            pygame.K_z: lambda: "Z",
        }.get(key, lambda: None)()

    def query_events(self):
        if pygame == None or self.disabled:
            return False
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                return True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.mouseCallback != None:
                    self.mouseCallback(pos[0], pos[1])
            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If so
                # adjust speed.
                # see https://www.pygame.org/docs/ref/key.html
                key = None
                if event.key == pygame.K_ESCAPE:
                    return True 
                else:
                    key = self.process_keys(event.key)
                
                if key != None and self.keyCallback != None:
                    self.keyCallback(key)

        return False


class AnimatedSpriteRenderer(Component):

    def __init__(self, image, name: str = None):
        Component.__init__(self, "AnimatedSpriteRenderer" if name is None else name)
        self.image = image
        self.rows = 1
        self.columns = 2
        self.width = image.get_width()
        self.height = image.get_height()

        self.framecount = self.rows * self.columns
        self.frame = 0

        self.framewidth = self.width // self.columns
        self.frameheight = self.height // self.rows

    def update(self, time_delta: float):
        self.frame = (self.frame + 1) % self.framecount

    def draw(self):
        x = self.parent.position.x
        y = self.parent.position.y
        Toucan.current.draw_image(self.image, x, y)


class SpriteRenderer(Component):

    def __init__(self, image, name: str = None):
        Component.__init__(self, "SpriteRenderer" if name is None else name)
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

    def update(self, time_delta: float):
        pass

    def draw(self):
        x = self.parent.position.x
        y = self.parent.position.y
        Toucan.current.draw_image(self.image, x, y)


class CircleCollider(Component):

    def __init__(self, radius: float, name: str = None):
        Component.__init__(self, "CircleCollider" if name is None else name)
        self.radius = radius

    def update(self, time_delta: float):
        pass

    def draw(self):
        pass


class BoxCollider(Component):

    def __init__(self, name: str = None):
        Component.__init__(self, "BoxCollider" if name is None else name)

    def update(self, time_delta: float):
        pass

    def draw(self):
        pass


class FpsDisplay(Component):
    """Displays the FPS on the screens."""

    def __init__(self, name: str = None):
        Component.__init__(self, "FpsDisplay" if name is None else name)

    def draw(self):
        pass


class CircleShape(Component):
    """Displays a circle on screen"""

    def __init__(self, r: int, name: str = None):
        Component.__init__(self, "CircleShape" if name is None else name)
        self.radius = r

    def draw(self):
        Toucan.current.filled_circle(self.parent.position.x, self.parent.position.y, self.radius, Toucan.GREEN)


class RectangleShape(Component):
    """Displays a rectangle on screen"""

    def __init__(self, w: int, h: int, name: str = None):
        Component.__init__(self, "RectangleShape" if name is None else name)
        self.width = w
        self.height = h
    
    def draw(self):
        Toucan.current.rectangle(self.parent.position.x - self.width / 2, 
                                self.parent.position.y - self.height / 2,
                                self.parent.position.x + self.width / 2, 
                                self.parent.position.y + self.height / 2, 
                                Toucan.RED, 
                                0)


if __name__ == "__main__":
    pass
