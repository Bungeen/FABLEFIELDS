import pygame
import sys


class Connect_Widget(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.size = max(pygame.display.get_surface().get_width() / (2 * 600),
                        pygame.display.get_surface().get_height() / (2 * 500))
        self.image = pygame.transform.scale(image, (300 * self.size, 400 * self.size)).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.centerx = pygame.display.get_surface().get_width() // 2
        self.rect.centery = pygame.display.get_surface().get_height() // 2

        self.buttons_base_keys = ['title_Name', 'Name', 'title_RoomID', 'RoomID', 'title_RoomPass', 'RoomPass', 'continue', 'cancel']
        self.buttons_base = {'title_Name': [(self.rect.topleft[0], self.rect.topleft[1]), (
            self.rect.topleft[0] + self.image.get_size()[0], self.rect.topleft[1] + 40 * self.size)],
                             'Name': [(self.rect.topleft[0], self.rect.topleft[1] + 40 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 120 * self.size)],
                             'title_RoomID': [(self.rect.topleft[0], self.rect.topleft[1] + 120 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 160 * self.size)],
                             'RoomID': [(self.rect.topleft[0], self.rect.topleft[1] + 160 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 240 * self.size)],
                             'title_RoomPass': [(self.rect.topleft[0], self.rect.topleft[1] + 240 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 280 * self.size)],
                             'RoomPass': [(self.rect.topleft[0], self.rect.topleft[1] + 280 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 360 * self.size)],
                             'continue': [(self.rect.topleft[0], self.rect.topleft[1] + 360 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0] // 2,
                                 self.rect.topleft[1] + 400 * self.size)],
                             'cancel': [(self.rect.topleft[0] + self.image.get_size()[0] // 2,
                                         self.rect.topleft[1] + 360 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 400 * self.size)]}

    def reet(self, name):
        tmp = None
        if name == 'title_Name':
            tmp = pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1],
                                   self.image.get_size()[0],
                                   40 * self.size)
        elif name == 'Name':
            tmp = pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] + 40 * self.size,
                                   self.image.get_size()[0],
                                   80 * self.size)
        elif name == 'title_RoomID':
            tmp = pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] + 120 * self.size,
                                   self.image.get_size()[0],
                                   40 * self.size)
        elif name == 'RoomID':
            tmp = pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] + 160 * self.size,
                                   self.image.get_size()[0],
                                   80 * self.size)
        elif name == 'title_RoomPass':
            tmp = pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] + 240 * self.size,
                                   self.image.get_size()[0],
                                   40 * self.size)
        elif name == 'RoomPass':
            tmp = pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] + 280 * self.size,
                                   self.image.get_size()[0],
                                   80 * self.size)
        elif name == 'continue':
            tmp = pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] + 360 * self.size,
                                   self.image.get_size()[0] // 2,
                                   40 * self.size)
        elif name == 'cancel':
            tmp = pygame.rect.Rect(self.rect.centerx, self.rect.topleft[1] + 360 * self.size,
                                   self.image.get_size()[0] // 2,
                                   40 * self.size)
        return tmp.center

    def checking_button(self, mouse_position=None):
        if mouse_position is None:
            return None
        for key in self.buttons_base_keys:
            top_left = self.buttons_base[key][0]
            down_right = self.buttons_base[key][1]
            if top_left[0] <= mouse_position[0] <= down_right[0] and top_left[1] <= mouse_position[1] <= down_right[1]:
                print(key)
                return key
        return None

    def font_size(self):
        return pygame.display.get_surface().get_height() / 90 / 19

    def sc_size(self):
        return pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()

    def update(self, screen):
        screen.blit(self.image, self.rect)


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
group = pygame.sprite.Group()
image = pygame.image.load('connection_test2.0.png')
a = Connect_Widget(group, image)
font = pygame.font.Font(None, int(a.font_size() * 100))
font1 = pygame.font.Font(None, int(a.font_size() * 110))
is_running = True
text_Name = ''
text_RoomID = ''
text_RoomPass = ''
title_Name_txt = 'Your NickName'
title_RoomId_txt = 'Room ID'
title_RoomPass_txt = 'Room Password'
continue_text = 'Continue'
cancel_text = 'Cancel'
ft1 = False
ft2 = False
ft3 = False

while is_running:
    time_delta = clock.tick(60) / 1000.0
    group = pygame.sprite.Group()
    image = pygame.image.load('connection_test2.0.png')
    a = Connect_Widget(group, image)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if ft1:
                if event.key == pygame.K_BACKSPACE:
                    text_Name = text_Name[:-1]
                else:
                    if len(text_Name) < 15:
                        text_Name += event.unicode
            if ft2:
                if event.key == pygame.K_BACKSPACE:
                    text_RoomID = text_RoomID[:-1]
                else:
                    if len(text_RoomID) < 15:
                        text_RoomID += event.unicode
            if ft3:
                if event.key == pygame.K_BACKSPACE:
                    text_RoomPass = text_RoomPass[:-1]
                else:
                    if len(text_RoomPass) < 15:
                        text_RoomPass += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if a.checking_button(event.pos) == 'Name':
                ft1 = True
                ft2 = False
                ft3 = False
            elif a.checking_button(event.pos) == 'RoomID':
                ft1 = False
                ft2 = True
                ft3 = False
            elif a.checking_button(event.pos) == 'RoomPass':
                ft1 = False
                ft2 = False
                ft3 = True
            else:
                continue

    screen.fill((0, 0, 0))
    clock.tick(60)
    group.update(screen)
    Name_txt_surface = font.render(text_Name, True, (255, 255, 255))
    text_rect_Name = Name_txt_surface.get_rect(center=a.reet('Name'))
    screen.blit(Name_txt_surface, text_rect_Name)
    RoomID_txt_surface = font.render(text_RoomID, True, (255, 255, 255))
    text_rect_RoomID = RoomID_txt_surface.get_rect(center=a.reet("RoomID"))
    screen.blit(RoomID_txt_surface, text_rect_RoomID)
    RoomPass_txt_surface = font.render(text_RoomPass, True, (255, 255, 255))
    text_rect_RoomPass = RoomPass_txt_surface.get_rect(center=a.reet('RoomPass'))
    screen.blit(RoomPass_txt_surface, text_rect_RoomPass)
    Namet_txt_surface = font1.render(title_Name_txt, True, (255, 255, 255))
    text_rect_Namet = Namet_txt_surface.get_rect(center=a.reet('title_Name'))
    screen.blit(Namet_txt_surface, text_rect_Namet)
    RoomIDt_txt_surface = font1.render(title_RoomId_txt, True, (255, 255, 255))
    text_rect_RoomIDt = RoomIDt_txt_surface.get_rect(center=a.reet("title_RoomID"))
    screen.blit(RoomIDt_txt_surface, text_rect_RoomIDt)
    RoomPasst_txt_surface = font1.render(title_RoomPass_txt, True, (255, 255, 255))
    text_rect_RoomPasst = RoomPasst_txt_surface.get_rect(center=a.reet('title_RoomPass'))
    screen.blit(RoomPasst_txt_surface, text_rect_RoomPasst)
    continue_txt_surface = font1.render(continue_text, True, (255, 255, 255))
    text_rect_continue = continue_txt_surface.get_rect(center=a.reet('continue'))
    screen.blit(continue_txt_surface, text_rect_continue)
    cancel_txt_surface = font1.render(cancel_text, True, (255, 255, 255))
    text_rect_cancel = cancel_txt_surface.get_rect(center=a.reet('cancel'))
    screen.blit(cancel_txt_surface, text_rect_cancel)
    pygame.display.update()

