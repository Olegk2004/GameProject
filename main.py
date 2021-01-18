from abc import abstractmethod
from ObjectFile import GameObject, Platform, Humanoid, Zombie, Hero
import pygame


class App:  # приложение

    def __init__(self, display_size):
        self._state = None

        pygame.init()
        self._screen = pygame.display.set_mode(display_size)
        self._display_size = display_size

        self._running = True
        self._clock = pygame.time.Clock()

    def set_state(self, state):  # изменить состояние (меню, пауза, игра)
        self._state = state
        self._state.set_app(self)
        self._state.setup()

    def get_screen(self):  # получить сам экран изображения
        return self._screen

    def get_display_size(self):  # получить размер экрана приложения
        return self._display_size

    def run(self):  # основной процесс приложения
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                self._state.process_event(event)

            dt = self._clock.tick()
            self._state.loop(dt)
            pygame.display.flip()
        self._state.destroy()


class AppState:  # состояние приложения

    def __init__(self):
        self._app = None  # приложение, к которому привязано

    def set_app(self, app):  # изменить приложение, к которому привязано
        self._app = app

    def get_app(self):  # получить приложение, к которому привязано
        return self._app

    @abstractmethod
    def setup(self):  # описание запуска состояния
        pass

    @abstractmethod
    def process_event(self, event):  # описание реакций состояния на определённые действия пользователя
        pass

    @abstractmethod
    def loop(self, dt):  # описание того, что происходит на экране, пока работает состояние (заливка, текст, анимация, не зависимые от действий)
        pass

    @abstractmethod  # описание прекращения работы состояния
    def destroy(self):
        pass


class MenuState(AppState):

    def __init__(self, background_image, text):
        super().__init__()
        self._bg_img = imgs[background_image]  # берём картинку фона из листа imgs
        self._text = text.split('\n')  # текст меню

    def setup(self):
        self._bg_img = pygame.transform.scale(self._bg_img, self.get_app().get_display_size())  # ставим картинку на фон

    def process_event(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):  # если что-то нажато, запускаем игровой процесс
            self.get_app().set_state(GameState())

    def loop(self, dt):
        screen = self.get_app().get_screen()
        screen.fill((0, 0, 0))
        screen.blit(self._bg_img, (0, 0))
        font = pygame.font.Font(None, 30)
        for i, line in enumerate(self._text):
            line_img = font.render(line, True, pygame.Color('magenta'))
            screen.blit(line_img, (0, i * line_img.get_rect().height * 1.1))

    def destroy(self):
        pass


class PauseState(AppState):  # состояние паузы

    def __init__(self, text):  # подразумевается, что будет Пауза с прозрачным фоном, предлагающая выйти в меню или продолжить
        super().__init__()
        self._text = text


class GameState(AppState):  # состояние игры

    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.get_app().set_state(PauseState('Пауза\nEnter - продолжить\nEsc - выйти в меню'))  # запуск паузы при нажатии esc

    def loop(self, dt):
        self.get_app().get_screen().fill((0, 0, 0))

    def destroy(self):
        pass


def load_image(image_path, colorkey=None):  # функция для работы с картинками
    result = pygame.image.load(image_path)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = result.get_at((0, 0))
        result.set_colorkey(colorkey)
    else:
        result.convert_alpha()
    return result


if __name__ == '__main__':   # запуск самой игры

    app = App((640, 480))

    imgs = {'menu_background': load_image('sea.jpg'),
            'game_background': load_image('black.jpg')
            }

    menu_state = MenuState('menu_background', 'Привет!\nТы попал в игру!')
    app.set_state(menu_state)
    app.run()
