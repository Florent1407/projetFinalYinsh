import pygame
import pygame.mixer
import sys
import os
from options import Options
from SubMenuBlitz import SubMenuBlitz  

class Menu:
    def __init__(self, window, width, height):
        from NetworkMenu import NetworkMenu
        from SubMenu import SubMenu
        self.window = window
        self.width = width
        self.height = height
        self.background_image = pygame.image.load(os.path.join("images", "fondmenu.jpg"))
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.font = pygame.font.Font(None, 36) 
        self.submenu = SubMenu(window, width, height)
        self.network_menu = NetworkMenu(window, width, height)
        self.submenublitz = SubMenuBlitz(window, width, height)  
        self.show_submenu = False
        self.show_network_menu = False
        self.show_submenublitz = False
        self.options = Options(window, width, height)
        self.show_options = False
        pygame.mixer.init()
        self.menu_music = pygame.mixer.music.load('musiques/musique1.mp3')

    def play_menu_music(self):
        pygame.mixer.music.play(-1)

    def draw_text(self, text, color, x, y):
        text_obj = self.font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, width, height, background_color, border_color, action=None, radius=0):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, background_color, button_surface.get_rect(), border_radius=radius)

        button_rect = button_surface.get_rect(topleft=(x, y))
        self.window.blit(button_surface, button_rect)

        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.window, border_color, button_rect, 3, border_radius=radius)
            if click[0] == 1 and action is not None:
                if action == "normal" and not self.show_submenu:
                    self.show_submenu = True
                elif action == "blitz":
                    self.show_submenublitz = True  
                    self.show_submenu = False
                    self.show_options = False
                elif action == "reseau":
                    self.show_network_menu = True
                    self.show_submenu = False
                    self.show_options = False
                elif action == "options":
                    self.show_options = True
                elif action == "quitter":
                    pygame.quit()
                    sys.exit()

        self.draw_text(text, (0, 0, 0), x + width / 2, y + height / 2)

    def run(self):
        button_width = 200  
        button_height = 50  
        button_padding = 10  
        button_margin_top = 100 
        title_margin_bottom = 250 
        title_text = "YINSH"
        title_color = (255, 255, 255)
        title_size = 100
        title_font = pygame.font.Font(None, title_size)

        title_x = self.width // 2
        title_y = title_margin_bottom + title_size // 2

        button_total_width = button_width * 5 + button_padding * 4

        button_x = (self.width - button_total_width) // 2

        button_y = title_y + title_margin_bottom + button_margin_top - 80

        self.play_menu_music()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.window.blit(self.background_image, (0, 0))

            if self.show_submenu:
                if self.submenu.draw():
                    self.show_submenu = False
                pygame.display.update()
                continue
            
            if self.show_network_menu:
                if self.network_menu.draw():  
                    self.show_network_menu = False
                pygame.display.update()
                continue

            if self.show_submenublitz:
                if self.submenublitz.draw():  
                    self.show_submenublitz = False
                pygame.display.update()
                continue

            if self.show_options:
                if self.options.draw():  
                    self.show_options = False
                pygame.display.update()
                continue

            title_text_obj = title_font.render(title_text, True, title_color)
            title_text_rect = title_text_obj.get_rect()
            title_text_rect.center = (title_x, title_y)
            self.window.blit(title_text_obj, title_text_rect)

            self.draw_button("Normal", button_x, button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="normal", radius=10)
            self.draw_button("Blitz", button_x + button_width + button_padding, button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="blitz", radius=10)
            self.draw_button("Jeu en réseau", button_x + 2 * (button_width + button_padding), button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="reseau", radius=10)
            self.draw_button("Options", button_x + 3 * (button_width + button_padding), button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="options", radius=10)
            self.draw_button("Quitter le jeu", button_x + 4 * (button_width + button_padding), button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="quitter", radius=10)
            pygame.display.update()


pygame.init()

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Menu de jeu")

menu = Menu(window, WINDOW_WIDTH, WINDOW_HEIGHT)
menu.run()
