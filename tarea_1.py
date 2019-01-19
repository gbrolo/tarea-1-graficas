import struct
from random import randint
import random

def char(c) :
    return struct.pack("=c", c.encode('ascii'))

def word(w) :
    return struct.pack("=h", w)

def dword(d) :
    return struct.pack("=l", d)

def color(r, g, b):
    return bytes([b, g, r])

class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = []
        self.clear()

    def clear(self):
        self.pixels = [
            [color(0, 0, 0) for x in range(self.width)]
            for y in range(self.height)
        ]

    def clearStatic(self):
        colors = [color(0,0,0), color(255,255,255)]

        self.pixels = [
            [random.choice(colors) for x in range(self.width)]
            for y in range(self.height)
        ]

    def clearColor(self):
        self.pixels = [
            [color(randint(0,255), randint(0,255), randint(0,255)) for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def write(self, filename):
        f = open(filename, 'bw')

        # file header 14 bytes
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header 40 bytes
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])

        f.close()

    def point(self, x, y, color):
        self.pixels[y][x] = color

    # 100x100 square
    def square(self, x, y, color):
        for i in range (x, x+100):
            for j in range (y, y+100):
                self.pixels[i][j] = color

    def diagonal(self, x, y, color):
        for y in range(self.height):
            self.pixels[y][y] = color

    def contourSquare(self, padding, color):
        # bottom line
        for x in range(padding, self.width - padding):
            self.pixels[padding][x] = color

        # top line
        for x in range(padding, self.width - padding):
            self.pixels[self.height - padding][x] = color

        # left line
        for x in range(padding, self.height - padding):
            self.pixels[x][padding] = color

        # right line
        for x in range(padding, self.height - padding):
            self.pixels[x][self.width - padding] = color

    def stars(self, colors):        
        loop = 0

        while (loop < 100):
            loop = loop + 1
            x = randint(0, self.width)
            y = randint(0, self.height)
            
            x2 = randint(0, self.width)
            y2 = randint(0, self.height)
            
            # star type 1
            try:
                self.point(x, y, random.choice(colors))            
            except:
                print('')

            # star type 2
            try:
                self.point(x2, y2, random.choice(colors)) 
                self.point(x2+1, y2, random.choice(colors))
                self.point(x2-1, y2, random.choice(colors))
                self.point(x2, y2+1, random.choice(colors))
                self.point(x2, y2-1, random.choice(colors))
            except:
                print('')

    def randomPoint(self):
        try:
            self.point(randint(0, self.height), randint(0, self.height), color(255,255,255))            
        except:
            print('')

    def contourSquarePoints(self, padding, color):
        # bottom point left
        self.pixels[padding][padding] = color

        # top point left
        self.pixels[self.height - padding][padding] = color

        # bottom point right
        self.pixels[padding][self.width - padding] = color

        # top point right
        self.pixels[self.height - padding][self.width - padding] = color


r = Bitmap(600, 400)
# 1 (10 puntos) por llenar su imagen entera de puntos blancos y negros
# r.clearStatic()

# 2 (10 puntos) por llenar su imagen entera de puntos de colores random
# r.clearColor()

# 3 (10 puntos) por renderizar una línea blanca en diagonal por el centro de su imagen.
# r.diagonal(10,10,color(255,255,255))

# 4 (10 puntos) por renderizar líneas blancas en toda la orilla de su imagen (4 lineas)
# r.contourSquare(10, color(255,255,255))

# 5 (20 puntos) por crear una escena de un cielo con estrellas
# r.stars([color(255,255,255), color(200,200,200)])

# 6 (05 puntos) por renderizar una imagen negra con un punto blanco en una ubicación random dentro de la imagen.
# r.randomPoint()

# (05 puntos) por renderizar una imagen negra con un punto blanco en cada esquina.
# r.contourSquarePoints(10, color(255,255,255))

# (10 puntos) por renderizar un cubo de 100 pixeles en el centro de su imagen
# r.square(150,250,color(255,255,255))

r.write('tarea_1.bmp')