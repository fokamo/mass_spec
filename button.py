""" button.py: for a Button class """

import pygame
import text

# required initialization step
pygame.init()

# font constants
BUTTON_FONT = pygame.font.SysFont('calibri', 35)

class Button(pygame.Rect):
    """A button which can draw itself and be clicked"""

    def __init__(self, left: int, top: int, width: int, height: int,
                 txt: str, color: pygame.Color):
        """ Initialize a Button

        left, top, width, and height determine the size of the Button
        text is the Button's label, color is the Button's background color
        """
        
        super().__init__(left, top, width, height)
        
        # make a text-surface to be blitted later
        self.__text = text.Text(txt, BUTTON_FONT, self, color)
        self.__color = color

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """ Check if a given mouse click is on the button """
        
        return super().collidepoint(mouse_x, mouse_y)

    def draw(self, screen: pygame.Surface) -> None:
        """ Draw the Button onto a given Surface """

        # draw rectangle then text on top
        pygame.draw.rect(screen, self.__color, self)
        self.__text.draw(screen)
