""" text.py: for a Text class """

import pygame

# required initialization step
pygame.init()

# color constant
TEXT_COLOR = pygame.Color(0, 0, 0)

class Text():
    """A textbox which draws itself in a particular area"""

    def __init__(self, text: str, font: pygame.font.Font,
                 area: pygame.Rect, background_color: pygame.Color):
        """ Initialize a Text

        text is the string to display, font is the Font the text should be in
        area is the rectangle the text should be centered & displayed in
        background_color is the expected background color for the font
        """
        
        # create the needed text-surface
        self.__text = font.render(text, True, TEXT_COLOR, background_color)
        # get (top, left) position to center text with
        self.__pos = self.__center_text(area)
        
    def __center_text(self, rect: pygame.Rect) -> (int, int):
        """ Helper function to center text

        text is a text-surface which needs to be centered
        rect is the rectangular field which the text should be centered in
        the return value is a tuple with (left, top) values for where
            the text should be blitted to
        """
        
        # temporary text Rect, used to grab width/height for centering text
        temp_rect = self.__text.get_rect()
        return (rect.left + (rect.width / 2) - (temp_rect.width / 2),
                rect.top + (rect.height / 2) - (temp_rect.height / 2)
                )

    def draw(self, screen: pygame.Surface):
        """ Blits the text onto the designated surface """
        
        screen.blit(self.__text, self.__pos)
