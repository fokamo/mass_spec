""" runner.py

Runs the simulator, dealing with the high-level logic

Has three main screens: Start, Simulator, and Info.
Info has several sub-screens with information.
"""

import pygame, sys
import button

# required initialization step
pygame.init()

# the game clock & frame-rate
FPS = 30
game_clock = pygame.time.Clock()

# set up color constants
BLUE = pygame.Color(38, 228, 235)
RED = pygame.Color(235, 91, 91)

# set up the display screen
WINDOW_SIZE = (1000, 600)
window = pygame.display.set_mode(WINDOW_SIZE)
window.fill(BLUE)
background = pygame.Surface(WINDOW_SIZE)

def main():
    """Main runner function. Implements high-level logic"""

    # flags used to indicate current screen (only one screen right now)
    START = 1

    # initially on start screen
    screen = START

    exit_button = button.Button(500, 450, 50, 100, "Exit", RED)

    while True:
        print("hello")
        if screen == START:
            pygame.display.set_caption("Start")

            exit_button.draw(background)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.is_clicked(pygame.mouse.get_pos()):
                        # must do both to exit properly
                        pygame.quit()
                        sys.exit()
                        
        # update screen & tick clock
        pygame.display.update()
        game_clock.tick(FPS)
    

# call the "main" function if running this script
if __name__ == "__main__":
    main()
