from pygame import gfxdraw
from buttons import *
from settings import *


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
        pass

    def update_color(self):
        r = int(self.app.color_selector.inputs[0].num) if self.app.color_selector.inputs[0].num != "" else 0
        g = int(self.app.color_selector.inputs[1].num) if self.app.color_selector.inputs[1].num != "" else 0
        b = int(self.app.color_selector.inputs[2].num) if self.app.color_selector.inputs[2].num != "" else 0
        self.color = (r, g, b, 255)

    def draw(self):
        self.surf.fill((30, 30, 30))
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if self.grid[y][x][3] == 0:
                    if self.stack > 0:
                        if self.app.manager.stack_buttons[self.stack - 1].grid[y][x][3] == 0:
                            gfxdraw.box(self.surf, (BLOCK_SIZE * x + SPACE, BLOCK_SIZE * y + SPACE, BLOCK_SIZE - SPACE * 2, BLOCK_SIZE - SPACE * 2), (0, 0, 0))
                        else:
                            c = self.app.manager.stack_buttons[self.stack - 1].grid[y][x]
                            co = (c[0], c[1], c[2], c[3] / 4)
                            gfxdraw.box(self.surf, (BLOCK_SIZE * x, BLOCK_SIZE * y, BLOCK_SIZE, BLOCK_SIZE), co)
                    else:
                        gfxdraw.box(self.surf, (BLOCK_SIZE * x + SPACE, BLOCK_SIZE * y + SPACE, BLOCK_SIZE - SPACE * 2, BLOCK_SIZE - SPACE * 2), (0, 0, 0))
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


class GuiElement:
    def __init__(self, app, pos: tuple, width: int, height: int):
        self.app = app
        self.width = width
        self.height = height
        self.pos = pos
        self.surf = pg.Surface([width, height])

    def update(self):
        pass

    def draw(self):
        self.app.screen.blit(self.surf, self.pos)

    def check_events(self, event):
        pass


class Manager(GuiElement):
    def __init__(self, app, pos: tuple, width: int, height: int):
        super().__init__(app, pos, width, height)
        self.stack_buttons = [StackButton(self, (5, 5), width - 10, 25, 0)]
        self.add_button = AddButton(self, (5, self.height - 30), 25, 25)
        self.remove_button = RemoveButton(self, (35, self.height - 30), 25, 25)
        self.up_button = UpButton(self, (65, self.height - 30), 25, 25)
        self.down_button = DownButton(self, (95, self.height - 30), 25, 25)
        self.stack_buttons_interval = [0, 0]

    def update(self):
        self.add_button.update()
        self.remove_button.update()
        self.up_button.update()
        self.down_button.update()

    def reload_stack_index(self):
        for stack in self.stack_buttons:
            index = self.stack_buttons.index(stack)
            stack.index = index
            if self.stack_buttons_interval[0] <= index <= self.stack_buttons_interval[1]:
                index = index - self.stack_buttons_interval[0]
                stack.pos = (5, 30 * index + 5)
            stack.render()

    def draw(self):
        self.surf.fill((100, 100, 100))
        for ib in self.stack_buttons:
            if self.stack_buttons_interval[0] <= ib.index <= self.stack_buttons_interval[1]:
                ib.draw()
        self.add_button.draw()
        self.remove_button.draw()
        self.up_button.draw()
        self.down_button.draw()
        super().draw()

    def check_events(self, event):
        for ib in self.stack_buttons:
            if self.stack_buttons_interval[0] <= ib.index <= self.stack_buttons_interval[1]:
                ib.check_events(event)
        self.add_button.check_events(event)
        self.remove_button.check_events(event)
        self.up_button.check_events(event)
        self.down_button.check_events(event)


class ColorSelector(GuiElement):
    def __init__(self, app, pos: tuple, width: int, height: int):
        super().__init__(app, pos, width, height)
        self.inputs = [
            Input(self, (10, 10), 30, 20),
            Input(self, (50, 10), 30, 20),
            Input(self, (90, 10), 30, 20)
        ]

    def update(self):
        for ipt in self.inputs:
            ipt.update()

    def draw(self):
        self.surf.fill((30, 30, 30))
        for ipt in self.inputs:
            ipt.draw()
        super().draw()

    def check_events(self, event):
        for ipt in self.inputs:
            ipt.check_events(event)
