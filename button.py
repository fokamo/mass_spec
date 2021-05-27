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

    def is_clicked(self, mouse_pos) -> bool:
        """ Check for button clicks """
        
        return pygame.Rect.collidepoint(mouse_pos[0], mouse_pos[1])

    def draw(self, screen: pygame.Surface) -> None:
        """ Draw the Button onto a given Surface """

        # draw rectangle then text on top
        pygame.draw.rect(screen, self.__color, self)
        screen.blit(self.__text, self)
