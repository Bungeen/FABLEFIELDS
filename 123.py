import pygame
import pygame_gui

from pygame_gui.core.ui_container import UIContainer

pygame.init()
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((600, 800), pygame.RESIZABLE)
background = pygame.Surface((600, 800), pygame.RESIZABLE)
background.fill(pygame.Color('#000000'))
manager = pygame_gui.UIManager((600, 800))
# hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
#                                             text='Say Hello',
#                                             manager=manager)
button_layout_rect = pygame.Rect(30, 20, 100, 20)

hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                            text='Hello', manager=manager)
clock = pygame.time.Clock()
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        # if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #    if event.ui_element == hello_button:
        #        print('Hello World!')
        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()
