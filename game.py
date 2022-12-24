import os
import sys
import time
import json
import ast

import pygame
import pytmx

import spritesheet

from network import Network
from menu import Menu


# def load_image(name, colorkey=None):
#     fullname = os.path.join('assets', name)
#     # если файл не существует, то выходим
#     if not os.path.isfile(fullname):
#         print(f"Файл с изображением '{fullname}' не найден")
#         sys.exit()
#     image = pygame.image.load(fullname)
#     return image


class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, player_id=0, status=0):
        super().__init__(group)
        sprite_sheet_image = pygame.image.load('assets/JessyWithNull.png').convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        self.image = sprite_sheet.get_image(0, 32, 32, 4.5, (0, 0, 0))
        self.image_top = sprite_sheet.get_image(1, 32, 32, 4.5, (0, 0, 0))
        self.image_left = sprite_sheet.get_image(3, 32, 32, 4.5, (0, 0, 0))
        self.image_right = sprite_sheet.get_image(2, 32, 32, 4.5, (0, 0, 0))
        self.image_behind = sprite_sheet.get_image(4, 32, 32, 4.5, (0, 0, 0))
        self.image_nothing = sprite_sheet.get_image(0, 32, 32, 4.5, (0, 0, 0))
        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))

        self.status = status

        self.animation_type = 0
        self.using = 0
        self.tool_type = 0
        self.can_do = 0

        self.resize_initialization(size, True)
        self.direction = pygame.math.Vector2()
        self.speed = 2 * size
        self.rect = self.image.get_rect()
        print(pos[0], pos[1])
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        print(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())
        print(self.rect.x, self.rect.y)
        self.coordinates = pygame.math.Vector2(0, 0)
        self.old_size = size

        self.using_tile = (-100000, -100000)

    # NETWORKING BREAKING
    #     keys = pygame.key.get_pressed()
    #     # NETWORKING BREAKING

    def change_view(self):
        if self.status == 0:
            self.image = self.image_nothing
            return
        if self.direction.x == -1:
            self.image = self.image_left
            self.status = 1
        elif self.direction.x == 1:
            self.image = self.image_right
            self.status = 2
        elif self.direction.y == 1:
            self.image = self.image_top
            self.status = 3
        elif self.direction.y == -1:
            self.image = self.image_behind
            self.status = 4
        elif self.status != 0:
            if self.status == 1:
                self.image = self.image_left
            elif self.status == 2:
                self.image = self.image_right
            elif self.status == 3:
                self.image = self.image_top
            elif self.status == 4:
                self.image = self.image_behind

    def resize_initialization(self, size, fl=False):
        sprite_sheet_image = pygame.image.load('assets/JessyWithNull.png').convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        self.image = sprite_sheet.get_image(0, 32, 32, size, (0, 0, 0))
        self.image_top = sprite_sheet.get_image(1, 32, 32, size, (0, 0, 0))
        self.image_left = sprite_sheet.get_image(3, 32, 32, size, (0, 0, 0))
        self.image_right = sprite_sheet.get_image(2, 32, 32, size, (0, 0, 0))
        self.image_behind = sprite_sheet.get_image(4, 32, 32, size, (0, 0, 0))
        self.image_nothing = sprite_sheet.get_image(0, 32, 32, size, (0, 0, 0))
        self.speed = 2 * size
        if not fl:
            print(self.rect)
            # self.rect.x += (size - self.old_size) * 32
            # self.rect.y += (size - self.old_size) * 32
            print(self.rect)
        self.old_size = size
        if self.status == 0:
            self.image = self.image_nothing
            return
        self.image = self.image_top

    def move(self, dirn):
        self.activating()

    def update(self):
        self.rect.center += self.direction * self.speed

    def activating(self):
        self.is_active = True


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        # self.ground_surf = pygame.image.load("graphics/ground.png").convert()
        # size = max(int(pygame.display.get_surface().get_width() / (13 * 32)),
        #            int(pygame.display.get_surface().get_height() / (8 * 32)))
        # self.ground_surf = pygame.transform.scale(self.ground_surf, (
        # self.ground_surf.get_size()[0] * size, self.ground_surf.get_size()[1] * size))
        # self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # Offset
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.map = []
        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))
        self.tile_size = int(size * 32)
        self.tiled_base = {'1': pygame.transform.scale(pygame.image.load("assets/test_grass_1.png").convert_alpha(),
                                                       (self.tile_size, self.tile_size)),
                           '2': pygame.transform.scale(pygame.image.load("assets/test_grass_2.png").convert_alpha(),
                                                       (self.tile_size, self.tile_size)),
                           '3': {'0': pygame.transform.scale(
                                     pygame.image.load("assets/test_dirt.png").convert_alpha(),
                                     (self.tile_size, self.tile_size)),
                                 '1': pygame.transform.scale(
                                     pygame.image.load("assets/test_plant_first.png").convert_alpha(),
                                     (self.tile_size, self.tile_size)),
                                 '2': pygame.transform.scale(
                                     pygame.image.load("assets/test_plant_second.png").convert_alpha(),
                                     (self.tile_size, self.tile_size)),
                                 '3': pygame.transform.scale(
                                     pygame.image.load("assets/test_plant_third.png").convert_alpha(),
                                     (self.tile_size, self.tile_size)),
                                 '4': pygame.transform.scale(
                                     pygame.image.load("assets/test_plant_first_water.png").convert_alpha(),
                                     (self.tile_size, self.tile_size)),
                                 '5': pygame.transform.scale(
                                     pygame.image.load("assets/test_plant_second_water.png").convert_alpha(),
                                     (self.tile_size, self.tile_size)),
                                 '6': pygame.transform.scale(
                                     pygame.image.load("assets/test_plant_third_water.png").convert_alpha(),
                                     (self.tile_size, self.tile_size)),
                                 '7': pygame.transform.scale(
                                     pygame.image.load("assets/test_dirt_water.png").convert_alpha(),
                                     (self.tile_size, self.tile_size))
                                 }}

        # IMPORTANT. LOADING SAVE #################################
        # with open("maps/mapp.txt", 'r', encoding='utf8') as f:
        #     base = f.read().split('\n')
        #     for el in base:
        #         self.map += [el.split(', ')]
        #     f.close()
        # print(sys.getsizeof(self.map))
        # print(self.map)
        # os._exit(1)
        ###########################################################

        # self.map = pytmx.load_pygame("maps\mappp.tmx")
        # size = max(pygame.display.get_surface().get_width() / (13 * 32),
        #            pygame.display.get_surface().get_height() / (8 * 32))
        # for y in range(20):
        #     for x in range(30):
        #         image = pygame.transform.scale(self.map.get_tile_image(x, y, 0), (size * 32, size * 32))
        #         self.map.set_tile_properties(x, y, image)
        # for tile_object in self.map.tmxdata.objects:
        #     tile_object.x *= int(400 / self.map.tilesize)
        #     tile_object.y *= int(400 / self.map.tilesize)

    # def resize_initialization(self, size):
    # self.ground_surf = pygame.image.load("graphics/ground.png").convert()
    # self.ground_surf = pygame.transform.scale(self.ground_surf, (
    #    self.ground_surf.get_size()[0] * size, self.ground_surf.get_size()[1] * size))
    # self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.center_target_camera(player)

        # size = max(pygame.display.get_surface().get_width() / (13 * 32),
        #            pygame.display.get_surface().get_height() / (8 * 32))
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                tile = self.map[y][x]
                id_tile, id_state = map(str, tile.split(' - '))
                # print(id_tile)
                ground_offset = (x * self.tile_size - self.offset[0], y * self.tile_size - self.offset[1])
                if type(self.tiled_base[id_tile]) == dict:
                    self.display_surface.blit(self.tiled_base[id_tile][id_state], ground_offset)
                else:
                    self.display_surface.blit(self.tiled_base[id_tile], ground_offset)

        # for y in range(20):
        #     for x in range(30):
        #         image = pygame.transform.scale(self.map.get_tile_image(x, y, 0), (size * 32, size * 32))
        #         ground_offset = (x * self.map.tilewidth - self.offset[0], y * self.map.tilewidth - self.offset[1])
        #         # ground_offset = (x * size * 8, y * size * 8)
        #         # print(ground_offset)
        #         self.display_surface.blit(image, ground_offset) # (, y * size)

        # ground
        # ground_offset = self.ground_rect.topleft - self.offset
        # self.display_surface.blit(self.ground_surf, ground_offset)

        if player.status == 1:
            selected_rect = (((player.rect.center[0]) // self.tile_size - 1) * self.tile_size,
                             (player.rect.center[
                                 1]) // self.tile_size * self.tile_size) - self.offset
            player.using_tile = (
                (player.rect.center[0] // self.tile_size - 1), (player.rect.center[1] // self.tile_size))
        elif player.status == 2:
            selected_rect = (((player.rect.center[0]) // self.tile_size + 1) * self.tile_size,
                             (player.rect.center[
                                 1]) // self.tile_size * self.tile_size) - self.offset
            player.using_tile = (
                (player.rect.center[0] // self.tile_size + 1), (player.rect.center[1] // self.tile_size))
        elif player.status == 3:
            selected_rect = (((player.rect.center[0]) // self.tile_size) * self.tile_size,
                             ((player.rect.center[
                                 1]) // self.tile_size + 1) * self.tile_size) - self.offset
            player.using_tile = (
                (player.rect.center[0] // self.tile_size), (player.rect.center[1] // self.tile_size + 1))
        elif player.status == 4:
            selected_rect = (((player.rect.center[0]) // self.tile_size) * self.tile_size,
                             ((player.rect.center[
                                 1]) // self.tile_size - 1) * self.tile_size) - self.offset
            player.using_tile = (
                (player.rect.center[0] // self.tile_size), (player.rect.center[1] // self.tile_size - 1))
        else:
            selected_rect = (-100000, -100000)
        if player.tool_type == 1:
            image_selected = pygame.transform.scale(pygame.image.load('assets/Selected.png'),
                                                    (self.tile_size, self.tile_size))
            self.display_surface.blit(image_selected, selected_rect)
        if player.tool_type == 2:
            try:
                if self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[0] != '3' or \
                        self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[1] not in ['0', '7']:
                    image_selected = pygame.transform.scale(pygame.image.load('assets/Bad_Selected.png'),
                                                            (self.tile_size, self.tile_size))
                    self.display_surface.blit(image_selected, selected_rect)
                    player.can_do = 0
                else:
                    image_selected = pygame.transform.scale(pygame.image.load('assets/Good_Selected.png'),
                                                            (self.tile_size, self.tile_size))
                    self.display_surface.blit(image_selected, selected_rect)
                    player.can_do = 1
            except:
                pass
        if player.tool_type == 3:
            try:
                if self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[0] != '3' or \
                        self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[1] not in ['3', '6']:
                    image_selected = pygame.transform.scale(pygame.image.load('assets/Bad_Selected.png'),
                                                            (self.tile_size, self.tile_size))
                    self.display_surface.blit(image_selected, selected_rect)
                    player.can_do = 0
                else:
                    image_selected = pygame.transform.scale(pygame.image.load('assets/Good_Selected.png'),
                                                            (self.tile_size, self.tile_size))
                    self.display_surface.blit(image_selected, selected_rect)
                    player.can_do = 1
            except:
                pass
        if player.tool_type == 4:
            try:
                if self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[0] != '3':
                    image_selected = pygame.transform.scale(pygame.image.load('assets/Bad_Selected.png'),
                                                            (self.tile_size, self.tile_size))
                    self.display_surface.blit(image_selected, selected_rect)
                    player.can_do = 0
                else:
                    image_selected = pygame.transform.scale(pygame.image.load('assets/Good_Selected.png'),
                                                            (self.tile_size, self.tile_size))
                    self.display_surface.blit(image_selected, selected_rect)
                    player.can_do = 1
            except:
                pass

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
        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))
        self.tile_size = int(size * 32)
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
                os._exit(1)
            data = 'tmp_1'
            print(data)
            df = self.net.send(data)
            if df == '0XE000':
                print(1)
                self.is_running = False
                m = Menu(w, h)
                m.run()
                os._exit(1)
        except:
            self.is_running = False
            m = Menu(w, h)
            m.run()
            os._exit(1)

        # Take information about self
        data = self.net.send('KEY')
        if data == '0XE000':
            self.is_running = False
            m = Menu(w, h)
            m.run()
            sys.exit()
        self.player = Player(self.camera_group, (data['Player Position'][0] * size, data['Player Position'][1] * size), status=1)
        self.map = data['Package']['Map']
        # print((data[0] - 100, data[1] - 100))
        self.player2 = Player(self.camera_group, (100, 100), status=0)
        self.player3 = Player(self.camera_group, (100, 100), status=0)
        self.player4 = Player(self.camera_group, (100, 100), status=0)
        self.base_id.remove(self.net.id)
        self.camera_group.map = self.map

        self.package = {}

    # def render(self, screen):
    #     for y in range(20):
    #         for x in range(30):
    #             image = self.map.get_tile_image(x, y, 0)
    #             size = max(pygame.display.get_surface().get_width() / (13 * 32),
    #                        pygame.display.get_surface().get_height() / (8 * 32))
    #             screen.blit(image, (x * size, y * size))

    def run(self):
        clock = pygame.time.Clock()
        using = 0
        while self.is_running:
            clock.tick(60)

            self.package = {'World change': []}

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        sys.exit()
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        m = Menu(self.canvas.width, self.canvas.height)
                        m.run()
                        sys.exit()
                if event.type == pygame.QUIT:
                    self.is_running = False
                    print('EXIT')
                    os._exit(1)

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

            if self.player.using:
                self.player.using -= 1

            if keys[pygame.K_e]:
                if not self.player.using:
                    self.player.using = 10
                    self.player.tool_type = (self.player.tool_type + 1) % 5

            if keys[pygame.K_q]:
                if not self.player.using:
                    self.player.using = 10
                    self.player.tool_type = (self.player.tool_type - 1) % 5

            if keys[pygame.K_f]:
                if not self.player.using:
                    #os._exit(1)
                    if self.player.using_tile != (-100000, -100000) and self.player.tool_type == 1:
                        #os._exit(1)
                        if 0 <= self.player.using_tile[1] < len(self.map) and 0 <= self.player.using_tile[0] < len(
                                self.map[0]):
                            tile = self.map[self.player.using_tile[1]][self.player.using_tile[0]]
                            tile_id, tile_state = tile.split(' - ')
                            if tile_id == '1':
                                tile_id = 2
                            elif tile_id == '2':
                                tile_id = 3
                            else:
                                tile_id = 1
                            tile_state = 0
                            new_tile = f"{tile_id} - {tile_state}"
                            self.package['World change'] = [self.player.using_tile, new_tile]
                            print(new_tile, tile)
                            self.map[self.player.using_tile[1]][self.player.using_tile[0]] = new_tile
                        self.player.using = 15
                    if self.player.tool_type == 2:
                        if self.player.can_do == 1:
                            if 0 <= self.player.using_tile[1] < len(self.map) and 0 <= self.player.using_tile[0] < len(
                                    self.map[0]):
                                tile = self.map[self.player.using_tile[1]][self.player.using_tile[0]]
                                tile_id, tile_state = tile.split(' - ')
                                if tile_state == '7':
                                    tile_state = '4'
                                if tile_state == '0':
                                    tile_state = '1'
                                new_tile = f"{tile_id} - {tile_state}"
                                self.package['World change'] = [self.player.using_tile, new_tile]
                                print(new_tile, tile)
                                self.map[self.player.using_tile[1]][self.player.using_tile[0]] = new_tile
                        self.player.using = 15
                    if self.player.tool_type == 3:
                        if self.player.can_do == 1:
                            if 0 <= self.player.using_tile[1] < len(self.map) and 0 <= self.player.using_tile[0] < len(
                                    self.map[0]):
                                tile = self.map[self.player.using_tile[1]][self.player.using_tile[0]]
                                tile_id, tile_state = tile.split(' - ')
                                if tile_state == '6':
                                    tile_state = '7'
                                if tile_state == '3':
                                    tile_state = '0'
                                new_tile = f"{tile_id} - {tile_state}"
                                self.package['World change'] = [self.player.using_tile, new_tile]
                                print(new_tile, tile)
                                self.map[self.player.using_tile[1]][self.player.using_tile[0]] = new_tile
                        self.player.using = 15
                    if self.player.tool_type == 4:
                        if self.player.can_do == 1:
                            if 0 <= self.player.using_tile[1] < len(self.map) and 0 <= self.player.using_tile[0] < len(
                                    self.map[0]):
                                tile = self.map[self.player.using_tile[1]][self.player.using_tile[0]]
                                tile_id, tile_state = tile.split(' - ')
                                if tile_state == '0':
                                    tile_state = '7'
                                if tile_state == '1':
                                    tile_state = '4'
                                if tile_state == '2':
                                    tile_state = '5'
                                if tile_state == '3':
                                    tile_state = '6'
                                # tile_state = '1'
                                new_tile = f"{tile_id} - {tile_state}"
                                self.package['World change'] = [self.player.using_tile, new_tile]
                                print(new_tile, tile)
                                self.map[self.player.using_tile[1]][self.player.using_tile[0]] = new_tile
                        self.player.using = 15

            self.player.activating()
            self.player.change_view()

            # Send Network Stuff
            # self.player2.rect.x, self.player2.rect.y, self.player2.is_active = self.parse_data()

            # Players synh
            data = self.send_data()
            for key in data.keys():
                if key == self.base_id[0]:
                    self.player2.rect.x, self.player2.rect.y, self.player2.status, self.player2.animation_type, self.player2.using = self.parse_data(
                        data[key])
                if key == self.base_id[1]:
                    self.player3.rect.x, self.player3.rect.y, self.player3.status, self.player3.animation_type, self.player3.using = self.parse_data(
                        data[key])
                if key == self.base_id[2]:
                    self.player4.rect.x, self.player4.rect.y, self.player4.status, self.player4.animation_type, self.player4.using = self.parse_data(
                        data[key])
                if key == self.net.id:
                    for key_package in data[key]['Package'].keys():
                        if key_package == 'World change':
                            for i in range(0, len(data[key]['Package']['World change']), 2):
                                x, y = data[key]['Package']['World change'][i][0], \
                                       data[key]['Package']['World change'][i][1]
                                self.map[y][x] = data[key]['Package']['World change'][i + 1]
                            # print(data[key]['Package']['World change'])
                            # print(data[key]['Package']['World change'])
                            # x, y = data[key]['Package']['World change'][0][0], data[key]['Package']['World change'][0][1]
                            # self.map[y][x] = data[key]['Package']['World change'][1]

            self.player2.change_view()
            self.player3.change_view()
            self.player4.change_view()

            # Update Canvas
            self.canvas.draw_background()
            self.camera_group.update()
            self.camera_group.custom_draw(self.player)
            self.canvas.update()

        # pygame.quit()

    def send_data(self):
        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))
        data = {'ID': self.net.id, 'Player Position': (self.player.rect.x / size, self.player.rect.y / size),
                'Player Status': self.player.status, 'Player Animation Type': 0,
                'Player Using State': self.player.using, 'Package': self.package}
        # print(data)
        # data = str(self.net.id) + ":" + str(self.player.rect.x) + "," + str(self.player.rect.y) + ',1'
        # print(data)
        reply = self.net.send(data)
        print(reply, "GET_DATA_GAME")
        if reply == '0XE000':
            self.is_running = False
            m = Menu(self.canvas.width, self.canvas.height)
            m.run()
            sys.exit()
        return reply

    @staticmethod
    def parse_data(data):
        try:
            size = max(pygame.display.get_surface().get_width() / (13 * 32),
                       pygame.display.get_surface().get_height() / (8 * 32))
            d = [data['Player Position'][0] * size, data['Player Position'][1] * size, data['Player Status'],
                 data['Player Animation Type'], data['Player Using State']]
            # print(int(d[0]), int(d[1]), bool(int(d[2])))
            return int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4])
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
