"""
Represents two words and which index in the word will intersect with the other word.
"""
class Intersection:

    def __init__(self, acrossWord, downWord, acrossWordIndex, downWordIndex ):
        self.across = acrossWord
        self.down = downWord
        self.acrossIndex = acrossWordIndex
        self.downIndex = downWordIndex
