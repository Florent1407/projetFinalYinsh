import pygame
import random
from Game import *

class GameVsComputer(Game):
    def __init__(self):
        super ().__init__()
        self.bot_marker_placed = False
        self.pawn_delet = False
        self.deleting_player = None
        self.number_pawn_delte = {1: 0, 2: 0}
        self.game_over = False
        self.victory_player = 0
    
    def delete_pawns(self, x, y):
        print("delete_pawns")
        print(self.current_player)
        if not self.pawn_delet:
            return
        elif self.current_player == 2:
            while self.pawn_delet:
                self.computer_deletepawn()
            self.pawn_delet = False
        elif self.current_player == 1:
            hitbox_taille = 20
            for key, value in self.indexPosition.items():
                cell_x, cell_y = key
                if (cell_x - hitbox_taille < x < cell_x + hitbox_taille) and \
                (cell_y - hitbox_taille < y < cell_y + hitbox_taille):
                    row, col = value
                    if self.boardList[row][col] == self.current_player:
                        self.boardList[row][col] = 0
                        self.number_pawn_delte[self.deleting_player] += 1
                        self.current_player = self.current_player % 2 + 1
                        if self.number_pawn_delte[self.deleting_player] == 3:
                            self.victory_player = 2
                            self.display_winner()
                        self.pawn_delet = False
                        break

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

        if self.current_player == 1:
            self.victory_player = 2
        else:
            self.victory_player = 1

        victory_font = pygame.font.SysFont(None, 70)
        victory_text = f"Joueur {self.current_player} a gagné !"
        label = victory_font.render(victory_text, True, (0, 0, 0))
        label_rect = label.get_rect(center=(self.screen.get_rect().centerx, 250))
        self.screen.blit(label, label_rect)

        x = (self.screen_width - (4 * ring_radius + 3 * ring_spacing) - self.board_width) // 2 + 150
        y = self.screen_height - (2 * ring_radius + 20)
        for i in range(self.number_pawn_delte[2]):
            pygame.draw.circle(self.screen, self.color_player_1, (x + i * (ring_radius + ring_spacing), y - 250), ring_radius, ring_thickness)

        x_right = (self.screen_width + (4 * ring_radius + 3 * ring_spacing) - self.board_width) // 2 + 355
        y_right = self.screen_height - (2 * ring_radius + 20)
        for i in range(self.number_pawn_delte[1] - 1, -1, -1):
            pygame.draw.circle(self.screen, self.color_player_2, (x_right - i * (ring_radius + ring_spacing), y_right - 250), ring_radius, ring_thickness)

        button_width = 200
        button_height = 50
        button_x = self.screen.get_rect().centerx - button_width * 1.25
        button_y = 600
        self.draw_button("Menu principal", button_x, button_y, button_width, button_height, self.return_main_menu)
        self.draw_button("Rejouer", button_x + button_width * 1.5, button_y, button_width, button_height, self.restart_game)

        pygame.display.flip()

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