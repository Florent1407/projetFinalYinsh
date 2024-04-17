import pygame
import sys
import os
import math
import menu
import options

class Plateau:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.points = set()
        self.placer_points()    

    def placer_points(self):
        BOARD_TEMPLATE = [
                          [3, 5],
                          [2, 4, 6],
                          [1, 3, 5, 7],
                          [2, 4, 6],
                          [1, 3, 5, 7],
                          [0, 2, 4, 6, 8],
                          [1, 3, 5, 7],
                          [0, 2, 4, 6, 8],
                          [1, 3, 5, 7],
                          [0, 2, 4, 6, 8],
                          [1, 3, 5, 7],
                          [2, 4, 6],
                          [1, 3, 5, 7],
                          [2, 4, 6],
                        [3, 5],
                        ]

        for row_index, row in enumerate(BOARD_TEMPLATE):
            for column_index in row:
                self.points.add((column_index, row_index))

    def draw_hexagon(self, screen, x, y, size, color):
        hexagon_vertices = [(x + size * math.cos(angle), y + size * math.sin(angle)) for angle in
                            [2 * math.pi / 6 * i + math.pi/6 for i in range(6)]]
        pygame.draw.polygon(screen, color, hexagon_vertices)
        return hexagon_vertices

    def afficher_plateau(self, screen, plateau_x, plateau_y):
        plateau_couleur = (178, 161, 155)
        ligne_couleur = (0, 0, 0)  
        for point in self.points:
            x, y = plateau_x + point[0]*41, plateau_y + point[1]*23.5
            self.draw_hexagon(screen, x, y, 45, plateau_couleur)
            for i in range(6):
                start_point = (x + 45 * math.cos(2 * math.pi / 6 * i + math.pi/6),
                               y + 45 * math.sin(2 * math.pi / 6 * i + math.pi/6))
                end_point = (x + 45 * math.cos(2 * math.pi / 6 * (i + 3) + math.pi/6),
                             y + 45 * math.sin(2 * math.pi / 6 * (i + 3) + math.pi/6))
                pygame.draw.line(screen, ligne_couleur, start_point, end_point, 2)

    def reinitialiser_plateau(self):
        self.points.clear()
        self.placer_points()


class Pion:
    def __init__(self, joueur, couleur):
        self.joueur = joueur
        self.couleur = couleur

class Jeu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Plateau de Jeu")
        self.font = pygame.font.SysFont(None, 36)
        self.charger_fond() 
        self.plateau = Plateau(10.1, 18)
        self.positions_clics = [(559, 141), (638, 138), 
                                (515, 160), (598, 160), (678, 159),
                                (476, 185), (556, 181), (639, 181), (718, 182),
                                (437, 208), (517, 205), (598, 204), (680, 205), (758, 204),
                                (474, 232), (557, 230), (642, 228), (722, 228),
                                (435, 256), (512, 252), (598, 252), (682, 255), (758, 254),
                                (392, 278), (474, 278), (557, 279), (638, 277), (720, 275), (800, 275),
                                (434, 301), (515, 300), (599, 300), (681, 300), (762, 300),
                                (393, 324), (475, 324), (557, 324), (640, 322), (721, 324), (800, 324),
                                (430, 348), (517, 348), (599, 348), (678, 348), (759, 347),
                                (392, 372), (474, 368), (558, 369), (638, 368), (723, 369), (800, 372),
                                (434, 392), (516, 395), (598, 395), (680, 395), (761, 393),
                                (398, 420), (476, 416), (558, 418), (638, 419), (721, 416), (800, 414),
                                (436, 443), (515, 440), (596, 440), (681, 440), (758, 441),
                                (475, 464), (556, 464), (639, 465), (721, 466),
                                (436, 488), (515, 488), (598, 489), (679, 488), (758, 484),
                                (476, 510), (556, 512), (639, 512), (718, 511),
                                (518, 535), (598, 533), (678, 533),
                                (559, 556), (639, 555)]
        self.listPplateau = [[0,0],
                             [0,0,0],
                             [0,0,0,0],
                             [0,0,0,0,0],
                             [0,0,0,0],
                             [0,0,0,0,0],
                             [0,0,0,0,0,0],
                             [0,0,0,0,0],
                             [0,0,0,0,0,0],
                             [0,0,0,0,0],
                             [0,0,0,0,0,0],
                             [0,0,0,0,0],
                             [0,0,0,0,0,0],
                             [0,0,0,0,0],
                             [0,0,0,0],
                             [0,0,0,0,0],
                             [0,0,0,0],
                             [0,0,0],
                             [0,0]
                             ]

        self.plateau.placer_points()
        self.joueur_actuel = 0
        self.nb_pions_par_joueur = 5
        self.nb_pions_places = {i: 0 for i in range(2)}
        self.couleur_joueur_1 = (189, 61, 61)  
        self.couleur_joueur_2 = (99, 99, 99)  
        self.joueur_actuel = 1
        self.nb_pions_par_joueur = 5
        self.nb_pions_places = {1: 0, 2: 0}
        self.plateau_largeur = self.plateau.largeur * 50
        self.plateau_hauteur = self.plateau.hauteur * 30
        self.ecran_largeur, self.ecran_hauteur = self.screen.get_size()
        self.plateau_x = (self.ecran_largeur - self.plateau_largeur) // 1.6
        self.plateau_y = (self.ecran_hauteur - self.plateau_hauteur) // 0.87
        self.paused = False
        self.pause_button_rect = pygame.Rect(20, 20, 100, 40)
        pygame.mixer.init()
        self.game_music = pygame.mixer.music.load('musiques/musique2.mp3')
        option_instance = options.Options(self.screen, self.ecran_largeur, self.ecran_hauteur)
        self.volume = option_instance.get_volume()

    def play_game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

    def charger_fond(self):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "images", "fondplateau.png")
        self.fond = pygame.image.load(image_path).convert()  
        self.fond = pygame.transform.smoothscale(self.fond, self.screen.get_size())

    def afficher_tour_joueur(self):
        label_text = f"Tour du joueur {self.joueur_actuel}"
        label = self.font.render(label_text, True, (255, 255, 255))

        label_rect = label.get_rect()
        label_rect.centerx = self.screen.get_rect().centerx
        label_rect.top = 10
        self.screen.blit(label, label_rect)

    def afficher_menu_pause(self):
        dark_overlay = pygame.Surface((self.ecran_largeur, self.ecran_hauteur))
        dark_overlay.set_alpha(128)
        dark_overlay.fill((0, 0, 0))
        self.screen.blit(dark_overlay, (0, 0))

        pygame.draw.rect(self.screen, (245, 245, 220), (300, 150, 600, 300))
        pygame.draw.rect(self.screen, (0, 0, 0), (300, 150, 600, 300), 10)

        pause_font = pygame.font.SysFont(None, 40)
        menu_items = ["Reprendre le jeu", "Recommencer la partie", "Sauvegarder la partie", "Options", "Menu principal"]
        for i, item in enumerate(menu_items):
            pygame.draw.rect(self.screen, (255, 255, 255), (400, 180 + i * 50, 400, 40))  # Au lieu de 220 + i * 50
            pygame.draw.rect(self.screen, (0, 0, 0), (400, 180 + i * 50, 400, 40), 3)
            label = pause_font.render(item, True, (0, 0, 0))
            label_rect = label.get_rect(center=(self.screen.get_rect().centerx, 200 + i * 50))
            self.screen.blit(label, label_rect)

    def verifier_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    x, y = event.pos
                    if self.pause_button_rect.collidepoint(x, y):  
                        self.paused = not self.paused
                    elif not self.paused:  
                        self.trouver_cellule_clicquee(x, y)

                    if self.paused:
                        menu_items_rects = [pygame.Rect(400, 180 + i * 50, 400, 40) for i in range(5)]
                        for i, rect in enumerate(menu_items_rects):
                            if rect.collidepoint(x, y):
                                if i == 0:  
                                    self.paused = False
                                elif i == 1:  
                                    self.recommencer_partie()
                                elif i == 2:  
                                    self.sauvegarder_partie()
                                elif i == 3:
                                    self.afficher_options()
                                elif i == 4: 
                                    self.retour_menu_principal()

    def trouver_cellule_clicquee(self, x, y):
        hitbox_taille = 15
        for index, (cell_x, cell_y) in enumerate(self.positions_clics):
            if (cell_x - hitbox_taille < x < cell_x + hitbox_taille) and \
            (cell_y - hitbox_taille < y < cell_y + hitbox_taille):
                for row_index, row in enumerate(self.listPplateau):
                    row_start_index = sum(len(r) for r in self.listPplateau[:row_index])
                    if index in range(row_start_index, row_start_index + len(row)):
                        self.row_index = row_index
                        self.col_index = index - row_start_index
                        self.placer_pion()  
                        return
                    
    def dessiner_pions(self):
        rayon_pion = 15
        epaisseur_pion = 2

        index = 0 
        for row in self.listPplateau:
            for cell in row:
                x, y = self.positions_clics[index]
                if cell == 1:
                    pygame.draw.circle(self.screen, self.couleur_joueur_1, (x, y), rayon_pion, epaisseur_pion)
                elif cell == 2:
                    pygame.draw.circle(self.screen, self.couleur_joueur_2, (x, y), rayon_pion, epaisseur_pion)
                index += 1

    def placer_pion(self):
        if self.nb_pions_places[self.joueur_actuel] >= self.nb_pions_par_joueur:
            return

        if self.listPplateau[self.row_index][self.col_index] == 0:
            if self.joueur_actuel == 1:
                self.listPplateau[self.row_index][self.col_index] = 1
                self.nb_pions_places[1] += 1
                self.joueur_actuel = 2
            else:
                self.listPplateau[self.row_index][self.col_index] = 2
                self.nb_pions_places[2] += 1
                self.joueur_actuel = 1

    def draw_remaining_pions(self):
        pion_radius = 15
        pion_gap = 20
        column_width = 80
        column_height = self.ecran_hauteur - 100
        column_x1 = 50
        column_x2 = self.ecran_largeur - 50 - column_width
        column_y = 50

        for i in range(1, 3):
            x = column_x1 if i == 1 else column_x2
            y = column_y + column_height - (self.nb_pions_par_joueur - self.nb_pions_places[i]) * (2 * pion_gap + 2 * pion_radius)
            remaining_pions = self.nb_pions_par_joueur - self.nb_pions_places[i]

            for _ in range(remaining_pions):
                pygame.draw.circle(self.screen, self.couleur_joueur_1 if i == 1 else self.couleur_joueur_2, (x + column_width // 2, y), pion_radius)
                y += 2 * (pion_radius + pion_gap)


    def recommencer_partie(self):
        self.listPplateau = [[0, 0],
                            [0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0],
                            [0, 0]
                            ]

        self.nb_pions_places = {1: 0, 2: 0}
        self.joueur_actuel = 1
        self.paused = False

    def sauvegarder_partie(self):
        pass

    def afficher_options(self):
        options_instance = options.Options(self.screen, self.ecran_largeur, self.ecran_hauteur)
        options_instance.run()
        self.volume = options_instance.get_volume()

    def retour_menu_principal(self):
        menu_instance = menu.Menu(self.screen, self.ecran_largeur, self.ecran_hauteur)
        menu_instance.run()
        options_instance = options.Options(self.screen, self.ecran_largeur, self.ecran_hauteur)
        self.volume = options_instance.get_volume()
        pass

    def demarrer(self):
        self.play_game_music()
        while True:
            self.verifier_evenements()
            self.screen.fill((255, 255, 255))  
            self.screen.blit(self.fond, (0, 0))  
            if self.paused:
                self.afficher_menu_pause()
            else:
                self.afficher_tour_joueur()
                self.draw_remaining_pions()
                self.plateau.afficher_plateau(self.screen, self.plateau_x, self.plateau_y)
                self.dessiner_pions()
                pygame.draw.rect(self.screen, (0, 0, 0), self.pause_button_rect)  
                pause_font = pygame.font.SysFont(None, 30)
                label = pause_font.render("Pause", True, (255, 255, 255))
                label_rect = label.get_rect(center=self.pause_button_rect.center)
                self.screen.blit(label, label_rect)
            pygame.display.flip()

if __name__ == "__main__":
    jeu = Jeu()
    jeu.demarrer()
