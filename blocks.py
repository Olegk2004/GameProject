from pygame import *

TILE_WIDTH = 70
TILE_HEIGHT = 70


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("blocks_sprites/platform.png")
        self.rect = Rect(x, y, TILE_WIDTH, TILE_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("blocks_sprites/block_die.png")
