""" runner.py

Runs the simulator, dealing with the high-level logic

Has three main screens: Start, Simulator, and Info.
Info has several sub-screens with information.
"""

import pygame, sys
import button, text, fonts, info_section, mass_spectrometer

# required initialization step
pygame.init()

# the game clock & frame-rate
FPS = 30
game_clock = pygame.time.Clock()

# color constants
BACKGROUND_COLOR = pygame.Color(38, 228, 235)
BACK_COLOR = pygame.Color(235, 91, 91)
MOVE_FURTHER_COLOR = pygame.Color(79, 240, 146)

# set up the display screen
WINDOW_SIZE = (1000, 600)
window = pygame.display.set_mode(WINDOW_SIZE)

def main():
    """Main runner function. Implements high-level logic"""

    # flags used to indicate current screen
    START = 1
    SIMULATOR = 2
    INFO = 3
    INFO_SUBSCREEN = 4
    subscreen_num = -1

    # initially on start screen
    screen = START
    window.fill(BACKGROUND_COLOR)

    # start screen elements
    
    # buttons which navigate to other screens
    exit_button = button.Button(450, 500, 100, 50, "Exit", BACK_COLOR)
    sim_button = button.Button(200, 300, 200, 50, "Simulation",
                               MOVE_FURTHER_COLOR)
    info_button = button.Button(600, 300, 200, 50, "Science",
                                MOVE_FURTHER_COLOR)
    # title & subtitle
    title = text.Text("Mass Spectrometer", fonts.TITLE_FONT,
                      pygame.Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1] / 2),
                      BACKGROUND_COLOR)
    subtitle = text.Text("by Faith Okamoto", fonts.SUBTITLE_FONT,
                         pygame.Rect(0, 100, WINDOW_SIZE[0],
                                     WINDOW_SIZE[1] / 2), BACKGROUND_COLOR)

    start_screen_elems = (exit_button, sim_button, info_button, title, subtitle)


    # main info screen elements
    
    back_button = button.Button(450, 500, 100, 50, "Back", BACK_COLOR)
    mass_spec_intro_button = button.Button(125, 150, 300, 50, "Mass Spec 101",
                                           MOVE_FURTHER_COLOR)
    # buttons which lead to info subscreens
    info_title = text.Text("The Science Behind It", fonts.TITLE_FONT,
                           pygame.Rect(0, 0, WINDOW_SIZE[0],
                                       WINDOW_SIZE[1] / 4), BACKGROUND_COLOR)

    info_screen_elems = (back_button, mass_spec_intro_button, info_title)


    # info subscreen elements
    info_subscreens = info_section.load_info_sections('physics_info.txt')
    # placeholders elements for a particular subscreen
    info_subscreen_title = None
    info_area = pygame.Rect(200, 150, 600, 300)
    sources_area = pygame.Rect(200, 450, 600, 50)

    info_subscreen_elems = [back_button, info_subscreen_title]

    # simulation screen elements
    mass_spec = mass_spectrometer.MassSpectrometer(
        pygame.Rect(0, 0, 2 * WINDOW_SIZE[0] / 3, WINDOW_SIZE[1]),
        10, 1, 5, 1, 0)
    reset_button = button.Button(50, 50, 100, 50, "Reset", MOVE_FURTHER_COLOR)

    simulator_screen_elems = (back_button, mass_spec, reset_button)
   
    # game loop
    while True:
        if screen == START:
            pygame.display.set_caption("Start")

            # draw start screen elements
            for elem in start_screen_elems:
                elem.draw(window)
                
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if exit_button.is_clicked(mouse_x, mouse_y):
                        # must do both to exit properly
                        pygame.quit()
                        sys.exit()
                        
                    elif info_button.is_clicked(mouse_x, mouse_y):
                        screen = INFO
                        window.fill(BACKGROUND_COLOR)
                        
                    elif sim_button.is_clicked(mouse_x, mouse_y):
                        screen = SIMULATOR
                        mass_spec.reset_particle()
                        window.fill(BACKGROUND_COLOR)

        elif screen == SIMULATOR:
            pygame.display.set_caption("Simulator")

            window.fill(BACKGROUND_COLOR)

            # draw simulation screen elements
            for elem in simulator_screen_elems:
                elem.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if back_button.is_clicked(mouse_x, mouse_y):
                        screen = START
                        window.fill(BACKGROUND_COLOR)
                    if reset_button.is_clicked(mouse_x, mouse_y):
                        mass_spec.reset_particle()
                        
        elif screen == INFO:
            pygame.display.set_caption("Info")


            # draw info screen elements
            for elem in info_screen_elems:
                elem.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # back button goes to start screen
                    if back_button.is_clicked(mouse_x, mouse_y):
                        screen = START
                        window.fill(BACKGROUND_COLOR)
                        
                    # mass spec intro button goes to first subscreen
                    elif mass_spec_intro_button.is_clicked(mouse_x, mouse_y):
                        subscreen_num = 0

                    # if a subscreen has been set, set it up 
                    if subscreen_num != -1:
                        info_subscreen_title = text.Text(
                            info_subscreens[subscreen_num].title,
                            fonts.TITLE_FONT,
                            pygame.Rect(0, 0, WINDOW_SIZE[0],
                                        WINDOW_SIZE[1] / 4), BACKGROUND_COLOR)
                        info_subscreen_elems = [back_button,
                                                info_subscreen_title]
                        for line in text.paragraphs_to_lines(
                            info_area, info_subscreens[subscreen_num].info,
                            fonts.PARAGRAPH_FONT, BACKGROUND_COLOR):
                            info_subscreen_elems.append(line)
                        for line in text.paragraphs_to_lines(
                            sources_area,
                            info_subscreens[subscreen_num].sources,
                            fonts.PARAGRAPH_FONT, BACKGROUND_COLOR):
                            info_subscreen_elems.append(line)
                        screen = INFO_SUBSCREEN
                        window.fill(BACKGROUND_COLOR)
                        

        elif screen == INFO_SUBSCREEN:
            pygame.display.set_caption(info_subscreens[subscreen_num].title)

            # draw info subscreen elements
            for elem in info_subscreen_elems:
                elem.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if back_button.is_clicked(mouse_x, mouse_y):
                        screen = INFO
                        subscreen_num = -1
                        window.fill(BACKGROUND_COLOR)
            
                        
        # update screen & tick clock
        pygame.display.update()
        game_clock.tick(FPS)
    

# call the "main" function if running this script
if __name__ == "__main__":
    main()
