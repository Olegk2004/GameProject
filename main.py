import pygame


PLAYER_WIDTH = 60  # размер игрока
PLAYER_HEIGHT = 71
PLAYER_SPEED = 5  # скорость игрока
DISPLAY_SIZE = (500, 500)  # размер экрана

WALK_RIGHT = [pygame.image.load('pygame_right_1.png'),  # анимация ходьбы вправо
              pygame.image.load('pygame_right_2.png'),
              pygame.image.load('pygame_right_3.png'),
              pygame.image.load('pygame_right_4.png'),
              pygame.image.load('pygame_right_5.png'),
              pygame.image.load('pygame_right_6.png')]

WALK_LEFT = [pygame.image.load('pygame_left_1.png'),  # анимация ходьбы влево
             pygame.image.load('pygame_left_2.png'),
             pygame.image.load('pygame_left_3.png'),
             pygame.image.load('pygame_left_4.png'),
             pygame.image.load('pygame_left_5.png'),
             pygame.image.load('pygame_left_6.png')]

PLAYER_STAND = pygame.image.load('pygame_idle.png')


pygame.init()
win = pygame.display.set_mode((DISPLAY_SIZE[0], DISPLAY_SIZE[1]))
pygame.display.set_caption("Cubes Game")  # заголовок к окну

clock = pygame.time.Clock()
player_stand = pygame.image.load('pygame_idle.png')
bg = pygame.image.load('bg.jpg')


class Platform:  # платформа
    def __init__(self, pos_x, pos_y):
        self.image = pygame.image.load('platform.png')
        self.rect = pygame.Rect(pos_x, pos_y, *self.image.get_size())


class Bullet:  # снаряд
    def __init__(self, pos_x, pos_y, radius, color, current_facing):
        self.x = pos_x
        self.y = pos_y
        self.radius = radius
        self.color = color
        self.facing = current_facing
        self.vel = 8 * facing

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 10, 5))


x = 0  # положение игрока
y = 429

is_jump = False  # атрибуты для проведения прыжка
jump_count = 10

left = False  # атрибуты для определения необходимой анимации
right = False
anim_count = 0
last_move = "right"

is_on_pause = False  # флаг для паузы


def draw():
    global anim_count
    win.blit(bg, [0, 0])
    if is_on_pause:  # рисование надписи "Пауза"
        font = pygame.font.Font(None, 40)
        text1 = font.render("Пауза", True, (0, 0, 0))
        win.blit(text1, (DISPLAY_SIZE[0] // 2 - text1.get_width() // 2,
                         DISPLAY_SIZE[1] // 2 - text1.get_height()))
        font = pygame.font.Font(None, 20)
        text2 = font.render("Esc - продолжить", True, (0, 0, 0))
        win.blit(text2, (DISPLAY_SIZE[0] // 2 - text2.get_width() // 2,
                         DISPLAY_SIZE[1] // 2 + text2.get_height()))

    if anim_count + 1 >= 30:  # условие для создания цикла анимации
        anim_count = 0

    if left:  # если игрок идёт влево, проигрывать анимацию хождения влево
        win.blit(WALK_LEFT[anim_count // 5], [x, y])
        anim_count += 1 * (not is_on_pause)
    elif right:  # иначе - хождения вправо
        win.blit(WALK_RIGHT[anim_count // 5], [x, y])
        anim_count += 1 * (not is_on_pause)
    else:  # если ничего не происходит, не производить анимации
        win.blit(PLAYER_STAND, [x, y])

    for elem in bullets:  # рисуем каждую пулю на экране
        elem.draw(win)

    pygame.display.update()


def pause_manipulation():  # функция, изменяющая состояние игры
    global is_on_pause
    is_on_pause = 1 - is_on_pause


platforms = []  # все платформы игры
lev1 = [(150, 300), (450, 50)]
q = 0
running = True
bullets = []  # все пули игры на экране


while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # если нажат esc - обновить состояние паузы
            pause_manipulation()

    for bullet in bullets:  # для каждой пули проверяется, не за экраном ли она, иначе - удаляется из списка
        if 0 < bullet.x < DISPLAY_SIZE[0] and not is_on_pause:
            bullet.x += bullet.vel
        elif not is_on_pause:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not is_on_pause:  # если нажат space - выстрелить пулями
        if last_move == "right":
            facing = 1
        else:
            facing = -1

        if len(bullets) < 10:
            bullets.append(Bullet(x + PLAYER_WIDTH // 2, y + PLAYER_HEIGHT // 2,
                                  5, (255, 0, 0), facing))

    if keys[pygame.K_LEFT] and x > 0 and not is_on_pause:  # если нажаты стрелочки - идти в ту или иную сторону
        x -= PLAYER_SPEED
        left = True
        right = False
        last_move = "left"
    elif keys[pygame.K_RIGHT] and x < DISPLAY_SIZE[0] - PLAYER_WIDTH and not is_on_pause:
        x += PLAYER_SPEED
        left = False
        right = True
        last_move = "right"
    elif not is_on_pause:
        right = False
        left = False
        anim_count = 0

    if not is_jump:  # если нажата стрелка вверх - прыгнуть (если игрок не находится в воздухе)
        if keys[pygame.K_UP] and not is_on_pause:
            is_jump = True
    elif not is_on_pause:
        if jump_count >= -10:
            if jump_count >= 0:
                y -= (jump_count ** 2) / 3
                jump_count -= 1
            else:
                y += (jump_count ** 2) / 3
                jump_count -= 1
        else:
            is_jump = False
            jump_count = 10
    draw()

pygame.quit()
