import pygame
import math
import random


BIRD_SPEED = 5
EGG_DROP_SPEED = 30
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (135, 206, 235)
BLACK = (0, 0, 0)
kills = 0
level = 1  
NUM_PIGS = 5  
SCORE_TO_LEVEL_UP = 10 

pygame.init()

pig1_image = pygame.transform.scale(pygame.image.load('прост свин.png'), (50, 50))
pig2_image = pygame.transform.scale(pygame.image.load('дед.png'), (50, 50))
pig3_image = pygame.transform.scale(pygame.image.load('гавнюк.png'), (50, 50))


egg_image = pygame.transform.scale(pygame.image.load('яйко.png'), (50, 50))
bird_image = pygame.transform.scale(pygame.image.load('матильда.jpg'), (150, 150))

PIG_IMAGES = [pig1_image, pig2_image, pig3_image] 

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("энгрибердз")


class Egg(pygame.sprite.Sprite):
    def __init__(self, bird):
        super().__init__()
        self.image = egg_image
        self.rect = self.image.get_rect()
        self.dropping = False
        self.bird = bird
        self.follow_bird()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and not self.dropping:
            self.dropping = True
            self.rect.center = self.bird.rect.center

        if self.dropping:
            self.rect.y += 30

        if self.rect.bottom > 1000:
            self.dropping = False
            self.follow_bird()

    def follow_bird(self):
        self.rect.center = self.bird.rect.center
        self.rect.y = self.bird.rect.top


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (50, 50)
        self.speed = BIRD_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
class Pig(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(PIG_IMAGES)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 1000 - self.rect.width)
        self.rect.y = 500
        self.speed = 3

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > 1000 or self.rect.left < 0:
            self.speed *= -1

    def kill_pig(self):
        self.kill()


speed = 5
bird = Bird()
egg = Egg(bird)

pigs = pygame.sprite.Group()
for _ in range(NUM_PIGS):
    pig = Pig()
    pigs.add(pig)

all_sprites = pygame.sprite.Group()
all_sprites.add(bird, egg)
all_sprites.add(pigs)

running = True
clock = pygame.time.Clock()


def game_loop():
    global running, kills, BLACK, pigs, level

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        egg.update()
        bird.update()
        for pig in pigs:
            pig.update()

        
        if egg.dropping:
            for pig in pigs:
                if pygame.sprite.collide_rect(egg, pig):
                    pig.kill_pig()
                    kills += 1

                    
                    if kills % SCORE_TO_LEVEL_UP == 0:
                        level += 1


                    
                    new_pig = Pig()
                    pigs.add(new_pig)
                    all_sprites.add(new_pig)

                    egg.dropping = False
                    egg.follow_bird()
                    break

        if not egg.dropping:
            egg.follow_bird()

        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        font = pygame.font.Font(None, 36)
        text_score = font.render("Счет: " + str(kills), True, BLACK)
        text_level = font.render("Уровень: " + str(level), True, BLACK)
        screen.blit(text_score, (10, 10))
        screen.blit(text_level, (10, 40)) 
        pygame.display.flip()


game_loop()
pygame.quit()            
