"""Exceptions module for Santorini game-related exceptions"""

class SantoriniException(Exception):
    """Base class for Santorini game-related exception"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidMoveException(SantoriniException):
    """Exception that is raised for an invalid move"""

    def __init__(self, direction: str, *args: object) -> None:
        super().__init__(*args)
        self.direction = direction

class InvalidBuildException(SantoriniException):
    """Exception that is raised for an invalid build"""

    def __init__(self, direction: str, *args: object) -> None:
        super().__init__(*args)
        self.direction = direction
