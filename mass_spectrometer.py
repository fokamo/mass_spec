""" mass_spectrometer.py: for a MassSpectrometer class """

import pygame
import charged_particle

# required initialization step
pygame.init()

WALL_THICKNESS = 4
WALL_COLOR = pygame.Color(148, 134, 106)

class MassSpectrometer():

    def __init__(self, area: pygame.Rect, mass: int, charge: int,
                 initial_x_velocity: int, e_field: int, mag_field: int):
        self.__area = area
        self.__mass = mass
        self.__charge = charge
        self.__initial_x_velocity = initial_x_velocity
        self.__particle_start_pos = (charged_particle.RADIUS, area.height / 2)
        self.reset_particle()
        self.e_field = e_field
        self.mag_field = mag_field
        self.__walls = self.__generate_walls(area)

    def __generate_walls(self, area: pygame.Rect):
        upper_horizontal = pygame.Rect(
            area.left, area.top + (2 * area.height / 5) - (WALL_THICKNESS / 2),
            (area.width / 2) - (WALL_THICKNESS / 2), WALL_THICKNESS)
        lower_horizontal = pygame.Rect(
            area.left, area.top + (3 * area.height / 5) - (WALL_THICKNESS / 2),
            (area.width / 2) - (WALL_THICKNESS / 2), WALL_THICKNESS)
        upper_vertical = pygame.Rect(
            area.left + (area.width / 2) - (WALL_THICKNESS / 2), 0,
            WALL_THICKNESS, 2 * area.height / 5)
        lower_vertical = pygame.Rect(
            area.left + (area.width / 2) - (WALL_THICKNESS / 2),
            3 * area.height / 5, WALL_THICKNESS, 2 * area.height / 5)
        return (upper_horizontal, lower_horizontal,
                upper_vertical, lower_vertical)

    def draw(self, screen: pygame.Surface):
        self.__particle.move(self.e_field, self.mag_field)
        self.__particle.draw(screen)
        
        for wall in self.__walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)

    def reset_particle(self):
        self.__particle = charged_particle.ChargedParticle(
            self.__mass, self.__charge, self.__initial_x_velocity,
            self.__particle_start_pos)
