import pygame
import math
import Game

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
        color_board = (245, 245, 220)
        color_line = (0, 0, 0)  
        for point in self.points:
            x, y = board_x + point[0]*41, board_y + point[1]*23.5
            self.draw_hexagon(screen, x, y, 45, color_board)
            for i in range(6):
                start_point = (x + 45 * math.cos(2 * math.pi / 6 * i + math.pi/6),
                               y + 45 * math.sin(2 * math.pi / 6 * i + math.pi/6))
                end_point = (x + 45 * math.cos(2 * math.pi / 6 * (i + 3) + math.pi/6),
                             y + 45 * math.sin(2 * math.pi / 6 * (i + 3) + math.pi/6))
                pygame.draw.line(screen, color_line, start_point, end_point, 3)

    def reset_board(self):
        self.points.clear()
        self.place_points()

if __name__ == "__main__":
    game = Game()
    game.start()