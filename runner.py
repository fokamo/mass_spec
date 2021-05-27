""" massspec.runner.py

Runs the simulator, dealing with the high-level logic

Has three main screens: Start, Simulator, and Info.
Info has several sub-screens with information.
"""

import pygame, sys

# required initialization step
pygame.init()

FPS = 30
GameClock = pygame.time.Clock()

# set up color constants
BLUE = (38, 228, 235)

# set up the display screen
DISPLAYSURF = pygame.display.set_mode((300, 500))
DISPLAYSURF.fill(BLUE)

def main():
    """Main runner function. Implements high-level logic"""

    # flags used to indicate current screen (only one screen right now)
    START = 1

    # initially on start screen
    screen = START

    while True:
        if screen == START:
            pygame.display.set_caption("Start")
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # must do both to exit properly
                    pygame.quit()
                    sys.exit()
        # update screen & tick clock
        pygame.display.update()
        GameClock.tick(FPS)
    

# call the "main: function if running this script
def __name__ == "__main__":
    main()
