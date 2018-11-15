import pyglet as pyglet
from numpy import array, pi, linspace, sin, cos


class Particle():

    def __init__(self, x, y, rad, color=[0, 255, 220, .7]):
        self.pos = array((x, y))
        self.r = rad

        N = 30
        self.clist = color * N
        self.vlist = []
        for angle in linspace(0, 2 * pi, N):
            self.vlist.append(self.r * cos(angle) + self.pos[0])
            self.vlist.append(self.r * sin(angle) + self.pos[1])

        self.vertices = pyglet.graphics.vertex_list(N, ('v2f', self.vlist),
                                                    ('c4f', self.clist))


    def update(self, dt, step):
        self.pos += step
        for i in range(len(self.vlist)):
            self.vlist[i] += step[i % 2]
        for i in range(len(self.vertices.vertices)):
            self.vertices.vertices[i] = self.vlist[i]
