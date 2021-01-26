import pygame
from pygame import *
from player import Player
from blocks import Platform, BlockDie
from monsters import Monster
from monet import Coin

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 600  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = (0, 0, 0)
TILE_WIDTH = 70
TILE_HEIGHT = 70


class Camera(object):  # класс для отображения уровня большего по размеру чем окно(эффект камеры)
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):  # функция для обьекта класса камеры
    left, top, _, _ = target_rect
    _, _, width, height = camera
    left, top = -left + WIN_WIDTH / 2, -top + WIN_HEIGHT / 2

    left = min(0, left)  # Не движемся дальше левой границы
    left = max(-(camera.width - WIN_WIDTH), left)  # Не движемся дальше правой границы
    top = max(-(camera.height - WIN_HEIGHT), top)  # Не движемся дальше нижней границы
    top = min(0, top)  # Не движемся дальше верхней границы

    return Rect(left, top, width, height)


def load_level(filename):  # загрузка уровня
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        return [line.strip() for line in mapFile]


def draw_pause(screen):  # рисуем паузу
    pause_font = pygame.font.Font(None, 50)
    text = pause_font.render("Пауза", True, (255, 255, 255))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2 - text.get_width() // 2))

    pause_font = pygame.font.Font(None, 30)
    text = pause_font.render("Esc - продолжить", True, (255, 255, 255))
    screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                       WIN_HEIGHT // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Trump - legend")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание заднего фона
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем фон сплошным цветом
    hero = Player(70, 70)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию — стоим
    up = False
    is_on_pause = False  # проверка на паузу
    entities = pygame.sprite.Group()  # Все объекты
    obstacles = []  # то, во что мы будем врезаться или опираться
    coins = []  # список для монет
    monsters = pygame.sprite.Group()  # все монстры
    entities.add(hero)
    levels = [load_level(f'level{i + 1}.txt') for i in range(1)]
    current_level = 0  # уровень на данный момент
    x = y = 0  # координаты
    for row in levels[current_level]:  # вся строка
        for col in row:  # каждый символ
            if col == "-":  # знак для платформ
                pf = Platform(x, y)
                entities.add(pf)
                obstacles.append(pf)
            elif col == "*":  # для шипов
                bd = BlockDie(x, y)
                entities.add(bd)
                obstacles.append(bd)
            elif col == "m":  # для монет
                mn = Coin(x, y)
                entities.add(mn)
                coins.append(mn)
            elif col == "e":  # для монстров
                en = Monster(x, y)
                entities.add(en)
                obstacles.append(en)
                monsters.add(en)

            x += TILE_WIDTH  # блоки платформы ставятся на ширине блоков
        y += TILE_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(levels[current_level][0]) * TILE_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(levels[current_level]) * TILE_HEIGHT  # высоту
    camera = Camera(camera_configure, total_level_width, total_level_height)
    timer = pygame.time.Clock()
    running = True
    while running:  # Основной цикл программы
        timer.tick(30)  # fps
        monsters.update(obstacles)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

            if e.type == KEYDOWN and e.key == K_ESCAPE:  # Esc - управляющая клавиша паузы
                is_on_pause = 1 - is_on_pause
                for obj in obstacles:  # останавливаем всех монстров в зависимости от состояния
                    if obj.__class__ == Monster:
                        obj.stop(is_on_pause)

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        if not is_on_pause:
            hero.update(left, right, up, obstacles, coins, levels[current_level])  # передвижение
            camera.update(hero)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        if is_on_pause:
            draw_pause(screen)
        pygame.display.update()  # обновление и вывод всех изменений на экран

    pygame.quit()


if __name__ == "__main__":
    main()
