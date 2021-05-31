""" slider.py: for a Slider class """

import pygame
import text, fonts

# required initialization step
pygame.init()

TICKS = 5

SLIDER_COLOR = pygame.Color(244, 248, 95)
CIRCLE_COLOR = pygame.Color(146, 199, 14)

class Slider():

    def __init__(self, name: str, val_range: (int, int), area: pygame.Rect,
                 background_color: pygame.Color, initial_value: int):
        if val_range[0] > val_range[1]:
            raise ValueError('First (min) must be greater than second (max)')

        self.__name = text.Text(name, fonts.SUBTITLE_FONT,
                                pygame.Rect(area.left, area.top, area.width,
                                            area.height / 2), background_color)
        self.__slide = pygame.Rect(area.left, area.top + (area.height / 2),
                                   area.width, area.height / 4)
        self.__circle_radius = area.height / 8
        self.__range = val_range
        self.__set_value(initial_value)
        self.__labels = self.__generate_labels(background_color)

    def __set_value(self, new_val: int):
        min_val, max_val = self.__range
        if new_val < min_val or new_val > max_val:
            raise ValueError('Value must be between', min_val, 'and', max_val)
        percent = (new_val - min_val) / (max_val - min_val)
        self.__circle_pos = (self.__slide.left + (self.__slide.width * percent),
                             self.__slide.top + (self.__slide.height / 2))
        self.__value = new_val

    def __generate_labels(self, background_color: pygame.Color):
        labels = []
        val_jump = (self.__range[1] - self.__range[0]) / (TICKS - 1)
        x_jump = self.__slide.width / (TICKS - 1)
        for i in range(TICKS):
            labels.append(text.get_text_by_center(
                (self.__slide.left + (x_jump * i), self.__slide.bottom + 5),
                (str) (self.__range[0] + (val_jump * i)), fonts.NUMBER_FONT,
                background_color))
        return labels
                

    def draw(self, screen: pygame.Surface):
        self.__name.draw(screen)
        pygame.draw.rect(screen, SLIDER_COLOR, self.__slide)
        pygame.draw.circle(screen, CIRCLE_COLOR, self.__circle_pos,
                           self.__circle_radius)
        for label in self.__labels:
            label.draw(screen)

    def is_clicked(self, mouse_x: int, mouse_y: int):
        """ Check if a given mouse click is on the slider """
        
        return self.__slide.collidepoint(mouse_x, mouse_y)

    def handle_click(self, mouse_x: int, mouse_y: int) -> int:
        """ Handle a click: if on the slider, move the circle & update value """
        
        if self.is_clicked(mouse_x, mouse_y):
            percent = (mouse_x - self.__slide.left) / self.__slide.width
            new_val = self.__range[0] + (
                (self.__range[1] - self.__range[0]) * percent)
            self.__set_value(new_val)
            return new_val
        return None
