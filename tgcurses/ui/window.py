import curses


class Window(object):
    '''
    A Window is a rectangular region of a canvas that contains a 1-character
    border on each edge and has a left-justitifed title displayed at the top.
    The frame specified in the initializer is in workspace coordiantes.
    '''
    def __init__(self, workspace, title, frame):
        self.workspace = workspace
        self.title     = title
        self.frame     = frame
        self.border    = workspace.make_canvas(frame)
        self.content   = workspace.make_canvas(frame.make_inset_frame(1, 1))
        self.hilited   = False
        self.visible   = False
        self.show()

    def hide(self):
        '''
        Removes the window and border from the screen on the next update.
        '''
        self.visible = False
        self.border.erase()
        self.border.noutrefresh()

    def show(self):
        '''
        Displays the window and border on the next update.
        '''
        self.visible = True
        max_title_width = self.frame.bounds.width - 4
        if len(self.title) > max_title_width:
            self.display_title = self.title[:max_title_width - 1] + u'\u2026'
            self.display_title = self.display_title.encode('utf-8')
        else:
            self.display_title = self.title

        self.border.border()
        if self.hilited:
            self.hilite()
        else:
            self.dehilite()

    def hilite(self):
        '''
        Draws the title in inverse text.
        '''
        self.border.addstr(self.display_title, (0, 3), curses.A_REVERSE)
        self.border.noutrefresh()

    def dehilite(self):
        '''
        Draws the title in regular text.
        '''
        self.border.addstr(self.display_title, (0, 3))
        self.border.noutrefresh()
