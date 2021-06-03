"""runner.py

Runs the simulator, dealing with the high-level logic, by calling main()

Has three main screens: Start, Simulator, and Info.
Info has several sub-screens with information.
"""

import pygame, sys, random
import button, text, fonts, info_section, mass_spectrometer, slider

# required initialization step
pygame.init()

# the game clock & frame-rate
FPS = 30
game_clock = pygame.time.Clock()

CORMAN_IMAGE = pygame.image.load('corman.jpg')
CORMAN_NAME = (pygame.K_c, pygame.K_o, pygame.K_r,
               pygame.K_m, pygame.K_a, pygame.K_n)

# color constants
BACKGROUND_COLOR = pygame.Color(38, 228, 235)
BACK_COLOR = pygame.Color(235, 91, 91)
MOVE_FURTHER_COLOR = pygame.Color(79, 240, 146)

# set up the display screen
WINDOW_SIZE = (1000, 600)
window = pygame.display.set_mode(WINDOW_SIZE)

def random_corman_pos() -> (int, int):
    """Generate a random valid position for the Corman image."""
    
    width, height = CORMAN_IMAGE.get_width(), CORMAN_IMAGE.get_height()
    return (random.randrange(0, WINDOW_SIZE[0] - width),
            random.randrange(0, WINDOW_SIZE[1] - height))

def main() -> None:
    """Main runner function. Implements high-level logic."""

    # flags used to indicate current screen
    START = 1
    SIMULATOR = 2
    INFO = 3
    INFO_SUBSCREEN = 4
    subscreen_num = -1

    # tracking easter egg
    corman_positions = []
    corman_name_index = 0

    # initially on start screen
    screen = START
    window.fill(BACKGROUND_COLOR)

    # by default simulator is not paused
    paused = False

    # start screen elements
    
    # buttons which navigate to other screens
    exit_button = button.Button('Exit', pygame.Rect(450, 500, 100, 50),
                                BACK_COLOR)
    sim_button = button.Button('Simulation', pygame.Rect(200, 300, 200, 50),
                               MOVE_FURTHER_COLOR)
    info_button = button.Button('Science', pygame.Rect(600, 300, 200, 50),
                                MOVE_FURTHER_COLOR)
    # title & subtitle
    title = text.Text('Mass Spectrometer', fonts.TITLE_FONT,
                      pygame.Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1] / 2),
                      BACKGROUND_COLOR)
    subtitle = text.Text('by Faith Okamoto', fonts.SUBTITLE_FONT,
                         pygame.Rect(0, 100, WINDOW_SIZE[0],
                                     WINDOW_SIZE[1] / 2), BACKGROUND_COLOR)

    start_screen_elems = (exit_button, sim_button, info_button, title, subtitle)

    # simulation screen elements
    mass_spec = mass_spectrometer.MassSpectrometer(
        5, -1, 20, 1, 5, pygame.Rect(0, 0, 2 * WINDOW_SIZE[0] / 3,
                                     WINDOW_SIZE[1]))
    reset_button = button.Button('Reset', pygame.Rect(50, 50, 100, 50),
                                 MOVE_FURTHER_COLOR)
    back_button = button.Button('Back', pygame.Rect(450, 500, 100, 50),
                                BACK_COLOR)
    pause_button = button.Button('Pause', pygame.Rect(50, 175, 100, 50),
                                 BACK_COLOR)
    unpause_button = button.Button('Go', pygame.Rect(50, 175, 100, 50),
                                   MOVE_FURTHER_COLOR)
    # set up sliders
    slider_area = pygame.Rect(WINDOW_SIZE[0] - 200, 0, 150, WINDOW_SIZE[1] / 5)
    charge_slider = slider.DiscreteSlider('Charge', (-2, 2), 1, slider_area,
                                          BACKGROUND_COLOR)
    slider_area.top += slider_area.height
    mass_slider = slider.Slider('Mass', (10, 50), 20, slider_area,
                                BACKGROUND_COLOR)
    slider_area.top += slider_area.height
    velocity_slider = slider.Slider('i. Velocity', (2, 10), 5, slider_area,
                                    BACKGROUND_COLOR)
    slider_area.top += slider_area.height
    e_field_slider = slider.Slider('E Field', (-5, 5), 5, slider_area,
                                   BACKGROUND_COLOR)
    slider_area.top += slider_area.height
    mag_field_slider = slider.Slider('Mag Field', (-5, 5), -1, slider_area,
                                     BACKGROUND_COLOR)
                                   
    simulator_screen_elems = (back_button, mass_spec, reset_button,
                              charge_slider, mass_slider,
                              velocity_slider, e_field_slider,
                              mag_field_slider)

    # main info screen elements
    info_title = text.Text('The Science Behind It', fonts.TITLE_FONT,
                           pygame.Rect(0, 0, WINDOW_SIZE[0],
                                       WINDOW_SIZE[1] / 4), BACKGROUND_COLOR)
    # buttons which lead to info subscreens
    mass_spec_intro_button = button.Button('Mass Spec 101',
                                           pygame.Rect(125, 150, 300, 50),
                                           MOVE_FURTHER_COLOR)
    straight_sec_button = button.Button("Straight Shootin'",
                                        pygame.Rect(550, 150, 300, 50),
                                        MOVE_FURTHER_COLOR)
    open_sec_button = button.Button('Open Curving',
                                    pygame.Rect(125, 225, 300, 50),
                                    MOVE_FURTHER_COLOR)
    a_c_button = button.Button('Centripetal', pygame.Rect(550, 225, 300, 50),
                               MOVE_FURTHER_COLOR)
    mag_force_button = button.Button('Magnetic Force',
                                     pygame.Rect(125, 300, 300, 50),
                                     MOVE_FURTHER_COLOR)
    e_force_button = button.Button('Electric Force',
                                   pygame.Rect(550, 300, 300, 50),
                                   MOVE_FURTHER_COLOR)
    int_charge_button = button.Button('Discrete Charges',
                                      pygame.Rect(125, 375, 300, 50),
                                      MOVE_FURTHER_COLOR)
    units_button = button.Button('Units',
                                 pygame.Rect(550, 375, 300, 50),
                                 MOVE_FURTHER_COLOR)
    subscreen_buttons = (mass_spec_intro_button, straight_sec_button,
                         open_sec_button, a_c_button, mag_force_button,
                         e_force_button, int_charge_button, units_button)

    info_screen_elems = [back_button, mass_spec_intro_button, info_title]
    info_screen_elems.extend(subscreen_buttons)


    # info subscreen elements
    info_subscreens = info_section.load_info_sections('physics_info.txt')
    # placeholders elements for a particular subscreen
    info_subscreen_title = None
    info_area = pygame.Rect(200, 150, 600, 300)
    source_area = pygame.Rect(200, 450, 600, 50)

    info_subscreen_elems = [back_button, info_subscreen_title]
   
    # game loop
    while True:
        if screen == START:
            pygame.display.set_caption('Start')

            for elem in start_screen_elems:
                elem.draw(window)

            for pos in corman_positions:
                window.blit(CORMAN_IMAGE, pos)
                
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # if this was the next key in "corman"
                    if event.key == CORMAN_NAME[corman_name_index]:
                        # move "next key" index
                        corman_name_index += 1
                        # if full name has been typed generate a new image pos
                        if corman_name_index == len(CORMAN_NAME):
                            corman_name_index = 0
                            corman_positions.append(random_corman_pos())
                    # any wrong key resets counter
                    else:
                        corman_name_index = 0
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # exit button quits simulation
                    if exit_button.is_clicked(mouse_x, mouse_y):
                        # must do both to exit properly
                        pygame.quit()
                        sys.exit()

                    # info button goes to info screen
                    elif info_button.is_clicked(mouse_x, mouse_y):
                        screen = INFO
                        window.fill(BACKGROUND_COLOR)

                    # simulation button goes to simulation screen
                    elif sim_button.is_clicked(mouse_x, mouse_y):
                        screen = SIMULATOR
                        mass_spec.reset_particle()
                        window.fill(BACKGROUND_COLOR)

        elif screen == SIMULATOR:
            pygame.display.set_caption('Simulator')

            # erase before drawing, so that particle doesn't drag when moving
            window.fill(BACKGROUND_COLOR)

            for elem in simulator_screen_elems:
                elem.draw(window)

            if paused:
                unpause_button.draw(window)
            else:
                pause_button.draw(window)
                mass_spec.move()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # back button goes to start screen
                    if back_button.is_clicked(mouse_x, mouse_y):
                        screen = START
                        window.fill(BACKGROUND_COLOR)

                    # reset button resets particle
                    elif reset_button.is_clicked(mouse_x, mouse_y):
                        mass_spec.reset_particle()

                    # pause and unpause buttons in same spot
                    elif pause_button.is_clicked(mouse_x, mouse_y):
                        paused = not paused

                    # handle slider clicks
                    elif charge_slider.is_clicked(mouse_x, mouse_y):
                        mass_spec.set_charge(
                            charge_slider.handle_click(mouse_x, mouse_y))

                    elif mass_slider.is_clicked(mouse_x, mouse_y):
                        mass_spec.set_mass(
                            mass_slider.handle_click(mouse_x, mouse_y))

                    elif velocity_slider.is_clicked(mouse_x, mouse_y):
                        mass_spec.set_initial_x_velocity(
                            velocity_slider.handle_click(mouse_x, mouse_y))

                    elif e_field_slider.is_clicked(mouse_x, mouse_y):
                        mass_spec.e_field = \
                            e_field_slider.handle_click(mouse_x, mouse_y)

                    elif mag_field_slider.is_clicked(mouse_x, mouse_y):
                        mass_spec.mag_field = \
                            mag_field_slider.handle_click(mouse_x, mouse_y)
                    
                        
        elif screen == INFO:
            pygame.display.set_caption('Info')

            for elem in info_screen_elems:
                elem.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # back button goes to start screen
                    if back_button.is_clicked(mouse_x, mouse_y):
                        screen = START
                        window.fill(BACKGROUND_COLOR)

                    # check for click on any subscreen button
                    for i in range(len(subscreen_buttons)):
                        if subscreen_buttons[i].is_clicked(mouse_x, mouse_y):
                            subscreen_num = i

                    # if a subscreen has been set, set it up 
                    if subscreen_num != -1:
                        # set up title
                        info_subscreen_title = text.Text(
                            info_subscreens[subscreen_num].title,
                            fonts.TITLE_FONT,
                            pygame.Rect(0, 0, WINDOW_SIZE[0],
                                        WINDOW_SIZE[1] / 4), BACKGROUND_COLOR)
                        info_subscreen_elems = [back_button,
                                                info_subscreen_title]

                        # add info paragraph lines to elems
                        for line in text.paragraphs_to_lines(
                            info_subscreens[subscreen_num].info,
                            fonts.PARAGRAPH_FONT, info_area, BACKGROUND_COLOR):
                            info_subscreen_elems.append(line)
                        # add source line to elems
                        info_subscreen_elems.append(text.Text(
                                     info_subscreens[subscreen_num].source,
                                     fonts.PARAGRAPH_FONT, source_area,
                                     BACKGROUND_COLOR))
                            
                        screen = INFO_SUBSCREEN
                        window.fill(BACKGROUND_COLOR)
                        

        elif screen == INFO_SUBSCREEN:
            pygame.display.set_caption(info_subscreens[subscreen_num].title)

            for elem in info_subscreen_elems:
                elem.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # back button goes to info screen
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
