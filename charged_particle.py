""" charged_particle.py: for a ChargedParticle class """

import math
import pygame

# required initialization step
pygame.init()

# radius of charged particles - constant
RADIUS = 5

# the particle will have different colors depending on its charge
POSITIVE_COLOR = pygame.Color(25, 100, 230)
NEUTRAL_COLOR = pygame.Color(144, 144, 144)
NEGATIVE_COLOR = pygame.Color(204, 29, 6)

class ChargedParticle():
    """ a charge particle

    Affected by electric and magnetic fields - accelerates accordingly
    Can draw itself, move, and detect collisions
    """

    def __init__(self, mass: int, charge: int, initial_x_velocity: int,
                 pos: (int, int)):
        self.__mass = mass
        self.set_charge(charge)
        self.__velocity = (initial_x_velocity, 0)
        self.__pos = pos
        # flag to see if movement is allowed
        self.__stopped = False

    def move(self, e_field: int, mag_field: int):
        """ move the charged particle one frame's worth """

        # only move if allowed
        if not self.__stopped:
            # move with current velocity
            self.__pos = (self.__pos[0] + self.__velocity[0],
                          self.__pos[1] + self.__velocity[1])
            
            # calculate force on particle
            electric_force = e_field * self.__charge
            magnetic_force = self.__calc_mag_force(mag_field)
            total_force = (magnetic_force[0],
                           electric_force + magnetic_force[1])
            # a = F/m
            acceleration = (total_force[0] / self.__mass,
                            total_force[1] / self.__mass)
            # update velocity with acceleration
            self.__velocity = (self.__velocity[0] + acceleration[0],
                               self.__velocity[1] + acceleration[1])

    def __calc_mag_force(self, mag_field: int) -> (int, int):
        """ Internal helper function for calculating magnetic force

        Note that theta is measured clockwise, with 0 = to the right
        """

        # shorter variable names for easy reference
        v_x, v_y = self.__velocity

        # find angle which the particle is travelling in
        
        # -pi/2 < theta < pi/2
        if v_x > 0:
            theta = math.atan((-1 * v_y) / v_x)
        # pi/2 < theta < 3pi/2
        elif v_x < 0:
            # arctan only outputs in -pi/2 -> -pi/2 range 
            theta = math.pi + math.atan((-1 * v_y) / v_x)
        # theta = -pi/2
        elif v_y > 0:
            theta = -1 * (math.pi / 2)
        # theta = pi/2
        else:
            theta = (math.pi / 2)

        # use L/R HR to move in correct perpendicular direction
        theta -= math.pi / 2
        # calculate current velocity (round since that reflects normal usage)
        total_v = (int) ((100 * math.sqrt((v_y * v_y) + (v_x * v_x))) / 100)
        # F_M = qvB
        total_f = self.__charge * total_v * mag_field

        # calculate x and y components of magnetic force
        return total_f * math.cos(theta), -1 * (total_f * math.sin(theta))

    def stop(self):
        """ Set no-moving-allowed flag """
        
        self.__stopped = True

    def draw(self, screen: pygame.Surface):
        """ Draw particle """
        
        pygame.draw.circle(screen, self.__color, self.__pos, RADIUS)

    def set_charge(self, new_charge: int):
        """ Update charge & color """
        
        self.__charge = new_charge

        # color is dependent on sign
        if new_charge > 0:
            self.__color = POSITIVE_COLOR
        elif new_charge < 0:
            self.__color = NEGATIVE_COLOR
        else:
            self.__color = NEUTRAL_COLOR

    def set_mass(self, new_mass: int):
        """ Update mass, checking to make sure new value is legal """
        
        if new_mass > 0:
            self.__mass = new_mass
        else:
            raise ValueError("Mass must be positive")

    def is_collision(self, rect: pygame.Rect):
        """ Check if particle collides with given rectangle """

        # check for collision between rect & particle's collision box
        return rect.colliderect(
            pygame.Rect(self.__pos[0] - RADIUS, self.__pos[1] - RADIUS,
                        RADIUS * 2, RADIUS * 2)
            )

    def get_pos(self):
        """ Return current position """
        
        return self.__pos
