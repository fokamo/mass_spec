""" mass_spectrometer.py: for a MassSpectrometer class

Classes:
MassSpectromter -- representing a mass spectrometer

Constants:
WALL_THICKNESS -- thickness of walls, in pixels
WALL_COLOR -- color of walls
"""

import pygame
import charged_particle

# required initialization step
pygame.init()

# wall constants
WALL_THICKNESS = 10
WALL_COLOR = pygame.Color(148, 134, 106)

class MassSpectrometer():
    """A class to represent a mass spectrometer.

    Attributes:
    e_field -- electric field strength, positive is down
    mag_field -- magnetic field strength, positive is out of page
    _mass -- mass of charged particle
    _charge -- charge of charged particle
    _initial_x_velocity -- x velocity of charged particles at launch
    _area -- rectangular area that mass spectrometer takes up
    _particle -- current charged particle in mass spectrometer
    _walls -- list of Rects which are the walls of the mass spectrometer

    Methods:
    move -- move particle a frame
    draw -- draws the mass spectrometer on a Surface
    reset_particle -- reset the charged particle back to start
    set_mass -- sets _mass to a new value
    set_charge -- sets _charge to a new value
    set_initial_x_velocity -- sets initial x velocity to a new value
    """

    def __init__(self, e_field: int, mag_field: int, mass: int, charge: int,
                 initial_x_velocity: int, area: pygame.Rect):
        """Initialize a MassSpectrometer.

        e_field -- electric field strength, positive is down
        mag_field -- magnetic field strength, positive is out of page
        mass -- mass of charged particle
        charge -- charge of charged particle
        initial_x_velocity -- x velocity of charged particles at launch
        area -- rectangular area that mass spectrometer takes up
        """

        self.e_field = e_field
        self.mag_field = mag_field

        # save information about particle
        self._mass = mass
        self._charge = charge
        self.set_initial_x_velocity(initial_x_velocity)

        self._area = area

        # generate new particle
        self.reset_particle()
        self._walls = self._generate_walls(area)

    def _generate_walls(self, area: pygame.Rect) -> (pygame.Rect, pygame.Rect,
                                                     pygame.Rect, pygame.Rect):
        """Create properly-placed walls.

        2/5 from top/bottom to a horizontal wall, 1/5 between them
        1/2 of horizontal space goes to horizontal walls
        verticle walls sprout out from ends of horizontal ones

        area -- rectangular area that the mass spectrometer may take up

        Returns tuple with all walls as Rects
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

    def move(self):
        """Move particle one frame."""
        
        # electric field only works in first half (horizontal section)
        if (self._particle.get_pos()[0] >
            self._area.left + (self._area.width / 2)):
            self._particle.move(0, self.mag_field)
        else:
            self._particle.move(self.e_field, self.mag_field)

    def draw(self, screen: pygame.Surface):
        """Draw mass spectrometer onto a given Surface."""

        # draw particle
        self._particle.draw(screen)

        # draw each wall
        for wall in self._walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
            # particle stops if it hits a wall
            if self._particle.is_collision(wall):
                self._particle.stop()

        # particle stops if it hits the top or bottom edge
        particle_y = self._particle.get_pos()[1]
        if (particle_y < self._area.top or
            particle_y > self._area.top + self._area.height):
            self._particle.stop()

    def reset_particle(self):
        """Reset particle back to start position."""
        
        self._particle = charged_particle.ChargedParticle(
            self._mass, self._charge, self._initial_x_velocity,
            (charged_particle.RADIUS, self._area.height / 2))

    def set_mass(self, new_mass: int):
        """Update mass."""
        
        self._particle.set_mass(new_mass)
        # must also save to self for resetting purposes
        self._mass = new_mass

    def set_charge(self, new_charge: int):
        """Update charge."""

        self._particle.set_charge(new_charge)
        # must also save to self for resetting purposes
        self._charge = new_charge

    def set_initial_x_velocity(self, new_initial_x_velocity: int):
        """Update initial x velocit, checking if new value is legal."""

        if new_initial_x_velocity > 0:
            self._initial_x_velocity = new_initial_x_velocity
        else:
            raise ValueError("Initial x velocity must be positive")
