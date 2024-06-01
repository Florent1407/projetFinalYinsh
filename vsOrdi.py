import pygame
import sys
import os
import random
import menu
import options

class GameVsComputer:
    def __init__(self):
        from Board import Board
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
        self.boardList = [[None,None,None,None,0,None,0,None,None,None,None],
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
        self.color_player_1 = (0, 120, 255)
        self.color_player_2 = (255, 0, 0)
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
        option_instance = options.Options(self.screen, self.screen_width, self.screen_height)
        self.volume = option_instance.get_volume()
        self.position_cells()
        self.bot_marker_placed = False
        self.pawn_delet = False
        self.deleting_player = None
        self.number_pawn_delte={1: 0, 2: 0}
        self.game_over = False
        self.victory_player = 0
        self.detected_multiple_alignements = False
        self.choise_alignement = False
        self.multiple1=[]
        self.multiple2=[]

    def play_game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(self.volume)
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

        pygame.draw.rect(self.screen, (245, 245, 220), (300, 150, 600, 250))
        pygame.draw.rect(self.screen, (0, 0, 0), (300, 150, 600, 250), 10)

        pause_font = pygame.font.SysFont(None, 40)
        menu_items = ["Reprendre le jeu", "Recommencer la partie", "Options", "Menu principal"]
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
                    self.position_coordinates[(row_index, col_index)]=(x, y)
                    index_position += 1

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
                    elif self.pawn_delet:
                        self.delete_pawns(x, y)
                    if self.choise_alignement and self.current_player == 1:
                        self.choise_alignements_destroy(x, y)

                    if self.paused:
                        menu_items_rects = [pygame.Rect(400, 180 + i * 50, 400, 40) for i in range(4)]

                        for i, rect in enumerate(menu_items_rects):
                            if rect.collidepoint(x, y):
                                if i == 0:
                                    self.paused = False
                                elif i == 1:
                                    self.restart_game()
                                elif i == 2:
                                    self.show_options()
                                elif i == 3:
                                    self.return_main_menu()

    def find_clicked_cell(self, x, y):
        hitbox_taille = 20
        for key, value in self.indexPosition.items():
            cell_x, cell_y = key
            if (cell_x - hitbox_taille < x < cell_x + hitbox_taille) and \
                    (cell_y - hitbox_taille < y < cell_y + hitbox_taille):
                self.clic_value = value
                if not self.pawn_delet and  not self.choise_alignement:
                    self.place_pawn()
                    self.place_markers_on_board()
                    self.displacement()
                elif self.pawn_delet:
                    self.delete_pawns(x, y)
                if self.choise_alignement and self.current_player == 1:
                    self.choise_alignements_destroy(x, y)      

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
                    
    def draw_pawn(self):
        pawn_ray = 20
        pawn_thickness = 4

        for row in range(len(self.boardList)):
            for cell in range(len(self.boardList[row])):
                
                if self.boardList[row][cell] == 1:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), pawn_ray, pawn_thickness)
                elif self.boardList[row][cell] == 2:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), pawn_ray, pawn_thickness)  

    def place_pawn(self):
        row,cols=self.clic_value
        if self.pawn_on_board[self.current_player] >= self.pawn_per_player:
            return

        if self.boardList[row][cols] == 0:
            if self.current_player == 1 and self.pawn_on_board[1] < self.pawn_per_player:
                self.boardList[row][cols] = 1
                self.pawn_on_board[1] += 1
                self.current_player = 2
            elif self.current_player == 2 and self.pawn_on_board[2] < self.pawn_per_player:
                self.boardList[row][cols] = 2
                self.pawn_on_board[2] += 1
                self.current_player = 1

    def draw_marker(self):
        radius_marker = 10
        marker_thickness = 0
        pawn_ray = 20
        pawn_thickness = 4
      
        for row in range(len(self.boardList)):
            for cell in range(len(self.boardList[row])):
                if self.boardList[row][cell]==3:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), radius_marker, marker_thickness)
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), pawn_ray, pawn_thickness)
                elif self.boardList[row][cell]== 4:
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
        tracking = False
        sequence_broken = False
        for i in range(row_marker, row - 1, -1):
            if self.boardList[i][cols] == 1 or self.boardList[i][cols] == 2:
                return
        for i in range(row_marker, row - 1, -1):
            if self.boardList[i][cols] == 5 or self.boardList[i][cols] == 6:
                coords.append((i, cols))
                if tracking==False:
                    tracking = True
            elif self.boardList[i][cols]==0 and tracking==True and i!=row:
                sequence_broken=True
                break
        if sequence_broken==False and tracking==True:
                x, y = coords[-1]
                if x - 2 == row and y == cols:
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.return_marker_vertical_high(row, cols, row_marker, cols_marker)
                        self.alignment_verification()
                        self.current_player = self.current_player % 2 + 1
        else:
            if len(coords) == 0 and self.boardList[row][cols] == 0:
                self.boardList[row][cols] = self.current_player
                self.boardList[row_marker][cols_marker] = marker
                self.return_marker_vertical_high(row, cols, row_marker, cols_marker)
                self.alignment_verification()
                self.current_player = self.current_player % 2 + 1                

    def check_vertical_bottom(self,row,cols,row_marker,cols_marker):
        marker=self.current_player+4
        coords=[]
        tracking = False
        sequence_broken = False
        for i in range(row_marker,row+1,+1):
            if self.boardList[i][cols] == 1 or self.boardList[i][cols] == 2:
                return
        for i in range(row_marker,row+1,+1):
            if self.boardList[i][cols]==5 or self.boardList[i][cols]==6 :
                coords.append((i,cols))
                if tracking==False:
                    tracking = True
            elif self.boardList[i][cols]==0 and tracking==True and i!=row:
                sequence_broken=True
                break
        if sequence_broken==False and tracking==True:
                x,y=coords[-1]
                if x+2==row and y==cols:
                    if self.boardList[row][cols]==0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.return_marker_vertical_bottom(row,cols,row_marker,cols_marker)
                        self.alignment_verification()
                        self.current_player = self.current_player%2+1
        else:            
            if len(coords)==0:
                if self.boardList[row][cols]==0:
                    self.boardList[row][cols] = self.current_player
                    self.boardList[row_marker][cols_marker] = marker
                    self.return_marker_vertical_bottom(row,cols,row_marker,cols_marker)
                    self.alignment_verification()
                    self.current_player = self.current_player%2+1                    

    def check_diagonal_right_high(self, row, cols, row_marker, cols_marker):
        if abs(row - row_marker) != abs(cols - cols_marker):
            return
        marker = self.current_player + 4
        coords = []
        tracking = False
        sequence_broken = False
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
                if tracking == False:
                    tracking = True
            elif self.boardList[i][j] == 0 and tracking == True and i != row and j != cols:
                sequence_broken = True
                break
        if sequence_broken == False and tracking == True:
                x, y = coords[-1]
                if x - 1 == row and y + 1 == cols:
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.return_marker_diagonal_right_high(row, cols, row_marker, cols_marker)
                        self.alignment_verification()
                        self.current_player = self.current_player % 2 + 1                        
        else:           
            if len(coords) == 0:
                if self.boardList[row][cols] == 0:
                    self.boardList[row][cols] = self.current_player
                    self.boardList[row_marker][cols_marker] = marker
                    self.return_marker_diagonal_right_high(row, cols, row_marker, cols_marker)
                    self.alignment_verification()
                    self.current_player = self.current_player % 2 + 1

    def check_diagonal_left_high(self, row, cols, row_marker, cols_marker):
        if abs(row - row_marker) != abs(cols - cols_marker):
            return
        marker = self.current_player + 4
        coords = []
        tracking = False
        sequence_broken = False
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
                if tracking == False:
                    tracking = True
            elif self.boardList[i][j] == 0 and tracking == True and i != row and j != cols:
                sequence_broken = True
                break
        if sequence_broken == False and tracking == True:
                x, y = coords[-1]
                if x - 1 == row and y - 1 == cols:
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.return_marker_diagonal_left_high(row, cols, row_marker, cols_marker)
                        self.alignment_verification()
                        self.current_player = self.current_player % 2 + 1
        else:           
            if len(coords) == 0:
                if self.boardList[row][cols] == 0:
                    self.boardList[row][cols] = self.current_player
                    self.boardList[row_marker][cols_marker] = marker
                    self.return_marker_diagonal_left_high(row, cols, row_marker, cols_marker)
                    self.alignment_verification()
                    self.current_player = self.current_player % 2 + 1                    

    def check_diagonal_left_low(self, row, cols, row_marker, cols_marker):
        if abs(row - row_marker) != abs(cols - cols_marker):
            return
        marker = self.current_player + 4
        coords = []
        tracking = False
        sequence_broken = False
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
                if tracking == False:
                    tracking = True
            elif self.boardList[i][j] == 0 and tracking == True and i != row and j != cols:
                sequence_broken = True
                break
        if sequence_broken == False and tracking == True:
                x, y = coords[-1]
                if x + 1 == row and y - 1 == cols:
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.return_marker_diagonal_left_low(row, cols, row_marker, cols_marker)
                        self.alignment_verification()
                        self.current_player = self.current_player % 2 + 1
        else:            
            if len(coords) == 0:
                if self.boardList[row][cols] == 0:
                    self.boardList[row][cols] = self.current_player
                    self.boardList[row_marker][cols_marker] = marker
                    self.return_marker_diagonal_left_low(row, cols, row_marker, cols_marker)
                    self.alignment_verification()
                    self.current_player = self.current_player % 2 + 1                    

    def check_diagonal_right_low(self, row, cols, row_marker, cols_marker):
        if abs(row - row_marker) != abs(cols - cols_marker):
            return
        marker = self.current_player + 4
        coords = []
        tracking = False
        sequence_broken = False
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
                if tracking == False:
                    tracking = True
            elif self.boardList[i][j] == 0 and tracking == True and i != row and j != cols:
                sequence_broken = True
                break
        if sequence_broken == False and tracking == True:
                x, y = coords[-1]
                if x + 1 == row and y + 1 == cols:
                    if self.boardList[row][cols] == 0:
                        self.boardList[row][cols] = self.current_player
                        self.boardList[row_marker][cols_marker] = marker
                        self.return_marker_diagonal_right_low(row, cols, row_marker, cols_marker)
                        self.alignment_verification()
                        self.current_player = self.current_player % 2 + 1
        else:
            if len(coords) == 0:
                if self.boardList[row][cols] == 0:
                    self.boardList[row][cols] = self.current_player
                    self.boardList[row_marker][cols_marker] = marker
                    self.return_marker_diagonal_right_low(row, cols, row_marker, cols_marker)
                    self.alignment_verification()
                    self.current_player = self.current_player % 2 + 1
                    
    def displacement (self):
        pawn_marker=self.current_player+2
        row,cols=self.clic_value
        if self.place_markers[1] == True:
            for rows in range(len(self.boardList)):
                for cell in range(len(self.boardList[rows])):
                    if self.boardList[rows][cell] == pawn_marker:
                        row_marker, cols_marker = rows, cell
                        if cols-cols_marker == 0:
                            if row_marker>row:
                                self.check_vertical_high(row,cols,row_marker,cols_marker)
                            elif row_marker<row:
                                self.check_vertical_bottom(row,cols,row_marker,cols_marker)
                        elif row_marker<row and cols_marker<cols:
                            self.check_diagonal_right_low(row,cols,row_marker,cols_marker)
                        elif row_marker>row and cols_marker<cols:
                            self.check_diagonal_right_high(row,cols,row_marker,cols_marker)
                        elif row_marker>row and cols_marker>cols:
                            self.check_diagonal_left_high(row,cols,row_marker,cols_marker) 
                        elif row_marker<row and cols_marker>cols:
                            self.check_diagonal_left_low(row,cols,row_marker,cols_marker)

    def draw_solo_marqueur(self):
        radius_marker = 9
        marker_thickness = 0
        for row in range(len(self.boardList)):
            for cell in range(len(self.boardList[row])):
                if self.boardList[row][cell]==5:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_1, (x, y), radius_marker, marker_thickness)
                elif self.boardList[row][cell]==6:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen, self.color_player_2, (x, y), radius_marker, marker_thickness)
                elif self.boardList[row][cell]==10:
                    for key,value in self.position_coordinates.items():
                        i,j=key
                        if i==row and j==cell:
                            x,y=value
                            pygame.draw.circle(self.screen,(0,255,0), (x, y), radius_marker, marker_thickness)            

    def return_marker_vertical_high(self, row, cols, row_marker, cols_marker):
        for i in range(row_marker-1, row - 1, -1):
            if 0<=i<=18:
                if self.boardList[i][cols_marker] == 5:
                    self.boardList[i][cols_marker] = 6
                elif self.boardList[i][cols_marker] == 6:
                    self.boardList[i][cols_marker] = 5

    def return_marker_vertical_bottom(self, row, cols, row_marker, cols_marker):
        for i in range(row_marker+1,row+1,+1):
            if 0<=i<=18:
                if self.boardList[i][cols_marker] == 5:
                    self.boardList[i][cols_marker] = 6
                elif self.boardList[i][cols_marker] == 6:
                    self.boardList[i][cols_marker] = 5

    def return_marker_diagonal_right_low(self, row, cols, row_marker, cols_marker):
        row=row-1
        cols=cols-1
        row_marker=row_marker+1
        cols_marker=cols_marker+1
        num_steps = min(row - row_marker, cols - cols_marker) + 2
        for step in range(num_steps):
            i = row_marker  + step
            j = cols_marker  + step
            if 0<=i<=18 and 0<=j<=10:
                if self.boardList[i][j]==5:
                    self.boardList[i][j] = 6
                elif self.boardList[i][j]==6:
                    self.boardList[i][j] = 5

    def return_marker_diagonal_right_high(self, row, cols, row_marker, cols_marker):
        row=row+1
        cols=cols-1
        row_marker=row_marker-1
        cols_marker=cols_marker+1
        num_steps = min(row_marker - row, cols - cols_marker)+2
        for step in range(num_steps):
            i = row_marker - step
            j = cols_marker + step
            if 0<=i<=18 and 0<=j<=10:
                if self.boardList[i][j] == 5:
                    self.boardList[i][j] = 6
                elif self.boardList[i][j] == 6:
                    self.boardList[i][j] = 5

    def return_marker_diagonal_left_high(self, row, cols, row_marker, cols_marker):
        row=row+1
        cols=cols+1
        row_marker=row_marker-1
        cols_marker=cols_marker-1
        num_steps = min(row_marker - row, cols_marker - cols) + 2
        for step in range(num_steps):
            i = row_marker - step
            j = cols_marker - step
            if 0<=i<=18 and 0<=j<=10:
                if self.boardList[i][j] == 5:
                    self.boardList[i][j] = 6
                elif self.boardList[i][j] == 6:
                    self.boardList[i][j] = 5

    def return_marker_diagonal_left_low(self, row, cols, row_marker, cols_marker):
        row=row-1
        cols=cols+1
        row_marker=row_marker+1
        cols_marker=cols_marker-1
        num_steps = min(row - row_marker, cols_marker - cols) + 2
        for step in range(num_steps):
            i = row_marker + step
            j = cols_marker - step
            if 0<=i<=18 and 0<=j<=10:
                if self.boardList[i][j] == 5:
                    self.boardList[i][j] = 6
                elif self.boardList[i][j] == 6:
                    self.boardList[i][j] = 5

    def alignment_verification(self):
        self.vertical_alignment()
        self.alignment_diag_left_to_right()
        self.alignment_diagonal_right_to_left()
        
    def vertical_alignment(self):
        marker_current_player = self.current_player + 4
        if self.current_player % 2 == 0:
            marker_other_player = 5
        else:
            marker_other_player = 6
        for col in range(11):
            alignment = 0
            coords_alignment = []
            for row in range(19):
                if self.boardList[row][col] == marker_current_player:
                    alignment += 1
                    coords_alignment.append((row, col))
                    if alignment == 5:
                        self.deleting_player = self.current_player
                        self.pawn_delet = True
                        self.delete_alignments(coords_alignment)
                elif self.boardList[row][col]==0 or self.boardList[row][col] == marker_other_player or self.boardList[row][col] == 1 or self.boardList[row][col]==2:
                    alignment = 0
                    coords_alignment = []

    def alignment_diag_left_to_right(self):
        marker_current_player = self.current_player + 4
        marker_other_player = 5 if self.current_player % 2 == 0 else 6
        max_rows = 19
        max_columns = 11
        for start_row in range(max_rows):
            self.check_diagonal_left_to_right(start_row, 0, marker_current_player, marker_other_player, max_rows, max_columns)

        for start_col in range(1, max_columns):  
            self.check_diagonal_left_to_right(0, start_col, marker_current_player, marker_other_player, max_rows, max_columns)

    def check_diagonal_left_to_right(self, start_row, start_col, marker_current_player, marker_other_player, max_rows, max_columns):
        alignment = 0
        coords_alignment = []

        step_limit = min(max_rows - start_row, max_columns - start_col)
        for step in range(step_limit):
            i, j = start_row + step, start_col + step
            if self.boardList[i][j] == marker_current_player:
                alignment += 1
                coords_alignment.append((i, j))
                if alignment == 5:
                    self.deleting_player = self.current_player
                    self.pawn_delet = True
                    self.delete_alignments(coords_alignment)
                    break
            elif self.boardList[i][j] in [0, marker_other_player, 1, 2]:
                alignment = 0
                coords_alignment = []

    def alignment_diagonal_right_to_left(self):
        marker_current_player = self.current_player + 4
        marker_other_player = 5 if self.current_player % 2 == 0 else 6
        max_rows = 19
        max_columns = 11
        
        for start_row in range(max_rows):
            self.check_diagonal_right_to_left(start_row, max_columns - 1, marker_current_player, marker_other_player, max_rows, max_columns)
        for start_col in range(max_columns - 1):
            self.check_diagonal_right_to_left(0, start_col, marker_current_player, marker_other_player, max_rows, max_columns)

    def check_diagonal_right_to_left(self, start_row, start_col, marker_current_player, marker_other_player, max_rows, max_columns):
        alignment = 0
        coords_alignment = []

        step_limit = min(max_rows - start_row, start_col + 1) 
        for step in range(step_limit):
            i, j = start_row + step, start_col - step
            if self.boardList[i][j] == marker_current_player:
                alignment += 1
                coords_alignment.append((i, j))
                if alignment == 5:
                    self.deleting_player = self.current_player
                    self.pawn_delet = True
                    self.delete_alignments(coords_alignment)
                    break
            elif self.boardList[i][j] in [0, marker_other_player, 1, 2]:
                alignment = 0
                coords_alignment = []
    def multiple_alignements(self):
        self.check_alignemente_vertical_and_diagonal_one()
        self.check_alignemente_vertical_and_diagonal_two()
        self.alignment_diagonal_multiple()
        if self.choise_alignement==False:
            self.alignment_verification()

    def choise_alignements_destroy(self,v,w):
        coords_delete1 = []
        coords_delete2 = []
        if not self.choise_alignement:
            return
        hitbox_taille = 10
        for key, value in self.indexPosition.items():
            cell_x, cell_y = key
            if (cell_x - hitbox_taille < v < cell_x + hitbox_taille) and \
                (cell_y - hitbox_taille < w < cell_y + hitbox_taille):
                row, col = value
                for x, y in self.multiple1:
                    if x==row and y==col:
                        coords_delete1.append((x, y))
                for i, j in self.multiple2:
                    if i==row and j==col:
                        coords_delete2.append((i, j))
            if len(coords_delete1) == 1 and len(coords_delete2) == 0:
                coords_delete1=self.multiple1
                self.delete_alignments(coords_delete1)
                self.choise_alignement = False
                self.deleting_player = self.current_player%2+1
                self.pawn_delet = True
                self.multiple1 = []
                self.multiple2 = []
                
            elif len(coords_delete1) == 0 and len(coords_delete2) == 1:
                coords_delete2=self.multiple2
                self.delete_alignments(coords_delete2)
                self.choise_alignement = False
                self.deleting_player = self.current_player%2+1
                self.pawn_delet = True
                self.multiple1 = []
                self.multiple2 = []

    def check_alignemente_vertical_and_diagonal_one(self):
        coords_diagonal = []
        marker_current_player = self.current_player + 4
        marker_other_player = 5 if self.current_player % 2 == 0 else 6
        for col in range(11):
            alignment = 0
            coords= []
            for row in range(19):
                if self.boardList[row][col] == marker_current_player :
                    alignment += 1
                    coords.append((row, col))
                    if alignment == 5:
                        coords_vertical=coords
                        coords_diagonal = self.alignment_diag_left_to_right_multiple()
                        if len(coords_diagonal) == 5 and len(coords_vertical) == 5:
                            self.multiple1 = coords_diagonal
                            self.multiple2 = coords_vertical
                            self.choise_alignement = True
                            self.detected_multiple_alignements = True
                        
                elif self.boardList[row][col] in [0, marker_other_player, 1, 2]:
                    alignment = 0
                    coords_vertical = []
                

    def alignment_diag_left_to_right_multiple(self):
        marker_current_player = self.current_player + 4
        marker_other_player = 5 if self.current_player % 2 == 0 else 6
        max_rows = 19
        max_columns = 11
        coords = []

        for start_row in range(max_rows):
            result = self.check_diagonal_left_to_right_for_multiple_alignements(start_row, 0, marker_current_player, marker_other_player, max_rows, max_columns)
            if result:
                coords = result

        for start_col in range(1, max_columns):
            result = self.check_diagonal_left_to_right_for_multiple_alignements(0, start_col, marker_current_player, marker_other_player, max_rows, max_columns)
            if result:
                coords = result
        return coords if coords else []

    def check_diagonal_left_to_right_for_multiple_alignements(self, start_row, start_col, marker_current_player, marker_other_player, max_rows, max_columns):
        alignment = 0
        coords_alignment = []

        step_limit = min(max_rows - start_row, max_columns - start_col)
        for step in range(step_limit):
            i, j = start_row + step, start_col + step
            if self.boardList[i][j] == marker_current_player:
                alignment += 1
                coords_alignment.append((i, j))
                if alignment == 5:
                    return coords_alignment
            elif self.boardList[i][j] in [0, marker_other_player, 1, 2]:
                alignment = 0
                coords_alignment = []

        return []

    def check_alignemente_vertical_and_diagonal_two(self):
        coords_diagonal = []
        marker_current_player = self.current_player + 4
        marker_other_player = 5 if self.current_player % 2 == 0 else 6
        for col in range(11):
            alignment = 0
            coords_vertical = []
            for row in range(19):
                if self.boardList[row][col] == marker_current_player:
                    alignment += 1
                    coords_vertical.append((row, col))
                    if alignment == 5:
                        coords_diagonal = self.alignment_diagonal_right_to_left_multiple()
                        if len(coords_diagonal) == 5 and len(coords_vertical) == 5:
                            self.multiple1 = coords_diagonal
                            self.multiple2 = coords_vertical
                            self.choise_alignement = True
                            self.detected_multiple_alignements = True
                            break
                        
                elif self.boardList[row][col] in [0, marker_other_player, 1, 2]:
                    alignment = 0
                    coords_vertical = []         

    def check_diagonal_right_to_left_multiple_alignements(self, start_row, start_col, marker_current_player, marker_other_player, max_rows, max_columns):
        alignment = 0
        coords_alignment = []

        step_limit = min(max_rows - start_row, start_col + 1)
        for step in range(step_limit):
            i, j = start_row + step, start_col - step
            if self.boardList[i][j] == marker_current_player:
                alignment += 1
                coords_alignment.append((i, j))
                if alignment == 5:
                    return coords_alignment
            elif self.boardList[i][j] in [0, marker_other_player, 1, 2]:
                alignment = 0
                coords_alignment = []

        return []

    def alignment_diagonal_right_to_left_multiple(self):
        marker_current_player = self.current_player + 4
        marker_other_player = 5 if self.current_player % 2 == 0 else 6
        max_rows = 19
        max_columns = 11
        coords = []

        for start_row in range(max_rows):
            result = self.check_diagonal_right_to_left_multiple_alignements(start_row, max_columns - 1, marker_current_player, marker_other_player, max_rows, max_columns)
            if result:
                coords = result

        for start_col in range(max_columns - 1):
            result = self.check_diagonal_right_to_left_multiple_alignements(0, start_col, marker_current_player, marker_other_player, max_rows, max_columns)
            if result:
                coords = result

        return coords if coords else []

    def alignment_diagonal_multiple(self):
        coords1 = self.alignment_diag_left_to_right_multiple()
        coords2 = self.alignment_diagonal_right_to_left_multiple()
        if coords1 and len(coords1) == 5 and coords2 and len(coords2) == 5:
            self.multiple1 = coords1
            self.multiple2 = coords2
            self.choise_alignement = True
            self.detected_multiple_alignements = True
    def delete_alignments(self,coords):
        for x,y in coords:
            self.boardList[x][y]=0

    def delete_pawns(self, x, y):
        if not self.pawn_delet:
            return
        elif self.deleting_player == 2:
            while self.pawn_delet:
                self.computer_deletepawn()
            self.pawn_delet = False
        else:
            hitbox_taille = 20
            for key, value in self.indexPosition.items():
                cell_x, cell_y = key
                if (cell_x - hitbox_taille < x < cell_x + hitbox_taille) and \
                (cell_y - hitbox_taille < y < cell_y + hitbox_taille):
                    row, col = value
                    if self.boardList[row][col] == self.deleting_player:
                        self.boardList[row][col] = 0
                        self.number_pawn_delte[self.deleting_player] += 1
                        if self.number_pawn_delte[self.deleting_player] == 3:
                            self.victory_player = 1
                            self.display_winner()
                        self.pawn_delet = False
                        break

    def draw_button(self, text, x, y, width, height, action=None):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
            pygame.draw.rect(self.screen, (128, 128, 128), (x, y, width, height))
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 3)
            if mouse_click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.screen, (245, 245, 220), (x, y, width, height))
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 3)

        button_font = pygame.font.SysFont(None, 30)
        button_text = button_font.render(text, True, (0, 0, 0))
        text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(button_text, text_rect)

    def display_winner(self):
        dark_overlay = pygame.Surface(self.screen.get_size())
        dark_overlay.set_alpha(128)
        dark_overlay.fill((0, 0, 0))
        self.screen.blit(dark_overlay, (0, 0))

        self.screen.blit(self.fond, (0, 0))

        ring_radius = 30
        ring_thickness = 5
        ring_spacing = 50

        pygame.draw.rect(self.screen, (245, 245, 220), (300, 150, 600, 300))
        pygame.draw.rect(self.screen, (0, 0, 0), (300, 150, 600, 300), 10)

        if self.victory_player == 1:
            victory_font = pygame.font.SysFont(None, 70)
            victory_text = "Le Joueur 1 a gagné !"
            label = victory_font.render(victory_text, True, (0, 0, 0))
            label_rect = label.get_rect(center=(self.screen.get_rect().centerx, 250))
            self.screen.blit(label, label_rect)

        elif self.victory_player == 2:
            victory_font = pygame.font.SysFont(None, 70)
            victory_text = "L'ordinateur a gagné !"
            label = victory_font.render(victory_text, True, (0, 0, 0))
            label_rect = label.get_rect(center=(self.screen.get_rect().centerx, 250))
            self.screen.blit(label, label_rect)

        x = (self.screen_width - (4 * ring_radius + 3 * ring_spacing) - self.board_width) // 2 + 150
        y = self.screen_height - (2 * ring_radius + 20)
        for i in range(self.number_pawn_delte[1]):
            pygame.draw.circle(self.screen, self.color_player_1, (x + i * (ring_radius + ring_spacing), y - 250), ring_radius, ring_thickness)

        x_right = (self.screen_width + (4 * ring_radius + 3 * ring_spacing) - self.board_width) // 2 + 355
        y_right = self.screen_height - (2 * ring_radius + 20)
        for i in range(self.number_pawn_delte[2]-1, -1, -1):
            pygame.draw.circle(self.screen, self.color_player_2, (x_right - i * (ring_radius + ring_spacing), y_right - 250), ring_radius, ring_thickness)

        button_width = 200
        button_height = 50
        button_x = self.screen.get_rect().centerx - button_width * 1.25
        button_y = 600
        self.draw_button("Menu principal", button_x, button_y, button_width, button_height, self.return_main_menu)
        self.draw_button("Rejouer", button_x + button_width * 1.5, button_y, button_width, button_height, self.restart_game)

        pygame.display.flip()
    
    def draw_rings(self):
        ring_radius = 30
        ring_thickness = 5
        ring_spacing = 50

        x = (self.screen_width - (4 * ring_radius + 3 * ring_spacing) - self.board_width) // 2
        y = self.screen_height - (2 * ring_radius + 20)

        for i in range(3):
            if self.number_pawn_delte[1]  >= i + 1:
                color = self.color_player_1
            else:
                color = (128, 128, 128)

            pygame.draw.circle(self.screen, color, (x + i * (ring_radius + ring_spacing), y), ring_radius, ring_thickness)

        x = (self.screen_width + (4 * ring_radius + 3 * ring_spacing) - self.board_width) // 2 + 510
        y = self.screen_height - (2 * ring_radius + 20)

        for i in range(2, -1, -1):
            if self.number_pawn_delte[2]  >= i + 1:
                color = self.color_player_2
            else:
                color = (128, 128, 128)

            pygame.draw.circle(self.screen, color, (x - i * (ring_radius + ring_spacing), y), ring_radius, ring_thickness)

        if self.number_pawn_delte[1] == 3 or self.number_pawn_delte[2] == 3:
            self.game_over = True

    def restart_game(self):
        self.boardList = [[None,None,None,None,0,None,0,None,None,None,None],
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
        self.pawn_delet = False
        self.deleting_player = None
        self.number_pawn_delte = {1: 0, 2: 0}
        self.game_over = False
        self.bot_marker_placed = False
        self.positions_clics = []
        self.pawn_per_player = 5
        self.number_pawn_delte = {1: 0, 2: 0}

    def show_options(self):
        options_instance = options.Options(self.screen, self.screen.get_width(), self.screen.get_height())
        options_instance.run()
        self.volume = options_instance.get_volume()

    def return_main_menu(self):
        menu_instance = menu.Menu(self.screen, self.screen_width, self.screen_height)
        menu_instance.run()
        options_instance = options.Options(self.screen, self.screen_width, self.screen_height)
        self.volume = options_instance.get_volume()
        pass 

    def Computers(self):
        deplacement = False
        if self.current_player == 2:
            if self.pawn_on_board[2] < self.pawn_per_player:
                while not self.comptureur_pawn():
                    pass
            elif self.pawn_on_board[2] == self.pawn_per_player and not self.bot_marker_placed:
                while not self.computer_marker():
                    pass
                self.bot_marker_placed = True

            for j in range(11):
                for i in range(19):
                    if self.boardList[i][j] == 4:
                        self.place_markers[2] = True
                        self.place_markers[1] = False
                        while not deplacement:
                            deplacement = self.computer_deplacement(i, j)
                        self.bot_marker_placed = False

    def comptureur_pawn(self):
        i = random.randint(0, 18)
        j = random.randint(0, 10)
        if self.boardList[i][j] == 0:
            self.boardList[i][j] = 2
            self.pawn_on_board[2] += 1
            self.current_player = 1
            return True
        return False

    def computer_marker(self):
        if self.bot_marker_placed:
            return True
        i = random.randint(0, 18)
        j = random.randint(0, 10)
        if self.boardList[i][j] == 2:
            self.boardList[i][j] = 4
            self.bot_marker_placed = True
            return True
        return False

    def computer_deplacement(self, row_marker, cols_marker):
        row = random.randint(0, 18)
        cols = random.randint(0, 10)
        if cols - cols_marker == 0:
            if row_marker > row:
                self.check_vertical_high(row, cols, row_marker, cols_marker)
            elif row_marker < row:
                self.check_vertical_bottom(row, cols, row_marker, cols_marker)
        elif row_marker < row and cols_marker < cols:
            self.check_diagonal_right_low(row, cols, row_marker, cols_marker)
        elif row_marker > row and cols_marker < cols:
            self.check_diagonal_right_high(row, cols, row_marker, cols_marker)
        elif row_marker > row and cols_marker > cols:
            self.check_diagonal_left_high(row, cols, row_marker, cols_marker)
        elif row_marker < row and cols_marker > cols:
            self.check_diagonal_left_low(row, cols, row_marker, cols_marker)
        if self.boardList[row_marker][cols_marker] != 4:
            self.bot_marker_placed = False
            return True
        return False

    def computer_deletepawn(self):
        row = random.randint(0, 18)
        col = random.randint(0, 10)
        if self.boardList[row][col] == 2:
            self.boardList[row][col] = 0
            self.number_pawn_delte[self.deleting_player] += 1
            if self.number_pawn_delte[self.deleting_player] == 3:
                self.victory_player = 2
                self.display_winner()
            self.pawn_delet = False
            self.current_player = 1

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
            elif self.game_over:
                self.display_winner()
            else:
                self.show_player_turn()
                self.draw_remaining_pions()
                self.board.display_board(self.screen, self.board_x, self.board_y)
                self.Computers()
                self.draw_pawn()
                self.draw_marker()
                self.draw_solo_marqueur()
                self.draw_rings()

                pygame.draw.rect(self.screen, (245, 245, 220), self.pause_button_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), self.pause_button_rect, 2)

                self.screen.blit(pause_text, pause_text_rect)

            pygame.display.flip()

    def run(self):
        self.start()