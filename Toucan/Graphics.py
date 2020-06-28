from abc import ABC, abstractmethod
import os   
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
try:
    import pygame
    import pygame.gfxdraw
except ImportError:
    print("pygame not available")
    pygame = None

class Vector2(pygame.Vector2):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        

    def limit(self, maxsize):
        if self.magnitude > maxsize:
            self.scale_to_length(maxsize)

class Vector3(pygame.Vector3):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        

class TextPrint(object):
    """
    This is a simple class that will help us print to the screen.
    """
    
    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        if pygame == None:
            return
        self.font = pygame.font.SysFont("arial", 24)
 
    def print(self, my_screen, text_string, color):
        if pygame == None:
            return
        text_bitmap = self.font.render(text_string, True, color)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height
 
    def printCentered(self, my_screen, x, y, text_string, color):
        if pygame == None:
            return
        text_bitmap = self.font.render(text_string, True, color)
        textRect = text_bitmap.get_rect()
        textRect.center = (x, y)   
        my_screen.blit(text_bitmap, textRect)

    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15
 
    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10
 
    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10


class Graphics(ABC):
    """
    http://www.pygame.org/docs/ref/gfxdraw.html
    https://www.pygame.org/docs/ref/math.html
    """

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    GRAY = [200, 200, 200]

    def __init__(self, title: str, width: int, height: int):
        self.screen = None
        self.clock = None
        self.textPrint = None
        self.disabled = True
        self.keyCallback = None
        self.mouseCallback = None
        self.done = False
        self.timeDelta = 0
        self.clearColor = Graphics.BLACK
        self.targetFps = 60
        self.renderFps = True

        self.init(title, width, height)

    def init(self, title: str, width: int, height: int):

        if pygame == None:
            return

        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.textPrint = TextPrint()
        self.disabled = False

        self.setMouseCallback(self.mouseEvent)
        self.setKeyCallback(self.keyEvent)

    def setClearColor(self, color):
        self.clearColor = color

    def setTargetFps(self, fps: int):
        self.targetFps = fps

    def showFps(self, flag: bool):
        self.renderFps = flag

    @abstractmethod
    def mouseEvent(self, x: int, y: int):
        pass

    @abstractmethod
    def keyEvent(self, key: str):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    def loop(self):

        self.setup()

        # Loop until the user clicks the close button.
        while not self.done:

            self.done = self.queryEvents()

            # Set the screen background
            self.fill(self.clearColor)

            # Show FPS in top eft corner
            if self.renderFps:
                self.print(f"{self.fps():.2f}")
    
            # Do physics
            self.update(self.timeDelta)

            # Draw everything 
            self.draw()

            # Update screen
            self.flip()

        self.cleanup()
        
        # Exit
        self.quit()

    def setKeyCallback(self, cb):
        self.keyCallback = cb

    def setMouseCallback(self, cb):
        self.mouseCallback = cb 

    def quit(self):
        if pygame == None or self.disabled:
            return
        pygame.quit()

    def fill(self, color):
        if pygame == None or self.disabled:
            return
        self.screen.fill(color)

    def flip(self):
        if pygame == None or self.disabled:
            return
        pygame.display.flip()
        self.timeDelta = self.clock.tick(self.targetFps)
        self.timeDelta /= 1000 # Convert milliseconds to seconds
        self.textPrint.reset()

    def fps(self):
        if pygame == None or self.disabled:
            return 0
        return self.clock.get_fps()
    
    def print(self, value: str):
        if pygame == None or self.disabled:
            return
        self.textPrint.print(self.screen, value, Graphics.WHITE)

    def printCentered(self, x, y, value):
        if pygame == None or self.disabled:
            return
        self.textPrint.printCentered(self.screen, x, y, value)

    def circle_(self, x, y, r, color, lineWidth = 1):
        if pygame == None or self.disabled:
            return
        pygame.draw.circle(self.screen, color, [int(x), int(y)], int(r), lineWidth)

    def circle(self, x, y, r, color):
        if pygame == None or self.disabled:
            return
        pygame.gfxdraw.aacircle(self.screen, int(x), int(y), r, color)

    def filled_circle(self, x, y, r, color):
        if pygame == None or self.disabled:
            return
        pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), r, color)

    def line(self, x1, y1, x2, y2, color, lineWidth = 1):
        if pygame == None or self.disabled:
            return
        pygame.draw.aaline(self.screen, color, [x1, y1], [x2, y2], lineWidth)

    def rectangle(self, x1, y1, x2, y2, color, lineWidth = 1):
        if pygame == None or self.disabled:
            return

        r = pygame.Rect(x1, y1, x2 - x1, y2 - y1)		
        pygame.draw.rect(self.screen, color, r, lineWidth)

    def processKeys(self, key):
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

    def queryEvents(self):
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
                    key = self.processKeys(event.key)
                
                if key != None and self.keyCallback != None:
                    self.keyCallback(key)

        return False
