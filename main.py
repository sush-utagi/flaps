import os
import time
import random
import neat
import neat.config
import neat.nn.feed_forward
import pygame
import neat
pygame.font.init()

# Set the window size
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

# Load the images
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

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
        # print(f"bird moving at: {self.velocity}(m/s)")
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

        if self.image_count <= self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count <= self.ANIMATION_TIME*2:
            self.image = self.IMAGES[1]
        elif self.image_count <= self.ANIMATION_TIME*3:
            self.image = self.IMAGES[2]
        elif self.image_count <= self.ANIMATION_TIME*4:
            self.image = self.IMAGES[1]
        elif self.image_count <= self.ANIMATION_TIME*4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0

        if self.tilt <= -80:
            self.image       = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME*2

        blitRotateCenter(window, self.image, (self.x, self.y), self.tilt)


    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    


class Pipe:
    GAP             = 200
    VELOCITY        = 5

    def __init__(self, x):
        self.x      = x
        self.height = 0
        self.gap    = 100

        self.top    = 0
        self.bottom = 0
        self.PIPE_TOP    = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top    = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask    = bird.get_mask()
        top_mask     = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask  = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False
    

class Base:
    VELOCITY = 5
    WIDTH    = BASE_IMAGE.get_width()
    IMAGE    = BASE_IMAGE

    def __init__(self, y):
        self.y  = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if (self.x1 + self.WIDTH) < 0:
            self.x1 = (self.x2 + self.WIDTH)
        
        if (self.x2 + self.WIDTH) < 0:
            self.x2 = (self.x1 + self.WIDTH)

    def draw(self, window):
        window.blit(self.IMAGE, (self.x1, self.y))
        window.blit(self.IMAGE, (self.x2, self.y))



    
# HELPER FUNCTIONS -----------------------------------------------------------------------------------------

def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)



# ----------------------------------------------------------------------------------------------------------

# WINDOW DRAWING FUNCTIONS
def draw_window(window, birds, pipes, base, score):
    window.blit(BACKGROUND_IMAGE, (0,0))

    for pipe in pipes:
        pipe.draw(window)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    window.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

    base.draw(window)
    # bird.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()


def main(genomes, config):

    nets = []
    ge = []
    birds = []  # Bird(230, 350)

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        genome.fitness = 0
        ge.append(genome)




    base = Base(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if (len(pipes) > 1) and birds[0].x > birds[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index +=1
        else:
            running = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1

            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()


        add_pipe = False
        removed_pipes = []
        for pipe in pipes:

            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    print("COLLISION WITH PIPE")
                    ge[i].fitness -= 2
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)


                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed_pipes.append(pipe)


            pipe.move()
        
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for item in removed_pipes:
            pipes.remove(item)

        for i, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        base.move()
        draw_window(window, birds, pipes, base, score)       # draw frame


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                                config_path)
    
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)

    winner = population.run(main,100)



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)