from pygame import *

MONET_WIDTH = 35
MONET_HEIGHT = 35


class Monet(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("blocks_sprites/monet.png")
        self.rect = Rect(x, y, MONET_WIDTH, MONET_HEIGHT)
