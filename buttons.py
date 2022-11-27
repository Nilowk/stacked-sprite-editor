import pygame as pg
import pygame.transform


class Button:
    def __init__(self, app, icon, pos: tuple, width: int, height: int, mod_id: int):
        self.app = app
        self.icon = pg.image.load(icon).convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (width - 8, height - 8))
        self.pos = pos
        self.width = width
        self.height = height
        self.mod_id = mod_id
        self.surf = pg.Surface([width, height])

    def draw(self):
        self.surf.fill((50, 50, 50) if not self.app.canvas.mod == self.mod_id else (30, 30, 30))
        self.surf.blit(self.icon, (4, 4))
        self.app.screen.blit(self.surf, self.pos)

    def update(self):
        pass

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - self.pos[0], pg.mouse.get_pos()[1] - self.pos[1])
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        self.app.canvas.mod = self.mod_id


class PaintButton(Button):
    def __init__(self, app, pos: tuple, width: int, height: int):
        super().__init__(app, "./icons/paint-icon.png", pos, width, height, 0)


class RubberButton(Button):
    def __init__(self, app, pos: tuple, width: int, height: int):
        super().__init__(app, "./icons/rubber-icon.png", pos, width, height, 1)