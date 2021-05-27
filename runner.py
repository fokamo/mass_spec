""" runner.py

Runs the simulator, dealing with the high-level logic

Has three main screens: Start, Simulator, and Info.
Info has several sub-screens with information.
"""

import pygame, sys
import button, text

# required initialization step
pygame.init()

# the game clock & frame-rate
FPS = 30
game_clock = pygame.time.Clock()

# color constants
BLUE = pygame.Color(38, 228, 235)
RED = pygame.Color(235, 91, 91)

# font constants
TITLE_FONT = pygame.font.SysFont('inkfree', 60)
SUBTITLE_FONT = pygame.font.SysFont('inkfree', 20, False, True)

# set up the display screen
WINDOW_SIZE = (1000, 600)
window = pygame.display.set_mode(WINDOW_SIZE)
# not quite sure what this does - need to check documentation
# background = pygame.Surface(WINDOW_SIZE)

def main():
    """Main runner function. Implements high-level logic"""

    # flags used to indicate current screen (only one screen right now)
    START = 1

    # initially on start screen
    screen = START
    background_color = BLUE
    window.fill(background_color)

    # set up UI elements
    exit_button = button.Button(450, 500, 100, 50, "Exit", RED)
    title = text.Text("Mass Spectrometer", TITLE_FONT,
                      pygame.Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1] / 2),
                      background_color)
    subtitle = text.Text("by Faith Okamoto", SUBTITLE_FONT,
                         pygame.Rect(0, 100, WINDOW_SIZE[0],
                                     WINDOW_SIZE[1] / 2), background_color)
                                  
    # game loop
    while True:
        if screen == START:
            pygame.display.set_caption("Start")

            exit_button.draw(window)
            title.draw(window)
            subtitle.draw(window)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if exit_button.is_clicked(mouse_x, mouse_y):
                        # must do both to exit properly
                        pygame.quit()
                        sys.exit()
                        
        # update screen & tick clock
        pygame.display.update()
        game_clock.tick(FPS)
    

# call the "main" function if running this script
if __name__ == "__main__":
    main()
