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

        self.buttons_base = {'menu': [(self.rect.topleft[0],self.rect.topleft[1]), ()}

    def

    def update(self, screen):
        screen.blit(self.image, self.rect)
