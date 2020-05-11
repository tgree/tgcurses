#!/usr/bin/env python3
import tgcurses
import tgcurses.ui

import curses


def main(screen):
    # Create the main workspace.
    ws = tgcurses.ui.Workspace(screen)

    # Add a regular menu window.
    menu_win = ws.make_edge_window('Menu 1', w=15, h=7)
    menu_win.show()
    menu_win.menu = tgcurses.ui.Menu(menu_win, ['One', 'Two', 'Three', 'Four'])
    menu_win.content.timeout(100)
    menu_win.content.keypad(1)

    # Add a checkable menu window.
    check_win = ws.make_anchored_window('Menu 2', w=15, h=7,
                    left_anchor=menu_win.frame.right_anchor(),
                    top_anchor=menu_win.frame.top_anchor())
    check_win.show()
    check_win.menu = tgcurses.ui.Menu(
                    check_win,
                    ['Alpha', 'Beta', 'Gamma', 'Delta'],
                    checked=[2])
    check_win.content.timeout(100)
    check_win.content.keypad(1)

    # Handle user input.
    windows = [menu_win, check_win]
    windows[0].hilite()
    tgcurses.ui.curs_set(0)
    while True:
        tgcurses.ui.doupdate()
        w = windows[0]
        c = w.content.getch()
        if c == -1:
            continue
        elif c == ord('q'):
            break
        elif c == ord('x') and w == check_win:
            w.menu.toggle_item(w.menu.selection)
            w.menu.draw()
        elif c == curses.KEY_DOWN:
            w.menu.select_next()
            w.menu.draw()
        elif c == curses.KEY_UP:
            w.menu.select_prev()
            w.menu.draw()
        elif c == ord('\t'):
            windows[0].dehilite()
            windows = windows[1:] + windows[:1]
            windows[0].hilite()
        elif c == curses.KEY_BTAB:
            windows[0].dehilite()
            windows = windows[-1:] + windows[:-1]
            windows[0].hilite()


if __name__ == '__main__':
    tgcurses.wrapper(main)
