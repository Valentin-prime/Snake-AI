from random import randint
import pygame

class Snake:
    def __init__(self, center_x: int, center_y: int, pixel_size: int) -> None:
        self.size = 3
        self.direction = 'right'
        self.head = (center_x, center_y)
        self.body = [(center_x - (i+1)*pixel_size, center_y) for i in range(self.size - 1)]
        self.pixel_size = pixel_size
    
    def move(self) -> None:
        if self.size == len(self.body) + 1:
            self.body.pop(-1)
        self.body.insert(0, self.head)
        
        if self.direction == 'left':
            self.head = (self.head[0] - self.pixel_size, self.head[1])
        elif self.direction == 'right':
            self.head = (self.head[0] + self.pixel_size, self.head[1])
        elif self.direction == 'up':
            self.head = (self.head[0], self.head[1] - self.pixel_size)
        elif self.direction == 'down':
            self.head = (self.head[0], self.head[1] + self.pixel_size)
    
    def get_body_pos(self) -> list:
        return [self.head] + self.body

    def display(self, screen, pixel_size: int) -> None:
        for segment in self.get_body_pos():
            pygame.draw.rect(screen, (0, 255, 0), (*segment, pixel_size, pixel_size))

def spawn_apple(window_size: tuple, pixel_size: int, snake: Snake) -> tuple:
    while True:
        x = randint(0, window_size[0]//pixel_size - 1) * pixel_size
        y = randint(0, window_size[1]//pixel_size - 1) * pixel_size
        if (x, y) not in snake.get_body_pos():
            return x, y

def game():
    pygame.init()
    pygame.display.set_caption('Snake')

    WINDOW_SIZE = (400, 400)
    PIXEL_SIZE = 20
    SCREEN = pygame.display.set_mode(WINDOW_SIZE)

    clock = pygame.time.Clock()
    score = 0

    snake = Snake((WINDOW_SIZE[0]) // 2, (WINDOW_SIZE[1]) // 2, PIXEL_SIZE)
    apple = (randint(0, WINDOW_SIZE[0]//PIXEL_SIZE - 1) * PIXEL_SIZE, randint(0, WINDOW_SIZE[1]//PIXEL_SIZE - 1) * PIXEL_SIZE)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        SCREEN.fill((0, 0, 0))

        # Controls
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and snake.direction != 'right':
            snake.direction = 'left'
        elif keys[pygame.K_RIGHT] and snake.direction != 'left':
            snake.direction = 'right'
        elif keys[pygame.K_UP] and snake.direction != 'down':
            snake.direction = 'up'
        elif keys[pygame.K_DOWN] and snake.direction != 'up':
            snake.direction = 'down'
        snake.move()

        snake.display(SCREEN, PIXEL_SIZE)

        # Apple
        pygame.draw.rect(SCREEN, (255, 0, 0), (apple[0], apple[1], PIXEL_SIZE, PIXEL_SIZE))
        if apple[0] == snake.head[0] and apple[1] == snake.head[1]:
            apple = spawn_apple(WINDOW_SIZE, PIXEL_SIZE, snake)
            snake.size += 1
            score += 1
            print(score)

        # Death
        if snake.head in snake.get_body_pos()[1:]:
            running = False
        if snake.head[0] < 0 or snake.head[0] >= WINDOW_SIZE[0] or snake.head[1] < 0 or snake.head[1] >= WINDOW_SIZE[1]:
            running = False

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

# game()