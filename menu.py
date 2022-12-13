import pygame
import sys

from menu_widget import Menu_Widget

import connection_menu

import game


class Menu:
    def __init__(self, w, h):
        pygame.font.init()
        pygame.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('FABLEFIELDS')

        self.is_running = True
        self.group = pygame.sprite.Group()
        self.widget = Menu_Widget(self.group, pygame.image.load("assets/menu.png").convert_alpha())
        self.font = pygame.font.Font("assets/font.ttf", 40)
        self.TEXT_COLOR = "#FFFFFF"

    # Doesn't need maybe
    def draw_text(self, x, y, text, font, text_color):
        image = self.font.render(text, True, text_color)
        place = image.get_rect(center=(x, y))
        self.screen.blit(image, place)

    def run(self):
        # game loop
        while self.is_running:
            self.screen.fill((52, 78, 91))
            mouse_position = pygame.mouse.get_pos()

            # event-handler
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tmp = self.widget.checking_button(mouse_position)
                    if tmp == 'multiplayer':
                        m = connection_menu.Connection_Menu(self.width, self.height)
                        m.run()
                        # g = game.Game(self.width, self.height)
                        # g.run()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        sys.exit()
                if event.type == pygame.QUIT:
                    self.is_running = False
            self.group.update(self.screen)
            pygame.display.update()

        pygame.quit()
