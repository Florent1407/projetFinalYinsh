import pygame
import sys
import menu
import plateau

def main():
    pygame.init()

    menuinstance = menu.Menu(pygame.display.setmode((1100, 700)), 1100, 700)
    startgame = menuinstance.run()

    if startgame:
        gameInstance = plateau.Game()
        gameInstance.start()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
