import pygame
import sys

# Dimensiones de la ventana
ANCHO_VENTANA = 760
ALTO_VENTANA = 600

# Tamaño de cada celda en el laberinto
TAMANO_CELDA = 40

# Colores
COLOR_FONDO = (0, 0, 0)
COLOR_FINAL = (0, 0, 0)

SCORE = 0

# Texturas
textura_fondo = pygame.transform.scale(pygame.image.load("assets/background.jpg"), (ANCHO_VENTANA, ALTO_VENTANA))
textura_pared = pygame.transform.scale(pygame.image.load("assets/wall.jpg"), (TAMANO_CELDA, TAMANO_CELDA))
textura_sandia = pygame.transform.scale(pygame.image.load("assets/sandia.png"), (TAMANO_CELDA, TAMANO_CELDA))
textura_fantasma = pygame.transform.scale(pygame.image.load("assets/ghost.png"), (TAMANO_CELDA, TAMANO_CELDA))
textura_jugador = pygame.transform.scale(pygame.image.load("assets/ave.png"), (TAMANO_CELDA, TAMANO_CELDA))
textura_house = pygame.transform.scale(pygame.image.load("assets/house.png"), (TAMANO_CELDA, TAMANO_CELDA))

# Mapa del laberinto
laberinto = [
    "###################",
    "# ..........#.....#",
    "#.#####.#####.###.#",
    "#.#..$..........#.#",
    "#.#.###.#######.#.#",
    "#$#.....#.....#.#.#",
    "#.#######.###.#$#.#",
    "#.......#...#.#.#.#",
    "#.#######.#.#.#.#.#",
    "#.........#.#.#.#.#",
    "###########.#.#.#.#",
    "#...........#.....#",
    "#.#####.#####.###.#",
    "#.#.........$...#.#",
    "##########%########"
]

# Inicialización de Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laberinto")

jugador_x = 1
jugador_y = 1
fuente = pygame.font.Font(None, 70)
fuente_score = pygame.font.Font(None, 40)
pausado = False

def dibujar_laberinto():
    # Dibuja el laberinto en la ventana
    for y in range(len(laberinto)):
        for x in range(len(laberinto[y])):
            if laberinto[y][x] == "#":
                ventana.blit(textura_pared, (x * TAMANO_CELDA, y * TAMANO_CELDA))
            elif laberinto[y][x] == ".":
                ventana.blit(textura_sandia, (x * TAMANO_CELDA, y * TAMANO_CELDA))
            elif laberinto[y][x] == "$":
                ventana.blit(textura_fantasma, (x * TAMANO_CELDA, y * TAMANO_CELDA))
            elif laberinto[y][x] == "%":
                ventana.blit(textura_house, (x * TAMANO_CELDA, y * TAMANO_CELDA))

def verificar_victoria(jugador_x, jugador_y):
    # Verifica si el jugador ha ganado o perdido
    global pausado
    if laberinto[jugador_y][jugador_x] == "%":
        if SCORE == 1240:
            pausado = True
            mensaje = fuente.render("You win", True, (0, 0, 255))
            ventana.blit(mensaje, (ANCHO_VENTANA // 2 - mensaje.get_width() // 2, ALTO_VENTANA // 2 - mensaje.get_height() // 2))
    elif laberinto[jugador_y][jugador_x] == "$":
        pausado = True
        mensaje = fuente.render("Game over", True, (255, 0, 0))
        ventana.blit(mensaje, (ANCHO_VENTANA // 2 - mensaje.get_width() // 2, ALTO_VENTANA // 2 - mensaje.get_height() // 2))


# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if not pausado:
                if event.key == pygame.K_UP:
                    if laberinto[jugador_y - 1][jugador_x] != "#":
                        if laberinto[jugador_y - 1][jugador_x] == ".":
                            SCORE += 10
                            laberinto[jugador_y - 1] = laberinto[jugador_y - 1][:jugador_x] + " " + laberinto[jugador_y - 1][jugador_x + 1:]
                        jugador_y -= 1

                elif event.key == pygame.K_DOWN:
                    if jugador_y + 1 < len(laberinto) and laberinto[jugador_y + 1][jugador_x] != "#":
                        if laberinto[jugador_y + 1][jugador_x] == ".":
                            SCORE += 10
                            laberinto[jugador_y + 1] = laberinto[jugador_y + 1][:jugador_x] + " " + laberinto[jugador_y + 1][jugador_x + 1:]
                        jugador_y += 1
                        
                elif event.key == pygame.K_LEFT:
                    if laberinto[jugador_y][jugador_x - 1] != "#":
                        if laberinto[jugador_y][jugador_x - 1] == ".":
                            SCORE += 10
                            laberinto[jugador_y] = laberinto[jugador_y][:jugador_x - 1] + " " + laberinto[jugador_y][jugador_x:]
                        jugador_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if laberinto[jugador_y][jugador_x + 1] != "#":
                        if laberinto[jugador_y][jugador_x + 1] == ".":
                            SCORE += 10
                            laberinto[jugador_y] = laberinto[jugador_y][:jugador_x + 1] + " " + laberinto[jugador_y][jugador_x + 2:]
                        jugador_x += 1

    ventana.blit(textura_fondo, (0, 0))
    dibujar_laberinto()
    ventana.blit(textura_jugador, (jugador_x * TAMANO_CELDA, jugador_y * TAMANO_CELDA))
    # Dibujar el texto "Score"
    texto_score = fuente_score.render(f"Score: {SCORE}", True, (255, 255, 255))
    ventana.blit(texto_score, (10, 10))

    verificar_victoria(jugador_x, jugador_y)
    pygame.display.update()
