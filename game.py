import os
import sys

import pygame

import spritesheet

from network import Network
from menu import Menu


def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image



class Player(pygame.sprite.Sprite):
    def __init__(self, group, start_x, start_y, player_id=0, active=0):
        super().__init__(group)
        sprite_sheet_image = pygame.image.load('assets/jessy.png').convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

        BLACK = (0, 0, 0)

        image = sprite_sheet.get_image(0, 32, 32, 3, BLACK)
        self.x = start_x
        self.y = start_y
        self.velocity = 10
        self.image = image
        self.rect = self.image.get_rect()
        self.is_active = bool(active)

    def get_size(self, canvas):
        tmp_size = min(canvas.get_width() / 30, canvas.get_height() / 30)
        return tmp_size

    def get_correct_coordinates(self, type_coordinate, canvas):
        if type_coordinate == 'x':
            return self.x #* canvas.get_width()
        if type_coordinate == 'y':
            return self.y #* canvas.get_height()
        return "ERROR"

    # def draw(self, canvas):
    #     tmp_size = min(canvas.get_width() / 30, canvas.get_height() / 30)
    #     pygame.draw.rect(canvas, self.color,
    #                      (self.x * canvas.get_width(), self.y * canvas.get_height(), tmp_size, tmp_size), 0)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity
        self.activating()

    def activating(self):
        self.is_active = True


class Game:

    def __init__(self, w, h, is_fullscreen=False):
        pygame.init()
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, is_fullscreen)
        self.all_sprites = pygame.sprite.Group()
        self.net = Network()
        self.player = Player(self.all_sprites, 0.05, 0.05, active=1)
        self.player2 = Player(self.all_sprites, 0.05, 0.05, active=0)

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        print(self.canvas.is_fullscreen)
                        self.canvas.is_fullscreen = not self.canvas.is_fullscreen
                        self.canvas.initialization_screen()
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        m = Menu(self.canvas.width, self.canvas.height, self.canvas.is_fullscreen)
                        m.run()
                        return
                if event.type == pygame.VIDEORESIZE:
                    if not self.canvas.is_fullscreen:
                        self.canvas.width = event.w
                        self.canvas.height = event.h
                        self.canvas.initialization_screen()
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self.player.get_correct_coordinates('x', self.canvas.get_canvas()) \
                        <= self.canvas.get_canvas().get_width() - self.player.get_size(self.canvas.get_canvas()):
                    self.player.move(0)

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.player.get_correct_coordinates('x', self.canvas.get_canvas()) >= 0:
                    self.player.move(1)

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if self.player.get_correct_coordinates('y', self.canvas.get_canvas()) >= 0:
                    self.player.move(2)

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if self.player.get_correct_coordinates('y', self.canvas.get_canvas()) \
                        <= self.canvas.get_canvas().get_height() - self.player.get_size(self.canvas.get_canvas()):
                    self.player.move(3)

            print(self.canvas.get_canvas().get_height(), self.player.y)

            # Send Network Stuff
            self.player2.x, self.player2.y, self.player2.is_active = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            # if self.player.is_active:
            #     print('Act')
            #     self.player.draw(self.canvas.get_canvas())
            # if self.player2.is_active:
            #     print('Act2')
            #     self.player2.draw(self.canvas.get_canvas())
            self.all_sprites.draw(self.canvas.get_canvas())
            self.canvas.update()

        # pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + ',1'
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1]), bool(int(d[2]))
        except:
            return 0, 0, 0


class Canvas(Menu):

    def __init__(self, w, h, is_fullscreen=False, name="None"):
        super().__init__(w, h, is_fullscreen)
        self.screen = None
        self.initialization_screen()
        print(self.width, self.height)
        # self.screen = pygame.display.set_mode((w, h))
        # pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    # def draw_text(self, text, size, x, y):
    #     pygame.font.init()
    #     font = pygame.font.SysFont("comicsans", size)
    #     render = font.render(text, 1, (0, 0, 0))
    #
    #     self.screen.draw(render, (x, y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255, 255, 255))
