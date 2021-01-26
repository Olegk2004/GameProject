from pygame import *


MONSTER_SPEED = 2
LEFT_IMAGE = image.load('blocks_sprites/monster0.png')
RIGHT_IMAGE = image.load('blocks_sprites/monster1.png')


class Monster(sprite.Sprite):
    def __init__(self, x, y, left_vel=MONSTER_SPEED, up_vel=3, max_length_up=15):
        sprite.Sprite.__init__(self)
        self.reached_final_destination = False  # флаг для выбора изображения (т.е. в какую сторону летит)
        self.can_move = True

        self.image = LEFT_IMAGE
        self.rect = Rect(x, y, self.image.get_width(), self.image.get_height())
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthUp = max_length_up  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.x_vel = left_vel  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.y_vel = up_vel  # скорость движения по вертикали, 0 - не двигается

    def update(self, obstacles):  # по принципу героя
        if self.can_move:
            if self.reached_final_destination:
                self.image = LEFT_IMAGE
            else:
                self.image = RIGHT_IMAGE

            self.rect.y += self.y_vel
            self.rect.x += self.x_vel

            self.collide(obstacles)

            if abs(self.startY - self.rect.y) > self.maxLengthUp:
                self.y_vel = -self.y_vel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, obstacles):
        for obj in obstacles:
            if sprite.collide_rect(self, obj) and self != obj:  # если с чем-то или кем-то столкнулись
                self.x_vel = -self.x_vel  # то поворачиваем в обратную сторону
                self.y_vel = -self.y_vel
                self.reached_final_destination = 1 - self.reached_final_destination

    def stop(self, is_on_pause):
        self.can_move = 1 - is_on_pause
