import pygame, random

#Returns random velocity
def get_random_velocity(velocity, intensity):
    velocity = velocity.copy()
    velocity[0] += random.uniform(0,intensity*2)-intensity
    velocity[1] += random.uniform(0,intensity*2)-intensity
    return velocity

def get_colliding_rects(rect1, rects):
    colliding_rects = []

    for rect in rects:
        if rect1.colliderect(rect):
            colliding_rects.append(rect)

    return colliding_rects

class Particle:
    def __init__(self, position, velocity, size, decrementation, color, special_flags, collidables):
        self.position = [position[0]-size/2, position[1]-size/2]
        self.velocity = velocity
        self.size = size
        self.r = size
        self.decrementation = decrementation
        self.color = color
        self.special_flags = special_flags
        self.collidables = collidables

    #Returns surface
    @property
    def surface(self):
        surface = pygame.Surface((self.size*2, self.size*2))
        pygame.draw.circle(surface, self.color, (self.size,self.size), self.r)
        surface.set_colorkey((0,0,0))
        return surface

    #Returns if the radius is 0
    @property
    def dead(self):
        return self.r <= 0

    #Renders the particle
    def render(self, surface, scroll):
        surface.blit(self.surface, [self.position[0]-scroll[0], self.position[1]-scroll[1]], special_flags=self.special_flags)

    #Moves the particle
    def move(self):
        collisions = {k:False for k in ['vertical', 'horizontal']}
        self.position[0] += self.velocity[0]
        rect = self.rect
        hit_list = get_colliding_rects(rect, self.collidables)

        for obj in hit_list:
            if self.velocity[0] > 0:
                rect.right = obj.left
                self.position[0] = rect.x
            if self.velocity[0] < 0:
                rect.left = obj.right
                self.position[0] = rect.x
            collisions['horizontal'] = True

        self.position[1] += self.velocity[1]
        rect = self.rect
        hit_list = get_colliding_rects(rect, self.collidables)

        for obj in hit_list:
            if self.velocity[1] > 0:
                rect.bottom = obj.top
                self.position[1] = rect.y
            if self.velocity[1] < 0:
                rect.top = obj.bottom
                self.position[1] = rect.y
            collisions['vertical'] = True

        if collisions['horizontal']:
            self.velocity[0] *= -1
        if collisions['vertical']:
            self.velocity[1] *= -1

    #Runs the particle
    def run(self):
        self.move()
        self.r -= self.decrementation

    @property
    def rect(self):
        return pygame.Rect(self.position[0]-self.r/2, self.position[1]-self.r/2, self.r, self.r)

class Particle_System:
    def __init__(self):
        self.particles = []

    def render(self, surface, scroll):
        for particle in self.particles[:]:
            particle.render(surface, scroll)

    #Runs all the particles
    def run(self):
        for particle in self.particles[:]:
            particle.run()

            if particle.dead:
                self.particles.remove(particle)

    #Adds a particle to the list
    def add_particle(self, position, velocity, size=10, decrementation=0.1, color=(255,255,255), special_flags=0, intensity=1, number=1, collidables=[]):
        for i in range(number):
            vel = get_random_velocity(velocity, intensity)
            dec = random.uniform(0.2, decrementation)
            self.particles.append(Particle(position, vel, size, dec, color, special_flags, collidables))

    #Removes all the particles from the list
    def clear(self):
        self.particles.clear()
