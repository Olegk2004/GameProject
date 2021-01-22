import pygame

pygame.init()
DISPLAY_SIZE = (500, 500)
win = pygame.display.set_mode((DISPLAY_SIZE[0], DISPLAY_SIZE[1]))

pygame.display.set_caption("Cubes Game")  # заголовок к окну

walk_right = [pygame.image.load('pygame_right_1.png'),
              pygame.image.load('pygame_right_2.png'),
              pygame.image.load('pygame_right_3.png'),
              pygame.image.load('pygame_right_4.png'),
              pygame.image.load('pygame_right_5.png'),
              pygame.image.load('pygame_right_6.png')]

walk_left = [pygame.image.load('pygame_left_1.png'),
             pygame.image.load('pygame_left_2.png'),
             pygame.image.load('pygame_left_3.png'),
             pygame.image.load('pygame_left_4.png'),
             pygame.image.load('pygame_left_5.png'),
             pygame.image.load('pygame_left_6.png')]
clock = pygame.time.Clock()
player_stand = pygame.image.load('pygame_idle.png')
bg = pygame.image.load('bg.jpg')

x = 0  # положение игрока
y = 429
width = 60  # размер игрока
height = 71
speed = 5

is_jump = False
jump_count = 10

left = False
right = False
anim_count = 0
last_move = "right"

is_on_pause = False


class Platform:
    def __init__(self, x, y):
        self.image = pygame.image.load('platform.png')
        self.rect = pygame.Rect(x, y, *self.image.get_size())
        

class Bullet:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, 10, 5))


def draw():
    global anim_count
    win.blit(bg, [0, 0])
    if is_on_pause:
        font = pygame.font.Font(None, 40)
        text1 = font.render("Пауза", True, (0, 0, 0))
        win.blit(text1, (DISPLAY_SIZE[0] // 2 - text1.get_width() // 2,
                         DISPLAY_SIZE[1] // 2 - text1.get_height()))
        font = pygame.font.Font(None, 20)
        text2 = font.render("Esc - продолжить", True, (0, 0, 0))
        win.blit(text2, (DISPLAY_SIZE[0] // 2 - text2.get_width() // 2,
                         DISPLAY_SIZE[1] // 2 + text2.get_height()))

    if anim_count + 1 >= 30:
        anim_count = 0

    if left:
        win.blit(walk_left[anim_count // 5], [x, y])
        anim_count += 1 * (not is_on_pause)
    elif right:
        win.blit(walk_right[anim_count // 5], [x, y])
        anim_count += 1 * (not is_on_pause)
    else:
        win.blit(player_stand, [x, y])

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


platforms = []
lev1 = [(150, 300), (450, 50)]
q = 0
running = True
bullets = []


def pause_manipulation():
    global is_on_pause
    is_on_pause = 1 - is_on_pause


while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pause_manipulation()

    for bullet in bullets:
        if 0 < bullet.x < DISPLAY_SIZE[0] and not is_on_pause:
            bullet.x += bullet.vel
        elif not is_on_pause:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not is_on_pause:
        if last_move == "right":
            facing = 1
        else:
            facing = -1

        if len(bullets) < 10:
            bullets.append(Bullet(x + width // 2, y + height // 2,
                                  5, (255, 0, 0), facing))

    if keys[pygame.K_LEFT] and x > 0 and not is_on_pause:
        x -= speed
        left = True
        right = False
        last_move = "left"
    elif keys[pygame.K_RIGHT] and x < DISPLAY_SIZE[0] - width and not is_on_pause:
        x += speed
        left = False
        right = True
        last_move = "right"
    elif not is_on_pause:
        right = False
        left = False
        anim_count = 0
    if not is_jump:
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
