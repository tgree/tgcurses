import curses

from ..layout import Bounds, Frame, StaticFrame


class Canvas(object):
    '''
    A Canvas represents a region of the screen in which drawing operations can
    be performed.  Its dimensions are defined by a frame and it is inherently
    resizable.

    This class is essentially delegates all calls to the equivalent curses
    window class.  We do it like this instead of just subclassing the curses
    one to add the two or three methods we care about because the curses window
    class isn't actually exposed publicly at all and can't be spelled in
    python.

    Canvas is essentially a wrapper for an ncurses window object.  We don't
    just call it a window because our ui library has a window class that
    provides borders and a title like a real GUI-type window and we don't want
    to confuse the two.
    '''
    def __init__(self, parent, frame, cwin):
        super(Canvas, self).__init__()
        self.parent   = parent
        self.frame    = frame
        self._cwin    = cwin
        self.children = []

        if parent:
            parent.children.append(self)

    @staticmethod
    def _from_stdscr(cwin):
        h, w  = cwin.getmaxyx()
        frame = StaticFrame(h, w, 0, 0)
        return Canvas(None, frame, cwin)

    def make_canvas(self, frame):
        '''
        Return a new child Canvas anchored using the specified anchors.
        '''
        b    = frame.bounds
        cwin = curses.newwin(b.height, b.width, b.y1, b.x1)
        return Canvas(self.parent, frame, cwin)

    @property
    def bounds(self):
        return self.frame.bounds

    @property
    def width(self):
        return self.frame.bounds.width

    @property
    def height(self):
        return self.frame.bounds.height

    def keypad(self, enabled):
        '''
        Enables or disables keypad input characters.
        '''
        self._cwin.keypad(enabled)

    def timeout(self, delay):
        '''
        Sets the input timeout to delay:
            delay | Behaviour
            ------+----------------------------------------
              < 0 | Blocks indefinitely.
             == 0 | No block; returns -1 if no input.
              > 0 | Waits delay ms; returns -1 if no input.
            ------+----------------------------------------
        '''
        self._cwin.timeout(delay)

    def getch(self):
        '''
        Returns the next character from the input stream.  Does not write it to
        the canvas.  getch() implicitly does a refresh() on the target Canvas:
        the target canvas is marked as dirty and then all dirty canvases will
        be sync'd to the physical screen.
        '''
        return self._cwin.getch()

    def noutrefresh(self):
        '''
        Updates the curses virtual screen with the canvas contents but does not
        sync the virtual screen with the physical screen.  Multiple calls to
        noutrefresh() across multiple canvases can be used to batch drawing
        commands into the virtual screen and finally update the physical screen
        in a single operation via screen.doupdate().
        '''
        self._cwin.noutrefresh()

    def refresh(self):
        '''
        Updates the curses virtual screen with the canvas contents and then
        immediately syncs the virtual screen to the physical screen.  This is
        the equivalent of calling:

            canvas.noutrefresh()
            screen.doupdate()
        '''
        self._cwin.refresh()

    def erase(self):
        '''
        Draws the background character over the entire canvas.  Does not
        automatically refresh anything, a call to noutrefresh() or refresh()
        is required to see the change.
        '''
        self._cwin.erase()

    def clear(self):
        '''
        Seems to do the same thing as erase().
        '''
        self._cwin.clear()

    def move(self, y, x):
        '''
        Moves the cursor to the specified position in canvas coordinates.
        '''
        self._cwin.move(y, x)

    def getyx(self):
        '''
        Returns the cursor position as a (y, x) tuple.
        '''
        return self._cwin.getyx()

    def set_focus(self):
        '''
        Display the cursor at its current location in this canvas.
        '''
        y, x = self.getyx()
        self.move(y, x)

    def addch(self, ch, pos=None, attr=None):
        '''
        Draws the character (specified as an integer and not a character-string)
        at the specified position.
        '''
        if pos is not None:
            if attr is not None:
                self._cwin.addch(pos[0], pos[1], ch, attr)
            else:
                self._cwin.addch(pos[0], pos[1], ch)
        else:
            if attr is not None:
                self._cwin.addch(ch, attr)
            else:
                self._cwin.addch(ch)

    def addchs(self, chs, pos=None, attr=None):
        '''
        Draws the character sequence (specified as an array of integers and not
        a character-string) at the specified position.
        '''
        if pos is not None:
            self.move(pos[0], pos[1])
        for c in chs:
            self.addch(c, attr=attr)

    def addstr(self, text, pos=None, attr=None):
        '''
        Draws the specified text in the canvas.  Is pos is specified, it can be
        an (y, x) tuple defining the position relative to the top-left corner
        of the canvas at which to draw the text.  Otherwise the text is drawn
        at the current cursor position.
        '''
        if pos is not None:
            if attr is not None:
                self._cwin.addstr(pos[0], pos[1], text, attr)
            else:
                self._cwin.addstr(pos[0], pos[1], text)
        else:
            if attr is not None:
                self._cwin.addstr(text, attr)
            else:
                self._cwin.addstr(text)

    def addstr_center(self, text):
        '''
        Draws a string centered in the canvas.
        '''
        x = (self.frame.width - len(text))/2
        y = self.frame.height/2
        self.addstr(text, pos=(y, x))

    def border(self):
        '''
        Draws a border around the edges of the canvas.  The characters for the
        border are included in the canvas content, so the usable width and
        height of the canvas is decreased by 2 in each dimension.
        '''
        self._cwin.border()

    def scrollok(self, ok):
        '''
        Whether or not the canvas contents will scroll up one line if a
        character is drawn in the bottom-right corner or if a newline is drawn
        on the bottom line.
        '''
        self._cwin.scrollok(ok)

    def scroll(self, dy):
        '''
        Scrolls the canvas contents up 'dy' lines.  If 'dy' is negative, the
        contents will scroll down instead.
        '''
        self._cwin.scroll(dy)

    def attron(self, attr):
        '''
        Enables the specified curses attribute for the background character.
        '''
        self._cwin.attron(attr)

    def attroff(self, attr):
        '''
        Disables the specified curses attribute for the background character.
        '''
        self._cwin.attroff(attr)

    def bkgd(self, ch, attr=None):
        '''
        Sets the background character to ch and applies the optional attr
        parameter.  The background is then repainted.
        '''
        if attr is not None:
            self._cwin.bkgd(ch, attr)
        else:
            self._cwin.bkgd(ch)

    def clrline(self, y):
        '''
        Clears the entire line at the specified y coordinate.
        '''
        self.move(y, 0)
        self._cwin.clrtoeol()

    def hline(self, n, ch=None, pos=None):
        ch = curses.ACS_HLINE if ch is None else ch
        if pos is not None:
            self._cwin.hline(pos[0], pos[1], ch, n)
        else:
            self._cwin.hline(ch, n)
