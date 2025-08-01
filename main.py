import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drop Zone Activa - Pygame")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)

# --------------------------------------------------
# Clase: DraggableRect
# Un objeto que se puede arrastrar
# --------------------------------------------------
class DraggableRect:
    def __init__(self, x, y, width, height, color, name="Objeto"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.name = name
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = mouse_x - self.rect.x
                self.offset_y = mouse_y - self.rect.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x - self.offset_x
                self.rect.y = mouse_y - self.offset_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Borde
        font = pygame.font.SysFont(None, 20)
        text = font.render(self.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


# --------------------------------------------------
# Clase: DropZone
# La zona que detecta si un objeto fue soltado dentro
# --------------------------------------------------
class DropZone:
    def __init__(self, x, y, width, height, color=GRAY, label="Drop Zone"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.highlight_color = LIGHT_BLUE
        self.label = label
        self.current_object = None  # Objeto actualmente dentro (opcional)
        self.objects_received = []  # Historial de objetos recibidos

    def handle_event(self, event, draggable_objects):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo soltado
                mouse_pos = event.pos
                # Verificar si el soltar ocurrió dentro de esta zona
                if self.rect.collidepoint(mouse_pos):
                    # Buscar qué objeto estaba siendo arrastrado y está sobre la zona
                    for obj in draggable_objects:
                        if (obj.dragging == False  # Ya no está en modo drag
                                and obj.rect.colliderect(self.rect)):
                            # Evitar duplicados
                            if obj not in self.objects_received:
                                self.objects_received.append(obj)
                                print(f"📦 ¡{self.label} recibió: '{obj.name}'!")
                                self.on_drop(obj)
                            return

    def on_drop(self, obj):
        # Puedes sobrescribir este método
        obj.rect.center = self.rect.center
        print(f"✅ {obj.name} centrado en la zona.")

    def draw(self, screen):
        # Dibujar fondo normal o resaltado
        color = self.highlight_color if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 3)

        # Etiqueta
        font = pygame.font.SysFont(None, 28)
        label_surface = font.render(self.label, True, DARK_GRAY)
        label_rect = label_surface.get_rect(center=(self.rect.centerx, self.rect.top + 20))
        screen.blit(label_surface, label_rect)

        # Mostrar cuántos objetos ha recibido
        if self.objects_received:
            count_font = pygame.font.SysFont(None, 20)
            count_text = count_font.render(f"Recibidos: {len(self.objects_received)}", True, (0, 0, 0))
            screen.blit(count_text, (self.rect.x + 10, self.rect.bottom - 25))


# --------------------------------------------------
# Crear objetos
# --------------------------------------------------
drag_objects = [
    DraggableRect(100, 100, 80, 80, RED, "Caja Roja"),
    DraggableRect(200, 300, 100, 60, GREEN, "Regalo Verde"),
    DraggableRect(300, 150, 90, 90, BLUE, "Bloque Azul"),
]

# Crear una Drop Zone
drop_zone = DropZone(600, 400, 160, 120, GRAY, "📦 Zona de Entrega")

# --------------------------------------------------
# Bucle principal
# --------------------------------------------------
running = True
while running:
    screen.fill(WHITE)

    # --- DIBUJAR EN ORDEN CORRECTO ---

    # 1. Dibujar la Drop Zone (primero = fondo)
    drop_zone.draw(screen)

    # 2. Dibujar TODOS los eventos y actualizaciones
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Manejar eventos de los objetos arrastrables
        for obj in drag_objects:
            obj.handle_event(event)

        # La Drop Zone verifica si algo fue soltado
        drop_zone.handle_event(event, drag_objects)

    # 3. Dibujar los objetos arrastrables (último = siempre arriba)
    for obj in drag_objects:
        obj.draw(screen)

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()