"""
Represents two words and the index within each word where they intersect one another
"""
class Intersection:

    def __init__(self, acrossWord, downWord, acrossWordIndex, downWordIndex ):
        self.across = acrossWord
        self.down = downWord
        self.acrossIndex = acrossWordIndex
        self.downIndex = downWordIndex
