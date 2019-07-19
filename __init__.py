import locale
import curses

from .canvas import Canvas


def init():
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.noecho()
    curses.cbreak()

    s = Canvas._from_stdscr(stdscr)
    s.keypad(1)
    s.refresh()
    return s


def deinit(s):
    curses.nocbreak()
    if s:
        s.keypad(0)
    curses.echo()
    curses.endwin()


def wrapper(func, *args):
    '''
    Invokes the specified function with the specified arguments.  The argument
    list is prepended with a Canvas object that covers the entire screen and
    can be used to create more objects for display.
    '''
    locale.setlocale(locale.LC_ALL,'')
    s = None
    try:
        s = init()
        func(s, *args)
    except KeyboardInterrupt:
        pass
    finally:
        deinit(s)
