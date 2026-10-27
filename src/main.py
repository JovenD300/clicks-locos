import sys
import importlib

try:
    pygame = importlib.import_module("pygame")
except ModuleNotFoundError:
    raise SystemExit("Falta pygame. Instálalo con: python -m pip install pygame")

from github_sync import load_local_config, save_local_config, check_github_sync

pygame.init()

# Dimensiones adaptadas para móvil vertical sin ser excesivamente alta en PC
# (Se reduce de 480x800 a 360x600 manteniendo la proporción vertical)
WIDTH, HEIGHT = 360, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caballerito Jump")

clock = pygame.time.Clock()

# Carga de datos locales
config = load_local_config()
jumps = config.get("jumps", 0)
bg_index = config.get("background_index", 0)

# Verificación inicial en GitHub (Intervalo de 7 días)
check_github_sync()

# Posición y física del Caballerito (cubo)
char_width, char_height = 60, 80
char_x = WIDTH // 2 - char_width // 2
ground_y = HEIGHT - 160
char_y = ground_y
is_jumping = False
jump_vel = 0
gravity = 0.6

font = pygame.font.SysFont(None, 30)

running = True
while running:
    # Cambio de color de fondo según los bloques de 100 saltos (punto 4)
    if (bg_index // 1) % 2 == 0:
        screen.fill((25, 25, 35))
    else:
        screen.fill((45, 25, 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            # Acción al hacer click o toque (Punto 2)
            if not is_jumping:
                is_jumping = True
                jump_vel = -13
                jumps += 1
                
                # Actualiza índice de fondo cada 100 saltos exactos
                bg_index = jumps // 100
                
                # Guarda persistencia local
                config["jumps"] = jumps
                config["background_index"] = bg_index
                save_local_config(config)

    # Lógica de salto acumulativo
    if is_jumping:
        char_y += jump_vel
        jump_vel += gravity
        if char_y >= ground_y:
            char_y = ground_y
            is_jumping = False

    # Renderizado temporal del personaje y contadores
    pygame.draw.rect(screen, (0, 220, 120), (char_x, char_y, char_width, char_height)) # Placeholder del caballerito
    
    score_text = font.render(f"Saltos: {jumps}", True, (255, 255, 255))
    level_text = font.render(f"Fondo Nivel: {bg_index}", True, (200, 200, 200))
    
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 52))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
