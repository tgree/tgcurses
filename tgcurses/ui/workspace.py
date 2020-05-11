from ..layout import StaticFrame, Frame, Bounds
from .window import Window


class Workspace(object):
    '''
    A workspace takes over the entire region specified by the canvas and uses
    it to present ui.Window objects to the user.
    '''
    def __init__(self, canvas):
        self.canvas  = canvas
        self.windows = []

    def make_canvas(self, frame):
        '''
        Creates a canvas in the workplace.
        '''
        return self.canvas.make_canvas(frame)

    def make_window(self, title, frame):
        '''
        Creates a window in the workplace.
        '''
        w = Window(self, title, frame)
        self.windows.append(w)
        return w

    def make_static_window(self, title, y, x, h, w):
        '''
        Creates a new window in the specified workspace.  The new window will
        have dimensions (h, w), including the window border.  The window's
        interior canvas will therefore have dimensions (h-1, w-1).
        '''
        b = Bounds(x, y, x + w, y + h)
        f = self.canvas.make_sub_frame(b)
        return self.make_window(title, f)

    def make_anchored_window(self, title, h=None, w=None, **kwargs):
        '''
        Return a new Window on the same screen using a new Frame with the
        given anchor points.  This is syntactic sugar for:

            f = Frame(workspace.canvas, **kwargs)
            w = Window(workspace.canvas, f)
        '''
        f = Frame(height=h, width=w, **kwargs)
        return self.make_window(title, f)

    def make_edge_window(self, title, h=None, w=None):
        '''
        Return a new Window snapped to the edges of the current Workspace.  The
        window coordinates are as follows:

                h    | Position
            ---------+----------------------------------------------
            positive | top-aligned, height=h
            negative | bottom-aligned, height=abs(h)
            None     | top- and bottom-aligned, height tracks parent
            ---------+----------------------------------------------
                w    | Position
            ---------+----------------------------------------------
            positive | left-aligned, width=w
            negative | right-aligned, width=abs(w)
            None     | left- and right-aligned, width tracks parent
            ---------+----------------------------------------------
        '''
        l = self.canvas.frame.left_anchor() if w is None or w >= 0 else None
        r = self.canvas.frame.right_anchor() if w is None or w < 0 else None
        w = None if w is None else abs(w)

        t = self.canvas.frame.top_anchor() if h is None or h >= 0 else None
        b = self.canvas.frame.bottom_anchor() if h is None or h < 0 else None
        h = None if h is None else abs(h)

        return self.make_anchored_window(title,
                                         left_anchor=l,
                                         right_anchor=r,
                                         top_anchor=t,
                                         bottom_anchor=b,
                                         w=w, h=h)
