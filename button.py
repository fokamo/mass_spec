""" button.py: for a Button class """

import pygame

# required initialization step
pygame.init()

# font constants
BUTTON_FONT = pygame.font.SysFont('calibri', 35)
FONT_COLOR = pygame.Color(0, 0, 0)

class Button(pygame.Rect):
    """A button which can draw itself and be clicked"""

    def __init__(self, left: int, top: int, width: int, height: int,
                 text: str, color: pygame.Color):
        """ Initializes a Button

        left, top, width, and height determine the size of the Button
        text is the Button's label, color is the Button's background color
        """
        
        super().__init__(left, top, width, height)
        # make a text-surface to be blitted later
        self.__text = BUTTON_FONT.render(text, True, FONT_COLOR, color)
        self.__color = color

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """ Check for button clicks """
        
        return super().collidepoint(mouse_x, mouse_y)

    def draw(self, screen: pygame.Surface) -> None:
        """ Draw the Button onto a given Surface """

        # draw rectangle then text on top
        pygame.draw.rect(screen, self.__color, self)
        screen.blit(self.__text, self)
