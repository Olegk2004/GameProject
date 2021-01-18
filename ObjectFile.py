import pygame
from abc import abstractmethod


clock = pygame.time.Clock()
imgs = {'hero_walking': ,  # список с анимациями персонажей (возможно)
        'hero_attack':  ,
        'zombie_walking': ,
        'zombie_attack': }


class Weapon:  # класс оружия с уроном, дальностью стрельбы и картинкой
    def __init__(self, damage, damage_range, picture):
        self._damage = damage
        self._range = damage_range
        self._picture = picture


class Gun(Weapon):  # винтовка
    pass


class Pistol(Weapon):  # пистолет
    pass

class MeleeWeapon(Weapon):  # оружие ближнего боя (разделил, чтобы было удобнее понимать, чем является то или другое оружие, но смысл у них один и тот же)
    pass


class GameObject:  # класс игрового объекта
    def __init__(self, pos):
        self.pos = list(pos)

    def get_pos(self):
        return self.pos


class Platform(GameObject):  # платформы
    pass


class Humanoid(GameObject):  # класс человек (скорость, анимация ходьбы и атаки)
    def __init__(self, pos, velocity, walking_pictures, attack_pictures):
        super().__init__(pos)
        self._velocity = velocity
        self._walking = imgs[walking_pictures]
        self._attacking = imgs[attack_pictures]

    def go_right(self):
        self.pos[0] += self._velocity

    def go_left(self):
        self.pos[0] -= self._velocity


class Hero(Humanoid):  # класс Герой (+ прыжок, пока не доделан)
    def __init__(self, pos, velocity, *weapons):
        super().__init__(pos, velocity)
        self._weapons = weapons

    def jump(self):
        while True:
            self.pos[0] += self._velocity - 9.8 * clock.tick() / 1000


class Zombie(Humanoid):  # класс Зомби, не доделан
    pass
