"""Constants module for Santorini game-related contants"""

DIRECTIONS = {
    'n':  (-1, 0),
    'ne': (-1, 1),
    'e':  (0, 1),
    'se': (1, 1),
    's':  (1, 0),
    'sw': (1, -1),
    'w':  (0, -1),
    'nw': (-1, -1)
}

PLAYERS = [ 'white', 'blue' ]

# specific to the 2-player CLI version
WORKERS = [ { 'col': 'white', 'name': 'A', 'pos': (3, 1) },
            { 'col': 'white', 'name': 'B', 'pos': (1, 3) },
            { 'col': 'blue',  'name': 'Y', 'pos': (1, 1) },
            { 'col': 'blue',  'name': 'Z', 'pos': (3, 3) }, ]
