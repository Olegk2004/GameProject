import pygame
from pygame import *
from player import Player
from blocks import Platform, BlockDie
from monsters import Monster
from monet import Monet

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = (0, 0, 0)
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32


class Camera(object):  # класс из интернета для отображения уровня большего по размеру чем окно(эффект камеры)
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):  # функция для обьекта класса камеры
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Tramp - legend")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание заднего фона
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем фон сплошным цветом
    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию — стоим
    up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)
    level = [
        "------------------------------------------------------",
        "-                                  m                 -",
        "-                       --                  ---      -",
        "-        *                                           -",
        "-                          m                         -",
        "-            --                        -----         -",
        "--                  m                                -",
        "-                                                    -",
        "-        m          ----     ---                     -",
        "-                                          ---       -",
        "--                               -                   -",
        "-            *        m                              -",
        "-      m                     ---         -           -",
        "-                                                    -",
        "-               m                        *           -",
        "-  *   ---                  *            ---         -",
        "-                                                    -",
        "-   -------         ----                             -",
        "-                                    ***           ---",
        "-           m             -  m                       -",
        "---                         --                      --",
        "-           ***                              ***     -",
        "-                                                    -",
        "-                        ---           ---           -",
        "---    ---                     **                    -",
        "-                                                  ---",
        "-               ----------          ***              -",
        "-                                                    -",
        "-**********                           ----           -",
        "------------------------------------------------------"]
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту
    monsters = pygame.sprite.Group()  # все монстры
    camera = Camera(camera_configure, total_level_width, total_level_height)
    timer = pygame.time.Clock()
    running = True
    mn1 = Monster(190, 200, 2, 3, 150, 15)  # создание монстров и добавление их во всевозможные группы
    mn2 = Monster(600, 700, 2, 3, 150, 15)
    mn3 = Monster(130, 650, 2, 3, 150, 15)
    mn4 = Monster(800, 400, 2, 3, 150, 15)
    mn5 = Monster(800, 150, 2, 3, 150, 15)
    entities.add(mn1, mn2, mn3, mn4, mn5)
    platforms.append(mn1)
    platforms.append(mn2)
    platforms.append(mn3)
    platforms.append(mn4)
    platforms.append(mn5)
    monsters.add(mn1, mn2, mn3, mn4, mn5)
    monets = []  # список для монет
    while running:  # Основной цикл программы
        timer.tick(60)  # fps
        monsters.update(platforms)
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
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":  # знак для платформ
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)
                if col == "*":  # для шипов
                    bd = BlockDie(x, y)
                    entities.add(bd)
                    platforms.append(bd)
                if col == "m":  # для монет
                    mn = Monet(x, y)
                    entities.add(mn)
                    monets.append(mn)

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля
        hero.update(left, right, up, platforms, monets, level)  # передвижение
        camera.update(hero)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # обновление и вывод всех изменений на экран

    pygame.quit()


if __name__ == "__main__":
    main()
