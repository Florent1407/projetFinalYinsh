import pygame
from Game import Game

class BlitzGame(Game):
    def __init__(self):
        super().__init__()

    def alignment_verification(self):
        self.vertical_alignment()
        self.alignment_diag_left_to_right()
        self.alignment_diagonal_right_to_left()

        if self.pawn_delet:
            self.game_over = True
            self.current_player = self.current_player % 2 + 1
            
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
                self.draw_pawn()
                self.draw_marker()
                self.draw_solo_marqueur()

                pygame.draw.rect(self.screen, (245, 245, 220), self.pause_button_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), self.pause_button_rect, 2)

                self.screen.blit(pause_text, pause_text_rect)

            pygame.display.flip()

    def run(self):
        self.start()