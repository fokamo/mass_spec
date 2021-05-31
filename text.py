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
            self.__pos = (area.left, area.top)
        
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

def paragraphs_to_lines(area: pygame.Rect, paragraphs: list,
                        font: pygame.font.Font, background_color: pygame.Color):
    """  Helper function which converts paragraphs to line-by-line Texts """
    
    # 2D array: array per paragrah, with elements being words
    words = [paragraph.split(' ') for paragraph in paragraphs]
    
    line_length, line_height = 0, 0
    y = area.top
    lines = []
    
    for paragraph in words:
        cur_line = []
        for word in paragraph:
            # grab width & height of this word
            word_width, word_height = \
                        font.render(word, True, TEXT_COLOR).get_size()
            
            if line_height < word_height:
                line_height = word_height
                
            # if this word would cause an overflow
            if line_length + word_width >= area.width:
                # blit line so far
                lines.append(Text(" ".join(cur_line), font,
                                  pygame.Rect(area.left, y,
                                              area.width, line_height),
                                  background_color, False))                
                # reset back down to next line
                y += line_height + 1
                line_length, line_height = 0, 0
                cur_line = []
                
            cur_line.append(word)
            line_length += word_width

        lines.append(Text(" ".join(cur_line), font,
                          pygame.Rect(area.left, y, area.width, line_height),
                          background_color, False))
        line_length = 0
        y += (2 * (line_height + 1))
        
    return lines

def get_text_by_center(center: (int, int), text: str, font: pygame.font.Font,
                       background_color: pygame.Color):
    word_width, word_height = font.render(text, True, TEXT_COLOR).get_size()
    return Text(text, font, pygame.Rect(center[0] - (word_width / 2),
                                        center[1] - (word_height / 2),
                                        word_width, word_height),
                background_color)
