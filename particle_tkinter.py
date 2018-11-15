
class Circle():
    def __init__(self, canvas, posx, posy, rad, *args, **kargs):
        self.canvas = canvas
        self.circle = canvas.create_oval(
            float(posx - rad), float(posy - rad), float(posx + rad),
            float(posy + rad), *args, **kargs)
        self.x = float(posx)
        self.y = float(posy)
        self.r = rad

    def move_circle(self, dx, dy):
        self.canvas.move(self.circle, dx, dy)
        self.x += dx
        self.y += dy