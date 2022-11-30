import pygame as pg
import pygame.transform
from settings import *
from PIL import Image


class Button:
    def __init__(self, app, pos: tuple, width: int, height: int):
        self.app = app
        self.pos = pos
        self.width = width
        self.height = height
        self.surf = pg.Surface([width, height])

    def update(self):
        pass

    def draw(self):
        self.app.screen.blit(self.surf, self.pos)

    def check_events(self, event):
        pass


class ToolsButton(Button):
    def __init__(self, app, icon: str, pos: tuple, width: int, height: int, mod_id: int):
        super().__init__(app, pos, width, height)
        self.icon = pg.image.load(icon).convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (width - 8, height - 8))
        self.mod_id = mod_id

    def draw(self):
        self.surf.fill((50, 50, 50) if not self.app.canvas.mod == self.mod_id else (30, 30, 30))
        self.surf.blit(self.icon, ((self.width / 2) - (self.icon.get_width() / 2), (self.height / 2) - (self.icon.get_height() / 2)))
        super().draw()

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - self.pos[0], pg.mouse.get_pos()[1] - self.pos[1])
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        self.app.canvas.mod = self.mod_id


class PaintButton(ToolsButton):
    def __init__(self, app, pos: tuple, width: int, height: int):
        super().__init__(app, "./icons/paint-icon.png", pos, width, height, 0)


class RubberButton(ToolsButton):
    def __init__(self, app, pos: tuple, width: int, height: int):
        super().__init__(app, "./icons/rubber-icon.png", pos, width, height, 1)


class StackButton(Button):
    def __init__(self, manager, pos: tuple, width: int, height: int, index: int):
        super().__init__(manager.app, pos, width, height)
        self.manager = manager
        self.image = Image.new("RGBA", (GRID_WIDTH, GRID_HEIGHT), (0, 0, 0, 0))
        self.index = index
        self.font = pg.font.SysFont("Comic Sans MS", self.height - 8)
        self.img = self.font.render("stack " + str(self.index + 1), True, (255, 255, 255))
        self.grid = [[(0, 0, 0, 0) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.surf = pg.Surface([width, height])

    def update_grid(self, x, y):
        self.grid = self.manager.app.canvas.grid
        self.image.putpixel((x, y), self.grid[y][x])
        self.app.render_window.reload(x, y)

    def render(self):
        self.img = self.font.render("stack " + str(self.index + 1), True, (255, 255, 255))

    def draw(self):
        self.surf.fill((50, 50, 50) if self.manager.app.canvas.stack != self.index else (30, 30, 30))
        self.surf.blit(self.img, ((self.width / 2) - (self.img.get_width() / 2), (self.height / 2) - (self.img.get_height() / 2)))
        self.manager.surf.blit(self.surf, self.pos)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        self.manager.app.canvas.stack = self.index
                        self.manager.app.canvas.grid = self.grid


class ManagerButton(Button):
    def __init__(self, manager, icon: str, pos: tuple, width: int, height: int):
        super().__init__(manager.app, pos, width, height)
        self.manager = manager
        self.icon = pg.image.load(icon).convert_alpha()
        self.icon = pg.transform.scale(self.icon, (self.width - 8, self.height - 8))

    def draw(self):
        self.surf.fill((50, 50, 50))
        self.surf.blit(self.icon, ((self.width / 2) - (self.icon.get_width() / 2), (self.height / 2) - (self.icon.get_height() / 2)))
        self.manager.surf.blit(self.surf, self.pos)


class AddButton(ManagerButton):
    def __init__(self, manager, pos: tuple, width: int, height: int):
        super().__init__(manager, "./icons/add-icon.png", pos, width, height)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        self.manager.stack_buttons.insert(self.manager.app.canvas.stack + 1, StackButton(self.manager, (5, 30 * len(self.manager.stack_buttons) + 5), self.manager.width - 10, 25, 0))
                        self.manager.app.canvas.stack += 1
                        if len(self.manager.stack_buttons) >= 8:
                            self.manager.stack_buttons_interval[0] = (len(self.manager.stack_buttons) - 1) - 7
                            self.manager.stack_buttons_interval[1] = len(self.manager.stack_buttons) - 1
                        else:
                            self.manager.stack_buttons_interval[1] = len(self.manager.stack_buttons) - 1
                        self.manager.reload_stack_index()
                        self.manager.app.canvas.grid = self.manager.stack_buttons[self.manager.app.canvas.stack].grid
                        self.app.render_window.reload_stack()


class RemoveButton(ManagerButton):
    def __init__(self, manager, pos: tuple, width: int, height: int):
        super().__init__(manager, "./icons/remove-icon.png", pos, width, height)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if len(self.manager.stack_buttons) > 1:
                    pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                    if not pos[0] < 0 and not pos[1] < 0:
                        if not pos[0] > self.width and not pos[1] > self.height:
                            if self.manager.app.canvas.stack >= len(self.manager.stack_buttons) - 1:
                                self.manager.app.canvas.stack = len(self.manager.stack_buttons) - 2
                            self.manager.stack_buttons.remove(self.manager.stack_buttons[self.manager.app.canvas.stack])
                            if len(self.manager.stack_buttons) > 8 and self.manager.stack_buttons_interval[0] != 0:
                                self.manager.stack_buttons_interval[0] -= 1
                                self.manager.stack_buttons_interval[1] -= 1
                            self.manager.app.canvas.grid = self.manager.stack_buttons[self.manager.app.canvas.stack].grid
                            self.manager.reload_stack_index()
                            self.app.render_window.reload_stack()


class UpButton(ManagerButton):
    def __init__(self, manager, pos: tuple, width: int, height: int):
        super().__init__(manager, "./icons/up-icon.png", pos, width, height)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        if self.manager.stack_buttons_interval[0] > 0:
                            self.manager.stack_buttons_interval[0] -= 1
                            self.manager.stack_buttons_interval[1] -= 1
                            self.manager.reload_stack_index()


class DownButton(ManagerButton):
    def __init__(self, manager, pos: tuple, width: int, height: int):
        super().__init__(manager, "./icons/down-icon.png", pos, width, height)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        if self.manager.stack_buttons_interval[1] < len(self.manager.stack_buttons) - 1:
                            self.manager.stack_buttons_interval[0] += 1
                            self.manager.stack_buttons_interval[1] += 1
                            self.manager.reload_stack_index()


class Input:
    def __init__(self, color_selector, pos, width, height):
        self.color_selector = color_selector
        self.num = "255"
        self.pos = pos
        self.width = width
        self.height = height
        self.font = pg.font.SysFont("Comic Sans MS", self.height - 8)
        self.img = self.font.render(self.num, True, (255, 255, 255))
        self.surf = pg.Surface([width, height])
        self.selected = False

    def draw(self):
        pg.draw.rect(self.surf, (255, 255, 255), (0, 0, self.width, self.height))
        pg.draw.rect(self.surf, (0, 0, 30), (2, 2, self.width - 4, self.height - 4))
        self.surf.blit(self.img, ((self.width / 2) - (self.img.get_width() / 2), (self.height / 2) - (self.img.get_height() / 2)))
        self.color_selector.surf.blit(self.surf, self.pos)

    def update(self):
        pass

    def render(self):
        self.img = self.font.render(self.num, True, (255, 255, 255))
        self.color_selector.app.canvas.update_color()

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                p = (pg.mouse.get_pos()[0] - self.pos[0] + self.color_selector.pos[0], pg.mouse.get_pos()[1] - self.pos[1] + self.color_selector.pos[1])
                if not p[0] < 0 and not p[1] < 0:
                    if not p[0] > self.width and not p[1] > self.height:
                        self.selected = True
                    else:
                        self.selected = False
                else:
                    self.selected = False
        if event.type == pg.KEYDOWN:
            if self.selected:
                if event.key == pg.K_BACKSPACE:
                    self.num = self.num[0:-1]
                    self.render()
                elif pg.key.name(event.key)[1:-1].isdigit():
                    next_num = self.num + pg.key.name(event.key)[1:-1]
                    if int(next_num) <= 255:
                        self.num = next_num
                        self.render()

