import pygame
import random

# Tamaño de la ventana
ANCHO_VENTANA = 760
ALTO_VENTANA = 600

# Tamaño de los elementos
TAMANO_CELDA = 40
TAMANO_JUGADOR = 30
TAMANO_FANTASMA = 30

# Laberinto
laberinto = [
    "###################",
    "#...........#.....#",
    "#.#####.#####.###.#",
    "#.#.............#.#",
    "#.#.###.#######.#.#",
    "#.#.....#.....#.#.#",
    "#.#######.###.#.#.#",
    "#.......#...#.#.#.#",
    "#.#######.#.#.#.#.#",
    "#.........#.#.#.#.#",
    "###########.#.#.#.#",
    "#...........#.....#",
    "#.#####.#####.###.#",
    "#.#.............#.#",
    "#.###.###########.#",
    "#.....#.....#.....#",
    "#######.###.#######",
    "#...........#.....#",
    "#.###########.###.#",
    "#.................#",
    "###################"
]

# Direcciones de movimiento
ARRIBA = (0, -1)
ABAJO = (0, 1)
IZQUIERDA = (-1, 0)
DERECHA = (1, 0)

# Inicializar pygame
pygame.init()

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de Pacman")

# Cargar el fondo, el jugador y los fantasmas
fondo = pygame.image.load("assets/background.jpg").convert()
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))  # Escalar el fondo al tamaño de la ventana
jugador = pygame.transform.scale(pygame.image.load("assets/pacman.png").convert_alpha(), (TAMANO_JUGADOR, TAMANO_JUGADOR))
fantasma = pygame.transform.scale(pygame.image.load("assets/ghost.png").convert_alpha(), (TAMANO_FANTASMA, TAMANO_FANTASMA))
dot = pygame.transform.scale(pygame.image.load("assets/sandia.png").convert_alpha(), (TAMANO_CELDA, TAMANO_CELDA))
pared = pygame.transform.scale(pygame.image.load("assets/wall.jpg").convert(), (TAMANO_CELDA, TAMANO_CELDA))

# Obtener posición inicial del jugador
jugador_x = TAMANO_CELDA
jugador_y = TAMANO_CELDA

# Inicializar posición y dirección de los fantasmas
fantasmas = []
for i in range(4):
    x = random.randint(0, ANCHO_VENTANA // TAMANO_CELDA - 1) * TAMANO_CELDA
    y = random.randint(0, ALTO_VENTANA // TAMANO_CELDA - 1) * TAMANO_CELDA
    while abs(x - jugador_x) < 2 * TAMANO_CELDA and abs(y - jugador_y) < 2 * TAMANO_CELDA:
        x = random.randint(0, ANCHO_VENTANA // TAMANO_CELDA - 1) * TAMANO_CELDA
        y = random.randint(0, ALTO_VENTANA // TAMANO_CELDA - 1) * TAMANO_CELDA
    direccion = random.choice([ARRIBA, ABAJO, IZQUIERDA, DERECHA])
    fantasmas.append((x, y, direccion))

# Inicializar dots y score
dots = []
score = 0
for y, fila in enumerate(laberinto):
    for x, casilla in enumerate(fila):
        if casilla == '.':
            dot_x = x * TAMANO_CELDA + TAMANO_CELDA // 2
            dot_y = y * TAMANO_CELDA + TAMANO_CELDA // 2
            dots.append((dot_x, dot_y))

reloj = pygame.time.Clock()

# Cargar fuente de texto
fuente_score = pygame.font.Font(None, 36)
fuente = pygame.font.Font(None, 72)

# Variables de estado del juego
game_over = False

# Función para mover los fantasmas
def mover_fantasmas():
    for i, (x, y, direccion) in enumerate(fantasmas):
        opciones = []
        if y > TAMANO_CELDA and laberinto[(y - TAMANO_CELDA) // TAMANO_CELDA][x // TAMANO_CELDA] != '#':
            opciones.append(ARRIBA)
        if y < ALTO_VENTANA - 2 * TAMANO_CELDA and laberinto[(y + TAMANO_CELDA) // TAMANO_CELDA][x // TAMANO_CELDA] != '#':
            opciones.append(ABAJO)
        if x > TAMANO_CELDA and laberinto[y // TAMANO_CELDA][(x - TAMANO_CELDA) // TAMANO_CELDA] != '#':
            opciones.append(IZQUIERDA)
        if x < ANCHO_VENTANA - 2 * TAMANO_CELDA and laberinto[y // TAMANO_CELDA][(x + TAMANO_CELDA) // TAMANO_CELDA] != '#':
            opciones.append(DERECHA)

        if opciones:
            direccion = random.choice(opciones)
        x += direccion[0] * TAMANO_CELDA
        y += direccion[1] * TAMANO_CELDA
        fantasmas[i] = (x, y, direccion)

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()

    if not game_over:
        # Obtener las teclas presionadas
        teclas = pygame.key.get_pressed()

        # Calcular la posición de destino del jugador
        jugador_destino_x = jugador_x
        jugador_destino_y = jugador_y

        if teclas[pygame.K_UP]:
            jugador_destino_y = max(jugador_y - TAMANO_CELDA, TAMANO_CELDA)
        elif teclas[pygame.K_DOWN]:
            jugador_destino_y = min(jugador_y + TAMANO_CELDA, ALTO_VENTANA - TAMANO_JUGADOR - TAMANO_CELDA)
        elif teclas[pygame.K_LEFT]:
            jugador_destino_x = max(jugador_x - TAMANO_CELDA, TAMANO_CELDA)
        elif teclas[pygame.K_RIGHT]:
            jugador_destino_x = min(jugador_x + TAMANO_CELDA, ANCHO_VENTANA - TAMANO_JUGADOR - TAMANO_CELDA)

        # Verificar si el movimiento es permitido
        if laberinto[jugador_destino_y // TAMANO_CELDA][jugador_destino_x // TAMANO_CELDA] != '#':
            jugador_x = jugador_destino_x
            jugador_y = jugador_destino_y

        # Comprobar colisión entre el jugador y los dots
        for dot_x, dot_y in dots:
            if abs(dot_x - jugador_x) < TAMANO_JUGADOR and abs(dot_y - jugador_y) < TAMANO_JUGADOR:
                score += 1
                dots.remove((dot_x, dot_y))

        mover_fantasmas()  # Mover los fantasmas

        # Comprobar colisión entre el jugador y los fantasmas
        for x, y, _ in fantasmas:
            if abs(x - jugador_x) < TAMANO_JUGADOR and abs(y - jugador_y) < TAMANO_JUGADOR:
                game_over = True
                break

    ventana.blit(fondo, (0, 0))  # Dibujar el fondo

    # Dibujar el laberinto
    for y, fila in enumerate(laberinto):
        for x, casilla in enumerate(fila):
            if casilla == '#':
                ventana.blit(pared, (x * TAMANO_CELDA, y * TAMANO_CELDA))

    # Dibujar dots
    for dot_x, dot_y in dots:
        dot_rect = dot.get_rect(center=(dot_x, dot_y))
        ventana.blit(dot, dot_rect)

    ventana.blit(jugador, (jugador_x, jugador_y))  # Dibujar el jugador

    # Dibujar los fantasmas
    for x, y, _ in fantasmas:
        ventana.blit(fantasma, (x, y))

    # Dibujar score
    texto_score = fuente_score.render(f"Score: {score}", True, (255, 255, 255))
    ventana.blit(texto_score, (10, 10))

    if game_over:
        texto_game_over = fuente.render("Game Over", True, (255, 0, 0))
        texto_rect = texto_game_over.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        ventana.blit(texto_game_over, texto_rect)

    if score == 129:
        texto_win = fuente.render("You win", True, (0, 0, 255))
        texto_rect = texto_win.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        ventana.blit(texto_win, texto_rect)

    pygame.display.update()  # Actualizar la ventana
    reloj.tick(10)  # Controlar la velocidad del juego
