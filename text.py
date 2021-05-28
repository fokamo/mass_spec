""" text.py: for a Text class """

import pygame

# required initialization step
pygame.init()

# color constant
TEXT_COLOR = pygame.Color(0, 0, 0)

class Text():
    """A textbox which draws itself in a particular area"""

    def __init__(self, text: str, font: pygame.font.Font,
                 area: pygame.Rect, background_color: pygame.Color,
                 centered=True):
        """ Initialize a Text

        text is the string to display, font is the Font the text should be in
        area is the rectangle the text should be centered & displayed in
        background_color is the expected background color for the font
        """
        
        # create the needed text-surface
        self.__text = font.render(text, True, TEXT_COLOR, background_color)
        if centered:
            # get (top, left) position to center text with
            self.__pos = self.__center_text(area)
        else:
            self.__pos = (0, 0)
        
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

def blit_paragraphs(area: pygame.Rect, paragraphs: list,
                    font: pygame.font.Font, background_color: pygame.Color,
                    screen: pygame.Surface):
    """  Helper function which uses Text to write multiline paragraphs """
    
    # 2D array: array per paragrah, with elements being words
    words = [paragraph.split(' ') for paragraph in paragraphs]
    
    line_length = 0
    line_height = 0
    y = area.top
    
    for paragraph in words:
        line = ''
        for word in paragraph:
            # grab width & height of this word
            word_width, word_height = \
                        font.render(word, 0, TEXT_COLOR).get_size()

            # if this word would cause an overflow
            if line_length + word_width >= area.width:
                # blit line so far
                final_line = Text(line, font,
                                  pygame.Rect(area.left, y,
                                              area.width, line_height),
                                  background_color)
                final_line.draw(screen)
                # reset back down to next line
                line_length = 0
                y += line_height + 1
                line = word
            # otherwise just add the word to the line
            else:
                line += ' ' + word
                if line_height < word_height:
                    line_height = word_height
            line_length += word_width
            line += word
            
        line_length - 0
        y += (2 * (line_height + 1))
