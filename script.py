#!/usr/bin/env python3


# Oulala c'est pas très beau tout ça.
#
# Faudra que je prenne le temps de revoir un peu ce code.
#
# ('< _ '


import pyglet
from math import *
import random
import os, sys
window = pyglet.window.Window(600 ,600)


coords = 300, 200


class Face():
    """docstring for Face"""
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.s = size

    def generate(self):
        self.width = self.s * random.uniform(.5, 0.8)
        self.height = self.s * random.uniform(0.8, 1)


        self.elements = [
            *self.gen_head(),
            *self.gen_eyes(),
            self.gen_nose(),
            self.gen_mouth(),
            # *self.gen_hair()
        ]
    

    def gen_hair(self):
        num_verts = random.randint(6,12)
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        
        verlists = []
        for i in (*range(num_verts), 0):
            angle = radians((float(i)+.5)/num_verts * 180.0)
            verts = []
            verts.append(width*cos(angle)*1.5+x)
            verts.append(height*sin(angle)*1.5+y)
            verts.append(width*cos(angle)*1.2+x)
            verts.append(height*sin(angle)*1.2+y)
            verlists.append(
                pyglet.graphics.vertex_list(2, ('v2f', verts), 'c3B'))
        return verlists

    def gen_eyes(self):
        
        num_verts = random.randint(2,4)
        orientation = random.choice((0, 180.0))
        froncage = random.uniform(-30, 30)
        r_x = self.x + self.width /5 +self.width/6
        l_x = self.x - self.width /5 - self.width/6
        y = self.y + self.height * random.uniform(.1, .2)
        width = self.width /5
        height = self.height * random.uniform(.0, .1)
        
        l_verts = []
        r_verts = []
        for i in range(num_verts):
            angle = radians((float(i)+.5)/num_verts * 180.0 + orientation +froncage)
            l_verts.append(width*cos(angle)+l_x)
            l_verts.append(height*sin(angle)+y)
            angle = radians((float(i)+.5)/num_verts * 180.0 + orientation-froncage)

            r_verts.append(width*cos(angle)+r_x)
            r_verts.append(height*sin(angle)+y)

        return (pyglet.graphics.vertex_list(num_verts, ('v2f', l_verts), 'c3B'),
                pyglet.graphics.vertex_list(num_verts, ('v2f', r_verts), 'c3B'), )


    def gen_head(self):
        num_verts = random.randint(8,12)
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        
        bombee = random.uniform(0.5,0.1)
        verts = []
        for i in (*range(num_verts), 0):
            angle = radians((float(i)+.5)/num_verts * 360.0)
            verts.append((width*cos(angle)+x + cos(sin(angle))*width*bombee))
            verts.append((height*sin(angle)+y))

        returnedlist = []

        returnedlist.append(pyglet.graphics.vertex_list(num_verts+1, ('v2f', verts), 'c3B'))

        return returnedlist

    def gen_nose(self):
        num_verts = random.randint(3,4)
        orientation = random.uniform(-10., 10.)
        x = self.x
        y = self.y - self.height* 0.2
        width = self.width * random.uniform(.2, 1)
        height = self.height * random.uniform(.07, .12)
        
        # def simple_nose(x, y, w, h, o, n):
        verts = []
        for i in range(num_verts):
            angle = radians((float(i)+.5)/num_verts * 180.0 + 90.0 + orientation)
            verts.append(width*cos(angle)+x)
            verts.append(height*sin(angle)+y)
        return pyglet.graphics.vertex_list(num_verts, ('v2f', verts), 'c3B')

    def gen_mouth(self):
        num_verts = random.randint(2,4)
        orientation = random.choice((0, 180.0))
        x = self.x
        y = self.y - self.height * random.uniform(.5, .6)
        width = self.width * random.uniform(.2, .4)
        height = self.height * random.uniform(.0, .1)
        
        verts = []
        for i in range(num_verts):
            angle = radians((float(i)+.5)/num_verts * 180.0 + orientation)
            verts.append(width*cos(angle)+x)
            verts.append(height*sin(angle)+y)
        return pyglet.graphics.vertex_list(num_verts, ('v2f', verts), 'c3B')

    def draw(self):
        for e in self.elements:
            e.colors = [0]*len(e.colors)
            e.draw(pyglet.gl.GL_POLYGON)
            e.colors = [255]*len(e.colors)

            e.draw(pyglet.gl.GL_LINE_STRIP)



compl = {
    'qqch':(
        'un humain',
        'le plus beau',
        'un incompris',
        'un personnage',
        'mon ombre',
    ),
    'verb':(
        'courir partout',
        'trouver la solution',
        'partir à tout jamais',
        'chercher la vérité',
        'tout jeter',
        'te suivre'
    )
}

boutdephrase = {
    'verb':('{verb}',),
    'qqch':('{qqch}',),
    'de':(
        'de {verb}',
        'd\'être {qqch}',
        'd\'aimer {qqch}',
        'de vouloir {verb}',
        'd\'être capable de {verb}',
        'd\'être prêt à {verb}'

    )
}
compl = {k:random.choice(v) for k, v in compl.items()}
boutdephrase = {k:random.choice(v).format(**compl) for k, v in boutdephrase.items()}
phrases = (
    'Je suis pas sûr {de}...',
    'J\'ai toujours rêvé {de}.',
    'Il suffit {de}.',
    'Il faut {verb}.',
    'à quoi bon {verb}.',
)
p = random.choice(phrases)
p = p.format(**boutdephrase).capitalize()

face = Face(window.width/2, window.height/2-50, 100)
face.generate()

label = pyglet.text.Label(p,
            font_name='BGP Sans GPL&GNU Regular',
            font_size=12,
            x=face.x, y=face.y+face.height+100,
            anchor_x='center', anchor_y='center')

margin = 10
w, h = label.content_width + margin*2, label.content_height + margin*2
x, y = label.x -w/2, label.y-h/2
margin = 5

verts = (
    x, y,
    x+w/3-10, y-margin,
    x+w/3, y-margin-20,
    x+w/3+10, y-margin,

    x+w, y,
    x+w+margin, y+h/2,
    x+w, y+h,
    x+w/2, y+h+margin,
    x, y+h,
    x-margin, y+h/2,
)

bulle = pyglet.graphics.vertex_list(len(verts)//2, ('v2f', verts))


@window.event
def on_draw():
    window.clear()
    label.draw()
    face.draw()
    bulle.draw(pyglet.gl.GL_LINE_LOOP)
@window.event
def on_key_press(symbol, modifiers):
    os.execv(__file__, sys.argv)
    # global face
    # face.generate()
    # window.dispatch_event('on_draw')


pyglet.app.run()

