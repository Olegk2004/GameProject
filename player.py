from pygame import *
import blocks
import monsters

MOVE_EXTRA_SPEED = 2.5  # Ускорение
JUMP_EXTRA_POWER = 1  # дополнительная сила прыжка
ANIMATION_SUPER_SPEED_DELAY = 0.05  # скорость смены кадров при ускорении
MOVE_SPEED = 8
WIDTH = 43
HEIGHT = 69
JUMP_POWER = 10
GRAVITY = 0.75  # Сила, которая будет тянуть нас вниз
WALKING_RIGHT = [image.load('hero_sprites/pygame_right_1.png'),
                 image.load('hero_sprites/pygame_right_2.png'),
                 image.load('hero_sprites/pygame_right_3.png'),
                 image.load('hero_sprites/pygame_right_4.png'),
                 image.load('hero_sprites/pygame_right_5.png'),
                 image.load('hero_sprites/pygame_right_6.png')]
WALKING_LEFT = [image.load('hero_sprites/pygame_left_1.png'),
                image.load('hero_sprites/pygame_left_2.png'),
                image.load('hero_sprites/pygame_left_3.png'),
                image.load('hero_sprites/pygame_left_4.png'),
                image.load('hero_sprites/pygame_left_5.png'),
                image.load('hero_sprites/pygame_left_6.png'),]
IDLE = image.load('hero_sprites/pygame_idle.png')


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_vel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = IDLE
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.y_vel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.anim_count = 0  # переменная какой картинку в данный момент времени всавлять
        self.scores = 0

    def update(self, left, right, up, platforms, coins, level):
        if self.anim_count + 1 >= 30:
            self.anim_count = 0
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.y_vel = -JUMP_POWER

        if left and not right:
            self.x_vel = -MOVE_SPEED  # Лево = x- n
            self.image = WALKING_LEFT[self.anim_count // 5]
            self.anim_count += 1

        elif right and not left:
            self.x_vel = MOVE_SPEED  # Право = x + n
            self.image = WALKING_RIGHT[self.anim_count // 5]
            self.anim_count += 1

        else:  # стоим, когда нет указаний идти
            self.x_vel = 0
            self.image = IDLE
            self.anim_count = 0

        if not self.onGround:
            self.y_vel += GRAVITY  # если ни на что не опираемся, то падаем(

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.y_vel
        self.collide(0, self.y_vel, platforms, coins)

        self.rect.x += self.x_vel  # переносим свои положение на x_vel
        self.collide(self.x_vel, 0, platforms, coins)

    def collide(self, x_vel, y_vel, platforms, coins):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if x_vel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if x_vel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if y_vel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.y_vel = 0  # и энергия падения пропадает

                if y_vel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.y_vel = 0  # и энергия прыжка пропадает

                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster):  # если пересакаемый блок -
                    self.die()  # - blocks.BlockDie или Monster - умираем
        for m in coins:
            if sprite.collide_rect(self, m):
                self.scores += 1
                m.kill()

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)  # перемещаемся в начальные координаты

    def teleporting(self, go_x, go_y):
        self.rect.x = go_x
        self.rect.y = go_y
