from pygame import *

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#2110FF"


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, max_length_left, max_length_up):
        sprite.Sprite.__init__(self)
        self.image = image.load('blocks_sprites/monster.png')
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = max_length_left  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = max_length_up  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.x_vel = left  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.y_vel = up  # скорость движения по вертикали, 0 - не двигается

    def update(self, platforms):  # по принципу героя

        self.image = image.load('blocks_sprites/monster.png')

        self.rect.y += self.y_vel
        self.rect.x += self.x_vel

        self.collide(platforms)

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.x_vel = -self.x_vel  # если прошли максимальное растояние, то идеи в обратную сторону
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.y_vel = -self.y_vel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.x_vel = - self.x_vel  # то поворачиваем в обратную сторону
                self.y_vel = - self.y_vel
