from pyglet.gl import *
import pyglet
import ctypes
import OpenGL.GL.shaders

# https://www.youtube.com/watch?v=bzz8PfKQpTk
# https://www.youtube.com/watch?v=NqSSWmpKppE

class Triangle():
	def __init__(self):
		self.vertices = pyglet.graphics.vertex_list(3, ('v3f', [-0.5, -0.5, 0.0,
																0.5, -0.5, 0.0,
																0.0, 0.5, 0.0]),
														('c3B', [100, 200, 220, 
																200, 220, 200,
																100, 250, 100]))

class Triangle2():
	def __init__(self):
		self.vertex = [-0.5, -0.5, 0.0,  0.5, -0.5, 0.0,  0.0, 0.5, 0.0]
		self.color = [0, 0, 255,  0, 255, 0,  255, 0, 0]
		
	def render(self):
		pyglet.graphics.draw(3, GL_TRIANGLES, ('v3f', self.vertex), ('c3B', self.color))


class Triangle3():
	def __init__(self):
		self.triangle = [-0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
						  0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
						  0.0,  0.5, 0.0,  0.0, 0.0, 1.0]
		# https://www.youtube.com/watch?v=chaIYg7_7KM
		self.vertex_shader_source = """
		#version 330
		in layout(location = 0) vec3 position;
		in layout(location = 1) vec3 color;

		out vec3 newColor;
		void main()
		{
			gl_Position = vec4(position, 1.0f);
			newColor = color;
		}
		"""
		self.fragment_shader_source = """
		#version 330
		in vec3 newColor;

		out vec4 outColor;
		void main()
		{
			outColor = vec4(newColor, 1.0f);
		}
		"""
		vertex_shader = str.encode(self.vertex_shader_source)
		fragment_shader = str.encode(self.fragment_shader_source)
		shader = OpenGL.GL.shaders.compileProgram(
			OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
			OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

		glUseProgram(shader)

		vbo = GLuint(0)
		glGenBuffers(1, vbo)
		glBindBuffer(GL_ARRAY_BUFFER, vbo)
		glBufferData(GL_ARRAY_BUFFER, 18 * 4, (GLfloat * len(self.triangle))(*self.triangle), GL_STATIC_DRAW)

		#postions
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
		glEnableVertexAttribArray(0)

		#colors
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(12))
		glEnableVertexAttribArray(1)

	def render(self):
		glDrawArrays(GL_TRIANGLES, 0, 3)


class Quad():
	def __init__(self):
		self.vertices = pyglet.graphics.vertex_list_indexed(4, [0, 1, 2, 2, 3, 0],
																('v3f', [-0.5, -0.5, 0.0,
																		0.5, -0.5, 0.0,
																		0.5, 0.5, 0.0,
																		-0.5, 0.5, 0.0]),
																('c3f', [ 1.0, 0, 0,
																		  0, 1.0, 0.0,
																		  0.0, 0.0, 1.0,
																		  1.0,1.0,1.0 ]))

class Quad2():
	def __init__(self):
		self.vertex = [-0.5, -0.5, 0.0,  0.5, -0.5, 0.0,   0.5, 0.5, 0.0,  -0.5, 0.5, 0.0]
		self.indexes = [0, 1, 2, 2, 3, 0]
		self.colors = [ 1.0, 0, 0,   0, 1.0, 0.0,  0.0, 0.0, 1.0,  0.0,0.0,0.0 ]
		self.vertices = pyglet.graphics.vertex_list_indexed(4, self.indexes, ('v3f', self.vertex), ('c3f', self.colors))

class Quad3():
	def __init__(self):
		self.vertex = [-0.5, -0.5, 0.0,  0.5, -0.5, 0.0,   0.5, 0.5, 0.0,  -0.5, 0.5, 0.0]
		self.indexes = [0, 1, 2, 2, 3, 0]
		self.colors = [ 1.0, 0, 0,   0, 1.0, 0.0,  0.0, 0.0, 1.0,  0.0,0.0,0.0 ]

	def render(self):
		self.vertices = pyglet.graphics.draw_indexed(4, GL_TRIANGLES, self.indexes, ('v3f', self.vertex), ('c3f', self.colors))

class MyWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_minimum_size(200, 200)
		glClearColor(0.2, 0.3, 0.2, 1.0)
		self.triangle = Triangle()
		self.triangle2 = Triangle2()
		self.triangle3 = Triangle3()
		self.quad = Quad()
		self.quad2 = Quad2()
		self.quad3 = Quad3()

	def on_draw(self):
		self.clear()
		# self.triangle.vertices.draw(GL_TRIANGLES)
		# self.quad.vertices.draw(GL_TRIANGLES)
		# self.quad2.vertices.draw(GL_TRIANGLES)
		# self.quad3.render()
		# self.triangle2.render()
		self.triangle3.render()

	def on_resize(self, width, height):
		glViewport(0, 0, width, height)

#window = pyglet.window.Window(320, 240, "Hello World")
#pyglet.app.run()

if __name__ == "__main__":
	window = MyWindow(320, 240, "ÔpenGL Window", resizable=True)
	# window.on_draw()
	pyglet.app.run()

