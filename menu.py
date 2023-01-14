import os
import time
from _thread import start_new_thread

import pygame

import game

from menu_widget import Menu_Widget
from select_game_widget import Select_Game_Widget
from connection_widget import Connection_Widget
from server_system import Server


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
        self.widget = Menu_Widget(self.group, pygame.image.load("assets/Main_Menu.png").convert_alpha())
        self.font = pygame.font.Font("assets/font.ttf", 40)
        self.TEXT_COLOR = "#FFFFFF"

    def run(self):
        # game loop
        while self.is_running:
            self.screen.fill('#6CAD34')
            mouse_position = pygame.mouse.get_pos()

            # event-handler
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tmp = self.widget.checking_button(mouse_position)
                    if tmp == 'tutorial':
                        m = Tutorial(self.width, self.height)
                        m.run()
                    elif tmp == 'play':
                        m = Connection_Menu(self.width, self.height)
                        m.run()
                    elif tmp == 'exit':
                        os._exit(1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        os._exit(1)
                if event.type == pygame.QUIT:
                    self.is_running = False
                    os._exit(1)
            self.group.update(self.screen)
            pygame.display.update()

        pygame.quit()


class Connection_Menu:
    def __init__(self, w, h):
        pygame.font.init()
        pygame.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('FABLEFIELDS')

        self.is_running = True
        self.group = pygame.sprite.Group()
        self.widget = Select_Game_Widget(self.group, pygame.image.load("assets/Select_Game.png").convert_alpha())
        self.font = pygame.font.Font("assets/font.ttf", 40)

    def run(self):
        # game loop
        while self.is_running:
            self.screen.fill('#6CAD34')
            mouse_position = pygame.mouse.get_pos()

            # event-handler
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tmp = self.widget.checking_button(mouse_position)
                    if tmp == 'back':
                        m = Menu(500, 500)
                        m.run()
                        os._exit(1)
                    elif tmp == 'connect':
                        m = Connection_Input_Menu(500, 500)
                        m.run()
                    elif tmp == 'create':
                        m = Create_Server_Input_Menu(500, 500)
                        m.run()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        os._exit(1)
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        return
                if event.type == pygame.QUIT:
                    os._exit(1)
                    self.is_running = False
            self.group.update(self.screen)
            pygame.display.update()

        pygame.quit()


class Connection_Input_Menu:
    def __init__(self, w, h):
        pygame.font.init()
        pygame.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('FABLEFIELDS')

        self.is_running = True
        self.group = pygame.sprite.Group()
        self.widget = Connection_Widget(self.group, pygame.image.load("assets/Connection_Menu.png").convert_alpha())
        self.font = pygame.font.Font("assets/font.ttf", 40)

        self.ip = 'localhost'
        self.port = '5555'
        self.username = 'user'
        self.first_input = False
        self.second_input = False
        self.third_input = False

    def run(self):
        # game loop
        while self.is_running:
            self.screen.fill('#6CAD34')
            mouse_position = pygame.mouse.get_pos()

            # event-handler
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tmp = self.widget.checking_button(mouse_position)
                    print(tmp)
                    if tmp == 'Cancel':
                        self.first_input = False
                        self.second_input = False
                        self.third_input = False
                        m = Connection_Menu(self.width, self.height)
                        m.run()
                    elif tmp == 'Connect':
                        self.first_input = False
                        self.second_input = False
                        self.third_input = False
                        g = game.Game(self.width, self.height, self.ip, int(self.port), self.username)
                        g.run()
                    elif tmp == 'IP_Input':
                        self.first_input = False
                        self.second_input = True
                        self.third_input = False
                    elif tmp == 'Port_Input':
                        self.first_input = False
                        self.second_input = False
                        self.third_input = True
                    elif tmp == 'Username_Input':
                        self.first_input = True
                        self.second_input = False
                        self.third_input = False
                    else:
                        self.first_input = False
                        self.second_input = False
                        self.third_input = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        os._exit(1)
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        return
                    if self.first_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            if len(self.username) < 15:
                                self.username += event.unicode
                    if self.second_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.ip = self.ip[:-1]
                        else:
                            if len(self.ip) < 15:
                                self.ip += event.unicode
                    if self.third_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.port = self.port[:-1]
                        else:
                            if len(self.port) < 15:
                                if event.unicode.isdigit():
                                    self.port += event.unicode
                if event.type == pygame.QUIT:
                    os._exit(1)
                    self.is_running = False
            self.group.update(self.screen)
            font = pygame.font.Font('assets/font.ttf', int(pygame.display.get_surface().get_height() / 32))
            text_username = font.render(self.username, True, (255, 255, 255))
            text_username_rect = text_username.get_rect(center=self.widget.get_center('Username_Input'))
            self.screen.blit(text_username, text_username_rect)
            text_ip = font.render(self.ip, True, (255, 255, 255))
            text_ip_rect = text_ip.get_rect(center=self.widget.get_center('IP_Input'))
            self.screen.blit(text_ip, text_ip_rect)
            text_port = font.render(self.port, True, (255, 255, 255))
            text_port_rect = text_port.get_rect(center=self.widget.get_center('Port_Input'))
            self.screen.blit(text_port, text_port_rect)
            pygame.display.update()

        pygame.quit()


class Create_Server_Input_Menu:
    def __init__(self, w, h):
        pygame.font.init()
        pygame.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('FABLEFIELDS')

        self.is_running = True
        self.group = pygame.sprite.Group()
        self.widget = Connection_Widget(self.group, pygame.image.load("assets/Create_Server_Menu.png").convert_alpha())
        self.font = pygame.font.Font("assets/font.ttf", 40)

        self.ip = 'localhost'
        self.port = '5555'
        self.username = 'user'
        self.first_input = False
        self.second_input = False
        self.third_input = False

    def run(self):
        # game loop
        while self.is_running:
            self.screen.fill('#6CAD34')
            mouse_position = pygame.mouse.get_pos()

            # event-handler
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tmp = self.widget.checking_button(mouse_position)
                    if tmp == 'Cancel':
                        self.first_input = False
                        self.second_input = False
                        self.third_input = False
                        m = Connection_Menu(self.width, self.height)
                        m.run()
                    elif tmp == 'Connect':
                        self.first_input = False
                        self.second_input = False
                        self.third_input = False
                        server = Server({}, self.ip, int(self.port))
                        start_new_thread(server.run, ())
                        time.sleep(0.5)
                        g = game.Game(self.width, self.height, self.ip, int(self.port), self.username)
                        g.run()
                        server.game_going = 0
                        server.break_fl = 0
                        server.s.close()
                        time.sleep(0.5)
                    elif tmp == 'IP_Input':
                        self.first_input = False
                        self.second_input = True
                        self.third_input = False
                    elif tmp == 'Port_Input':
                        self.first_input = False
                        self.second_input = False
                        self.third_input = True
                    elif tmp == 'Username_Input':
                        self.first_input = True
                        self.second_input = False
                        self.third_input = False
                    else:
                        self.first_input = False
                        self.second_input = False
                        self.third_input = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        os._exit(1)
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        return
                    if self.first_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            if len(self.username) < 15:
                                self.username += event.unicode
                    if self.second_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.ip = self.ip[:-1]
                        else:
                            if len(self.ip) < 15:
                                self.ip += event.unicode
                    if self.third_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.port = self.port[:-1]
                        else:
                            if len(self.port) < 15:
                                if event.unicode.isdigit():
                                    self.port += event.unicode
                if event.type == pygame.QUIT:
                    os._exit(1)
                    self.is_running = False
            self.group.update(self.screen)
            font = pygame.font.Font('assets/font.ttf', int(pygame.display.get_surface().get_height() / 32))
            text_username = font.render(self.username, True, (255, 255, 255))
            text_username_rect = text_username.get_rect(center=self.widget.get_center('Username_Input'))
            self.screen.blit(text_username, text_username_rect)
            text_ip = font.render(self.ip, True, (255, 255, 255))
            text_ip_rect = text_ip.get_rect(center=self.widget.get_center('IP_Input'))
            self.screen.blit(text_ip, text_ip_rect)
            text_port = font.render(self.port, True, (255, 255, 255))
            text_port_rect = text_port.get_rect(center=self.widget.get_center('Port_Input'))
            self.screen.blit(text_port, text_port_rect)
            pygame.display.update()

        pygame.quit()


class Tutorial:
    def __init__(self, w, h):
        pygame.font.init()
        pygame.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('FABLEFIELDS')

        self.is_running = True
        self.group = pygame.sprite.Group()
        self.widget = pygame.image.load("assets/tutorial_of_Fable.png").convert_alpha()

    def run(self):
        # game loop
        while self.is_running:
            self.screen.fill('#6CAD34')
            mouse_position = pygame.mouse.get_pos()

            # event-handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        os._exit(1)
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        return
                if event.type == pygame.QUIT:
                    os._exit(1)
                    self.is_running = False
            self.screen.blit(self.widget, (0, 0))
            pygame.display.update()

        pygame.quit()