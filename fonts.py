""" fonts.py: for font constants across the simulations """

import pygame

# required initialization step
pygame.init()

TITLE_FONT = pygame.font.SysFont('inkfree', 60)
SUBTITLE_FONT = pygame.font.SysFont('inkfree', 20, False, True)
BUTTON_FONT = pygame.font.SysFont('calibri', 35)
PARAGRAPH_FONT = pygame.font.SysFont('arial', 15)
