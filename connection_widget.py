import pygame


class Connection_Widget(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.size = max(pygame.display.get_surface().get_width() / (3 * 600),
                        pygame.display.get_surface().get_height() / (1.5 * 700))
        self.image = pygame.transform.scale(image, (600 * self.size, 700 * self.size)).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.centerx = pygame.display.get_surface().get_width() // 2
        self.rect.centery = pygame.display.get_surface().get_height() // 2

        self.buttons_base_keys = ['Username_Input', 'IP_Input', 'Port_Input', 'Cancel', 'Connect']
        self.buttons_base = {'Username_Input': [(self.rect.topleft[0], self.rect.topleft[1] + 100 * self.size), (
            self.rect.topleft[0] + self.image.get_size()[0],
            self.rect.topleft[1] + 200 * self.size)],
                             'IP_Input': [(self.rect.topleft[0], self.rect.topleft[1] + 300 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 400 * self.size)],
                             'Port_Input': [(self.rect.topleft[0], self.rect.topleft[1] + 500 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 600 * self.size)],
                             'Cancel': [(self.rect.topleft[0], self.rect.topleft[1] + 600 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0] / 2,
                                 self.rect.topleft[1] + 700 * self.size)],
                             'Connect': [(self.rect.topleft[0] + self.image.get_size()[0] / 2,
                                          self.rect.topleft[1] + 600 * self.size), (
                                             self.rect.topleft[0] + self.image.get_size()[0],
                                             self.rect.topleft[1] + 700 * self.size)]
                             }

    def get_center(self, key):
        if key not in ['Username_Input', 'IP_Input', 'Port_Input']:
            return None
        tmp_rect = pygame.rect.Rect(self.buttons_base[key][0][0], self.buttons_base[key][0][1],
                                    abs(self.buttons_base[key][0][0] - self.buttons_base[key][1][0]),
                                    abs(self.buttons_base[key][0][1] - self.buttons_base[key][1][1]))
        return tmp_rect.center

    def checking_button(self, mouse_position=None):
        if mouse_position is None:
            return None
        for key in self.buttons_base_keys:
            top_left = self.buttons_base[key][0]
            down_right = self.buttons_base[key][1]
            if top_left[0] <= mouse_position[0] <= down_right[0] and top_left[1] <= mouse_position[1] <= down_right[1]:
                return key
            print(mouse_position, top_left, down_right, key)
        return None

    def update(self, screen):
        screen.blit(self.image, self.rect)
