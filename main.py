import sys
import pygame
from pygame.locals import *
import random
pygame.init()
pygame.mixer.init()
FPS = 60
fps = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 0, 0)
score = 3

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20
DISPLAYSURF = pygame.display.set_mode((600,600))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("snake")

def print_text(text):
    font = pygame.font.SysFont('Arial', 20)
    color = BLACK

    # рендерим текст
    img = font.render(text, True, color)

    # создаём rect текста
    text_rect = img.get_rect()

    # центрируем rect по центру экрана
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # рисуем текст на экране
    DISPLAYSURF.blit(img, text_rect)


class Snake:
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # пример: квадрат 50x50
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (150, 150)
        self.pos_y = float(self.rect.y)
        self.base_speed = 5
        self.current_speed = self.base_speed
        self.segments = [(x, y), (x - CELL_SIZE, y), (x - CELL_SIZE * 2, y)]

        # Направление движения (начинаем движение вправо)
        self.direction = (1, 0)
        # Множитель ускорения
        self.boost_multiplier = 2.0

        # Таймер для движения
        self.move_timer = 0

    def change_direction(self, new_direction, boost=False):
        """Меняет направление движения змейки"""
        # Проверяем, что новое направление не противоположно текущему
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            # Если нажата та же кнопка - ускоряемся
            if boost and new_direction == self.direction:
                self.current_speed = self.base_speed * self.boost_multiplier
            else:
                self.direction = new_direction
                self.current_speed = self.base_speed

    def update(self, dt):
        self.move_timer += dt
        # Вычисляем интервал движения на основе текущей скорости
        move_interval = 1.0 / self.current_speed

        if self.move_timer >= move_interval:
            self.move_timer = 0

            # Получаем голову змейки
            head_x, head_y = self.segments[0]

            # Вычисляем новую позицию головы
            new_head = (
                head_x + self.direction[0] * CELL_SIZE,
                head_y + self.direction[1] * CELL_SIZE
            )

            # Добавляем новую голову
            self.segments.insert(0, new_head)

            # Удаляем хвост (если не съели еду)
            self.segments.pop()

    def draw(self, surface):
        for i, (x, y) in enumerate(self.segments):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(DISPLAYSURF, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def reset_speed(self):
        """Сбрасывает скорость до базовой"""
        self.current_speed = self.base_speed

    def grow(self):
        """Увеличивает длину змейки"""
        # Дублируем последний сегмент
        self.segments.append(self.segments[-1])

    def check_collision(self):
        """Проверяет столкновение со стенами или собой"""
        head_x, head_y = self.segments[0]

        # Проверка столкновения со стенами
        if (head_x < 0 or head_x >= SCREEN_HEIGHT or
                head_y < 0 or head_y >= SCREEN_HEIGHT):
            return True

        # Проверка столкновения с собой
        if self.segments[0] in self.segments[1:]:
            return True

        return False

    def lower(self):
        self.segments.pop()

class Apple:
    def __init__(self):
        self.image = pygame.image.load("source/apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()

        self.position = self.random_position()
        self.rect.topleft = self.position

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def random_position(self):
        x = random.randrange(CELL_SIZE, SCREEN_WIDTH-CELL_SIZE, CELL_SIZE)
        y = random.randrange(CELL_SIZE, SCREEN_HEIGHT- 2 * CELL_SIZE, CELL_SIZE)
        return (x, y)

class Poisonous_Potato:
    def __init__(self):
        self.image = pygame.image.load("source/Poisonous_Potato.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()

        self.position = self.random_position()
        self.rect.topleft = self.position

    def draw(self, surface):
            surface.blit(self.image, self.rect)

    def random_position(self):
        x = random.randrange(CELL_SIZE, SCREEN_WIDTH - CELL_SIZE, CELL_SIZE)
        y = random.randrange(CELL_SIZE, SCREEN_HEIGHT- 2 * CELL_SIZE, CELL_SIZE)
        return (x, y)

s = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
a = Apple()
p = Poisonous_Potato()

fade_alpha = 0
fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
fade_surface.fill(GREEN)
clock = pygame.time.Clock()
game_over = False
keys_pressed = {
        pygame.K_UP: False,
        pygame.K_DOWN: False,
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False
    }

while True:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in keys_pressed:
                keys_pressed[event.key] = True

            if event.key == pygame.K_SPACE and game_over:
                # Перезапуск игры
                s = Snake(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
                a = Apple()
                p = Poisonous_Potato()
                score = 3
                game_over = False

        if event.type == pygame.KEYUP:
            if event.key in keys_pressed:
                keys_pressed[event.key] = False
                s.reset_speed()

    if not game_over:
        if keys_pressed[pygame.K_UP]:
            s.change_direction((0, -1), boost=True)
        elif keys_pressed[pygame.K_DOWN]:
            s.change_direction((0, 1), boost=True)
        elif keys_pressed[pygame.K_LEFT]:
            s.change_direction((-1, 0), boost=True)
        elif keys_pressed[pygame.K_RIGHT]:
            s.change_direction((1, 0), boost=True)

        s.update(dt)

        if s.segments[0] == a.position: ###------------------------
            DISPLAYSURF.fill(GREEN)
            s.grow()


            a.position = a.random_position()
            a.rect.topleft = a.position  # ← ВАЖНО
            score += 1

            eat_sound = pygame.mixer.Sound('tada.mp3')
            eat_sound.play()
            pygame.display.update()
            fade_alpha = 51

        if s.segments[0] == p.position: ###------------------------
            DISPLAYSURF.fill(RED)
            s.lower()

            p.position = p.random_position()
            p.rect.topleft = p.position  # ← ВАЖНО

            score -= 1
            if score < 2:
                game_over = True


            hit_sound = pygame.mixer.Sound('source/burp.mp3')
            hit_sound.play()

            pygame.display.update()
            fade_alpha = 51
        if s.check_collision():
            game_over = True



    DISPLAYSURF.fill(BLACK)
    s.draw(DISPLAYSURF)
    a.draw(DISPLAYSURF)
    p.draw(DISPLAYSURF)


    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
    DISPLAYSURF.blit(score_text, (10, 10))

    # Индикатор ускорения
    if s.current_speed > s.base_speed:
        boost_text = font.render("УСКОРЕНИЕ!", True, (255, 255, 0))
        DISPLAYSURF.blit(boost_text, (SCREEN_WIDTH - 200, 10))

    if game_over:
        game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
        restart_text = font.render("Нажмите ПРОБЕЛ для перезапуска", True, (255, 255, 255))
        DISPLAYSURF.blit(game_over_text, (SCREEN_HEIGHT // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        DISPLAYSURF.blit(restart_text, (SCREEN_HEIGHT // 2 - 250, SCREEN_HEIGHT // 2))

    if fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        DISPLAYSURF.blit(fade_surface, (0, 0))
        fade_alpha -= 1

    pygame.display.flip()


    pygame.display.update()
    fps.tick(FPS)