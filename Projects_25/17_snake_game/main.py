import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game by Saira')
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

class Snake:
    def __init__(self):
        self.body = [(100, 50), (80, 50), (60, 50)]
        self.direction = 'RIGHT'
        self.grow_pending = False

    def move(self):
        x, y = self.body[0]
        if self.direction == 'UP':
            y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            y += BLOCK_SIZE
        elif self.direction == 'LEFT':
            x -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            x += BLOCK_SIZE
        new_head = (x, y)
        self.body = [new_head] + self.body
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, DARK_GREEN, (segment[0]+2, segment[1]+2, BLOCK_SIZE-4, BLOCK_SIZE-4))

    def check_collision(self):
        head = self.body[0]
        return (
            head in self.body[1:] or
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT
        )

# Food class
class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):
        while True:
            x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# Draw grid 
def draw_grid(surface):
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

# Game Over 
def game_over_screen(score):
    screen.fill(BLACK)
    text1 = font.render(f"Game Over! Your Score: {score}", True, WHITE)
    text2 = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main game 
def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake.direction != 'DOWN':
            snake.direction = 'UP'
        elif keys[pygame.K_DOWN] and snake.direction != 'UP':
            snake.direction = 'DOWN'
        elif keys[pygame.K_LEFT] and snake.direction != 'RIGHT':
            snake.direction = 'LEFT'
        elif keys[pygame.K_RIGHT] and snake.direction != 'LEFT':
            snake.direction = 'RIGHT'

        snake.move()

        # Food collision
        if snake.body[0] == food.position:
            snake.grow()
            food = Food(snake.body)
            score += 1

        # Check game over
        if snake.check_collision():
            game_over_screen(score)

        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

main()

