class Anchor(object):
    '''
    Base anchor class which defines an anchor and an offset from the edge of
    some frame.  The edge in question depends on the Anchor subclass.
    '''
    def __init__(self, frame, delta):
        super(Anchor, self).__init__()
        self.frame = frame
        self.delta = delta

    def compute(self):
        raise NotImplementedError


class LeftAnchor(Anchor):
    '''
    Anchor defined relative to the left edge of a frame-like class.  The frame-
    like class must support the compute_left_edge() method.
    '''
    def compute(self):
        return self.frame.compute_left_edge() + self.delta


class RightAnchor(Anchor):
    '''
    Anchor defined relative to the right edge of a frame-like class.  The frame-
    like class must support the compute_right_edge() method.
    '''
    def compute(self):
        return self.frame.compute_right_edge() + self.delta


class TopAnchor(Anchor):
    '''
    Anchor defined relative to the top edge of a frame-like class.  The frame-
    like class must support the compute_top_edge() method.
    '''
    def compute(self):
        return self.frame.compute_top_edge() + self.delta


class BottomAnchor(Anchor):
    '''
    Anchor defined relative to the bottom edge of a frame-like class.  The
    frame-like class must support the compute_bottom_edge() method.
    '''
    def compute(self):
        return self.frame.compute_bottom_edge() + self.delta
