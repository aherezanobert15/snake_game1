import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Game settings
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
FPS = 10

# Directions
UP = (0, -BLOCK_SIZE)
DOWN = (0, BLOCK_SIZE)
LEFT = (-BLOCK_SIZE, 0)
RIGHT = (BLOCK_SIZE, 0)

class Snake:
    def __init__(self):
        self.body = [(200, 200), (210, 200), (220, 200)]  # Start position
        self.direction = LEFT
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        # Prevent reverse
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def check_collision(self):
        head = self.body[0]
        # Wall
        if head[0] >= WIDTH or head[0] < 0 or head[1] >= HEIGHT or head[1] < 0:
            return True
        # Self
        if head in self.body[1:]:
            return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = self.random_pos()

    def random_pos(self):
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, BLOCK_SIZE, BLOCK_SIZE))

def draw_score(screen, score):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        snake.move()

        # Eat food
        if snake.body[0] == food.position:
            snake.grow = True
            score += 1
            food.position = food.random_pos()

        if snake.check_collision():
            running = False

        # Draw
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, score)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()