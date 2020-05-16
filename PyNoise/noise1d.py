import queue
import random
import pygame 
from Graphics import Graphics

WIDTH = 512
HEIGHT = 100

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (128, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

graphics = Graphics()
graphics.init("Maze", (WIDTH, HEIGHT))

#########################################################################
#########################################################################
#########################################################################

# https://www.youtube.com/watch?v=6-0UaeJBumA
class Noide1D():

	width = 0
	output = []
	noiseSeed = []
	octaves = 9
	scalingBias = 20.0

	def __init__(self, width):
		self.width = width
		for i in range(self.width):
			f = random.random()
			self.noiseSeed.append(f)

	def generate(self):
		for x in range(self.width):
			noise = 0.0
			scale = 1.0
			scaleSum = 0.0
			for o in range(self.octaves):
				pitch = self.width >> o
				sample1 = int((x / pitch) * pitch)  	# integer division !!
				sample2 = int((sample1 + pitch) % self.width)
				blend = float(x - sample1) / float(pitch)
				sample = (1.0 - blend) * self.noiseSeed[sample1] + blend * self.noiseSeed[sample2]
				noise = noise + sample * scale
				if x == 1:
					print(o,scale)
				scaleSum = scaleSum + scale
				scale = scale / self.scalingBias

			self.output.append(noise / scaleSum)

	def draw(self):
		for x, n in enumerate(self.output):
			y = n * HEIGHT
			graphics.line(x, 0, x, y, 1, WHITE)

#########################################################################
#########################################################################
#########################################################################


#########################################################################
#########################################################################
#########################################################################


#########################################################################
#########################################################################
#########################################################################


#########################################################################
#########################################################################
#########################################################################


def run():
	done = False
	noise = Noide1D(WIDTH)
	noise.generate()
	while not done:
		done = graphics.queryQuit()
		graphics.fill(BLACK)

		noise.draw()

		graphics.flip()

	graphics.quit()


if __name__ == "__main__":
	run()
