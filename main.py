import os
import time
import random
import pygame
import neat

# Set the window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

# Load the images
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))


class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES[0]

    def jump(self):
        self.velocity   = -10.5       #
        self.tick_count =  0
        self.height     =  self.y

    def move(self):
        print(f"bird moving at: {self.velocty}(m/s)")

        self.tick_count += 1

        displacement = self.velocity*self.tick_count + 1.5*self.tick_count**2

        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2

        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME*2:
            self.image = self.IMAGES[1]
        elif self.image < self.ANIMATION_TIME*3:
            self.image = self.IMAGES[2]
        elif self.image < self.ANIMATION_TIME*4:
            self.image = self.IMAGES[1]
        elif self.image < self.ANIMATION_TIME*4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0

        if self.tilt <= -80:
            self.image       = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME*2


        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectanlge = rotated_image.get_rect(center= self.image.get_rect(topLeft = (self.x, self.y )).center) # from stack overflow
        window.blit(rotated_image, new_rectanlge.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    ###########################################################################################################################################




def draw_window(window, bird):
    window.blit(BACKGROUND_IMAGE, (0,0))
    bird.draw(window)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        draw_window(window, bird)

    
    pygame.quit()
    quit()


main()