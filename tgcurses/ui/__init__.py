import curses

from .window import Window
from .workspace import Workspace
from .menu import Menu
from .edit_field import EditField


def doupdate():
    '''
    Synchronize the curses virtual screen to the physical screen.  curses does
    this automatically when you call Canvas.refresh(), but it is useful when
    calling Canvas.noutrefresh() to allow batching of operations into the
    virtual screen and then a single synchronize operation to the physical
    screen.
    '''
    curses.doupdate()


def curs_set(visibility):
    '''
    Sets the cursor visibility to either 0, 1, or 2.  0 is invisible, 1 is
    visible (underline) and 2 is very visible (block).
    '''
    curses.curs_set(visibility)
