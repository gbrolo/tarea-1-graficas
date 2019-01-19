import struct

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

    # 6x6 square
    def square(self, x, y, color):
        for i in range (x, x+6):
            for j in range (y, y+6):
                self.pixels[i][j] = color

    # draw ears
    def drawEars(self, r):
        r.square(48, 25, color(255,255,255))
        r.square(48, 61, color(255,255,255))

        r.square(42, 31, color(255,255,255))
        r.square(42, 55, color(255,255,255))

    # draw body
    def drawBody(self, r):
        for i in range(25, 67, 6):
            r.square(36, i, color(255,255,255))
        
        for i in range(19, 73, 6):
            r.square(30, i, color(255,255,255))

            # eyes
            r.square(30, 31, color(0,0,0))
            r.square(30, 55, color(0,0,0))

        # full body
        for i in range(13, 78, 6):
            r.square(24, i, color(255,255,255))

        for i in range(13, 78, 6):
            r.square(18, i, color(255,255,255))

        r.square(18, 19, color(0,0,0))
        r.square(18, 67, color(0,0,0))

        for i in range(13, 78, 6):
            r.square(12, i, color(255,255,255))

        for i in range(31, 61, 6):
            r.square(12, i, color(0,0,0))

        r.square(12, 19, color(0,0,0))
        r.square(12, 67, color(0,0,0))

        # legs
        for i in range(31, 61, 6):
            r.square(6, i, color(255,255,255))

        r.square(6, 43, color(0,0,0))
        

r = Bitmap(80, 96)
# (30 puntos) por crear una escena de 80 x 96 pixeles o 160 x 192 pixeles representando un frame de un juego de Atari.
r.drawEars(r)
r.drawBody(r)
r.write('space-invader.bmp')