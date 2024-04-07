import pygame
import sys
import os
import plateau

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
                    jeu_instance = plateau.Jeu()
                    jeu_instance.demarrer()

                elif action == "ordinateur":
                    print("Jouer contre l'ordinateur")

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
    
import pygame.mixer

class Option:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.background_image = pygame.image.load(os.path.join("images", "fondmenu.jpg"))
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.volume_slider = VolumeSlider(window, width, height)
        self.show_options = False
        self.bold_font = pygame.font.Font(None, 48)

    def draw_text(self, text, color, x, y, font=None):
        if font is None:
            text_obj = self.font.render(text, True, color)
        else:
            text_obj = font.render(text, True, color)
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
                if action == "options":
                    self.show_options = True

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
        if self.show_options:
            self.draw_text("Options", (255, 255, 255), self.width // 2, 80, font=self.bold_font)

            volume_text_x = self.volume_slider.slider_x + self.volume_slider.slider_width // 2
            volume_text_y = self.volume_slider.slider_y - 20
            self.draw_text("Volume Musiques", (255, 255, 255), volume_text_x, volume_text_y)

            self.volume_slider.draw()
            if self.draw_return_button(50, 50, 150, 50, (255, 255, 255, 128), (0, 0, 0), action="retour", radius=10):
                self.show_options = False
                return True
        return False


class VolumeSlider:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.slider_width = 300
        self.slider_height = 30
        self.slider_x = (width - self.slider_width) // 2
        self.slider_y = height // 2
        self.slider_color = (255, 255, 255, 128)
        self.slider_border_color = (0, 0, 0)
        self.slider_radius = 10
        self.knob_radius = 15
        self.knob_color = (0, 0, 0)
        self.knob_border_color = (255, 255, 255)
        self.knob_x = self.slider_x + self.slider_width // 2
        self.knob_y = self.slider_y + self.slider_height // 2
        self.volume = pygame.mixer.music.get_volume()

    def draw(self):
        pygame.draw.rect(self.window, self.slider_color, (self.slider_x, self.slider_y, self.slider_width, self.slider_height), border_radius=self.slider_radius)
        pygame.draw.rect(self.window, self.slider_border_color, (self.slider_x, self.slider_y, self.slider_width, self.slider_height), 3, border_radius=self.slider_radius)
        pygame.draw.circle(self.window, self.knob_color, (self.knob_x, self.knob_y), self.knob_radius)
        pygame.draw.circle(self.window, self.knob_border_color, (self.knob_x, self.knob_y), self.knob_radius, 2)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.slider_x <= mouse[0] <= self.slider_x + self.slider_width and self.slider_y <= mouse[1] <= self.slider_y + self.slider_height:
            if click[0] == 1:
                new_knob_x = max(self.slider_x + self.knob_radius, min(mouse[0], self.slider_x + self.slider_width - self.knob_radius))
                self.knob_x = new_knob_x
                self.volume = (self.knob_x - self.slider_x - self.knob_radius) / (self.slider_width - 2 * self.knob_radius)
                pygame.mixer.music.set_volume(self.volume)
        return True
   

class Menu:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.background_image = pygame.image.load(os.path.join("images", "fondmenu.jpg"))
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.submenu = SubMenu(window, width, height)
        self.show_submenu = False
        self.options = Option(window, width, height)
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
                if action == "commencer" and not self.show_submenu:
                    self.show_submenu = True
                elif action == "reseau":
                   pass
                elif action == "option":
                    self.options.show_options = True
                elif action == "quitter":
                    pygame.quit()
                    sys.exit()

        self.draw_text(text, (0, 0, 0), x + width / 2, y + height / 2)

    def run(self):
        import plateau
        button_width = 250
        button_height = 50
        button_padding = 20
        button_x = (self.width - (button_width * 4 + button_padding * 3)) / 2
        button_y = self.height - button_height - 50
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

            if self.options.show_options:
                if self.options.draw():
                    self.options.show_options = False
                pygame.display.update()
                continue

            title_text = "YINSH"
            title_color = (255, 255, 255) 
            title_size = 100
            title_font = pygame.font.Font(None, title_size)
            title_x = self.width // 2
            title_y = self.height // 2 - title_size

            title_text_obj = title_font.render(title_text, True, title_color)
            title_text_rect = title_text_obj.get_rect()
            title_text_rect.center = (title_x, title_y)
            self.window.blit(title_text_obj, title_text_rect)    
            self.draw_button("Commencer le jeu", button_x, button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="commencer", radius=10)
            self.draw_button("Jeu en réseau", button_x + button_width + button_padding, button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="reseau", radius=10)
            self.draw_button("Options", button_x + 2 * (button_width + button_padding), button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="option", radius=10)
            self.draw_button("Quitter le jeu", button_x + 3 * (button_width + button_padding), button_y, button_width, button_height, (255, 255, 255, 128), (0, 0, 0), action="quitter", radius=10)

            pygame.display.update()

pygame.init()

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Menu de jeu")

menu = Menu(window, WINDOW_WIDTH, WINDOW_HEIGHT)
menu.run()
