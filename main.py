import pygame as pg
from pygame import gfxdraw
import inspect
from buttons import *
from gui import *
from settings import *
import sys


class App:
    def __init__(self):
        pg.font.init()
        self.screen = pg.display.set_mode(size=WIN_SIZE)
        self.clock = pg.time.Clock()
        self.paint_button = PaintButton(self, (10, 100), 30, 30)
        self.rubber_button = RubberButton(self, (50, 100), 30, 30)
        self.canvas = Canvas(self)
        self.manager = Manager(self, (410, HEIGHT - 300), 200, 300)
        self.color_selector = ColorSelector(self, (0, 0), 130, 40)
        self.canvas.update_color()

    def update(self):
        self.clock.tick(MAX_FPS)
        self.paint_button.update()
        self.rubber_button.update()
        self.canvas.update()
        self.manager.update()
        self.color_selector.update()
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill((0, 0, 30))
        self.paint_button.draw()
        self.rubber_button.draw()
        self.canvas.draw()
        self.manager.draw()
        self.color_selector.draw()
        pg.display.flip()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                self.paint_button.check_events(event)
                self.rubber_button.check_events(event)
                self.canvas.check_events(event)
                self.manager.check_events(event)
                self.color_selector.check_events(event)
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()