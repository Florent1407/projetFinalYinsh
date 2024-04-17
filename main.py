import pygame
import sys
import menu
import plateau

def main():
    pygame.init()

    # Définir la résolution de l'écran
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h

    # Créer la fenêtre en plein écran
    window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

    menuinstance = menu.Menu(window, width, height)
    startgame = menuinstance.run()

    if startgame:
        jeuinstance = plateau.Jeu()
        jeuinstance.demarrer()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
