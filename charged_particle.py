""" charged_particle.py: for a ChargedParticle class """

import pygame

# required initialization step
pygame.init()

RADIUS = 5
POSITIVE_COLOR = pygame.Color(25, 100, 230)
NEUTRAL_COLOR = pygame.Color(144, 144, 144)
NEGATIVE_COLOR = pygame.Color(204, 29, 6)

class ChargedParticle():

    def __init__(self, mass: int, charge: int, x_velocity: int,
                 pos: (int, int)):
        self.__mass = mass
        self.__velocity = (x_velocity, 0)
        self.__pos = pos
        self.__stopped = False
        self.set_charge(charge)

    def move(self, mag_field: int, elec_field: int):
        """ move the charged particle one frame's worth """
        self.__pos = (self.__pos[0] + self.__velocity[0],
                      self.__pos[1] + self.__velocity[1])

    def stop(self):
        self.__stopped = True

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.__color, pos, RADIUS)

    def erase(self, screen: pygame.Surface, background_color: pygame.Color):
        pygame.draw.circle(screen, background_color, pos, RADIUS)

    def set_charge(self, new_chage: int):
        self.__charge = new_charge
        if new_charge > 0:
            self.__color = POSITIVE_COLOR
        elif new_charge < 0:
            self.__color = NEGATIVE_COLOR
        else:
            self.__color = NEUTRAL_COLOR

    def set_mass(self, new_mass: int):
        if new_mass > 0:
            self.__mass = new_mass
        else:
            raise ValueError("Mass must be positive")
