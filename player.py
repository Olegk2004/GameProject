from pygame import *
import blocks
import monsters

MOVE_EXTRA_SPEED = 2.5  # Ускорение
JUMP_EXTRA_POWER = 1  # дополнительная сила прыжка
ANIMATION_SUPER_SPEED_DELAY = 0.05  # скорость смены кадров при ускорении
MOVE_SPEED = 10
WIDTH = 60
HEIGHT = 71
JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз
WALKING_RIGHT = [image.load('hero_sprites/pygame_right_1.png'),
                 image.load('hero_sprites/pygame_right_1.png'),
                 image.load('hero_sprites/pygame_right_1.png'),
                 image.load('hero_sprites/pygame_right_1.png'),
                 image.load('hero_sprites/pygame_right_1.png')]
WALKING_LEFT = [image.load('hero_sprites/pygame_left_1.png'),
                image.load('hero_sprites/pygame_left_2.png'),
                image.load('hero_sprites/pygame_left_3.png'),
                image.load('hero_sprites/pygame_left_4.png'),
                image.load('hero_sprites/pygame_left_5.png')]
IDLE = image.load('hero_sprites/pygame_idle.png')


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = IDLE
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.anim_count = 0  # переменная какой картинку в данный момент времени всавлять
        self.scores = 0

    def update(self, left, right, up, platforms, monets, level):
        if self.anim_count + 1 >= 30:
            self.anim_count = 0
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image = WALKING_LEFT[self.anim_count // 6]
            self.anim_count += 1

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image = WALKING_RIGHT[self.anim_count // 6]
            self.anim_count += 1

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            self.image = IDLE
            self.anim_count = 0

        if not self.onGround:
            self.yvel += GRAVITY  # если ни на что не опираемся, то падаем(

        self.onGround = False;  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, monets)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, monets)

    def collide(self, xvel, yvel, platforms, monets):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

                if isinstance(p, blocks.BlockDie) or isinstance(p,
                                                                monsters.Monster):  # если пересакаемый блок- blocks.BlockDie или Monster
                    self.die()  # умираем
        for m in monets:
            if sprite.collide_rect(self, m):
                self.scores += 1
                m.kill()

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)  # перемещаемся в начальные координаты

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY
