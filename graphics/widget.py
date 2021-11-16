from pygameutil import *

class DraggablePoint(DraggablePoint):
    def __init__(self, screen, x, y, r, inactiveColour, activeColour, zlayer=0, onDrag=None):
        super().__init__(screen, x, y, r, inactiveColour, activeColour, zlayer=0)
    self.onDrag = onDrag

    