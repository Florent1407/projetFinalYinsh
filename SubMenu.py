import pygame
import os
import Board
from Game import Game

class SubMenu:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.background_image = pygame.image.load(os.path.join("images", "fondmode.jpg"))
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.font = pygame.font.Font(None, 36)

    def draw_text(self, text, color, x, y):
        text_obj = self.font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, width, height, background_color, border_color, action=None, radius=0):
        from vsOrdi import GameVsComputer
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, background_color, button_surface.get_rect(), border_radius=radius)

        button_rect = button_surface.get_rect(topleft=(x, y))
        self.window.blit(button_surface, button_rect)

        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.window, border_color, button_rect, 3, border_radius=radius)
            if click[0] == 1 and action is not None:
                if action == "local":
                    game_instance = Game()
                    game_instance.run()

                elif action == "local_ordi":
                    game_instance = GameVsComputer()
                    game_instance.run()

        self.draw_text(text, (0, 0, 0), x + width / 2, y + height / 2)

    def draw_return_button(self, x, y, width, height, background_color, border_color, action=None, radius=0):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, background_color, button_surface.get_rect(), border_radius=radius)

        button_rect = button_surface.get_rect(topleft=(x, y))
        self.window.blit(button_surface, button_rect)

        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.window, border_color, button_rect, 3, border_radius=radius)
            if click[0] == 1 and action is not None:
                if action == "retour":
                    return True

        self.draw_text("Retour", (0, 0, 0), x + width / 2, y + height / 2)

    def draw(self):
        self.window.blit(self.background_image, (0, 0))
        self.draw_text("Choisissez votre mode de jeu", (255, 255, 255), self.width // 2, 100)
        self.draw_button("1 vs 1 local", 100, 550, 300, 50, (255, 255, 255, 128), (0, 0, 0), action="local", radius=10)
        self.draw_button("1 vs 1 local Blitz", 100, 620, 300, 50, (255, 255, 255, 128), (0, 0, 0), action="local_blitz", radius=10)
        self.draw_button("Contre l'ordinateur", 700, 550, 300, 50, (255, 255, 255, 128), (0, 0, 0), action="local_ordi", radius=10)
        self.draw_button("Contre l'ordinateur Blitz", 700, 620, 300, 50, (255, 255, 255, 128), (0, 0, 0), action="ordinateur_blitz", radius=10)
        if self.draw_return_button(50, 50, 150, 50, (255, 255, 255, 128), (0, 0, 0), action="retour", radius=10):
            return True
        return False
