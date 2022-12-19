import os
import sys
import time
import json
import ast

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
    def __init__(self, group, pos, player_id=0, active=0):
        super().__init__(group)
        sprite_sheet_image = pygame.image.load('assets/jessy.png').convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        self.image = sprite_sheet.get_image(0, 32, 32, 4.5, (0, 0, 0))
        self.image_top = sprite_sheet.get_image(0, 32, 32, 4.5, (0, 0, 0))
        self.image_left = sprite_sheet.get_image(2, 32, 32, 4.5, (0, 0, 0))
        self.image_right = sprite_sheet.get_image(1, 32, 32, 4.5, (0, 0, 0))
        self.image_behind = sprite_sheet.get_image(3, 32, 32, 4.5, (0, 0, 0))
        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))
        self.resize_initialization(size, True)
        self.direction = pygame.math.Vector2()
        self.speed = 2 * size
        self.rect = self.image.get_rect()
        print(pos[0], pos[1])
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        print(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())
        print(self.rect.x, self.rect.y)
        self.is_active = bool(active)
        self.coordinates = pygame.math.Vector2(0, 0)
        self.old_size = size

    # NETWORKING BREAKING
    #     keys = pygame.key.get_pressed()
    #     # NETWORKING BREAKING

    def change_view(self):
        if self.direction.x == -1:
            self.image = self.image_left
        elif self.direction.x == 1:
            self.image = self.image_right
        elif self.direction.y == 1:
            self.image = self.image_top
        elif self.direction.y == -1:
            self.image = self.image_behind

    def resize_initialization(self, size, fl=False):
        sprite_sheet_image = pygame.image.load('assets/jessy.png').convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        self.image = sprite_sheet.get_image(0, 32, 32, size, (0, 0, 0))
        self.image_top = sprite_sheet.get_image(0, 32, 32, size, (0, 0, 0))
        self.image_left = sprite_sheet.get_image(2, 32, 32, size, (0, 0, 0))
        self.image_right = sprite_sheet.get_image(1, 32, 32, size, (0, 0, 0))
        self.image_behind = sprite_sheet.get_image(3, 32, 32, size, (0, 0, 0))
        self.speed = 2 * size
        if not fl:
            print(self.rect)
            # self.rect.x += (size - self.old_size) * 32
            # self.rect.y += (size - self.old_size) * 32
            print(self.rect)
        self.old_size = size

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        # if dirn == 0:
        #     self.x += self.velocity
        # elif dirn == 1:
        #     self.x -= self.velocity
        # elif dirn == 2:
        #     self.y -= self.velocity
        # else:
        #     self.y += self.velocity
        self.activating()

    def update(self):
        # self.input()
        self.rect.center += self.direction * self.speed

    def activating(self):
        self.is_active = True


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.ground_surf = pygame.image.load("graphics/ground.png").convert()
        # size = max(int(pygame.display.get_surface().get_width() / (13 * 32)),
        #            int(pygame.display.get_surface().get_height() / (8 * 32)))
        # self.ground_surf = pygame.transform.scale(self.ground_surf, (
        # self.ground_surf.get_size()[0] * size, self.ground_surf.get_size()[1] * size))
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # Offset
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

    def resize_initialization(self, size):
        self.ground_surf = pygame.image.load("graphics/ground.png").convert()
        self.ground_surf = pygame.transform.scale(self.ground_surf, (
            self.ground_surf.get_size()[0] * size, self.ground_surf.get_size()[1] * size))
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.center_target_camera(player)

        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            sprite_offset = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, sprite_offset)


class Game:

    def __init__(self, w, h, ip, port):
        self.base_id = ["S0", "S1", "S2", "S3"]
        pygame.init()
        self.width = w
        self.height = h
        print(self.width, self.height)
        self.canvas = Canvas(self.width, self.height)
        self.all_sprites = pygame.sprite.Group()
        self.camera_group = CameraGroup()
        self.is_running = True
        try:
            self.net = Network(ip, port)
            if self.net.id == '0XE000':
                self.is_running = False
                m = Menu(w, h)
                m.run()
                return
            data = 'user'
            print(data)
            df = self.net.send(data)
            if df == '0XE000':
                print(1)
                self.is_running = False
                m = Menu(w, h)
                m.run()
                return
        except:
            self.is_running = False
            m = Menu(w, h)
            m.run()
            return

        # Take information about self
        data = self.net.send('KEY')
        if data == '0XE000':
            self.is_running = False
            m = Menu(w, h)
            m.run()
            return
        self.player = Player(self.camera_group, data['Player Position'], active=data['Player Active'])
        # print((data[0] - 100, data[1] - 100))
        self.player2 = Player(self.camera_group, (100, 100), active=0)
        self.player3 = Player(self.camera_group, (100, 100), active=0)
        self.player4 = Player(self.camera_group, (100, 100), active=0)
        self.base_id.remove(self.net.id)

    def run(self):
        clock = pygame.time.Clock()
        while self.is_running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        sys.exit()
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        m = Menu(self.canvas.width, self.canvas.height)
                        m.run()
                        return
                if event.type == pygame.QUIT:
                    self.is_running = False
                    sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.direction.y = -1
                self.player.coordinates.y += self.player.speed
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.direction.y = 1
                self.player.coordinates.y -= self.player.speed
            else:
                self.player.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.direction.x = 1
                self.player.coordinates.x += self.player.speed
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.direction.x = -1
                self.player.coordinates.x -= self.player.speed
            else:
                self.player.direction.x = 0
            self.player.activating()
            self.player.change_view()

            # Send Network Stuff
            # self.player2.rect.x, self.player2.rect.y, self.player2.is_active = self.parse_data()

            # Players synh
            data = self.send_data()
            for key in data.keys():
                if key == self.base_id[0]:
                    self.player2.rect.x, self.player2.rect.y, self.player2.is_active = self.parse_data(data[key])
                if key == self.base_id[1]:
                    self.player3.rect.x, self.player3.rect.y, self.player3.is_active = self.parse_data(data[key])
                if key == self.base_id[2]:
                    self.player4.rect.x, self.player4.rect.y, self.player4.is_active = self.parse_data(data[key])


            # Update Canvas
            self.canvas.draw_background()
            # if self.player.is_active:
            #     print('Act')
            #     self.player.draw(self.canvas.get_canvas())
            # if self.player2.is_active:
            #     print('Act2')
            #     self.player2.draw(self.canvas.get_canvas())
            # self.all_sprites.draw(self.canvas.get_canvas())
            # self.canvas.update()
            self.camera_group.update()
            self.camera_group.custom_draw(self.player)
            self.canvas.update()

        # pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = {'ID': self.net.id, 'Player Position': (self.player.rect.x, self.player.rect.y), 'Player Active': 1}
        # data = str(self.net.id) + ":" + str(self.player.rect.x) + "," + str(self.player.rect.y) + ',1'
        print(data)
        reply = self.net.send(data)
        print(reply, "SEND_DATA_GAME")
        if reply == '0XE000':
            self.is_running = False
            m = Menu(self.canvas.width, self.canvas.height)
            m.run()
            return
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = [data['Player Position'][0], data['Player Position'][1], data['Player Active']]
            print(int(d[0]), int(d[1]), bool(int(d[2])))
            return int(d[0]), int(d[1]), bool(int(d[2]))
        except:
            return 0, 0, 0


class Canvas(Menu):

    def __init__(self, w, h):
        super().__init__(w, h)
        # self.initialization_screen()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        print(self.width, self.height)

    @staticmethod
    def update():
        pygame.display.update()

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255, 255, 255))
