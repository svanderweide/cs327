"""
Python list subclass for fixed-width lists

Subclasses the existing 'list' class and overrides the __getitem__()
method so that negative indices are not allowed
"""

class FixedWidthList(list):

    def __getitem__(self, idx):
        if idx < 0:
            raise IndexError
        return list.__getitem__(self, idx)
