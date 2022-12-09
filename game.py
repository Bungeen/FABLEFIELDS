import sys

import pygame

from network import Network
from menu import Menu


class Player:
    width = height = 50

    def __init__(self, startx, starty, color=(255, 0, 0), active=0):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color
        self.is_active = bool(active)

    def get_size(self, canvas):
        tmp_size = min(canvas.get_width() / 30, canvas.get_height() / 30)
        return tmp_size

    def draw(self, canvas):
        tmp_size = min(canvas.get_width() / 30, canvas.get_height() / 30)
        pygame.draw.rect(canvas, self.color, (self.x, self.y, tmp_size, tmp_size), 0)

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
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50, active=1, color=(0, 200, 0))
        self.player2 = Player(100, 100, active=0, color=(200, 0, 0))
        self.canvas = Canvas(self.width, self.height, is_fullscreen)

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
                if self.player.x <= self.canvas.get_canvas().get_width() - self.player.get_size(
                        self.canvas.get_canvas()):
                    self.player.move(0)

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.player.x >= 0:
                    self.player.move(1)

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if self.player.y >= 0:
                    self.player.move(2)

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if self.player.y <= self.canvas.get_canvas().get_height() - self.player.get_size(
                        self.canvas.get_canvas()):
                    self.player.move(3)

            print(self.canvas.get_canvas().get_height(), self.player.y)

            # Send Network Stuff
            self.player2.x, self.player2.y, self.player2.is_active = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            if self.player.is_active:
                print('Act')
                self.player.draw(self.canvas.get_canvas())
            if self.player2.is_active:
                print('Act2')
                self.player2.draw(self.canvas.get_canvas())
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
