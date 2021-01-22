import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))

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
    if anim_count + 1 >= 30:
        anim_count = 0

    if left:
        win.blit(walk_left[anim_count // 5], [x, y])
        anim_count += 1
    elif right:
        win.blit(walk_right[anim_count // 5], [x, y])
        anim_count += 1
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
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
        if 0 < bullet.x < 500:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if last_move == "right":
            facing = 1
        else:
            facing = -1

        if len(bullets) < 10:
            bullets.append(Bullet(x + width // 2, y + height // 2,
                                  5, (255, 0, 0), facing))

    if keys[pygame.K_LEFT] and x > 0:
        x -= speed
        left = True
        right = False
        last_move = "left"
    elif keys[pygame.K_RIGHT] and x < 500 - width:
        x += speed
        left = False
        right = True
        last_move = "right"
    else:
        right = False
        left = False
        anim_count = 0
    if not is_jump:
        if keys[pygame.K_UP]:
            is_jump = True
    else:
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
