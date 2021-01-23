from pygame import *

COIN_WIDTH = 35
COIN_HEIGHT = 35


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("blocks_sprites/monet.png")
        self.rect = Rect(x, y, COIN_WIDTH, COIN_HEIGHT)
