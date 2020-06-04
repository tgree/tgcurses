import curses


class MenuItem(object):
    def __init__(self, name, checked=None):
        self.name    = name
        self.checked = checked

    def __str__(self):
        if self.checked is not None:
            return '[%c] %s' % (('x' if self.checked else ' '), self.name)
        return self.name

    def check(self):
        assert self.checked is not None
        self.checked = True

    def uncheck(self):
        assert self.checked is not None
        self.checked = False

    def toggle(self):
        assert self.checked is not None
        self.checked = not self.checked


class Menu(object):
    def __init__(self, window, items, selection=0, checked=None):
        self.window = window
        if checked is not None:
            self.items = [MenuItem(n, i in checked)
                          for i, n in enumerate(items)]
        else:
            self.items = [MenuItem(n) for n in items]
        self.selection = selection
        self.draw()

    def draw_item(self, index):
        attr = curses.A_REVERSE if index == self.selection else 0
        s    = '%-*s' % (self.window.content.width, self.items[index])
        self.window.content.addstr(s, pos=(index, 0), attr=attr)
        self.window.content.noutrefresh()

    def draw(self):
        for i in range(len(self.items)):
            self.draw_item(i)

    def select(self, index):
        prev_selection = self.selection
        self.selection = index
        self.draw_item(prev_selection)
        self.draw_item(self.selection)

    def select_next(self):
        if self.selection + 1 < len(self.items):
            self.select(self.selection + 1)
            return True
        return False

    def select_prev(self):
        if self.selection - 1 >= 0:
            self.select(self.selection - 1)
            return True
        return False

    def check_item(self, index):
        self.items[index].check()

    def uncheck_item(self, index):
        self.items[index].uncheck()

    def toggle_item(self, index):
        self.items[index].toggle()
