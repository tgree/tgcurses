class Bounds(object):
    '''
    Object describing some boundary.
    '''
    def __init__(self, x1, y1, x2, y2):
        self.x1  = x1
        self.y1  = y1
        self.x2  = x2
        self.y2  = y2

    @property
    def width(self):
        return self.x2 - self.x1
    
    @property
    def height(self):
        return self.y2 - self.y1

    def contains(self, bounds):
        '''
        Tests whether or not we contain the specified bounds.
        '''
        return (b.x1 >= 0 and b.x1 < self.width and
                b.y1 >= 0 and b.y1 < self.height and
                b.x2 > 0 and b.x2 <= self.width and
                b.y2 > 0 and b.y2 <= self.height and
                b.x1 < b.x2 and b.y1 < b.y2)
