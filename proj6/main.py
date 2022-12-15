"""
main module for Santorini clone
- CLI argument parsing
- setting up and starting a Game instance
"""

from argparse import ArgumentParser
from santorini.SantoriniCLI import SantoriniCLI

def parse() -> dict[str, str]:
    """Parse the CLI arguments and return them as a dict"""

    parser = ArgumentParser(description='Python implementation of Santorini game')

    parser.add_argument('white',
                        metavar='white',
                        choices=['human', 'heuristic', 'random'],
                        default='human',
                        help='white player type (human, heuristic, random)',
                        nargs='?',)

    parser.add_argument('blue',
                        metavar='blue',
                        choices=['human', 'heuristic', 'random'],
                        default='human',
                        help='blue player type (human, heuristic, random)',
                        nargs='?',)

    parser.add_argument('history',
                        metavar='history',
                        choices=['on', 'off'],
                        default='off',
                        help='enable undo/redo',
                        nargs='?',)

    parser.add_argument('score',
                        metavar='score',
                        choices=['on', 'off'],
                        default='off',
                        help='prints the heuristic scores after each move',
                        nargs='?',)

    args = parser.parse_args()

    return vars(args)


def main() -> None:
    """Main function called when the program is invoked via CLI"""

    args: dict[str, str] = parse()
    CLI = SantoriniCLI(**args)
    CLI.run()

if __name__ == '__main__':
    main()
