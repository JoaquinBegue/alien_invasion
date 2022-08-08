import pygame.font

class Button():
    def __init__(self, screen, image_path, text, size, bw=int):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Set button rect.
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        # Set button text
        if bw == 1:
            self.text_color = (0, 0, 0)
        else:
            self.text_color = (255, 255, 255)
        
        self.font = pygame.font.Font("fonts/back-to-1982.regular.ttf", size)
        self.msg_image = self.font.render(text, True, self.text_color, (255, 41, 41))
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        print(self.msg_image_rect.width)

        
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)