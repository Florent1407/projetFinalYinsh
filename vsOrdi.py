import pygame
import sys
import os
import math
import random
import menu
import options

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = set()
        self.place_points()    

    def place_points(self):
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

    def display_board(self, screen, board_x, board_y):
        color_board = (178, 161, 155)
        color_line = (0, 0, 0)  
        for point in self.points:
            x, y = board_x + point[0]*41, board_y + point[1]*23.5
            self.draw_hexagon(screen, x, y, 45, color_board)
            for i in range(6):
                start_point = (x + 45 * math.cos(2 * math.pi / 6 * i + math.pi/6),
                               y + 45 * math.sin(2 * math.pi / 6 * i + math.pi/6))
                end_point = (x + 45 * math.cos(2 * math.pi / 6 * (i + 3) + math.pi/6),
                             y + 45 * math.sin(2 * math.pi / 6 * (i + 3) + math.pi/6))
                pygame.draw.line(screen, color_line, start_point, end_point, 2)

    def reset_board(self):
        self.points.clear()
        self.place_points()

class Pion:
    def __init__(self, player, color):
        self.joueur = player
        self.couleur = color

class GameVsComputer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Plateau de Jeu")
        self.font = pygame.font.SysFont(None, 36)
        self.board_wallpaper() 
        self.board = Board(10.1, 18)
        self.indexPosition={}
        self.position_coordinates={}
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
        self.listPplateau = [[None,None,None,None,0,None,0,None,None,None,None],
                             [None,None,None,0,None,0,None,0,None,None,None],
                             [None,None,0,None,0,None,0,None,0,None,None],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [None,None,0,None,0,None,0,None,0,None,None],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [0,None,0,None,0,None,0,None,0,None,0],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [0,None,0,None,0,None,0,None,0,None,0],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [0,None,0,None,0,None,0,None,0,None,0],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [0,None,0,None,0,None,0,None,0,None,0],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [None,None,0,None,0,None,0,None,0,None,None],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [None,None,0,None,0,None,0,None,0,None,None],
                             [None,None,None,0,None,0,None,0,None,None,None],
                             [None,None,None,None,0,None,0,None,None,None,None]
                             ]

        self.board.place_points()
        self.pawn_per_player = 5
        self.place_markers = {1: False, 2: False}
        self.color_player_1 = (189, 61, 61)  
        self.color_player_2 = (99, 99, 99)  
        self.current_player = 1
        self.pawn_on_board = {1: 0, 2: 0}
        self.board_width = self.board.width * 50
        self.board_height = self.board.height * 30
        self.screen_width, self.screen_height = self.screen.get_size()
        self.board_x = (self.screen_width - self.board_width) // 1.6
        self.board_y = (self.screen_height - self.board_height) // 0.87
        self.paused = False
        self.pause_button_rect = pygame.Rect(20, 20, 100, 40)
        pygame.mixer.init()
        self.game_music = pygame.mixer.music.load('musiques/musique2.mp3')
        self.position_cells()

    def play_game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)

    def board_wallpaper(self):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "images", "fondplateau.png")
        self.fond = pygame.image.load(image_path).convert()  
        self.fond = pygame.transform.smoothscale(self.fond, self.screen.get_size())

    def show_player_turn(self):
        label_text = f"Tour du joueur {self.current_player}"
        label = self.font.render(label_text, True, (255, 255, 255))

        label_rect = label.get_rect()
        label_rect.centerx = self.screen.get_rect().centerx
        label_rect.top = 10
        self.screen.blit(label, label_rect)

    def show_menu_pause(self):
        dark_overlay = pygame.Surface(self.screen.get_size())
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

    def position_cells(self):
        index_position = 0
        for row_index, row in enumerate(self.listPplateau):
            for col_index, cell in enumerate(row):
                if cell == 0 and index_position < len(self.positions_clics):
                    # Associe la cellule `0` Ã  sa position dans `self.positions_clics`
                    x, y = self.positions_clics[index_position]
                    self.indexPosition[(x, y)] = (row_index, col_index)
                    self.position_coordinates[(row_index, col_index)]=(x, y)
                    index_position += 1
        # print(self.positionIndex, self.positioncoords)

    def check_events(self):
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
                        self.find_clicked_cell(x, y)

                    if self.paused:
                        menu_items_rects = [pygame.Rect(400, 180 + i * 50, 400, 40) for i in range(5)]
                        for i, rect in enumerate(menu_items_rects):
                            if rect.collidepoint(x, y):
                                if i == 0:  
                                    self.paused = False
                                elif i == 1:  
                                    self.restart_game()
                                elif i == 2:  
                                    self.save_game()
                                elif i == 3:
                                    self.show_options()
                                elif i == 4: 
                                    self.return_main_menu()


    def computer(self):
        if self.pawn_on_board[2] >= self.pawn_per_player:
            return

        available_cells = [(row_index, col_index) for row_index, row in enumerate(self.listPplateau) for col_index, cell in enumerate(row) if cell == 0]
        if available_cells:
            row_index, col_index = random.choice(available_cells)
            self.listPplateau[row_index][col_index] = 2
            self.pawn_on_board[2] += 1
            self.current_player = 1

    def find_clicked_cell(self, x, y):
        hitbox_taille = 10
        for key, value in self.indexPosition.items():
            cell_x, cell_y = key
            # VÃ©rifier si le clic est dans une zone autour de la cellule
            if (cell_x - hitbox_taille < x < cell_x + hitbox_taille) and \
               (cell_y - hitbox_taille < y < cell_y + hitbox_taille):
                self.clic_value = value
                self.place_pawn() 
                self.place_markers_on_board()
                #self.deplacement()
            elif self.current_player == 2:
                self.computer()

    def draw_pawn(self):
        pawn_ray = 15
        pawn_thickness = 2
 # Index pour `self.positions_clics`

        for row in range(len(self.listPplateau)):
            for cell in range(len(self.listPplateau[row])):
                
                if self.listPplateau[row][cell] == 1:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), pawn_ray, pawn_thickness)
                elif self.listPplateau[row][cell] == 2:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), pawn_ray, pawn_thickness)

    def place_pawn(self):
        row,cols=self.clic_value
        if self.pawn_on_board[self.current_player] >= self.pawn_per_player:
            return

        if self.listPplateau[row][cols] == 0:
            if self.current_player == 1:
                self.listPplateau[row][cols] = 1
                self.pawn_on_board[1] += 1
                self.current_player = 2
            elif self.current_player == 2:
                self.listPplateau[row][cols] = 2
                self.pawn_on_board[2] += 1
                self.current_player = 1

    def draw_marker(self):
        radius_marker = 9
        marker_thickness = 0
        pawn_ray = 15
        pawn_thickness =2
      
        for row in range(len(self.listPplateau)):
            for cell in range(len(self.listPplateau[row])):
                if self.listPplateau[row][cell]==3:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), radius_marker, marker_thickness)
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), pawn_ray, pawn_thickness)
                elif self.listPplateau[row][cell]== 4:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), radius_marker, marker_thickness)
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), pawn_ray, pawn_thickness)

    def place_markers_on_board(self):
        row,cols=self.clic_value
        if self.pawn_on_board[self.current_player] < self.pawn_per_player:
            return
        
        if self.place_markers[self.current_player]:
            return

        if self.current_player == 1:
            if self.listPplateau[row][cols] == 1:
                self.listPplateau[row][cols] = 3
                self.place_markers[1] = True
                self.place_markers[2] = False

        elif self.current_player == 2:
            if self.listPplateau[row][cols] == 2:
                self.listPplateau[row][cols] = 4
                self.place_markers[2] = True
                self.place_markers[1] = False

    def draw_solo_marqueur(self):
        radius_marker = 9
        marker_thickness = 0
        for row in range(len(self.listPplateau)):
            for cell in range(len(self.listPplateau[row])):
                if self.listPplateau[row][cell]==5:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), radius_marker, marker_thickness)
                elif self.listPplateau[row][cell]==6:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), radius_marker, marker_thickness)


    def draw_remaining_pions(self):
        pawn_radius = 15
        pawn_gap = 20
        column_width = 80
        column_height = self.screen_height - 100
        column_x1 = 50
        column_x2 = self.screen_width - 50 - column_width
        column_y = 50

        for i in range(1, 3):
            x = column_x1 if i == 1 else column_x2
            y = column_y + column_height - (self.pawn_per_player - self.pawn_on_board[i]) * (2 * pawn_gap + 2 * pawn_radius)
            remaining_pions = self.pawn_per_player - self.pawn_on_board[i]

            for _ in range(remaining_pions):
                pygame.draw.circle(self.screen, self.color_player_1 if i == 1 else self.color_player_2, (x + column_width // 2, y), pawn_radius)
                y += 2 * (pawn_radius + pawn_gap)


    def restart_game(self):
        self.listPplateau = [[None,None,None,None,0,None,0,None,None,None,None],
                             [None,None,None,0,None,0,None,0,None,None,None],
                             [None,None,0,None,0,None,0,None,0,None,None],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [None,None,0,None,0,None,0,None,0,None,None],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [0,None,0,None,0,None,0,None,0,None,0],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [0,None,0,None,0,None,0,None,0,None,0],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [0,None,0,None,0,None,0,None,0,None,0],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [0,None,0,None,0,None,0,None,0,None,0],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [None,None,0,None,0,None,0,None,0,None,None],
                             [None,0,None,0,None,0,None,0,None,0,None],
                             [None,None,0,None,0,None,0,None,0,None,None],
                             [None,None,None,0,None,0,None,0,None,None,None],
                             [None,None,None,None,0,None,0,None,None,None,None]
                            ]

        self.pawn_on_board = {1: 0, 2: 0}
        self.current_player = 1
        self.paused = False
        self.place_markers = {1: False, 2: False}

    def save_game(self):
        pass

    def show_options(self):
        options_instance = options.Options(self.screen, self.screen.get_width(), self.screen.get_height())
        options_instance.run()
        self.volume = options_instance.get_volume()

    def return_main_menu(self):
        menu_instance = menu.Menu(self.screen, self.screen_width, self.screen_height)
        menu_instance.run()
        pass

    def draw_cells(self):
        radius_circle = 15
        circle_thickness = 4
        none_color = (255, 0, 0)  
        zero_color = (0, 255, 0)  

        index_position = 0  # Index pour `self.positions_clics`

        for row in self.listPplateau:
            for cell in row:
                if index_position >= len(self.positions_clics):
                    break  # Sortez si on a dÃ©passÃ© le nombre de positions disponibles

                x, y = self.positions_clics[index_position]

                if cell is None:
                    pygame.draw.circle(self.screen, none_color, (x, y), radius_circle, circle_thickness)
                elif cell == 0:
                    pygame.draw.circle(self.screen, zero_color, (x, y), radius_circle, circle_thickness)

                index_position += 1

    def display_cells(self):
        radius_marker = 9
        marker_thickness = 0
        for key, value in self.position_coordinates.items():
            x,y=key
            row,coll=value
            if coll==0:
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y), radius_marker, marker_thickness)
            elif coll==1:
                pygame.draw.circle(self.screen, (0, 255, 0), (x, y), radius_marker, marker_thickness)
            elif coll==2:
                pygame.draw.circle(self.screen, (0, 0, 255), (x, y), radius_marker, marker_thickness)
            elif coll==3:
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), radius_marker, marker_thickness)
            elif coll==4:
                pygame.draw.circle(self.screen, (255, 255, 0), (x, y), radius_marker, marker_thickness)
            elif coll==5:
                pygame.draw.circle(self.screen, (255, 0, 255), (x, y), radius_marker, marker_thickness)
            elif coll==6:
                pygame.draw.circle(self.screen, (0, 255, 255), (x, y), radius_marker, marker_thickness)
            elif coll==7:
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), radius_marker, marker_thickness)
            elif coll==8:
                pygame.draw.circle(self.screen, (128, 0, 128) , (x, y), radius_marker, marker_thickness)
            elif coll==9:
                pygame.draw.circle(self.screen, (64, 224, 208), (x, y), radius_marker, marker_thickness)
            elif coll==10:
                pygame.draw.circle(self.screen, (255, 165, 0), (x, y), radius_marker, marker_thickness)
            elif coll==11:
                pygame.draw.circle(self.screen,  (169, 169, 169), (x, y), radius_marker, marker_thickness)        

    def start(self):
        self.play_game_music()
        pause_font = pygame.font.SysFont(None, 30)
        pause_text = pause_font.render("Pause", True, (0, 0, 0))
        pause_text_rect = pause_text.get_rect(center=self.pause_button_rect.center)

        while True:
            self.check_events()
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.fond, (0, 0))
            if self.paused:
                self.show_menu_pause()
            else:
                self.show_player_turn()
                self.draw_remaining_pions()
                self.board.display_board(self.screen, self.board_x, self.board_y)
                self.draw_pawn()
                self.draw_marker()
                self.draw_solo_marqueur()

                pygame.draw.rect(self.screen, (245, 245, 220), self.pause_button_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), self.pause_button_rect, 2)

                self.screen.blit(pause_text, pause_text_rect)

            pygame.display.flip()


if __name__ == "__main__":
    game = GameVsComputer()
    game.start()
