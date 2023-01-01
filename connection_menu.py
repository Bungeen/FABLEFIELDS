import os

import pygame
import sys


from network import Network
from menu_widget import Menu_Widget

import game


class Connection_Menu:
    def __init__(self, w, h):
        pygame.font.init()
        pygame.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('FABLEFIELDS')

        self.is_running = True
        # self.group = pygame.sprite.Group()
        # self.widget = Menu_Widget(self.group, pygame.image.load("assets/menu.png").convert_alpha())
        self.font = pygame.font.Font("assets/font.ttf", 40)
        # self.TEXT_COLOR = "#FFFFFF"

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
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     tmp = self.widget.checking_button(mouse_position)
                #     if tmp == 'multiplayer':
                #         g = game.Game(self.width, self.height)
                #         g.run()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        g = game.Game(self.width, self.height, '188.235.166.223', 5555)
                        g.run()
                        os._exit(1)
                        # print(123)
                if event.type == pygame.QUIT:
                    os._exit(1)
                    self.is_running = False
            # self.group.update(self.screen)
            pygame.display.update()

        pygame.quit()

    # def send_data(self):
    #     """
    #     Send position to server
    #     :return: None
    #     """
    #     data = str(self.net.id) + ":" + str(self.player.rect.x) + "," + str(self.player.rect.y) + ',1'
    #     reply = self.net.send(data)
    #     return reply
#
    # @staticmethod
    # def parse_data(data):
    #     try:
    #         d = data.split(":")[1].split(",")
    #         return int(d[0]), int(d[1]), bool(int(d[2]))
    #     except:
    #         return 0, 0, 0