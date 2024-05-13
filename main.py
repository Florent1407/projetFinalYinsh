import pygame
import sys
import menu
import Board

def main():
    pygame.init()

    info = pygame.display.Info()
    width, height = info.current_w, info.current_h

    window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

    menuinstance = menu.Menu(window, width, height)
    startgame = menuinstance.run()

    if startgame:
        gameInstance = Board.Game()
        gameInstance.start()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
