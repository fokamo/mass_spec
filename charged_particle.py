"""charged_particle.py: for a ChargedParticle class

Classes:
ChargedParticle -- for representing a moving charged particle

Constants:
RADIUS -- radius of a particle
POSITIVE_COLOR -- color of a particle with a positive (>0) charge
NEUTRAL_COLOR -- color of a particle with a netural (=0) charge
NEGATIVE_COLOR -- color of a particle with a negative (<0) charge
"""

import math
import pygame

# required initialization step
pygame.init()

# radius of charged particles
RADIUS = 5

# the particle will have different colors depending on its charge
POSITIVE_COLOR = pygame.Color(25, 100, 230)
NEUTRAL_COLOR = pygame.Color(144, 144, 144)
NEGATIVE_COLOR = pygame.Color(204, 29, 6)

class ChargedParticle():
    """A class to represent a charged particle.

    Attributes:
    _mass -- mass of the particle
    _charge -- charge of the particle
    _color -- color of the particle (depends on charge)
    _velocity -- (x, y) velocity of the particle
    _pos -- (x, y) position of the particle
    _stopped -- whether the particle is stopped

    Methods:
    move -- moves & accelerates the particle
    draw -- draws the particle on a Surface
    stop -- forces particle to stop moving (irreversible from outside)
    set_mass -- sets _mass to a new value
    set_charge -- sets _charge to a new value, also updating _color
    is_collision -- checks if the particle has collided with a Rect
    get_pos -- getter for _pos
    """

    def __init__(self, mass: int, charge: int, initial_x_velocity: int,
                 pos: (int, int)) -> None:
        """Initialize a ChargedParticle.

        mass -- mass of the particle
        charge -- charge of the particle
        initial_x_velocity -- initial x velocity of the particle (v_y_0 = 0)
        pos -- initial (x, y) position of the particle
        """
        
        self._mass = mass
        # will also set color
        self.set_charge(charge)
        self._velocity = (initial_x_velocity, 0)
        self._pos = pos
        self._stopped = False

    def move(self, e_field: int, mag_field: int) -> None:
        """Move and accelerate the charged particle one frame's worth.

        e_field -- electric field strength, positive is down
        mag_field -- magnetic field strength, positive is out of page
        """

        # only move if allowed
        if not self._stopped:
            # move with current velocity
            self._pos = (self._pos[0] + self._velocity[0],
                         self._pos[1] + self._velocity[1])
            
            # calculate force on particle
            electric_force = e_field * self._charge
            magnetic_force = self._calc_mag_force(mag_field)
            total_force = (magnetic_force[0],
                           electric_force + magnetic_force[1])
            # Newton's Second Law, a = F/m
            acceleration = (total_force[0] / self._mass,
                            total_force[1] / self._mass)
            
            # update velocity with acceleration
            self._velocity = (self._velocity[0] + acceleration[0],
                               self._velocity[1] + acceleration[1])

    def _calc_mag_force(self, mag_field: int) -> (int, int):
        """Calculate magnetic force on charge

        Note that theta is measured clockwise, with 0 = to the right

        mag_field -- magnetic field strength, positive is out of page

        Returns force on the particle in (x, y) direction
        """

        # shorter variable names for easy reference
        v_x, v_y = self._velocity

        # find angle which the particle is travelling in (velocity direction)
        
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

        # force is perpendicular to velocity
        theta -= math.pi / 2
        # calculate current velocity
        total_v = math.sqrt((v_y * v_y) + (v_x * v_x))
        # F_M = qvB, and use L/R HR
        total_f = self._charge * total_v * mag_field

        # calculate x and y components of magnetic force
        return total_f * math.cos(theta), -1 * (total_f * math.sin(theta))

    def stop(self) -> None:
        """Set no-moving-allowed flag."""
        
        self._stopped = True

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the particle onto a given Surface."""
        
        pygame.draw.circle(screen, self._color, self._pos, RADIUS)

    def set_mass(self, new_mass: int) -> None:
        """Update mass, checking to make sure new value is legal."""
        
        if new_mass > 0:
            self._mass = new_mass
        else:
            raise ValueError("Mass must be positive")

    def set_charge(self, new_charge: int) -> None:
        """Update charge, and then color to correspond."""
        
        self._charge = new_charge

        # color is dependent on sign
        if new_charge > 0:
            self._color = POSITIVE_COLOR
        elif new_charge < 0:
            self._color = NEGATIVE_COLOR
        else:
            self._color = NEUTRAL_COLOR

    
    def is_collision(self, rect: pygame.Rect) -> bool:
        """Check if particle collides with given rectangle."""
        
        # check for collision between rect & particle's collision box
        return rect.colliderect(
            pygame.Rect(self._pos[0] - RADIUS, self._pos[1] - RADIUS,
                        RADIUS * 2, RADIUS * 2)
            )

    def get_pos(self) -> (int, int):
        """Get current position."""
        
        return self._pos
