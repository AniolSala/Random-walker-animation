from tkinter import *
import random as random
import numpy as np
from particle import Circle



class MyWindow(Tk):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)


class MyCanvas(Canvas):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.w = float(self['width'])
        self.h = float(self['height'])

        self.clist = []
        self.rad = 5.
        for _ in range(200):
            color = '#{}{}{}'.format(random.randint(
                1, 9), random.randint(1, 9), random.randint(1, 9))
            self.clist.append(Circle(self, self.w / 2, self.h / 2,
                                     self.rad, fill=color))

    def begin_anim(self):
        '''
        La idea és que fem l'espaiat dx = dy = 2r, de manera que si
        hi ha dues partícules que es sol·lapen una mica ja baixi
        l'entropia.
        '''
        dx = 2. * self.rad
        Nx = int(self.w / dx)
        Ny = int(self.h / dx)
        Np = len(self.clist)
        grid = np.zeros((Nx, Ny), dtype=float)

        count = 0
        maxentr = False
        while True:
            grid *= 0.
            for particle in self.clist:
                particle.move_circle(
                    random.randint(-1, 1), random.randint(-1, 1))
                # Boundary conditions:
                if particle.x <= particle.r:
                    particle.move_circle(2, 0)
                elif particle.x >= self.w - particle.r:
                    particle.move_circle(-2, 0)
                if particle.y <= particle.r:
                    particle.move_circle(0, 2)
                elif particle.y >= self.h - particle.r:
                    particle.move_circle(0, -2)

                # print(int(particle.x / dx), int(particle.y / dy))
                grid[int(particle.x / dx), int(particle.y / dx)] += 1

            entropy = 0.
            row = -1
            for j in range(Nx * Ny):
                if j % Ny == 0:
                    row += 1
                col = j % Ny
                if grid[row, col] != 0.:
                    entropy -= np.log(grid[row, col] / Np
                                      ) * grid[row, col] / Np
            if count == 0:
                display = self.create_text(50, 10, text='Entropy = {}'.format(
                    str(round(entropy, 3))), fill='white', width=100)
            elif count > 0 and count % 50 == 0:
                self.delete(display)
                display = self.create_text(50, 10, text='Entropy = {}'.format(
                    str(round(entropy, 3))), fill='white', width=100)

            if (round(entropy, 3) == round(np.log(Np), 3)) and not maxentr:
                print('Max entropy ({}) achieved with {} iterations.'.format(
                      round(np.log(Np), 3), count + 1))
                maxentr = True

            count += 1
            self.update()


if __name__ == '__main__':
    root = MyWindow()
    w, h = 700, 700
    root.geometry('{}x{}'.format(w, h))

    canvas = MyCanvas(root, width=w, height=h, bg='black')
    canvas.pack()

    canvas.begin_anim()

    root.mainloop()
