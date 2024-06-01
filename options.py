import pygame
import os
import configparser

class Options:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.background_image = pygame.image.load(os.path.join("images", "fondplateau.png"))
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.volume_slider = VolumeSlider(window, width, height)
        self.show_options = False
        self.bold_font = pygame.font.Font(None, 48)
        self.volume = self.volume_slider.volume
        self.quit_options = False

    def get_volume(self):
        return self.volume

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
                if action == "retour":
                    self.quit_options = True
                    return True

        self.draw_text(text, (0, 0, 0), x + width / 2, y + height / 2)

    def draw(self):
        self.window.blit(self.background_image, (0, 0))

        dark_overlay = pygame.Surface((self.width, self.height))
        dark_overlay.set_alpha(128)
        dark_overlay.fill((0, 0, 0))
        self.window.blit(dark_overlay, (0, 0))

        self.draw_text("Options", (255, 255, 255), self.width // 2, 80, font=self.bold_font)

        volume_text_x = self.volume_slider.slider_x + self.volume_slider.slider_width // 2
        volume_text_y = self.volume_slider.slider_y - 70
        self.draw_text("Volume Musique", (255, 255, 255), volume_text_x, volume_text_y)

        self.volume_slider.draw()
        if self.draw_button("Retour", 50, 50, 150, 50, (255, 255, 255, 128), (0, 0, 0), action="retour", radius=10):
            self.show_options = False
            return True
        return False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.window.blit(self.background_image, (0, 0))

            self.show_options = True
            if self.draw():
                running = False

            pygame.mixer.music.set_volume(self.volume_slider.volume)
            pygame.display.update()


class VolumeSlider:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.slider_width = 300
        self.slider_height = 30
        self.slider_x = (width - self.slider_width) // 2
        self.slider_y = height // 2 - 100
        self.slider_color = (255, 255, 255, 128)
        self.slider_border_color = (0, 0, 0)
        self.slider_radius = 10
        self.knob_radius = 15
        self.knob_color = (0, 0, 0)
        self.knob_border_color = (255, 255, 255)

        if not os.path.exists('config.ini'):
            config = configparser.ConfigParser()
            config['Volume'] = {'level': 0.5}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.volume = config.getfloat('Volume', 'level')

        self.knob_x = self.slider_x + self.slider_width * self.volume - self.knob_radius
        self.knob_y = self.slider_y + self.slider_height // 2

        pygame.mixer.music.set_volume(self.volume)

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

                config = configparser.ConfigParser()
                config.read('config.ini')
                config.set('Volume', 'level', str(self.volume))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

        return True
