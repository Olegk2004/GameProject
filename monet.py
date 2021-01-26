from pygame import *


ACTIVATED_IMAGE = image.load("blocks_sprites/monet.png")


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = ACTIVATED_IMAGE
        self.rect = Rect(x, y, self.image.get_width(), self.image.get_height())
        self.can_be_taken = True

    def set_activated(self, flag):
        self.can_be_taken = flag
        if flag:
            self.image = ACTIVATED_IMAGE
        else:
            self.kill()

    def is_activated(self):
        return self.can_be_taken
