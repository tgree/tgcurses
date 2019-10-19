import curses
import curses.ascii


class EditField(object):
    '''
    An EditField is a single-line region of a canvas that can be used to input
    text.
    '''
    def __init__(self, canvas, pos, width, text=''):
        self.canvas   = canvas
        self.pos      = pos
        self.width    = width
        self.text     = text
        self.text_pos = 0
        self.show()

    def hide(self):
        '''
        Removes the edit field from the screen on the next update.
        '''
        self.canvas.addstr(' '*self.width, pos=self.pos)
        self.canvas.noutrefresh()

    def show(self):
        '''
        Displays the edit field on the next update.
        '''
        self.canvas.addstr('%-*s' % (self.width, self.text),
                            pos=self.pos, attr=curses.A_UNDERLINE)
        self.canvas.noutrefresh()

    def move(self):
        '''
        Positions the screen cursor at the edit point for this field.
        '''
        self.canvas.move(self.pos[0], self.pos[1] + self.text_pos)
        self.canvas.noutrefresh()

    def handlech(self, c):
        '''
        Handle the specified editing character.
        '''
        if c in (curses.KEY_BACKSPACE, curses.ascii.BS, curses.ascii.DEL):
            if self.text_pos:
                self.text      = (self.text[:self.text_pos - 1] +
                                  self.text[self.text_pos:])
                self.text_pos -= 1
        elif c == curses.KEY_LEFT:
            self.text_pos = max(self.text_pos - 1, 0)
        elif c == curses.KEY_RIGHT:
            self.text_pos = min(self.text_pos + 1, len(self.text))
        elif curses.ascii.isprint(c):
            if len(self.text) < self.width:
                self.text      = (self.text[:self.text_pos] + chr(c) +
                                  self.text[self.text_pos:])
                self.text_pos += 1
