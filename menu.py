import pygame
import sys

from button import Button

import game


class Menu:
    def __init__(self, w, h, is_fullscreen=False):
        pygame.font.init()
        self.width = w
        self.height = h
        self.is_fullscreen = is_fullscreen
        self.screen = None
        self.initialization_screen()
        pygame.display.set_caption('Main menu')

        self.is_running = True

        self.font = pygame.font.Font("assets/font.ttf", 40)
        self.TEXT_COLOR = "#FFFFFF"

    def draw_text(self, x, y, text, font, text_color):
        image = self.font.render(text, True, text_color)
        place = image.get_rect(center=(x, y))
        self.screen.blit(image, place)

    def initialization_screen(self):
        if self.is_fullscreen:
            print('FULL')
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            print('RESIZE')
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            self.width = self.screen.get_width()
            self.height = self.screen.get_height()

    def run(self):
        # game loop
        while self.is_running:
            self.screen.fill((52, 78, 91))
            self.draw_text(self.screen.get_width() / 2, self.screen.get_height() / 4, 'MENU', self.font,
                           self.TEXT_COLOR)

            MENU_MOUSE_POSITION = pygame.mouse.get_pos()

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"),
                                 pos=(self.screen.get_width() / 2, self.screen.get_height() / 2),
                                 text_input="PLAY", font=self.font, base_color="#d7fcd4", hovering_color="White")
            buttons = []
            buttons += [PLAY_BUTTON]
            for button in buttons:
                button.change_color(MENU_MOUSE_POSITION)
                button.update(self.screen)

            # event-handler
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_for_input(MENU_MOUSE_POSITION):
                        g = game.Game(self.screen.get_width(), self.screen.get_height(), self.is_fullscreen)
                        g.run()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        print(self.is_fullscreen)
                        self.is_fullscreen = not self.is_fullscreen
                        self.initialization_screen()
                if event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.width = event.w
                        self.height = event.h
                        self.initialization_screen()
                if event.type == pygame.QUIT:
                    self.is_running = False

            pygame.display.update()

        pygame.quit()
