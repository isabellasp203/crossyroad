import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
DORADO = (234, 190, 63)
# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Definir velocidad de movimiento del jugador
VELOCIDAD_JUGADOR = 5

# Clase para el jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO - 50)

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= VELOCIDAD_JUGADOR
        if teclas[pygame.K_RIGHT]:
            self.rect.x += VELOCIDAD_JUGADOR
        if teclas[pygame.K_UP]:
            self.rect.y -= VELOCIDAD_JUGADOR
        if teclas[pygame.K_DOWN]:
            self.rect.y += VELOCIDAD_JUGADOR

# Clase para los enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, color, velocidad):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(0, ALTO - self.rect.height)
        self.velocidad = velocidad

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.rect.y = 0
            self.rect.x = random.randint(0, ANCHO - self.rect.width)

# Clase para la meta
class Meta(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(DORADO)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, ANCHO - 50), random.randint(50, ALTO - 50))

# Función para mostrar el menú de selección de dificultad
def mostrar_menu(pantalla):
    pantalla.fill(BLANCO)
    fuente = pygame.font.SysFont(None, 40)
    texto_facil = fuente.render("Fácil", True, NEGRO)
    texto_dificil = fuente.render("Difícil", True, NEGRO)
    rect_facil = texto_facil.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    rect_dificil = texto_dificil.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
    pantalla.blit(texto_facil, rect_facil)
    pantalla.blit(texto_dificil, rect_dificil)
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if rect_facil.collidepoint(x, y):
                    return 'facil'
                elif rect_dificil.collidepoint(x, y):
                    return 'dificil'

# Función principal
def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Crossyroad")

    clock = pygame.time.Clock()
    jugador = Jugador()
    enemigos_verdes = pygame.sprite.Group()
    enemigos_rojos = pygame.sprite.Group()
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(jugador)

    # Mostrar menú de selección de dificultad
    dificultad = mostrar_menu(pantalla)

    # Ajustar las velocidades según la dificultad
    if dificultad == 'facil':
        VELOCIDAD_ENEMIGO_VERDE = 2
        VELOCIDAD_ENEMIGO_ROJO = 3  
    else:  # dificultad difícil
        VELOCIDAD_ENEMIGO_VERDE = 4  
        VELOCIDAD_ENEMIGO_ROJO = 6  

    # Crear enemigos verdes
    for _ in range(10):
        enemigo_verde = Enemigo(VERDE, VELOCIDAD_ENEMIGO_VERDE)
        enemigos_verdes.add(enemigo_verde)
        todos_los_sprites.add(enemigo_verde)

    # Crear enemigos rojos
    for _ in range(10):
        enemigo_rojo = Enemigo(ROJO, VELOCIDAD_ENEMIGO_ROJO)
        enemigos_rojos.add(enemigo_rojo)
        todos_los_sprites.add(enemigo_rojo)

    meta = Meta()
    todos_los_sprites.add(meta)

    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        todos_los_sprites.update()

        # Verificar colisiones con la meta
        if pygame.sprite.collide_rect(jugador, meta):
            print("¡Ganaste!")
            jugando = False

        # Verificar colisiones con los enemigos
        if pygame.sprite.spritecollide(jugador, enemigos_verdes, False) or \
           pygame.sprite.spritecollide(jugador, enemigos_rojos, False):
            print("Game Over")
            jugando = False

        pantalla.fill(BLANCO)
        todos_los_sprites.draw(pantalla)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Llamar a la función principal
if __name__ == "__main__":
    main()
