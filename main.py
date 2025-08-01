import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and Drop - Soltar en zona específica")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Clase para objetos arrastrables
class DraggableRect:
    def __init__(self, x, y, width, height, color, name="Objeto"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.name = name

    def handle_event(self, event, drop_zone):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_x = event.pos[0] - self.rect.x
                self.offset_y = event.pos[1] - self.rect.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragging:
                    # Verificar si está dentro de la zona de drop al soltar
                    if self.rect.colliderect(drop_zone):
                        print(f"✅ '{self.name}' fue soltado correctamente en la zona de drop!")
                    else:
                        print(f"❌ '{self.name}' fue soltado fuera de la zona.")
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.x = event.pos[0] - self.offset_x
                self.rect.y = event.pos[1] - self.offset_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Borde

# -------------------------------
# Zona de drop (área donde queremos soltar)
drop_zone = pygame.Rect(600, 400, 150, 100)

# Lista de objetos arrastrables
drag_objects = [
    DraggableRect(100, 100, 80, 80, RED, "Cuadrado Rojo"),
    DraggableRect(200, 300, 100, 60, GREEN, "Rectángulo Verde"),
    DraggableRect(300, 150, 90, 90, BLUE, "Cuadrado Azul"),
]

# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # Dibujar la zona de drop
    pygame.draw.rect(screen, GRAY, drop_zone)
    pygame.draw.rect(screen, DARK_GRAY, drop_zone, 3)  # Borde más oscuro
    font = pygame.font.SysFont(None, 24)
    label = font.render("Zona Drop", True, DARK_GRAY)
    screen.blit(label, (drop_zone.x + 20, drop_zone.y + 40))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Enviar evento a cada objeto arrastrable (y pasarle la zona de drop)
        for obj in drag_objects:
            obj.handle_event(event, drop_zone)

    # Dibujar todos los objetos arrastrables
    for obj in drag_objects:
        obj.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()