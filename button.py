import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, group, image, pos, text_input, font, base_color, hovering_color):
        super().__init__(group)
        size = max(int(pygame.display.get_surface().get_width() / (13 * 32)),
                   int(pygame.display.get_surface().get_height() / (8 * 32)))
        self.image = pygame.transform.scale(image, (400 * size, 100 * size)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = pygame.display.get_surface().get_width() / 2
        self.rect.centery = pygame.display.get_surface().get_height() / 2
        # self.x_pos, self.y_pos = pos
        # self.font = font
        # self.base_color, self.hovering_color = base_color, hovering_color
        # self.text_input = text_input
        # self.text = self.font.render(self.text_input, True, self.base_color)
        # if self.image is None:
        #     self.image = self.text
        # self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        # self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        # screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    # def change_color(self, position):
    #     if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
    #                                                                                       self.rect.bottom):
    #         # self.text = self.font.render(self.text_input, True, self.hovering_color)
    #     else:
    #         # self.text = self.font.render(self.text_input, True, self.base_color)
