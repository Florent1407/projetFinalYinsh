import pygame
import sys
import menu
import Board

def main():
    pygame.init()

    menuinstance = menu.Menu(pygame.display.setmode((1100, 700)), 1100, 700)
    startgame = menuinstance.run()

    if startgame:
        gameInstance = Board.Game()
        gameInstance.start()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
