import curses
import _curses


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
        self.selection   = selection
        self.top         = 0
        self.hilite_attr = curses.A_REVERSE
        self.draw()

    def draw_item(self, index):
        rows = self.window.content.height
        if index < self.top or index >= self.top + rows:
            return

        row  = index - self.top
        attr = self.hilite_attr if index == self.selection else 0
        if self.top > 0 and row == 0:
            s = '%-*s\u2191' % (self.window.content.width - 1,
                                self.items[index])
            s.encode('utf-8')
        elif self.top + rows < len(self.items) and row == rows - 1:
            s = '%-*s\u2193' % (self.window.content.width - 1,
                                self.items[index])
            s.encode('utf-8')
        else:
            s = '%-*s' % (self.window.content.width, self.items[index])
        try:
            self.window.content.addstr(s, pos=(row, 0), attr=attr)
        except _curses.error as e:
            pass
        self.window.content.noutrefresh()

    def draw(self):
        for i in range(len(self.items)):
            self.draw_item(i)

    def select(self, index):
        rows           = self.window.content.height
        prev_selection = self.selection
        self.selection = index
        if index < self.top:
            self.top = index
            self.draw()
        elif index >= self.top + rows:
            self.top = index - rows + 1
            self.draw()
        else:
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
