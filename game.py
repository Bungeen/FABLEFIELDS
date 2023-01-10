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

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, all_sprites, limited_group, display=False):
        super().__init__(all_sprites)
        self.add(limited_group)
        if display:
            self.image = pygame.Surface([abs(x2 - x1), abs(y2 - y1)])
        else:
            self.image = pygame.Surface([abs(x2 - x1), abs(y2 - y1)])
            self.image.set_alpha(0)
        self.rect = pygame.Rect(x1, y1, abs(x2 - x1), abs(y2 - y1))


class Seller(pygame.sprite.Sprite):
    def __init__(self, seller_group, tile_size, pos):
        super().__init__(seller_group)
        self.image = pygame.transform.scale(pygame.image.load('assets/Seller.png').convert_alpha(),
                                            (tile_size, tile_size))
        self.rect = pygame.Rect(pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size)


class Seller_Bought(pygame.sprite.Sprite):
    def __init__(self, seller_group, tile_size, pos):
        super().__init__(seller_group)
        self.image = pygame.transform.scale(pygame.image.load('assets/SellerBox_Buy.png').convert_alpha(),
                                            (tile_size, tile_size))
        self.rect = pygame.Rect(pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size)


class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, player_id='', status=0, limited_group=pygame.sprite.Group(),
                 seller_group=pygame.sprite.Group(), seller_box_group=pygame.sprite.Group()):
        super().__init__(group)
        sprite_sheet_image = pygame.image.load('assets/Character_Anim.png').convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        self.image = sprite_sheet.get_image(0, 32, 32, 4.5, (0, 0, 0))
        self.image_top = sprite_sheet.get_image(1, 32, 32, 4.5, (0, 0, 0))
        self.image_left = sprite_sheet.get_image(3, 32, 32, 4.5, (0, 0, 0))
        self.image_right = sprite_sheet.get_image(2, 32, 32, 4.5, (0, 0, 0))
        self.image_behind = sprite_sheet.get_image(4, 32, 32, 4.5, (0, 0, 0))
        self.image_nothing = sprite_sheet.get_image(0, 32, 32, 4.5, (0, 0, 0))
        self.image_top_box = sprite_sheet.get_image(5, 32, 32, 4.5, (0, 0, 0))
        self.image_left_box = sprite_sheet.get_image(7, 32, 32, 4.5, (0, 0, 0))
        self.image_right_box = sprite_sheet.get_image(6, 32, 32, 4.5, (0, 0, 0))
        self.image_behind_box = sprite_sheet.get_image(8, 32, 32, 4.5, (0, 0, 0))
        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))

        self.status = status

        self.animation_type = 0
        self.using = 0
        self.tool_type = 0
        self.can_do = 0
        self.changer = 0
        self.seed_type_selected = 0
        self.seed_type_can_use = ['8']
        self.bucket_status = 0
        self.seeds_id = ['8', '9', '10', '11', '12', '13', '14', '15', '16']
        self.money = 0
        self.can_buy = 0
        self.costs = []
        self.timer = 0
        self.score = 0
        self.id = player_id

        self.resize_initialization(size, True)
        self.direction = pygame.math.Vector2()
        self.speed = 2 * size
        self.rect = self.image.get_rect()
        # print(pos[0], pos[1])
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # print(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())
        # print(self.rect.x, self.rect.y)
        self.coordinates = pygame.math.Vector2(0, 0)
        self.old_size = size

        self.using_tile = (-100000, -100000)

        self.limited_group = limited_group
        self.seller_group = seller_group
        self.seller_box_group = seller_box_group

    # NETWORKING BREAKING
    #     keys = pygame.key.get_pressed()
    #     # NETWORKING BREAKING

    def change_view(self):
        if self.status == 0:
            self.image = self.image_nothing
            return
        if self.direction.x == -1:
            if self.animation_type == 0:
                self.image = self.image_left
            else:
                self.image = self.image_left_box
            self.status = 1
        elif self.direction.x == 1:
            if self.animation_type == 0:
                self.image = self.image_right
            else:
                self.image = self.image_right_box
            self.status = 2
        elif self.direction.y == 1:
            if self.animation_type == 0:
                self.image = self.image_top
            else:
                self.image = self.image_top_box
            self.status = 3
        elif self.direction.y == -1:
            if self.animation_type == 0:
                self.image = self.image_behind
            else:
                self.image = self.image_behind_box
            self.status = 4
        elif self.status != 0:
            if self.animation_type == 0:
                if self.status == 1:
                    self.image = self.image_left
                elif self.status == 2:
                    self.image = self.image_right
                elif self.status == 3:
                    self.image = self.image_top
                elif self.status == 4:
                    self.image = self.image_behind
            else:
                if self.status == 1:
                    self.image = self.image_left_box
                elif self.status == 2:
                    self.image = self.image_right_box
                elif self.status == 3:
                    self.image = self.image_top_box
                elif self.status == 4:
                    self.image = self.image_behind_box

    def resize_initialization(self, size, fl=False):
        if self.id in ['S0', 'S2']:
            sprite_sheet_image = pygame.image.load('assets/Character_Second_Animated.png').convert_alpha()
            sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
            self.image = sprite_sheet.get_image(0, 32, 32, size, (0, 0, 0))
            self.image_top = sprite_sheet.get_image(1, 32, 32, size, (0, 0, 0))
            self.image_left = sprite_sheet.get_image(3, 32, 32, size, (0, 0, 0))
            self.image_right = sprite_sheet.get_image(2, 32, 32, size, (0, 0, 0))
            self.image_behind = sprite_sheet.get_image(4, 32, 32, size, (0, 0, 0))
            self.image_nothing = sprite_sheet.get_image(0, 32, 32, size, (0, 0, 0))
            self.image_top_box = sprite_sheet.get_image(5, 32, 32, size, (0, 0, 0))
            self.image_left_box = sprite_sheet.get_image(7, 32, 32, size, (0, 0, 0))
            self.image_right_box = sprite_sheet.get_image(6, 32, 32, size, (0, 0, 0))
            self.image_behind_box = sprite_sheet.get_image(8, 32, 32, size, (0, 0, 0))
            self.speed = 2 * size
        else:
            sprite_sheet_image = pygame.image.load('assets/Character_First_Animated.png').convert_alpha()
            sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
            self.image = sprite_sheet.get_image(0, 32, 32, size, (0, 0, 0))
            self.image_top = sprite_sheet.get_image(1, 32, 32, size, (0, 0, 0))
            self.image_left = sprite_sheet.get_image(3, 32, 32, size, (0, 0, 0))
            self.image_right = sprite_sheet.get_image(2, 32, 32, size, (0, 0, 0))
            self.image_behind = sprite_sheet.get_image(4, 32, 32, size, (0, 0, 0))
            self.image_nothing = sprite_sheet.get_image(0, 32, 32, size, (0, 0, 0))
            self.image_top_box = sprite_sheet.get_image(5, 32, 32, size, (0, 0, 0))
            self.image_left_box = sprite_sheet.get_image(7, 32, 32, size, (0, 0, 0))
            self.image_right_box = sprite_sheet.get_image(6, 32, 32, size, (0, 0, 0))
            self.image_behind_box = sprite_sheet.get_image(8, 32, 32, size, (0, 0, 0))
            self.speed = 2 * size
        # if not fl:
        # print(self.rect)
        # self.rect.x += (size - self.old_size) * 32
        # self.rect.y += (size - self.old_size) * 32
        # print(self.rect)
        self.old_size = size
        if self.status == 0:
            self.image = self.image_nothing
            return
        self.image = self.image_top

    def move(self, dirn):
        self.activating()

    def update(self):
        self.rect.center += self.direction * self.speed
        if pygame.sprite.spritecollideany(self, self.limited_group):
            self.rect.center += (-self.direction) * self.speed * 2

        if pygame.sprite.spritecollideany(self, self.seller_group):
            if self.animation_type in range(8, 17):
                self.animation_type += 30
                # print(self.animation_type)

        if pygame.sprite.spritecollideany(self, self.seller_box_group):
            self.can_buy = 1
        else:
            self.can_buy = 0

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
        self.tiled_base = {'0': {'0': pygame.transform.scale(
            pygame.image.load("assets/Dirt.png").convert_alpha(), (self.tile_size, self.tile_size)),
            '7': pygame.transform.scale(
                pygame.image.load("assets/Dirt_Water.png").convert_alpha(),
                (self.tile_size, self.tile_size))},
            '1': pygame.transform.scale(pygame.image.load("assets/Grass.png").convert_alpha(),
                                        (self.tile_size, self.tile_size)),
            # '2': pygame.transform.scale(pygame.image.load("assets/test_grass_2.png").convert_alpha(),
            #                             (self.tile_size, self.tile_size)),
            '3': pygame.transform.scale(pygame.image.load("assets/Water.png").convert_alpha(),
                                        (self.tile_size, self.tile_size)),
            '4': pygame.transform.scale(pygame.image.load("assets/Base_Plate.png").convert_alpha(),
                                        (self.tile_size, self.tile_size)),
            '8': {'1': pygame.transform.scale(
                pygame.image.load("assets/Wheat_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Wheat_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Wheat_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Wheat_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Wheat_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Wheat_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            },
            '9': {'1': pygame.transform.scale(
                pygame.image.load("assets/Cucumbers_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Cucumbers_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Cucumbers_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Cucumbers_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Cucumbers_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Cucumbers_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            },
            '10': {'1': pygame.transform.scale(
                pygame.image.load("assets/Tomato_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Tomato_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Tomato_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Tomato_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Tomato_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Tomato_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            },
            '11': {'1': pygame.transform.scale(
                pygame.image.load("assets/Cabbage_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Cabbage_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Cabbage_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Cabbage_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Cabbage_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Cabbage_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            },
            '12': {'1': pygame.transform.scale(
                pygame.image.load("assets/Beet_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Beet_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Beet_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Beet_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Beet_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Beet_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            },
            '13': {'1': pygame.transform.scale(
                pygame.image.load("assets/Carrot_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Carrot_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Carrot_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Carrot_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Carrot_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Carrot_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            },
            '14': {'1': pygame.transform.scale(
                pygame.image.load("assets/Potato_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Potato_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Potato_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Potato_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Potato_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Potato_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            },
            '15': {'1': pygame.transform.scale(
                pygame.image.load("assets/Melon_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Melon_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Melon_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Melon_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Melon_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Melon_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            },
            '16': {'1': pygame.transform.scale(
                pygame.image.load("assets/Eggplant_First.png").convert_alpha(),
                (self.tile_size, self.tile_size)),
                '2': pygame.transform.scale(
                    pygame.image.load("assets/Eggplant_Second.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '3': pygame.transform.scale(
                    pygame.image.load("assets/Eggplant_Third.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '4': pygame.transform.scale(
                    pygame.image.load("assets/Eggplant_First_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '5': pygame.transform.scale(
                    pygame.image.load("assets/Eggplant_Second_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size)),
                '6': pygame.transform.scale(
                    pygame.image.load("assets/Eggplant_Third_Water.png").convert_alpha(),
                    (self.tile_size, self.tile_size))
            }
        }

        # MINIMUM SIZE IMPORTANT
        size = int(min(pygame.display.get_surface().get_width() / (13),
                       pygame.display.get_surface().get_height() / (8)))

        self.icon_base = {'0': {'0': pygame.transform.scale(pygame.image.load('assets/Wheat_Icon.png').convert_alpha(),
                                                            (size, size)),
                                '1': pygame.transform.scale(
                                    pygame.image.load('assets/Wheat_Icon_Bought.png').convert_alpha(),
                                    (size, size))},
                          '1': {
                              '0': pygame.transform.scale(pygame.image.load('assets/Cucumber_Icon.png').convert_alpha(),
                                                          (size, size)),
                              '1': pygame.transform.scale(
                                  pygame.image.load('assets/Cucumber_Icon_Bought.png').convert_alpha(),
                                  (size, size))},
                          '2': {'0': pygame.transform.scale(pygame.image.load('assets/Tomato_Icon.png').convert_alpha(),
                                                            (size, size)),
                                '1': pygame.transform.scale(
                                    pygame.image.load('assets/Tomato_Icon_Bought.png').convert_alpha(),
                                    (size, size))},
                          '3': {
                              '0': pygame.transform.scale(pygame.image.load('assets/Cabbage_Icon.png').convert_alpha(),
                                                          (size, size)),
                              '1': pygame.transform.scale(
                                  pygame.image.load('assets/Cabbage_Icon_Bought.png').convert_alpha(),
                                  (size, size))},
                          '4': {'0': pygame.transform.scale(pygame.image.load('assets/Beet_Icon.png').convert_alpha(),
                                                            (size, size)),
                                '1': pygame.transform.scale(
                                    pygame.image.load('assets/Beet_Icon_Bought.png').convert_alpha(),
                                    (size, size))},
                          '5': {'0': pygame.transform.scale(pygame.image.load('assets/Carrot_Icon.png').convert_alpha(),
                                                            (size, size)),
                                '1': pygame.transform.scale(
                                    pygame.image.load('assets/Carrot_Icon_Bought.png').convert_alpha(),
                                    (size, size))},
                          '6': {'0': pygame.transform.scale(pygame.image.load('assets/Potato_Icon.png').convert_alpha(),
                                                            (size, size)),
                                '1': pygame.transform.scale(
                                    pygame.image.load('assets/Potato_Icon_Bought.png').convert_alpha(),
                                    (size, size))},
                          '7': {'0': pygame.transform.scale(pygame.image.load('assets/Melon_Icon.png').convert_alpha(),
                                                            (size, size)),
                                '1': pygame.transform.scale(
                                    pygame.image.load('assets/Melon_Icon_Bought.png').convert_alpha(),
                                    (size, size))},
                          '8': {
                              '0': pygame.transform.scale(pygame.image.load('assets/Eggplant_Icon.png').convert_alpha(),
                                                          (size, size)),
                              '1': pygame.transform.scale(
                                  pygame.image.load('assets/Eggplant_Icon_Bought.png').convert_alpha(),
                                  (size, size))},
                          }
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

    def custom_draw(self, player, seller, seller_box):
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.center_target_camera(player)

        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                tile = self.map[y][x]
                id_tile, id_state = map(str, tile.split(' - '))
                ground_offset = (x * self.tile_size - self.offset[0], y * self.tile_size - self.offset[1])
                if id_tile == '5':
                    self.display_surface.blit(seller.image, ground_offset)
                    # seller.rect.topleft = ground_offset
                    # pygame.draw.rect(self.display_surface, '#FF00FF', seller.rect)
                    continue
                if id_tile == '6':
                    self.display_surface.blit(seller_box.image, ground_offset)
                    # seller_box.rect.topleft = ground_offset
                    # pygame.draw.rect(self.display_surface, '#FFFF00', seller_box.rect)
                    continue
                # print(id_tile)
                if type(self.tiled_base[id_tile]) == dict:
                    self.display_surface.blit(self.tiled_base[id_tile][id_state], ground_offset)
                else:
                    self.display_surface.blit(self.tiled_base[id_tile], ground_offset)
        # pygame.draw.rect(self.display_surface, '#FF0000', player.rect)
        # player.rect.topleft = (pygame.display.get_surface().get_width() / 2 - size / 2, pygame.display.get_surface().get_height() / 2 - size / 2)
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

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            sprite_offset = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, sprite_offset)

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

        size_x = pygame.display.get_surface().get_width() / 96
        size_y = pygame.display.get_surface().get_height() / 108

        if player.tool_type == 1:
            image_icon = pygame.transform.scale(pygame.image.load('assets/Shovel.png'),
                                                (self.tile_size, self.tile_size))
            self.display_surface.blit(image_icon, (size_x, size_y))
        elif player.tool_type == 2:
            image_icon = pygame.transform.scale(pygame.image.load('assets/Seeds.png'),
                                                (self.tile_size, self.tile_size))
            self.display_surface.blit(image_icon, (size_x, size_y))
        elif player.tool_type == 3:
            image_icon = pygame.transform.scale(pygame.image.load('assets/Hoe.png'),
                                                (self.tile_size, self.tile_size))
            self.display_surface.blit(image_icon, (size_x, size_y))
        elif player.tool_type == 4:
            if player.bucket_status == 1:
                image_icon = pygame.transform.scale(pygame.image.load('assets/Bucket_Water.png'),
                                                    (self.tile_size, self.tile_size))
                self.display_surface.blit(image_icon, (size_x, size_y))
            else:
                image_icon = pygame.transform.scale(pygame.image.load('assets/Bucket.png'),
                                                    (self.tile_size, self.tile_size))
                self.display_surface.blit(image_icon, (size_x, size_y))
        else:
            image_icon = pygame.transform.scale(pygame.image.load('assets/Nothing.png'),
                                                (self.tile_size, self.tile_size))
            self.display_surface.blit(image_icon, (size_x, size_y))

        if player.changer or player.tool_type == 2:
            image_icon = pygame.transform.scale(
                self.icon_base[str(int(player.seed_type_can_use[player.seed_type_selected]) - 8)]['0'],
                (self.tile_size, self.tile_size))
            self.display_surface.blit(image_icon, (size_x, size_y + self.tile_size))
        if not (((player.using_tile[0] < 0 or player.using_tile[0] >= len(self.map[0]) or player.using_tile[1] < 0 or
                  player.using_tile[1] >= len(self.map)))):
            if not self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[0] in ['5', '6']:
                if not player.changer:
                    if player.tool_type == 1:
                        if self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[0] == '3':
                            image_selected = pygame.transform.scale(pygame.image.load('assets/Bad_Selected.png'),
                                                                    (self.tile_size, self.tile_size))
                            self.display_surface.blit(image_selected, selected_rect)
                            player.can_do = 0
                        else:
                            image_selected = pygame.transform.scale(pygame.image.load('assets/Selected.png'),
                                                                    (self.tile_size, self.tile_size))
                            self.display_surface.blit(image_selected, selected_rect)
                            player.can_do = 1
                    if player.tool_type == 2:
                        try:
                            if self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[0] != '0':
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
                            if self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[
                                0] not in player.seeds_id or \
                                    self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[1] not in ['3',
                                                                                                                 '6'] or \
                                    player.animation_type != 0:
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
                            if self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[
                                0] not in player.seeds_id and \
                                    (self.map[player.using_tile[1]][player.using_tile[0]].split(' - ')[0] not in ['0',
                                                                                                                  '3']):
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
            else:
                player.can_do = 0
        else:
            player.can_do = 0

        font = pygame.font.Font('assets/font.ttf', int(self.tile_size * 0.2))

        money = font.render(f'Coins: {player.money}', True, (255, 255, 255))
        money_rect = money.get_rect()
        money_rect.topright = (self.display_surface.get_size()[0] - (self.tile_size * 0.1), (self.tile_size * 0.1))
        self.display_surface.blit(money, money_rect)

        score = font.render(f'Score: {player.score}', True, (255, 255, 255))
        score_rect = score.get_rect()
        score_rect.topright = (
            self.display_surface.get_size()[0] - (self.tile_size * 0.1),
            (self.tile_size * 0.1) + int(self.tile_size * 0.3))
        self.display_surface.blit(score, score_rect)

        format_time = time.strftime("%H:%M:%S", time.gmtime(player.timer))
        timer = font.render(f'Time: {format_time}', True, (255, 255, 255))
        timer_rect = timer.get_rect()
        timer_rect.center = (
            self.display_surface.get_size()[0] / 2,
            (self.tile_size * 0.3))
        self.display_surface.blit(timer, timer_rect)

        # MINIMUM SIZE IMPORTANT
        size = int(min(pygame.display.get_surface().get_width() / (13),
                       pygame.display.get_surface().get_height() / (8)))

        if player.can_buy:
            for i in range(9):
                if str(i + 8) in player.seed_type_can_use:
                    local_rect = self.icon_base[str(i)]['1'].get_rect()
                    local_rect.topleft = ((i + 2.5) * size, pygame.display.get_surface().get_height() - 1.3 * size)
                    self.display_surface.blit(self.icon_base[str(i)]['1'],
                                              local_rect)
                    info_text = font.render(f'{i + 1}', True, (55, 55, 55))
                    info_text_rect = timer.get_rect()
                    info_text_rect.bottomleft = (
                        (i + 2.5) * size, pygame.display.get_surface().get_height() - 0.3 * size)
                    self.display_surface.blit(info_text, info_text_rect)

                    info_text = font.render(f'{player.costs[str(i + 8)]}', True, (55, 55, 55))
                    info_text_rect = timer.get_rect()
                    info_text_rect.topright = (
                        local_rect.topleft[0], pygame.display.get_surface().get_height() - 1.2 * size)
                    self.display_surface.blit(info_text, info_text_rect.topright)
                else:
                    local_rect = self.icon_base[str(i)]['0'].get_rect()
                    local_rect.topleft = ((i + 2.5) * size, pygame.display.get_surface().get_height() - 1.3 * size)
                    self.display_surface.blit(self.icon_base[str(i)]['0'],
                                              local_rect)
                    info_text = font.render(f'{i + 1}', True, (55, 55, 55))
                    info_text_rect = timer.get_rect()
                    info_text_rect.bottomleft = (
                        (i + 2.5) * size, pygame.display.get_surface().get_height() - 0.3 * size)
                    self.display_surface.blit(info_text, info_text_rect)

                    info_text = font.render(f'{player.costs[str(i + 8)]}', True, (55, 55, 55))
                    info_text_rect = timer.get_rect()
                    info_text_rect.topright = (
                        local_rect.topleft[0], pygame.display.get_surface().get_height() - 1.2 * size)
                    self.display_surface.blit(info_text, info_text_rect.topright)

        if player.animation_type == 2:
            ready = font.render(f'Ready', True, (0, 155, 30))
            ready_rect = ready.get_rect()
            ready_rect.center = (
                self.display_surface.get_size()[0] / 2,
                (self.tile_size * 1.5))
            self.display_surface.blit(ready, ready_rect)


class Game:
    def __init__(self, w, h, ip, port, username='user'):
        self.base_id = ["S0", "S1", "S2", "S3"]
        pygame.init()
        self.width = w
        self.height = h
        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))
        self.tile_size = int(size * 32)
        # print(self.width, self.height)
        self.canvas = Canvas(self.width, self.height)
        self.all_sprites = pygame.sprite.Group()
        self.camera_group = CameraGroup()
        self.is_running = True
        try:
            self.net = Network(ip, port)
            if self.net.id == '0XE000':
                self.is_running = False
                self.game_going = 0
                # sys.exit()
                return
                # m = Menu(w, h)
                # m.run()
                # os._exit(1)
            data = username
            # print(data)
            df = self.net.send(data)
            if df == '0XE000':
                # print(1)
                self.is_running = False
                self.game_going = 0
                # sys.exit()
                return
                # m = Menu(w, h)
                # m.run()
                # os._exit(1)
        except:
            self.is_running = False
            self.game_going = 0
            # sys.exit()
            return
            # m = Menu(w, h)
            # m.run()
            # os._exit(1)

        # Take information about self
        data = self.net.send('KEY')
        if data == '0XE000':
            self.is_running = False
            self.game_going = 0
            # sys.exit()
            return
            # m = Menu(w, h)
            # m.run()
            # os._exit(1)

        self.limited_group = pygame.sprite.Group()
        self.seller_group = pygame.sprite.Group()
        self.seller_box_group = pygame.sprite.Group()

        self.local_base_id = {}
        print(data)
        try:
            self.player = Player(self.camera_group,
                                 (data['Player Position'][0] * size, data['Player Position'][1] * size),
                                 status=1, limited_group=self.limited_group, seller_group=self.seller_group,
                                 seller_box_group=self.seller_box_group, player_id=self.net.id)
        except:
            self.is_running = False
            self.game_going = 0
            return
        # self.player.id = self.net.id
        self.local_base_id[self.player.id] = self.player
        self.base_id.remove(self.net.id)
        self.base_id.sort()

        self.map = data['Package']['Map']
        self.costs = data['Package']['Costs']
        self.player.costs = data['Package']['Costs']
        self.player.timer = data['Package']['Time']
        self.game_going = data['Package']['Game Status']

        # Game already going - DISCONNECT
        if self.game_going:
            self.is_running = False
            self.game_going = 0
            print('Game already going')
            # sys.exit()
            return
            # m = Menu(w, h)
            # m.run()
            # os._exit(1)

        pos_seller = []
        pos_seller_box = []

        self.player2 = Player(self.camera_group, (100, 100), status=0, limited_group=self.limited_group,
                              seller_group=self.seller_group, seller_box_group=self.seller_box_group,
                              player_id=self.base_id[0])
        # self.player2.id = self.base_id[0]
        self.local_base_id[self.player2.id] = self.player2
        self.player3 = Player(self.camera_group, (100, 100), status=0, limited_group=self.limited_group,
                              seller_group=self.seller_group, seller_box_group=self.seller_box_group,
                              player_id=self.base_id[1])
        # self.player3.id = self.base_id[1]
        self.local_base_id[self.player3.id] = self.player3
        self.player4 = Player(self.camera_group, (100, 100), status=0, limited_group=self.limited_group,
                              seller_group=self.seller_group, seller_box_group=self.seller_box_group,
                              player_id=self.base_id[2])
        # self.player4.id = self.base_id[2]
        self.local_base_id[self.player4.id] = self.player4

        counter = -1
        print(self.local_base_id)
        # os._exit(1)
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                tile = self.map[y][x]
                id_tile, id_state = map(str, tile.split(' - '))
                if id_tile == '4':
                    counter += 1
                    print(f'S{counter}', self.player.id)
                    # os._exit(1)
                    if f'S{counter}' == self.player.id:
                        self.player.rect.x = x * self.tile_size
                        self.player.rect.y = y * self.tile_size
                    # elif f'S{counter}' == self.player2.id:
                    #     self.player2.rect.x = x * self.tile_size
                    #     self.player2.rect.y = y * self.tile_size
                    # elif f'S{counter}' == self.player3.id:
                    #     self.player3.rect.x = x * self.tile_size
                    #     self.player3.rect.y = y * self.tile_size
                    # elif f'S{counter}' == self.player4.id:
                    #     self.player4.rect.x = x * self.tile_size
                    #     self.player4.rect.y = y * self.tile_size
                if id_tile == '5':
                    pos_seller = [x, y]
                    continue
                if id_tile == '6':
                    pos_seller_box = [x, y]
                    continue

        self.seller = Seller(self.seller_group, self.tile_size, pos_seller)
        self.seller_box = Seller_Bought(self.seller_box_group, self.tile_size, pos_seller_box)

        self.player.money = data['Package']['Money']
        self.player.seed_type_can_use = data['Package']['Available Items']['Seeds']

        self.camera_group.map = self.map

        self.bd1 = Border(-self.tile_size, -self.tile_size * 2, (len(self.map[0]) + 1) * self.tile_size,
                          -self.tile_size * 0.25, self.camera_group, self.limited_group)
        self.bd2 = Border(-self.tile_size, (len(self.map) + 0.25) * self.tile_size,
                          (len(self.map[0]) + 1) * self.tile_size, (len(self.map) + 2) * self.tile_size,
                          self.camera_group, self.limited_group)
        self.bd3 = Border(-self.tile_size * 2, -self.tile_size, (-self.tile_size * 0.25),
                          ((len(self.map) + 1) * self.tile_size),
                          self.camera_group, self.limited_group)
        self.bd4 = Border((len(self.map[0]) + 0.25) * self.tile_size, -self.tile_size,
                          (len(self.map[0]) + 2) * self.tile_size,
                          ((len(self.map) + 1) * self.tile_size),
                          self.camera_group, self.limited_group)

        self.package = {'World change': []}

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
        # print(self.is_running)
        while not self.game_going and self.is_running:
            clock.tick(20)
            self.package = {'World change': []}
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        os._exit(1)
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        self.game_going = 0
                        # sys.exit()
                        return
                        # m = Menu(self.canvas.width, self.canvas.height)
                        # m.run()
                        # os._exit(1)
                if event.type == pygame.QUIT:
                    self.is_running = False
                    self.game_going = 0
                    print('EXIT')
                    os._exit(1)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                if self.player.animation_type:
                    self.player.animation_type = 0
                else:
                    self.player.animation_type = 2

            try:
                data = self.send_data()
            except:
                self.is_running = False
                self.game_going = False
                return

            self.game_going = data[self.net.id]['Package']['Game Status']

            try:
                for key in data.keys():
                    if key == self.base_id[0]:
                        self.player2.rect.x, self.player2.rect.y, self.player2.status, self.player2.animation_type, \
                        self.player2.using = self.parse_data(data[key])
                    if key == self.base_id[1]:
                        self.player3.rect.x, self.player3.rect.y, self.player3.status, self.player3.animation_type, \
                        self.player3.using = self.parse_data(data[key])
                    if key == self.base_id[2]:
                        self.player4.rect.x, self.player4.rect.y, self.player4.status, self.player4.animation_type, \
                        self.player4.using = self.parse_data(data[key])
            except:
                self.is_running = False
                self.game_going = False
                return

            self.player2.change_view()
            self.player3.change_view()
            self.player4.change_view()

            self.canvas.draw_background()
            self.camera_group.update()
            self.camera_group.custom_draw(self.player, self.seller, self.seller_box)
            self.canvas.update()

        if self.is_running:
            self.player.animation_type = 0

        while self.is_running:
            clock.tick(60)
            self.package = {'World change': []}
            if (self.player.animation_type in range(38, 47) or self.player.animation_type in range(18,
                                                                                                   27)) and using == 1:
                self.player.animation_type = 0
                using = 0
            elif (self.player.animation_type in range(38, 47) or self.player.animation_type in range(18,
                                                                                                     27)) and using == 0:
                using = 1
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        os._exit(1)
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        self.game_going = 0
                        return
                        # m = Menu(self.canvas.width, self.canvas.height)
                        # m.run()
                        # os._exit(1)
                if event.type == pygame.QUIT:
                    self.is_running = False
                    self.game_going = 0
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

            if keys[pygame.K_r]:
                if not self.player.using:
                    self.player.using = 10
                    self.player.changer = (self.player.changer + 1) % 2

            if keys[pygame.K_e]:
                if not self.player.using:
                    self.player.using = 10
                    if not self.player.changer:
                        self.player.tool_type = (self.player.tool_type + 1) % 5
                    else:
                        self.player.seed_type_selected = (self.player.seed_type_selected + 1) % len(
                            self.player.seed_type_can_use)

            if keys[pygame.K_q]:
                if not self.player.using:
                    self.player.using = 10
                    if not self.player.changer:
                        self.player.tool_type = (self.player.tool_type - 1) % 5
                    else:
                        self.player.seed_type_selected = (self.player.seed_type_selected - 1) % len(
                            self.player.seed_type_can_use)

            if not self.player.changer:
                if keys[pygame.K_f]:
                    if not self.player.using:
                        # os._exit(1)
                        if self.player.using_tile != (
                                -100000, -100000) and self.player.tool_type == 1 and self.player.can_do:
                            # os._exit(1)
                            if 0 <= self.player.using_tile[1] < len(self.map) and 0 <= self.player.using_tile[0] < len(
                                    self.map[0]):
                                tile = self.map[self.player.using_tile[1]][self.player.using_tile[0]]
                                tile_id, tile_state = tile.split(' - ')
                                if tile_id == '1':
                                    tile_id = 0
                                else:
                                    tile_id = 1
                                tile_state = 0
                                new_tile = f"{tile_id} - {tile_state}"
                                self.package['World change'] = [self.player.using_tile, new_tile]
                                # print(new_tile, tile)
                                self.map[self.player.using_tile[1]][self.player.using_tile[0]] = new_tile
                            self.player.using = 15
                        if self.player.tool_type == 2:
                            if self.player.can_do == 1:
                                if 0 <= self.player.using_tile[1] < len(self.map) and 0 <= self.player.using_tile[0] \
                                        < len(self.map[0]):
                                    tile = self.map[self.player.using_tile[1]][self.player.using_tile[0]]
                                    tile_id, tile_state = tile.split(' - ')
                                    tile_id = self.player.seed_type_can_use[self.player.seed_type_selected]
                                    if tile_state == '7':
                                        tile_state = '4'
                                    if tile_state == '0':
                                        tile_state = '1'
                                    new_tile = f"{tile_id} - {tile_state}"
                                    self.package['World change'] = [self.player.using_tile, new_tile]
                                    # print(new_tile, tile)
                                    self.map[self.player.using_tile[1]][self.player.using_tile[0]] = new_tile
                            self.player.using = 15
                        if self.player.tool_type == 3:
                            if self.player.can_do == 1:
                                if 0 <= self.player.using_tile[1] < len(self.map) and 0 <= self.player.using_tile[0] \
                                        < len(self.map[0]):
                                    tile = self.map[self.player.using_tile[1]][self.player.using_tile[0]]
                                    tile_id, tile_state = tile.split(' - ')
                                    if tile_state == '6':
                                        tile_state = '7'
                                    if tile_state == '3':
                                        tile_state = '0'
                                    self.player.animation_type = int(tile_id)
                                    tile_id = '0'
                                    new_tile = f"{tile_id} - {tile_state}"
                                    self.package['World change'] = [self.player.using_tile, new_tile]
                                    # print(new_tile, tile)
                                    self.map[self.player.using_tile[1]][self.player.using_tile[0]] = new_tile
                            self.player.using = 15
                        if self.player.tool_type == 4:
                            if self.player.can_do == 1:
                                if 0 <= self.player.using_tile[1] < len(self.map) and 0 <= self.player.using_tile[0] \
                                        < len(self.map[0]):
                                    tile = self.map[self.player.using_tile[1]][self.player.using_tile[0]]
                                    tile_id, tile_state = tile.split(' - ')
                                    if tile_id == '3':
                                        self.player.bucket_status = 1
                                    else:
                                        if self.player.bucket_status == 1:
                                            if tile_state == '0':
                                                tile_state = '7'
                                            if tile_state == '1':
                                                tile_state = '4'
                                            if tile_state == '2':
                                                tile_state = '5'
                                            if tile_state == '3':
                                                tile_state = '6'
                                            self.player.bucket_status = 0
                                    # tile_state = '1'
                                    new_tile = f"{tile_id} - {tile_state}"
                                    self.package['World change'] = [self.player.using_tile, new_tile]
                                    # print(new_tile, tile)
                                    self.map[self.player.using_tile[1]][self.player.using_tile[0]] = new_tile
                            self.player.using = 15

            # print(self.player.animation_type)
            if self.player.can_buy and self.player.animation_type == 0:
                if keys[pygame.K_2] and self.costs['9'] <= self.player.money \
                        and '9' not in self.player.seed_type_can_use:
                    self.player.animation_type = 19
                elif keys[pygame.K_3] and self.costs['10'] <= self.player.money \
                        and '10' not in self.player.seed_type_can_use:
                    self.player.animation_type = 20
                elif keys[pygame.K_4] and self.costs['11'] <= self.player.money \
                        and '11' not in self.player.seed_type_can_use:
                    self.player.animation_type = 21
                elif keys[pygame.K_5] and self.costs['12'] <= self.player.money \
                        and '12' not in self.player.seed_type_can_use:
                    self.player.animation_type = 22
                elif keys[pygame.K_6] and self.costs['13'] <= self.player.money \
                        and '13' not in self.player.seed_type_can_use:
                    self.player.animation_type = 23
                elif keys[pygame.K_7] and self.costs['14'] <= self.player.money \
                        and '14' not in self.player.seed_type_can_use:
                    self.player.animation_type = 24
                elif keys[pygame.K_8] and self.costs['15'] <= self.player.money \
                        and '15' not in self.player.seed_type_can_use:
                    self.player.animation_type = 25
                elif keys[pygame.K_9] and self.costs['16'] <= self.player.money \
                        and '16' not in self.player.seed_type_can_use:
                    self.player.animation_type = 26

            self.player.activating()
            self.player.change_view()

            if self.player.rect.x < -self.tile_size or self.player.rect.y < -self.tile_size or self.player.rect.x > (
                    len(self.map[0]) + 1) * self.tile_size or self.player.rect.y > (len(self.map) + 1) * self.tile_size:
                self.player.rect.x = self.tile_size
                self.player.rect.y = self.tile_size

            # Send Network Stuff
            # self.player2.rect.x, self.player2.rect.y, self.player2.is_active = self.parse_data()

            # Players synh
            try:
                data = self.send_data()
            except:
                self.is_running = False
                self.game_going = False
                return
            # print(self.package)
            try:
                for key in data.keys():
                    if key == self.base_id[0]:
                        self.player2.rect.x, self.player2.rect.y, self.player2.status, self.player2.animation_type, \
                        self.player2.using = self.parse_data(data[key])
                    if key == self.base_id[1]:
                        self.player3.rect.x, self.player3.rect.y, self.player3.status, self.player3.animation_type, \
                        self.player3.using = self.parse_data(data[key])
                    if key == self.base_id[2]:
                        self.player4.rect.x, self.player4.rect.y, self.player4.status, self.player4.animation_type, \
                        self.player4.using = self.parse_data(data[key])
                    if key == self.net.id:
                        for key_package in data[key]['Package'].keys():
                            if key_package == 'World change':
                                for i in range(0, len(data[key]['Package']['World change']), 2):
                                    x, y = data[key]['Package']['World change'][i][0], \
                                           data[key]['Package']['World change'][i][1]
                                    self.map[y][x] = data[key]['Package']['World change'][i + 1]
                            elif key_package == 'Money':
                                self.player.money = data[key]['Package']['Money']
                            elif key_package == 'Available Items':
                                self.player.seed_type_can_use = data[key]['Package']['Available Items']['Seeds']
                            elif key_package == 'Time':
                                self.player.timer = int(data[key]['Package']['Time'])
                            elif key_package == 'Map':
                                self.player.map = data[key]['Package']['Map'].copy()
                                self.map = data[key]['Package']['Map'].copy()
                                self.camera_group.map = data[key]['Package']['Map'].copy()
                            elif key_package == 'Score':
                                self.player.score = int(data[key]['Package']['Score'])
                                # print(data[key]['Package']['Map'])
            except:
                self.is_running = False
                self.game_going = False
                return

            self.player2.change_view()
            self.player3.change_view()
            self.player4.change_view()

            # Update Canvas
            self.canvas.draw_background()
            self.camera_group.update()
            self.camera_group.custom_draw(self.player, self.seller, self.seller_box)
            self.canvas.update()

        # pygame.quit()

    def send_data(self):
        size = max(pygame.display.get_surface().get_width() / (13 * 32),
                   pygame.display.get_surface().get_height() / (8 * 32))
        data = {'ID': self.net.id, 'Player Position': (self.player.rect.x / size, self.player.rect.y / size),
                'Player Status': self.player.status, 'Player Animation Type': self.player.animation_type,
                'Player Using State': self.player.using, 'Package': self.package}
        # print(data)
        # data = str(self.net.id) + ":" + str(self.player.rect.x) + "," + str(self.player.rect.y) + ',1'
        # print(data)
        reply = self.net.send(data)
        # tmp_2 = open('DEBUG.txt', 'r')
        # ttt = tmp_2.readlines()
        # tmp_2.close()
        # tmp_1 = open('DEBUG.txt', 'w')
        # tmp_3 = ttt + [str(reply)]
        # tmp_1.writelines(tmp_3)
        # tmp_1.close()
        # print(reply, "GET_DATA_GAME")
        if reply == '0XE000':
            self.is_running = False
            self.game_going = False
            # sys.exit()
            return
            # m = Menu(self.canvas.width, self.canvas.height)
            # m.run()
            # sys.exit()
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
        # print(self.width, self.height)

    @staticmethod
    def update():
        pygame.display.update()

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill('#7D8CC4')
