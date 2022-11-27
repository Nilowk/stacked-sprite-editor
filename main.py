import pygame as pg
from pygame import gfxdraw
import inspect
import buttons
from settings import *
import sys


class Input:
    def __init__(self, app, pos, width, height):
        self.app = app
        self.num = "255"
        self.pos = pos
        self.width = width
        self.height = height
        self.surf = pg.Surface([width, height])
        self.selected = False

    def draw(self):
        font = pg.font.SysFont("Comic Sans MS", self.height - 8)
        img = font.render(self.num, True, (255, 255, 255))
        pg.draw.rect(self.surf, (255, 255, 255), (0, 0, self.width, self.height))
        pg.draw.rect(self.surf, (0, 0, 30), (2, 2, self.width - 4, self.height - 4))
        self.surf.blit(img, ((self.width / 2) - (img.get_width() / 2), (self.height / 2) - (img.get_height() / 2)))
        self.app.screen.blit(self.surf, self.pos)

    def update(self):
        pass

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                p = (pg.mouse.get_pos()[0] - self.pos[0], pg.mouse.get_pos()[1] - self.pos[1])
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
                elif pg.key.name(event.key)[1:-1].isdigit():
                    next_num = self.num + pg.key.name(event.key)[1:-1]
                    if int(next_num) <= 255:
                        self.num = next_num


class ImageButton:
    def __init__(self, manager, pos: tuple, width: int, height: int, index, grid: list):
        self.manager = manager
        self.pos = pos
        self.width = width
        self.height = height
        self.index = index
        self.grid = grid
        self.surf = pg.Surface([width, height])

    def update(self):
        self.grid = self.manager.app.canvas.grid

    def draw(self):
        font = pg.font.SysFont("Comic Sans MS", self.height - 8)
        img = font.render("stack " + str(self.index + 1), True, (255, 255, 255))
        self.surf.fill((50, 50, 50) if self.manager.app.canvas.stack != self.index else (30, 30, 30))
        self.surf.blit(img, ((self.width / 2) - (img.get_width() / 2), (self.height / 2) - (img.get_height() / 2)))
        self.manager.surf.blit(self.surf, self.pos)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        self.manager.app.canvas.stack = self.index
                pos = (pg.mouse.get_pos()[0] - self.manager.app.canvas.surf_pos[0], pg.mouse.get_pos()[1] - self.manager.app.canvas.surf_pos[1])
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > GRID_WIDTH * BLOCK_SIZE and not pos[1] > GRID_HEIGHT * BLOCK_SIZE:
                        if self.manager.app.canvas.stack == self.index:
                            self.update()


class AddButton:
    def __init__(self, manager, pos: tuple, width: int, height: int):
        self.manager = manager
        self.pos = pos
        self.width = width
        self.height = height
        self.surf = pg.Surface([width, height])

    def update(self):
        pass

    def draw(self):
        font = pg.font.SysFont("Comic Sans MS", self.height)
        img = font.render("+", True, (255, 255, 255))
        self.surf.fill((50, 50, 50))
        self.surf.blit(img, (7, -7))
        self.manager.surf.blit(self.surf, self.pos)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        self.manager.image_buttons.insert(self.manager.app.canvas.stack + 1, ImageButton(self.manager, (5, 30 * len(self.manager.image_buttons) + 5), self.manager.width - 10, 25, 0, [[(0, 0, 0, 0) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]))
                        self.manager.app.canvas.stack += 1
                        if len(self.manager.image_buttons) >= 8:
                            self.manager.image_buttons_interval[0] = (len(self.manager.image_buttons) - 1) - 7
                            self.manager.image_buttons_interval[1] = len(self.manager.image_buttons) - 1
                        else:
                            self.manager.image_buttons_interval[1] = len(self.manager.image_buttons) - 1
                        self.manager.reload_stack_index()


class RemoveButton:
    def __init__(self, manager, pos: tuple, width: int, height: int):
        self.manager = manager
        self.pos = pos
        self.width = width
        self.height = height
        self.surf = pg.Surface([width, height])

    def update(self):
        pass

    def draw(self):
        font = pg.font.SysFont("Comic Sans MS", self.height)
        img = font.render("-", True, (255, 255, 255))
        self.surf.fill((50, 50, 50))
        self.surf.blit(img, (7, -7))
        self.manager.surf.blit(self.surf, self.pos)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if len(self.manager.image_buttons) > 1:
                    pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                    if not pos[0] < 0 and not pos[1] < 0:
                        if not pos[0] > self.width and not pos[1] > self.height:
                            if self.manager.app.canvas.stack >= len(self.manager.image_buttons) - 1:
                                self.manager.app.canvas.stack = len(self.manager.image_buttons) - 2
                            self.manager.image_buttons.remove(self.manager.image_buttons[self.manager.app.canvas.stack])
                            if len(self.manager.image_buttons) > 8 and self.manager.image_buttons_interval[0] != 0:
                                self.manager.image_buttons_interval[0] -= 1
                                self.manager.image_buttons_interval[1] -= 1
                            self.manager.reload_stack_index()


class UpButton:
    def __init__(self, manager, pos: tuple, width: int, height: int):
        self.manager = manager
        self.pos = pos
        self.width = width
        self.height = height
        self.surf = pg.Surface([width, height])

    def update(self):
        pass

    def draw(self):
        icon = pg.image.load("./icons/up-icon.png").convert_alpha()
        icon = pg.transform.scale(icon, (self.width - 8, self.height - 8))
        self.surf.fill((50, 50, 50))
        self.surf.blit(icon, ((self.width / 2) - (icon.get_width() / 2), (self.height / 2) - (icon.get_height() / 2)))
        self.manager.surf.blit(self.surf, self.pos)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        if self.manager.image_buttons_interval[0] > 0:
                            self.manager.image_buttons_interval[0] -= 1
                            self.manager.image_buttons_interval[1] -= 1
                            self.manager.reload_stack_index()


class DownButton:
    def __init__(self, manager, pos: tuple, width: int, height: int):
        self.manager = manager
        self.pos = pos
        self.width = width
        self.height = height
        self.surf = pg.Surface([width, height])

    def update(self):
        pass

    def draw(self):
        icon = pg.image.load("./icons/down-icon.png").convert_alpha()
        icon = pg.transform.scale(icon, (self.width - 8, self.height - 8))
        self.surf.fill((50, 50, 50))
        self.surf.blit(icon, ((self.width / 2) - (icon.get_width() / 2), (self.height / 2) - (icon.get_height() / 2)))
        self.manager.surf.blit(self.surf, self.pos)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - (self.manager.pos[0] + self.pos[0]), pg.mouse.get_pos()[1] - (self.manager.pos[1] + self.pos[1]))
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > self.width and not pos[1] > self.height:
                        if self.manager.image_buttons_interval[1] < len(self.manager.image_buttons) - 1:
                            self.manager.image_buttons_interval[0] += 1
                            self.manager.image_buttons_interval[1] += 1
                            self.manager.reload_stack_index()


class Manager:
    def __init__(self, app, pos: tuple, width: int, height: int):
        self.app = app
        self.width = width
        self.height = height
        self.pos = pos
        self.image_buttons = [ImageButton(self, (5, 5), width - 10, 25, 0, [[(0, 0, 0, 0) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)])]
        self.add_button = AddButton(self, (5, self.height - 30), 25, 25)
        self.remove_button = RemoveButton(self, (35, self.height - 30), 25, 25)
        self.up_button = UpButton(self, (65, self.height - 30), 25, 25)
        self.down_button = DownButton(self, (95, self.height - 30), 25, 25)
        self.selected = 0
        self.image_buttons_interval = [0, 0]
        self.surf = pg.Surface([width, height])

    def update(self):
        self.add_button.update()
        self.remove_button.update()
        self.up_button.update()
        self.down_button.update()

    def reload_stack_index(self):
        for stack in self.image_buttons:
            index = self.image_buttons.index(stack)
            stack.index = index
            if self.image_buttons_interval[0] <= index <= self.image_buttons_interval[1]:
                index = index - self.image_buttons_interval[0]
                stack.pos = (5, 30 * index + 5)

    def draw(self):
        self.surf.fill((100, 100, 100))
        for ib in self.image_buttons:
            if self.image_buttons_interval[0] <= ib.index <= self.image_buttons_interval[1]:
                ib.draw()
        self.add_button.draw()
        self.remove_button.draw()
        self.up_button.draw()
        self.down_button.draw()
        self.app.screen.blit(self.surf, self.pos)

    def check_events(self, event):
        for ib in self.image_buttons:
            if self.image_buttons_interval[0] <= ib.index <= self.image_buttons_interval[1]:
                ib.check_events(event)
        self.add_button.check_events(event)
        self.remove_button.check_events(event)
        self.up_button.check_events(event)
        self.down_button.check_events(event)


class Canvas:
    def __init__(self, app):
        self.app = app
        self.color = (0, 0, 0, 255)
        self.surf = pg.Surface([GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE])
        self.surf_pos = (0, HEIGHT - (GRID_HEIGHT * BLOCK_SIZE))
        self.mod = 0
        self.stack = 0
        self.grid = [[(0, 0, 0, 0) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

    def update(self):
        r = int(self.app.inputs[0].num) if self.app.inputs[0].num != "" else 0
        g = int(self.app.inputs[1].num) if self.app.inputs[1].num != "" else 0
        b = int(self.app.inputs[2].num) if self.app.inputs[2].num != "" else 0
        self.color = (r, g, b, 255)
        self.grid = self.app.manager.image_buttons[self.stack].grid

    def draw(self):
        self.surf.fill((30, 30, 30))
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if self.grid[y][x][3] == 0:
                    if self.stack > 0:
                        if self.app.manager.image_buttons[self.stack - 1].grid[y][x][3] == 0:
                            box = pg.Surface([BLOCK_SIZE - SPACE * 2, BLOCK_SIZE - SPACE * 2])
                            box.fill((0, 0, 0))
                            self.surf.blit(box, (BLOCK_SIZE * x + SPACE, BLOCK_SIZE * y + SPACE))
                        else:
                            c = self.app.manager.image_buttons[self.stack - 1].grid[y][x]
                            co = (c[0], c[1], c[2], c[3] / 4)
                            gfxdraw.box(self.surf, (BLOCK_SIZE * x, BLOCK_SIZE * y, BLOCK_SIZE, BLOCK_SIZE), co)
                    else:
                        box = pg.Surface([BLOCK_SIZE - SPACE * 2, BLOCK_SIZE - SPACE * 2])
                        box.fill((0, 0, 0))
                        self.surf.blit(box, (BLOCK_SIZE * x + SPACE, BLOCK_SIZE * y + SPACE))
                else:
                    gfxdraw.box(self.surf, (BLOCK_SIZE * x, BLOCK_SIZE * y, BLOCK_SIZE, BLOCK_SIZE), self.grid[y][x])

        self.app.screen.blit(self.surf, self.surf_pos)

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (pg.mouse.get_pos()[0] - self.surf_pos[0], pg.mouse.get_pos()[1] - self.surf_pos[1])
                if not pos[0] < 0 and not pos[1] < 0:
                    if not pos[0] > GRID_WIDTH * BLOCK_SIZE and not pos[1] > GRID_HEIGHT * BLOCK_SIZE:
                        if self.mod == 0:
                            self.grid[int(pos[1] // BLOCK_SIZE)][int(pos[0] // BLOCK_SIZE)] = self.color
                        elif self.mod == 1:
                            self.grid[int(pos[1] // BLOCK_SIZE)][int(pos[0] // BLOCK_SIZE)] = (0, 0, 0, 0)


class App:
    def __init__(self):
        pg.font.init()
        self.buttons = []
        self.screen = pg.display.set_mode(size=WIN_SIZE)
        for index, button in enumerate([obj for name, obj in inspect.getmembers(buttons) if inspect.isclass(obj)]):
            if button.__name__ != "Button":
                self.buttons.append(button(self, (10 + ((index - 1) * 40), 100), 30, 30))
        self.clock = pg.time.Clock()
        self.inputs = [Input(self, (10, 10), 30, 20), Input(self, (50, 10), 30, 20), Input(self, (90, 10), 30, 20)]
        self.canvas = Canvas(self)
        self.manager = Manager(self, (410, HEIGHT - 300), 200, 300)

    def update(self):
        self.clock.tick(MAX_FPS)
        for inp in self.inputs:
            inp.update()
        for button in self.buttons:
            button.update()
        self.canvas.update()
        self.manager.update()
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill((0, 0, 30))
        for inp in self.inputs:
            inp.draw()
        for button in self.buttons:
            button.draw()
        self.canvas.draw()
        self.manager.draw()
        pg.display.flip()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                for inp in self.inputs:
                    inp.check_events(event)
                for button in self.buttons:
                    button.check_events(event)
                self.canvas.check_events(event)
                self.manager.check_events(event)
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()