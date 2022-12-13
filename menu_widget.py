import pygame


class Menu_Widget(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.size = max(pygame.display.get_surface().get_width() / (7 * 300),
                        pygame.display.get_surface().get_height() / (3 * 400))
        self.image = pygame.transform.scale(image, (300 * self.size, 400 * self.size)).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.centerx = pygame.display.get_surface().get_width() // 2
        self.rect.centery = pygame.display.get_surface().get_height() // 2

        self.buttons_base_keys = ['menu', 'tutorial', 'singleplayer', 'multiplayer', 'settings', 'exit']
        self.buttons_base = {'menu': [(self.rect.topleft[0], self.rect.topleft[1]), (
            self.rect.topleft[0] + self.image.get_size()[0], self.rect.topleft[1] + 100 * self.size)],
                             'tutorial': [(self.rect.topleft[0], self.rect.topleft[1] + 100 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 160 * self.size)],
                             'singleplayer': [(self.rect.topleft[0], self.rect.topleft[1] + 160 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 220 * self.size)],
                             'multiplayer': [(self.rect.topleft[0], self.rect.topleft[1] + 220 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 280 * self.size)],
                             'settings': [(self.rect.topleft[0], self.rect.topleft[1] + 280 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 340 * self.size)],
                             'exit': [(self.rect.topleft[0], self.rect.topleft[1] + 340 * self.size), (
                                 self.rect.topleft[0] + self.image.get_size()[0],
                                 self.rect.topleft[1] + 400 * self.size)]}

    def checking_button(self, mouse_position=None):
        if mouse_position is None:
            return None
        for key in self.buttons_base_keys:
            top_left = self.buttons_base[key][0]
            down_right = self.buttons_base[key][1]
            if top_left[0] <= mouse_position[0] <= down_right[0] and top_left[1] <= mouse_position[1] <= down_right[1]:
                return key
        return None

    def update(self, screen):
        screen.blit(self.image, self.rect)
