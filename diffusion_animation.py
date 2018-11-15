import pyglet
import pyglet.gl
from particle import Particle
import numpy as np


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.label = pyglet.text.Label('', font_name='Times New Roman',
                                       x=70, y=self.height - 10,
                                       anchor_x='center', anchor_y='center')
        self.label.color = (255, 255, 255, 100)

        # Properties of the particle:
        self.radius = 5.0
        self.particleList = []
        for _ in range(100):
            color = np.zeros(4)
            color[:3] = np.random.rand(3)
            color[3] = .3
            self.particleList.append(
                Particle(self.width / 2, self.height / 2, self.radius,
                         color=list(color)))

        # Proterties of the grid:
        self.dx = 2. * self.radius  # Spacing of the grid
        self.Nx = int(self.width / self.dx)  # Number of columns
        self.Ny = int(self.height / self.dx)  # Number of rows
        self.Np = len(self.particleList)  # Number of particles
        self.grid = np.zeros((self.Nx, self.Ny), dtype=float)

        self.count = 0
        self.entropy = 0
        self.maxentr = False
        print(np.log(self.Np))

    def on_draw(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                              pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

        # Drawing the planets
        for particle in self.particleList:
            particle.vertices.draw(pyglet.gl.GL_POLYGON)

        self.label.draw()

        self.fps_display.draw()
        self.fps_display.set_fps(50)

    def update(self, dt):

        for particle in self.particleList:
            step = np.random.randint(-1, 2, 2)

            # We limit the step in one direction:
            while np.count_nonzero(step) > 1:
                step[np.random.randint(len(step))] = 0

            particle.update(dt, step)
            if particle.pos[0] <= particle.r:
                particle.update(dt, np.array((2, 0)))
            elif particle.pos[0] >= self.width - particle.r:
                particle.update(dt, np.array((-2, 0)))
            if particle.pos[1] <= particle.r:
                particle.update(dt, np.array((0, 2)))
            elif particle.pos[1] >= self.height - particle.r:
                particle.update(dt, np.array((0, -2)))

            # We add the particle to the grid:
            self.grid[int(particle.pos[0] / self.dx),
                      int(particle.pos[1] / self.dx)] += 1

        self.entropy = 0.
        row = -1
        for j in range(self.Nx * self.Ny):
            if j % self.Ny == 0:
                row += 1
            col = j % self.Ny
            if self.grid[row, col] != 0.:
                self.entropy -= np.log(self.grid[row, col] / self.Np
                                       ) * self.grid[row, col] / self.Np

        # Refresh the entropy value display every 30 frames:
        if self.count % 30 == 0:
            self.label.text = 'Entropy = {}'.format(round(self.entropy, 3))

        # Refresh the number of particles per grid and sum 1 to count.
        self.grid *= 0.
        self.count += 1



if __name__ == '__main__':
    world = MyWindow(width=200, height=200)
    pyglet.gl.glClearColor(.1, .1, .1, .1)
    world.on_draw()

    pyglet.clock.schedule_interval(world.update, 1 / 60.)
    pyglet.app.run()
