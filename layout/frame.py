from .anchor import LeftAnchor, RightAnchor, TopAnchor, BottomAnchor
from .bounds import Bounds

H_ANCHORS = (LeftAnchor, RightAnchor)
V_ANCHORS = (TopAnchor, BottomAnchor)


class _Frame(object):
    '''
    Base class for frame-like objects.
    '''
    def __init__(self, min_width=1, min_height=1):
        self.min_width  = min_width
        self.min_height = min_height

    def left_anchor(self, dx=0):
        return LeftAnchor(self, dx)

    def right_anchor(self, dx=0):
        return RightAnchor(self, dx)

    def top_anchor(self, dy=0):
        return TopAnchor(self, dy)

    def bottom_anchor(self, dy=0):
        return BottomAnchor(self, dy)

    def compute_left_edge(self):
        raise NotImplementedError

    def compute_top_edge(self):
        raise NotImplementedError

    def compute_right_edge(self):
        raise NotImplementedError

    def compute_bottom_edge(self):
        raise NotImplementedError

    @property
    def bounds(self):
        x1 = self.compute_left_edge()
        x2 = self.compute_right_edge()
        y1 = self.compute_top_edge()
        y2 = self.compute_bottom_edge()
        return Bounds(x1, y1, x2, y2)

    def is_size_valid(self):
        '''
        Checks if the frame meets its minimum dimensions.
        '''
        b = self.bounds
        return b.width >= self.min_width and b.height >= self.min_height

    def make_sub_frame(self, bounds):
        '''
        Return a new Frame with bounds anchored within the current frame.
        '''
        return Frame(left_anchor=self.left_anchor(bounds.x1),
                     top_anchor=self.top_anchor(bounds.y1),
                     width=bounds.width,
                     height=bounds.height)

    def make_inset_frame(self, dy, dx):
        '''
        Returns a new Frame anchored to the edges of the current frame but
        inset by (dx, dy) characters from each edge.
        '''
        return Frame(left_anchor=self.left_anchor(dx),
                     right_anchor=self.right_anchor(-dx),
                     top_anchor=self.top_anchor(dy),
                     bottom_anchor=self.bottom_anchor(-dy))


class Frame(_Frame):
    '''
    Frame class which defines a boundary in terms of anchors relative to other
    frames.  Enough anchor points or dimensions must be specified so that the
    bounds can actually be computed.  Frames are used for laying out graphical
    objects in some coordinate space but themselves do not have any physical
    representation.
    '''
    def __init__(self, left_anchor=None, right_anchor=None,
                 top_anchor=None, bottom_anchor=None, width=None, height=None,
                 min_width=1, min_height=1):
        super(Frame, self).__init__(min_width=min_width, min_height=min_height)
        self._left_anchor   = left_anchor
        self._right_anchor  = right_anchor
        self._top_anchor    = top_anchor
        self._bottom_anchor = bottom_anchor
        self._width         = width
        self._height        = height
        assert left_anchor or right_anchor
        assert top_anchor or bottom_anchor
        assert not left_anchor or type(left_anchor) in H_ANCHORS
        assert not right_anchor or type(right_anchor) in H_ANCHORS
        assert not top_anchor or type(top_anchor) in V_ANCHORS
        assert not bottom_anchor or type(bottom_anchor) in V_ANCHORS
        assert not (left_anchor and right_anchor and width)
        assert not (top_anchor and bottom_anchor and height)
        assert height is None or height != 0
        assert width is None or width != 0

    def compute_left_edge(self):
        if self._left_anchor:
            return self._left_anchor.compute()
        return self._right_anchor.compute() - self._width

    def compute_right_edge(self):
        if self._right_anchor:
            return self._right_anchor.compute()
        return self._left_anchor.compute() + self._width

    def compute_top_edge(self):
        if self._top_anchor:
            return self._top_anchor.compute()
        return self._bottom_anchor.compute() - self._height

    def compute_bottom_edge(self):
        if self._bottom_anchor:
            return self._bottom_anchor.compute()
        return self._top_anchor.compute() + self._height


class StaticFrame(_Frame):
    '''
    A frame-like class which has static dimensions and is anchored at an
    absolute position in the coordinate system.
    '''
    def __init__(self, h, w, y, x):
        super(StaticFrame, self).__init__(min_width=w, min_height=h)
        self.resize(h, w, y, x)

    def resize(self, h, w, y, x):
        self._x1 = x
        self._y1 = y
        self._x2 = x + w
        self._y2 = y + h

    def compute_left_edge(self):
        return self._x1

    def compute_top_edge(self):
        return self._y1

    def compute_right_edge(self):
        return self._x2

    def compute_bottom_edge(self):
        return self._y2
