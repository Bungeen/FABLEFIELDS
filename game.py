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
    def __init__(self, group, pos, player_id=0, active=0):
        super().__init__(group)
        sprite_sheet_image = pygame.image.load('assets/jessy.png').convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        self.image = sprite_sheet.get_image(0, 32, 32, 3, (0, 0, 0))
        self.image_top = sprite_sheet.get_image(0, 32, 32, 3, (0, 0, 0))
        self.image_left = sprite_sheet.get_image(2, 32, 32, 3, (0, 0, 0))
        self.image_right = sprite_sheet.get_image(1, 32, 32, 3, (0, 0, 0))
        self.image_behind = sprite_sheet.get_image(3, 32, 32, 3, (0, 0, 0))
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.rect = self.image.get_rect()
        self.is_active = bool(active)
        self.coordinates = pygame.math.Vector2(0, 0)

    # NETWORKING BREAKING
    #     keys = pygame.key.get_pressed()
    #     # NETWORKING BREAKING

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
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # Offset
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

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

    def __init__(self, w, h, is_fullscreen=False):
        pygame.init()
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, is_fullscreen)
        self.all_sprites = pygame.sprite.Group()
        self.camera_group = CameraGroup()
        self.net = Network()
        self.player = Player(self.camera_group, (200, 200), active=1)
        self.player2 = Player(self.camera_group, (200, 200), active=0)

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
            print(self.player2.rect)

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


            # Send Network Stuff
            self.player2.rect.x, self.player2.rect.y, self.player2.is_active = self.parse_data(self.send_data())

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
        data = str(self.net.id) + ":" + str(self.player.rect.x) + "," + str(self.player.rect.y) + ',1'
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
