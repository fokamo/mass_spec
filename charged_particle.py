""" charged_particle.py: for a ChargedParticle class """

import math
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
        self.__rect = pygame.Rect(pos[0] - RADIUS, pos[1] - RADIUS,
                                  RADIUS * 2, RADIUS * 2)
        self.set_charge(charge)

    def move(self, e_field: int, mag_field: int):
        """ move the charged particle one frame's worth """

        if not self.__stopped:
            self.__pos = (self.__pos[0] + self.__velocity[0],
                          self.__pos[1] + self.__velocity[1])
            self.__rect = pygame.Rect(self.__pos[0] - RADIUS,
                                      self.__pos[1] - RADIUS,
                                      RADIUS * 2, RADIUS * 2)

            electric_force = e_field * self.__charge
            magnetic_force = self.__calc_mag_force(mag_field)
            total_force = (magnetic_force[0],
                           electric_force + magnetic_force[1])
            acceleration = (total_force[0] / self.__mass,
                            total_force[1] / self.__mass)
            if acceleration != (0, 0):
                print(acceleration)
            self.__velocity = (self.__velocity[0] + acceleration[0],
                               self.__velocity[1] + acceleration[1])

    def __calc_mag_force(self, mag_field: int):
        v_x, v_y = self.__velocity
        if v_x != 0:
            theta = math.atan(v_y / v_x)
        elif v_y > 0:
            theta = -1 * (math.pi / 2)
        else:
            theta = math.pi / 2
        theta += (math.pi * (mag_field * self.__charge > 0)) - (math.pi / 2)
        print(theta)
        total_v = (int) ((100 * math.sqrt((v_y * v_y) + (v_x * v_x))) / 100)
        total_f = math.fabs(self.__charge * total_v * mag_field)
        return total_f * math.cos(theta), total_f * math.sin(theta)

    def stop(self):
        self.__stopped = True

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.__color, self.__pos, RADIUS)

    def set_charge(self, new_charge: int):
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

    def is_collision(self, rect: pygame.Rect):
        return rect.colliderect(self.__rect)

    def get_pos(self):
        return self.__pos
