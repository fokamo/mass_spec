""" mass_spectrometer.py: for a MassSpectrometer class """

import pygame
import charged_particle

# required initialization step
pygame.init()

WALL_THICKNESS = 10
WALL_COLOR = pygame.Color(148, 134, 106)

class MassSpectrometer():

    def __init__(self, area: pygame.Rect, mass: int, charge: int,
                 initial_x_velocity: int, e_field: int, mag_field: int):
        # save information about particle
        self.__area = area
        self.__mass = mass
        self.__charge = charge
        self.set_initial_x_velocity(initial_x_velocity)
        self.__particle_start_pos = (charged_particle.RADIUS, area.height / 2)

        # generates new particle
        self.reset_particle()

        self.e_field = e_field
        self.mag_field = mag_field
        
        self.__walls = self.__generate_walls(area)

    def __generate_walls(self, area: pygame.Rect) -> tuple:
        """ Create properly-placed walls

        2/5 from edge to a horizontal wall, 1/5 between them
        1/2 is given to horizontal walls
        verticle walls sprout out from ends of horizontal ones
        """
        
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
        """ Draw whole mass spectrometer, moving particle a frame """

        # electric field only works in first half (horizontal section)
        if (self.__particle.get_pos()[0] >
            self.__area.left + (self.__area.width / 2)):
            self.__particle.move(0, self.mag_field)
        else:
            self.__particle.move(self.e_field, self.mag_field)

        # draw moved particle
        self.__particle.draw(screen)

        # draw each wall
        for wall in self.__walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
            if self.__particle.is_collision(wall):
                self.__particle.stop()

        particle_y = self.__particle.get_pos()[1]
        if (particle_y < self.__area.top or
            particle_y > self.__area.top + self.__area.height):
            self.__particle.stop()

    def reset_particle(self):
        """ Resets particle back to start position """
        
        self.__particle = charged_particle.ChargedParticle(
            self.__mass, self.__charge, self.__initial_x_velocity,
            self.__particle_start_pos)

    def set_mass(self, new_mass: int):
        """ Update mass,

        Checks to make sure new value is legal
        """
        
        self.__particle.set_mass(new_mass)

    def set_charge(self, new_charge: int):
        """Update charge """

        self.__particle.set_charge(new_charge)

    def set_initial_x_velocity(self, new_initial_x_velocity: int):
        """ Update initial x velocity

        Checks to make sure new value is legal
        """

        if new_initial_x_velocity > 0:
            self.__initial_x_velocity = new_initial_x_velocity
        else:
            raise ValueError("Initial x velocity must be positive")
