"""
Memento module
--------------
Implements the various classes required to save the state of the
Santorini game with (1) undo, (2) redo, and (3) next capabilities
"""

from abc import ABC, abstractmethod
from copy import deepcopy


class Memento(ABC):
    """
    Memento
    -------
    Abstract class for a Memento object for the Memento design pattern;
    responsible for maintaining a saved state
    """

    @abstractmethod
    def get_state(self):
        """Return the memento's state"""
        pass


class SantoriniMemento(Memento):
    """
    SantoriniMemento
    ----------------
    Concrete subclass of the Memento abstract class for the Santorini game
    that stores the current turn and board in use by the State pattern
    """

    def __init__(self, state) -> None:
        self._state = deepcopy(state)

    def get_state(self):
        """Extract the state from the SantoriniMemento instance"""
        return self._state


class SantoriniOriginator:
    """
    SantoriniOriginator
    -------------------
    Originator class responsible for maintaining the state to be saved
    within the mementos and allowing updates to the state so that a
    series of mementos can be saved
    """

    _state = None

    def __init__(self, state) -> None:
        self._state = state

    def _get_state(self):
        return self._state

    def _set_state(self, state) -> None:
        self._state = state

    state = property(_get_state, _set_state)

    def save(self) -> Memento:
        """Create and return a memento of the current state"""
        return SantoriniMemento(self._state)

    def restore(self, memento: Memento):
        """Update the current state to the given memento's state"""
        self._state = memento.get_state()

class SantoriniCaretaker:
    """
    SantoriniCaretaker
    ------------------
    Caretaker class responsible for providing a public interface
    to maintain a collection of SantoriniMemento objects and update
    the associated SantoriniOriginator instance according to various
    user-available functions
    """

    def __init__(self, originator: SantoriniOriginator) -> None:
        self._idx = -1
        self._mementos = []
        self._originator = originator

    def save(self) -> None:
        """Add the originator's current state to the collection"""
        self._idx += 1
        mem = self._originator.save()
        self._mementos.append(mem)

    def undo(self) -> None:
        """Revert to the originator's previous stored state (if possible)"""
        if self._idx > 0:
            self._idx -= 1
            memento = self._mementos[self._idx]
            self._originator.restore(memento)

    def redo(self) -> None:
        """Advance to the originator's next stored state (if possible)"""
        if self._idx + 1 < len(self._mementos):
            self._idx += 1
            memento = self._mementos[self._idx]
            self._originator.restore(memento)

    def next(self) -> None:
        """Clear all stored states after the originator's current state"""
        self._mementos = self._mementos[:self._idx]
