import curses


class Menu(object):
    def __init__(self, window, items, selection=0):
        self.window    = window
        self.items     = items
        self.selection = selection
        self.draw()

    def draw_item(self, index):
        attr = curses.A_REVERSE if index == self.selection else 0
        s    = '%-*s' % (self.window.content.width, self.items[index])
        self.window.content.addstr(s, pos=(index, 0), attr=attr)
        self.window.content.noutrefresh()

    def draw(self):
        for i in xrange(len(self.items)):
            self.draw_item(i)

    def select(self, index):
        prev_selection = self.selection
        self.selection = index
        self.draw_item(prev_selection)
        self.draw_item(self.selection)

    def select_next(self):
        if self.selection + 1 < len(self.items):
            self.select(self.selection + 1)

    def select_prev(self):
        if self.selection - 1 >= 0:
            self.select(self.selection - 1)
