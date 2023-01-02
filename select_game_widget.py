import pygame


class Select_Game_Widget(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.size = max(pygame.display.get_surface().get_width() / (2 * 900),
                        pygame.display.get_surface().get_height() / (10.8 * 100))
        self.image = pygame.transform.scale(image, (900 * self.size, 100 * self.size)).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.centerx = pygame.display.get_surface().get_width() // 2
        self.rect.centery = pygame.display.get_surface().get_height() // 2

        self.buttons_base_keys = ['create', 'connect', 'back']
        self.buttons_base = {'create': [(self.rect.topleft[0], self.rect.topleft[1]), (
            self.rect.topleft[0] + self.image.get_size()[0] / 3, self.rect.bottomleft[1])],
                             'connect': [(self.rect.topleft[0] + self.image.get_size()[0] / 3, self.rect.topleft[1]),
                                         (self.rect.topleft[0] + self.image.get_size()[0] / 3 * 2,
                                          self.rect.bottomleft[1])],
                             'back': [(self.rect.topleft[0] + self.image.get_size()[0] / 3 * 2, self.rect.topleft[1]),
                                         (self.rect.topleft[0] + self.image.get_size()[0],
                                          self.rect.bottomleft[1])]}

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
