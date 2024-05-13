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
                            [2 * math.pi / 6 * i + math.pi / 6 for i in range(6)]]
        pygame.draw.polygon(screen, color, hexagon_vertices)
        return hexagon_vertices

    def display_board(self, screen, board_x, board_y):
        color_board = (178, 161, 155)
        color_line = (0, 0, 0)
        for point in self.points:
            x, y = board_x + point[0] * 41, board_y + point[1] * 23.5
            self.draw_hexagon(screen, x, y, 45, color_board)
            for i in range(6):
                start_point = (x + 45 * math.cos(2 * math.pi / 6 * i + math.pi / 6),
                               y + 45 * math.sin(2 * math.pi / 6 * i + math.pi / 6))
                end_point = (x + 45 * math.cos(2 * math.pi / 6 * (i + 3) + math.pi / 6),
                             y + 45 * math.sin(2 * math.pi / 6 * (i + 3) + math.pi / 6))
                pygame.draw.line(screen, color_line, start_point, end_point, 2)

    def reset_board(self):
        self.points.clear()
        self.place_points()

class GameVsComputer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Plateau de Jeu")
        self.font = pygame.font.SysFont(None, 36)
        self.board_wallpaper()
        self.board = Board(10.1, 18)
        self.indexPosition = {}
        self.position_coordinates = {}
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
        self.boardList = [[None, None, None, None, 0, None, 0, None, None, None, None],
                             [None, None, None, 0, None, 0, None, 0, None, None, None],
                             [None, None, 0, None, 0, None, 0, None, 0, None, None],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [None, None, 0, None, 0, None, 0, None, 0, None, None],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [0, None, 0, None, 0, None, 0, None, 0, None, 0],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [0, None, 0, None, 0, None, 0, None, 0, None, 0],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [0, None, 0, None, 0, None, 0, None, 0, None, 0],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [0, None, 0, None, 0, None, 0, None, 0, None, 0],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [None, None, 0, None, 0, None, 0, None, 0, None, None],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [None, None, 0, None, 0, None, 0, None, 0, None, None],
                             [None, None, None, 0, None, 0, None, 0, None, None, None],
                             [None, None, None, None, 0, None, 0, None, None, None, None]
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
        color_background = (245, 245, 220)
        color_border = (0, 0, 0)
        rect_width = 300
        rect_height = 70
        rect_x = (self.screen_width - rect_width) // 2
        rect_y = 10

        pygame.draw.rect(self.screen, color_background, (rect_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(self.screen, color_border, (rect_x, rect_y, rect_width, rect_height), 4)

        label_text = f"Tour du joueur {self.current_player}"
        label = self.font.render(label_text, True, (0, 0, 0))

        label_rect = label.get_rect()
        label_rect.centerx = rect_x + rect_width // 2
        label_rect.centery = rect_y + rect_height // 2
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
            pygame.draw.rect(self.screen, (255, 255, 255), (400, 180 + i * 50, 400, 40))
            pygame.draw.rect(self.screen, (0, 0, 0), (400, 180 + i * 50, 400, 40), 3)
            label = pause_font.render(item, True, (0, 0, 0))
            label_rect = label.get_rect(center=(self.screen.get_rect().centerx, 200 + i * 50))
            self.screen.blit(label, label_rect)

    def position_cells(self):
        index_position = 0
        for row_index, row in enumerate(self.boardList):
            for col_index, cell in enumerate(row):
                if cell == 0 and index_position < len(self.positions_clics):
                    x, y = self.positions_clics[index_position]
                    self.indexPosition[(x, y)] = (row_index, col_index)
                    self.position_coordinates[(row_index, col_index)] = (x, y)
                    index_position += 1
        #print(self.positionIndex, self.positioncoords)

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
                    elif not self.paused and self.current_player != 2:
                        self.find_clicked_cell(x, y)
                        if self.current_player == 2:
                            self.computer()

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

        available_cells = [(row_index, col_index) for row_index, row in enumerate(self.boardList) for col_index, cell in
                           enumerate(row) if cell == 0]
        if available_cells:
            row_index, col_index = random.choice(available_cells)
            self.boardList[row_index][col_index] = 2
            self.pawn_on_board[2] += 1
            self.current_player = 1
            self.place_marker_computer()
            self.displacement()

    def find_clicked_cell(self, x, y):
        hitbox_taille = 10
        for key, value in self.indexPosition.items():
            cell_x, cell_y = key
            if (cell_x - hitbox_taille < x < cell_x + hitbox_taille) and \
                    (cell_y - hitbox_taille < y < cell_y + hitbox_taille):
                self.clic_value = value
                self.place_pawn()
                self.place_markers_on_board()
                self.displacement()
            elif self.current_player == 2:
                self.computer()

    def draw_pawn(self):
        pawn_ray = 15
        pawn_thickness = 2

        for row in range(len(self.boardList)):
            for cell in range(len(self.boardList[row])):

                if self.boardList[row][cell] == 1:
                    for key, value in self.position_coordinates.items():
                        i, j = key
                        if i == row and j == cell:
                            x, y = value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), pawn_ray, pawn_thickness)
                elif self.boardList[row][cell] == 2:
                    for key, value in self.position_coordinates.items():
                        i, j = key
                        if i == row and j == cell:
                            x, y = value
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), pawn_ray, pawn_thickness)

    def draw_solo_marqueur(self):
        radius_marker = 9
        marker_thickness = 0
        for row in range(len(self.boardList)):
            for cell in range(len(self.boardList[row])):
                if self.boardList[row][cell] == 5:
                    for key, value in self.position_coordinates.items():
                        i, j = key
                        if i == row and j == cell:
                            x, y = value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), radius_marker,
                                               marker_thickness)
                elif self.boardList[row][cell] == 6:
                    for key, value in self.position_coordinates.items():
                        i, j = key
                        if i == row and j == cell:
                            x, y = value
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), radius_marker,
                                               marker_thickness)
                elif self.boardList[row][cell] == 10:
                    for key, value in self.position_coordinates.items():
                        i, j = key
                        if i == row and j == cell:
                            x, y = value
                            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), radius_marker, marker_thickness)

    def place_pawn(self):
        row, cols = self.clic_value
        if self.pawn_on_board[self.current_player] >= self.pawn_per_player:
            return

        if self.boardList[row][cols] == 0:
            if self.current_player == 1:
                self.boardList[row][cols] = 1
                self.pawn_on_board[1] += 1
                self.current_player = 2
            elif self.current_player == 2:
                self.boardList[row][cols] = 2
                self.pawn_on_board[2] += 1
                self.current_player = 1

    def draw_marker(self):
        radius_marker = 9
        marker_thickness = 0
        pawn_ray = 15
        pawn_thickness = 2

        for row in range(len(self.boardList)):
            for cell in range(len(self.boardList[row])):
                if self.boardList[row][cell] == 3:
                    for key, value in self.position_coordinates.items():
                        i, j = key
                        if i == row and j == cell:
                            x, y = value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), radius_marker,
                                               marker_thickness)
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), pawn_ray, pawn_thickness)
                elif self.boardList[row][cell] == 4:
                    for key, value in self.position_coordinates.items():
                        i, j = key
                        if i == row and j == cell:
                            x, y = value
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), radius_marker,
                                               marker_thickness)
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), pawn_ray, pawn_thickness)

    def place_markers_on_board(self):
        row, cols = self.clic_value
        if self.pawn_on_board[self.current_player] < self.pawn_per_player:
            return

        if self.place_markers[self.current_player]:
            return

        if self.current_player == 1:
            if self.boardList[row][cols] == 1:
                self.boardList[row][cols] = 3
                self.place_markers[1] = True
                self.place_markers[2] = False

        elif self.current_player == 2:
            if self.boardList[row][cols] == 2:
                self.boardList[row][cols] = 4
                self.place_markers[2] = True
                self.place_markers[1] = False

    def check_vertical_high(self, row, cols, row_marker, cols_marker):
        marker = self.current_player + 4
        coords = []
        for i in range(row_marker, row - 1, -1):
            if self.boardList[i][cols] == 1 or self.boardList[i][cols] == 2:
                return
        for i in range(row_marker, row - 1, -1):
            if self.boardList[i][cols] == 5 or self.boardList[i][cols] == 6:
                coords.append((i, cols))
                x, y = coords[-1]

                if x - 2 == row and y == cols:
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.current_player = self.current_player % 2 + 1
                        #self.return_marker_vertical_high(row, cols, row_marker, cols_marker)
                    break
        if len(coords) == 0 and self.boardList[row][cols] == 0:
            self.boardList[row][cols] = self.current_player
            self.boardList[row_marker][cols_marker] = marker
            self.current_player = self.current_player % 2 + 1
            #self.return_marker_vertical_high(row, cols, row_marker, cols_marker)

    def check_vertical_bottom(self, row, cols, row_marker, cols_marker):
        marker = self.current_player + 4
        coords = []
        for i in range(row_marker, row + 1, +1):
            if self.boardList[i][cols] == 1 or self.boardList[i][cols] == 2:
                return
        for i in range(row_marker, row + 1, +1):
            if self.boardList[i][cols] == 5 or self.boardList[i][cols] == 6:
                coords.append((i, cols))
                x, y = coords[-1]
                if x + 2 == row and y == cols:
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.current_player = self.current_player % 2 + 1
                        #self.return_marker_vertical_bottom(row, cols, row_marker, cols_marker)
                    break
        if len(coords) == 0:
            if self.boardList[row][cols] == 0:
                self.boardList[row][cols] = self.current_player
                self.boardList[row_marker][cols_marker] = marker
                self.current_player = self.current_player % 2 + 1
                print('joueur actuel :', self.current_player)
                #self.return_marker_vertical_bottom(row, cols, row_marker, cols_marker)

    def check_diagonal_right_high(self, row, cols, row_marker, cols_marker):
        if abs(row - row_marker) != abs(cols - cols_marker):
            return
        marker = self.current_player + 4
        coords = []
        num_steps = min(row_marker - row, cols - cols_marker) + 1
        for step in range(num_steps):
            i = row_marker - step
            j = cols_marker + step
            if self.boardList[i][j] == 1 or self.boardList[i][j] == 2:
                return
        for step in range(num_steps):
            i = row_marker - step
            j = cols_marker + step
            if self.boardList[i][j] == 5 or self.boardList[i][j] == 6:
                coords.append((i, j))
                x, y = coords[-1]
                if x - 1 == row and y + 1 == cols:
                    print('Diagonal droite haute condition 1')
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.current_player = self.current_player % 2 + 1
                        #self.return_marker_diagonal_right_high(row, cols, row_marker, cols_marker)
                    break
        if len(coords) == 0:
            print('Diagonal droite haute condition 2')
            if self.boardList[row][cols] == 0:
                self.boardList[row][cols] = self.current_player
                self.boardList[row_marker][cols_marker] = marker
                self.current_player = self.current_player % 2 + 1
                print('Joueur actuel :', self.current_player)
                #self.return_marker_diagonal_right_high(row, cols, row_marker, cols_marker)

    def check_diagonal_left_high(self, row, cols, row_marker, cols_marker):
        if abs(row - row_marker) != abs(cols - cols_marker):
            return
        marker = self.current_player + 4
        coords = []
        num_steps = min(row_marker - row, cols_marker - cols) + 1
        for step in range(num_steps):
            i = row_marker - step
            j = cols_marker - step
            if self.boardList[i][j] == 1 or self.boardList[i][j] == 2:
                return
        for step in range(num_steps):
            i = row_marker - step
            j = cols_marker - step
            if self.boardList[i][j] == 5 or self.boardList[i][j] == 6:
                coords.append((i, j))
                x, y = coords[-1]
                if x - 1 == row and y - 1 == cols:
                    print('Diagonal gauche haute condition 1')
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.current_player = self.current_player % 2 + 1
                        #self.return_marker_diagonal_left_high(row, cols, row_marker, cols_marker)
                    break
        if len(coords) == 0:
            print('Diagonal gauche haute condition 2')
            if self.boardList[row][cols] == 0:
                self.boardList[row][cols] = self.current_player
                self.boardList[row_marker][cols_marker] = marker
                self.current_player = self.current_player % 2 + 1
                #self.return_marker_diagonal_left_high(row, cols, row_marker, cols_marker)
                print('Joueur actuel :', self.current_player)

    def check_diagonal_left_low(self, row, cols, row_marker, cols_marker):
        if abs(row - row_marker) != abs(cols - cols_marker):
            return
        marker = self.current_player + 4
        coords = []
        num_steps = min(row - row_marker, cols_marker - cols) + 1
        for step in range(num_steps):
            i = row_marker + step
            j = cols_marker - step
            if self.boardList[i][j] == 1 or self.boardList[i][j] == 2:
                return
        for step in range(num_steps):
            i = row_marker + step
            j = cols_marker - step
            if self.boardList[i][j] == 5 or self.boardList[i][j] == 6:
                coords.append((i, j))
                x, y = coords[-1]
                if x + 1 == row and y - 1 == cols:
                    print('Diagonal gauche basse condition 1')
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.current_player = self.current_player % 2 + 1
                        #self.return_marker_diagonal_left_low(row, cols, row_marker, cols_marker)
                    break
        if len(coords) == 0:
            print('Diagonal gauche basse condition 2')
            if self.boardList[row][cols] == 0:
                self.boardList[row][cols] = self.current_player
                self.boardList[row_marker][cols_marker] = marker
                self.current_player = self.current_player % 2 + 1
                #self.return_marker_diagonal_left_low(row, cols, row_marker, cols_marker)
                print('Joueur actuel :', self.current_player)

    def check_diagonal_right_low(self, row, cols, row_marker, cols_marker):
        if abs(row - row_marker) != abs(cols - cols_marker):
            return
        marker = self.current_player + 4
        coords = []
        num_steps = min(row - row_marker, cols - cols_marker) + 1
        for step in range(num_steps):
            i = row_marker + step
            j = cols_marker + step
            if self.boardList[i][j] == 1 or self.boardList[i][j] == 2:
                return
        for step in range(num_steps):
            i = row_marker + step
            j = cols_marker + step
            if self.boardList[i][j] == 5 or self.boardList[i][j] == 6:
                coords.append((i, j))
                x, y = coords[-1]
                if x + 1 == row and y + 1 == cols:
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.current_player = self.current_player % 2 + 1
                        #self.return_marker_diagonal_right_low(row, cols, row_marker, cols_marker)
                    break
        if len(coords) == 0:
            if self.boardList[row][cols] == 0:
                self.boardList[row][cols] = self.current_player
                self.boardList[row_marker][cols_marker] = marker
                self.current_player = self.current_player % 2 + 1
                #self.return_marker_diagonal_right_low(row, cols, row_marker, cols_marker)

    def displacement(self):
        pawn_marker = self.current_player + 2
        row, cols = self.clic_value
        if self.place_markers[self.current_player] == True:
            for rows in range(len(self.boardList)):
                for cell in range(len(self.boardList[rows])):
                    if self.boardList[rows][cell] == pawn_marker:
                        row_marker, cols_marker = rows, cell
                        if cols - cols_marker == 0:
                            if row_marker > row:
                                self.check_vertical_high(row, cols, row_marker, cols_marker)
                                print("vertical hautte")
                            elif row_marker < row:
                                self.check_vertical_bottom(row, cols, row_marker, cols_marker)
                                print("vertical basse")
                        elif row_marker < row and cols_marker < cols:
                            self.check_diagonal_right_low(row, cols, row_marker, cols_marker)
                            print("diagonal droite basse")
                        elif row_marker > row and cols_marker < cols:
                            self.check_diagonal_right_high(row, cols, row_marker, cols_marker)
                            print("diagonal droite hautte")
                        elif row_marker > row and cols_marker > cols:
                            self.check_diagonal_left_high(row, cols, row_marker, cols_marker)
                            print("diagonal gauche hautte")
                        elif row_marker < row and cols_marker > cols:
                            self.check_diagonal_left_low(row, cols, row_marker, cols_marker)
                            print("diagonal gauche basse")


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
            y = column_y + column_height - (self.pawn_per_player - self.pawn_on_board[i]) * (
                        2 * pawn_gap + 2 * pawn_radius)
            remaining_pions = self.pawn_per_player - self.pawn_on_board[i]

            for _ in range(remaining_pions):
                pygame.draw.circle(self.screen, self.color_player_1 if i == 1 else self.color_player_2,
                                   (x + column_width // 2, y), pawn_radius)
                y += 2 * (pawn_radius + pawn_gap)

    def restart_game(self):
        self.boardList = [[None, None, None, None, 0, None, 0, None, None, None, None],
                             [None, None, None, 0, None, 0, None, 0, None, None, None],
                             [None, None, 0, None, 0, None, 0, None, 0, None, None],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [None, None, 0, None, 0, None, 0, None, 0, None, None],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [0, None, 0, None, 0, None, 0, None, 0, None, 0],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [0, None, 0, None, 0, None, 0, None, 0, None, 0],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [0, None, 0, None, 0, None, 0, None, 0, None, 0],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [0, None, 0, None, 0, None, 0, None, 0, None, 0],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [None, None, 0, None, 0, None, 0, None, 0, None, None],
                             [None, 0, None, 0, None, 0, None, 0, None, 0, None],
                             [None, None, 0, None, 0, None, 0, None, 0, None, None],
                             [None, None, None, 0, None, 0, None, 0, None, None, None],
                             [None, None, None, None, 0, None, 0, None, None, None, None]
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

        index_position = 0

        for row in self.boardList:
            for cell in row:
                if index_position >= len(self.positions_clics):
                    break

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
            x, y = key
            row, coll = value
            if coll == 0:
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y), radius_marker, marker_thickness)
            elif coll == 1:
                pygame.draw.circle(self.screen, (0, 255, 0), (x, y), radius_marker, marker_thickness)
            elif coll == 2:
                pygame.draw.circle(self.screen, (0, 0, 255), (x, y), radius_marker, marker_thickness)
            elif coll == 3:
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), radius_marker, marker_thickness)
            elif coll == 4:
                pygame.draw.circle(self.screen, (255, 255, 0), (x, y), radius_marker, marker_thickness)
            elif coll == 5:
                pygame.draw.circle(self.screen, (255, 0, 255), (x, y), radius_marker, marker_thickness)
            elif coll == 6:
                pygame.draw.circle(self.screen, (0, 255, 255), (x, y), radius_marker, marker_thickness)
            elif coll == 7:
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), radius_marker, marker_thickness)
            elif coll == 8:
                pygame.draw.circle(self.screen, (128, 0, 128), (x, y), radius_marker, marker_thickness)
            elif coll == 9:
                pygame.draw.circle(self.screen, (64, 224, 208), (x, y), radius_marker, marker_thickness)
            elif coll == 10:
                pygame.draw.circle(self.screen, (255, 165, 0), (x, y), radius_marker, marker_thickness)
            elif coll == 11:
                pygame.draw.circle(self.screen, (169, 169, 169), (x, y), radius_marker, marker_thickness)

    def place_marker_computer(self):
        row, cols = self.clic_value
        if self.pawn_on_board[self.current_player] < self.pawn_per_player:
            return

        if self.place_markers[self.current_player]:
            return

        if self.current_player == 1:
            if self.boardList[row][cols] == 1:
                self.boardList[row][cols] = 3
                self.place_markers[1] = True
                self.place_markers[2] = False

        elif self.current_player == 2:
            if self.boardList[row][cols] == 2:
                self.boardList[row][cols] = 4
                self.place_markers[2] = True
                self.place_markers[1] = False

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

    def run(self):
        self.start()

if __name__ == "__main__":
    game = GameVsComputer()
    game.start()