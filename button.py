""" button.py: for a Button class """

class Button(pygame.Rect):
    """A button which can draw itself and be clicked"""

    def __init__(self, left: int, top: int, width: int, height: int,
                 text: str, color: Color) -> Button:
        super().__init__(left, top, width, height)
        self.__text = text
        self.__color = color

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        return collidepoint(mouse_x, mouse_y)

    def draw(self, surface:) -> None:
        pygame.draw.rect(surface, self.__color, self.
        
