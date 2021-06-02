"""slider.py: for a Slider class

Slider class -- for an interactive slider
DiscreteSlider class -- subclass of Slider which only allows values
                        exactly at ticks
"""

import pygame
from math import fabs
import text, fonts

# required initialization step
pygame.init()

# number of ticks per slider
TICKS = 5

# color constants for sliders
SLIDER_COLOR = pygame.Color(244, 248, 95)
CIRCLE_COLOR = pygame.Color(146, 199, 14)

class Slider():
    """A class to represent a slider.

    Attributes:
    _title -- title of the Slider
    _slide -- Rect which the value-picker slides along
    _range -- (min, max) of the Slider's range
    _circle_pos -- (x, y) position of the value-picking circle
    _labels -- list of tick-value labels

    Methods:
    is_clicked -- checks if a given mouseclick-point is on the slide
    handle_click -- handles a click on the slide
    draw -- draws the Button onto a given Surface
    """

    def __init__(self, title: str, val_range: (int, int), initial_val: int,
                 area: pygame.Rect, background_color: pygame.Color,
                 set_initial_val: bool = True) -> None:
        """Initialize a Slider.

        title -- title of the Slider
        val_range -- (min, max) of the Slider's range
        initial_val -- initial value the Slider is set to
        area -- Rect where the Slider (title + slide) should go
        background_color -- expected background Color where the Slider will be
        set_initial_val -- whether to set an initial value or not, default True
                           use with caution; an initial value must be set before
                           drawing is possible
        """

        if val_range[0] > val_range[1]:
            raise ValueError('First value in range (min) must be greater than' \
                             'second value (max)')

        self._title = text.Text(title, fonts.SUBTITLE_FONT,
                                pygame.Rect(area.left, area.top, area.width,
                                            area.height / 2), background_color)
        self._slide = pygame.Rect(area.left, area.top + (area.height / 2),
                                   area.width, area.height / 4)
        self._range = val_range
        
        if set_initial_val:
            # will set up circle position
            self._set_value(initial_val)
            
        self._labels = self._generate_labels(background_color)

    def _set_value(self, new_val: int) -> int:
        """Set Slider value to a new one.

        new_val -- new value to set Slider to

        Returns the value it has been set to
        """

        # temporary variables to make referencing easier
        min_val, max_val = self._range
        
        if new_val < min_val or new_val > max_val:
            raise ValueError('Value must be between', min_val, 'and', max_val)

        # calculate percent along the slide this new value is
        percent = (new_val - min_val) / (max_val - min_val)
        # calculate new circle position
        self._circle_pos = (self._slide.left + (self._slide.width * percent),
                             self._slide.top + (self._slide.height / 2))
        
        return new_val

    def _generate_labels(self, background_color: pygame.Color) -> list:
        """Generate tick Text-lables.

        background_color -- expected background Color for this text

        Return a list of Text labels
        """

        # return variable
        labels = []

        # calculate value and x-coord jumps for each tick
        val_jump = (self._range[1] - self._range[0]) / (TICKS - 1)
        x_jump = self._slide.width / (TICKS - 1)
        
        for i in range(TICKS):
            # create and add Text label for this i-value
            labels.append(text.get_text_by_center(
                (str) (self._range[0] + (val_jump * i)), fonts.NUMBER_FONT,
                (self._slide.left + (x_jump * i), self._slide.bottom + 6),
                background_color))
            
        return labels

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if a given mouse click is on the Slider

        mouse_x -- the x coordinate of the mouseclick
        mouse_y -- the y coordinate of the mouseclick

        Returns a bool -- True if the click is on the Slider, False if not
        """
        
        return self._slide.collidepoint(mouse_x, mouse_y)

    def handle_click(self, mouse_x: int, mouse_y: int) -> int:
        """Handle a click on the Slider appropriately.

        mouse_x -- the x coordinate of the mouseclick
        mouse_y -- the y coordinate of the mouseclick

        Returns the new value the Slider is set to
        """
        
        if not self.is_clicked(mouse_x, mouse_y):
            raise ValueError('Click is not on slide')
        
        # calculate percent along the slide this click is
        percent = (mouse_x - self._slide.left) / self._slide.width
        # calculate new value and set it
        new_val = self._range[0] + \
                  ((self._range[1] - self._range[0]) * percent)
        
        return self.set_value(new_val)

    def draw(self, screen: pygame.Surface):
        """Draw the Button onto a given Surface."""
        
        self._title.draw(screen)
        
        # slide must be drawn before circle as circle is on top
        pygame.draw.rect(screen, SLIDER_COLOR, self._slide)
        pygame.draw.circle(screen, CIRCLE_COLOR, self._circle_pos,
                           self._slide.height / 2)
        
        for label in self._labels:
            label.draw(screen)

class DiscreteSlider(Slider):
    """A class to represent a slider. Subclass of Slider.

    Attributes:
    _title, _slide, _range, _circle_pos, _labels -- from Slider
    _allowed_vals -- allowed values the DiscreteSlider can be set to
    _allowed_x_coords -- allowed x-coordinates of the center of the circle

    Methods:
    is_clicked, handle_click, draw -- from Slider
    """
    
    def __init__(self, title: str, val_range: (int, int), initial_val: int,
                 area: pygame.Rect, background_color: pygame.Color):
        """Initialize a DiscreteSlider.

        title -- title of the Slider
        val_range -- (min, max) of the Slider's range
        initial_val -- initial value the Slider is set to
        area -- Rect where the Slider (title + slide) should go
        background_color -- expected background Color where the Slider will be
        """
        
        super().__init__(title, val_range, initial_val, area,
                         background_color, False)

        # calculate allowed values & x-coordinates
        
        val_jump = (val_range[1] - val_range[0]) / (TICKS - 1)
        self._allowed_vals = [val_range[0] + (val_jump * i)
                               for i in range(TICKS)]
        x_jump = area.width / (TICKS - 1)
        self._allowed_x_coords = [area.left + (x_jump * i)
                                  for i in range(TICKS)]

        self._set_value(initial_val)
            
    def _set_value(self, new_val: int):
        """Set DiscreteSlider value to a new one.

        new_val -- new value to set DiscreteSlider to

        Returns the value it has been set to
        """
        
        if new_val not in self._allowed_vals:
            raise ValueError("Not an allowed discrete value")
        else:
            return super()._set_value(new_val)

    def handle_click(self, mouse_x: int, mouse_y: int) -> int:
        """Handle a click on the DiscreteSlider appropriately.

        mouse_x -- the x coordinate of the mouseclick
        mouse_y -- the y coordinate of the mouseclick

        Returns the new value the DiscreteSlider is set to
        """

        if not self.is_clicked(mouse_x, mouse_y):
            raise ValueError('Click is not on slide')
        
        least_x_diff = float('inf')

        # check diff for each x coord
        for i in range(len(self._allowed_x_coords)):
            x_coord = self._allowed_x_coords[i]
            diff = fabs(x_coord - mouse_x)

            # if this difference is the best so far choose this index
            if diff < least_x_diff:
                least_x_diff = diff
                closest_index = i
                
        return self._set_value(self._allowed_vals[closest_index])
