import pygame
import random
import os

pygame.init()  


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PIPE_WIDTH = 70
PIPE_GAP = 150
GRAVITY = 0.10
FLAP_STRENGTH = -8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load Assets
flap_sound = pygame.mixer.Sound(os.path.join("assets", "flap.wav"))
hit_sound = pygame.mixer.Sound(os.path.join("assets", "hit.wav"))
bird_img = pygame.image.load(os.path.join("assets", "bird.png"))
bird_img = pygame.transform.scale(bird_img, (50, 35))  # Resize bird if needed

# Bird Class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH
        flap_sound.play()

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        rotated_bird = pygame.transform.rotate(bird_img, -self.velocity * 2)               # Rotate based on velocity
        screen.blit(rotated_bird, (self.x, self.y))

# Pipe Class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= 5

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

# Main Game Function

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if game_over and event.key == pygame.K_r:
                    main()

        if not game_over:
            bird.update()

            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

            for pipe in pipes:
                pipe.update()
                pipe.draw()

                if (pipe.x < bird.x + 50 < pipe.x + PIPE_WIDTH) and \
                   (bird.y < pipe.height or bird.y + 35 > pipe.height + PIPE_GAP):
                    hit_sound.play()
                    game_over = True

                if pipe.x + PIPE_WIDTH < bird.x and not pipe.passed:
                    score += 1
                    pipe.passed = True

            bird.draw()

            if bird.y + 35 >= SCREEN_HEIGHT:
                hit_sound.play()
                game_over = True

        else:
            font = pygame.font.SysFont(None, 55)
            text = font.render("Game Over! Score: " + str(score), True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
            restart_text = font.render("Press R to Restart", True, BLACK)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(FPS)

# Game run

if __name__ == "__main__":
    main()





