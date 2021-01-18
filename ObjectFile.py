import pygame
from abc import abstractmethod


clock = pygame.time.Clock()
imgs = {'hero_walking': ,
        'hero_attack':  ,
        'zombie_walking': ,
        'zombie_attack': }


class Weapon:
    def __init__(self, damage, damage_range, picture):
        self._damage = damage
        self._range = damage_range
        self._picture = picture


class Gun(Weapon):
    pass


class Pistol(Weapon):
    pass

class MeleeWeapon(Weapon):
    pass


class GameObject:
    def __init__(self, pos):
        self.pos = list(pos)

    def get_pos(self):
        return self.pos


class Platform(GameObject):
    pass


class Humanoid(GameObject):
    def __init__(self, pos, velocity, walking_pictures, attack_pictures):
        super().__init__(pos)
        self._velocity = velocity
        self._walking = imgs[walking_pictures]
        self._attacking = imgs[attack_pictures]

    def go_right(self):
        self.pos[0] += self._velocity

    def go_left(self):
        self.pos[0] -= self._velocity


class Hero(Humanoid):
    def __init__(self, pos, velocity, *weapons):
        super().__init__(pos, velocity)
        self._weapons = weapons

    def jump(self):
        while True:
            self.pos[0] += self._velocity - 9.8 * clock.tick() / 1000


class Zombie(Humanoid):
    pass
