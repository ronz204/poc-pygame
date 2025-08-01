import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drop Zone - Máximo 2 objetos")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)

# --------------------------------------------------
# Clase: DraggableRect
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
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        font = pygame.font.SysFont(None, 20)
        text = font.render(self.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


# --------------------------------------------------
# Clase: DropZone (actualizada - se auto-limpia)
# --------------------------------------------------
class DropZone:
    def __init__(self, x, y, width, height, color=GRAY, label="Drop Zone"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.highlight_color = LIGHT_BLUE
        self.label = label
        self.objects_inside = []  # Objetos actualmente dentro
        self.slot_positions = []
        self._calculate_slots()  # Calcular posiciones fijas

    def _calculate_slots(self):
        """Define 2 posiciones fijas dentro de la Drop Zone"""
        w, h = 80, 80
        padding = 20
        x1 = self.rect.x + padding
        x2 = self.rect.x + self.rect.width - padding - w
        y = self.rect.y + (self.rect.height - h) // 2
        self.slot_positions = [(x1, y), (x2, y)]

    def can_accept(self):
        """¿Puede aceptar más objetos?"""
        return len(self.objects_inside) < 2

    def is_inside(self, obj):
        """Verifica si el objeto está al menos parcialmente dentro"""
        return obj.rect.colliderect(self.rect)

    def update(self, draggable_objects):
        """Limpia objetos que ya no están dentro"""
        # Verificar si los objetos en objects_inside aún están dentro
        # Si no, removerlos
        self.objects_inside = [obj for obj in self.objects_inside if self.is_inside(obj)]

        # Reasignar posiciones a los que siguen dentro
        for i, obj in enumerate(self.objects_inside):
            if i < len(self.slot_positions):
                obj.rect.topleft = self.slot_positions[i]

    def handle_event(self, event, draggable_objects):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # Solo actuar si el soltar fue dentro de la zona
                if self.rect.collidepoint(event.pos) and self.can_accept():
                    for obj in draggable_objects:
                        if not obj.dragging and obj not in self.objects_inside:
                            if self.is_inside(obj):  # Verificar si está dentro
                                self.objects_inside.append(obj)
                                idx = len(self.objects_inside) - 1
                                obj.rect.topleft = self.slot_positions[idx]
                                print(f"✅ '{obj.name}' aceptado. ({len(self.objects_inside)}/2)")
                                self.on_drop(obj)
                                break

    def on_drop(self, obj):
        pass

    def draw(self, screen):
        # Fondo: resaltado si puede aceptar
        bg_color = self.highlight_color if self.can_accept() else (255, 200, 200)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, width=3, border_radius=12)

        # Etiqueta
        font = pygame.font.SysFont(None, 32, bold=True)
        label_surface = font.render(self.label, True, DARK_GRAY)
        label_rect = label_surface.get_rect(center=(self.rect.centerx, self.rect.top + 25))
        screen.blit(label_surface, label_rect)

        # Estado
        status_font = pygame.font.SysFont(None, 24)
        status_text = f"{len(self.objects_inside)}/2 ocupado(s)"
        text_color = (0, 150, 0) if self.can_accept() else (200, 0, 0)
        status_surface = status_font.render(status_text, True, text_color)
        screen.blit(status_surface, (self.rect.x + 20, self.rect.bottom - 30))

        # Guías visuales (opcional)
        for pos in self.slot_positions:
            pygame.draw.rect(screen, (255, 255, 0), (*pos, 80, 80), width=1, border_radius=5)


# --------------------------------------------------
# Crear objetos arrastrables
# --------------------------------------------------
drag_objects = [
    DraggableRect(100, 100, 80, 80, RED, "Rojo"),
    DraggableRect(200, 300, 80, 80, GREEN, "Verde"),
    DraggableRect(300, 150, 80, 80, BLUE, "Azul"),
    DraggableRect(400, 200, 80, 80, (255, 165, 0), "Naranja"),
]

# Crear Drop Zone grande (más que antes)
drop_zone = DropZone(300, 450, 300, 150, GRAY, "📦 Zona Segura")

# --------------------------------------------------
# Bucle principal
# --------------------------------------------------
# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # --- ACTUALIZAR ESTADO DE LA ZONA ---
    drop_zone.update(drag_objects)  # ← ¡Clave! Esto limpia objetos sacados

    # --- DIBUJAR ZONA PRIMERO ---
    drop_zone.draw(screen)

    # --- EVENTOS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Manejar eventos de los objetos
        for obj in drag_objects:
            obj.handle_event(event)

        # Drop Zone verifica si puede aceptar al soltar
        drop_zone.handle_event(event, drag_objects)

    # --- DIBUJAR OBJETOS ARRIBA ---
    for obj in drag_objects:
        obj.draw(screen)

    # Mensaje si está llena
    if not drop_zone.can_accept():
        font = pygame.font.SysFont(None, 28)
        msg = font.render("La zona está llena. No se aceptan más.", True, (200, 0, 0))
        screen.blit(msg, (250, 620))

    pygame.display.flip()

pygame.quit()
sys.exit()