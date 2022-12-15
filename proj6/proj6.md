
# Santorini Design Patterns

For this Python implementation of the basic Santorini game, I utilized four main
design patterns: (1) State, (2) Template Method, (3) Decorator, and (4) Memento.

## State

At first, I implemented the game's main loop only using the `SantoriniCLI` class
and its methods to control the game's logical flow. However, once I had to deal
with checking for the game's termination conditions and the 'undo/redo/next' cycle,
I realized that abstracting the game's flow into separate state classes would reduce
the complexity of the `SantoriniCLI` class. 

Implementing the State pattern required me to implement an abstract base class,
`SantoriniStateBase`, that only contains a reference to its context, a `SantoriniCLI`
object, and an abstract `run()` method. This allowed me to implement three (3) concrete
state classes responsible, respectively, for setting up the game, running the game and
checking for termination conditions, and printing the victory message and exiting.

## Template Method

Since all three of the different player types are required to choose a move and tell
the board to implement that move, it made sense to use either a Strategy pattern or a
Template Method pattern. I chose Template Method because I thought understanding and
implementing the separate player classes with inheritance would be easier for me, and
that proved true.

Like with the State pattern, the Template Method pattern requires an abstract base class,
`SantoriniPlayerBase`, that implemented all of the shared functionality across the
player classes while leaving the choice of the move an abstract method. Each of the concrete
player classes for the human, random, and heuristic players inherits from the base class
and implements the private `_make_choice()` method to select the move according to design.

## Decorator

I knew I would use the Decorator pattern for printing the heuristic scores as soon as
I looked over the Santorini game requirements because it takes the underlying string
of the player's description and adds another string to the end. In terms of implementing
the decorator, it was more difficult than expected because I was decorating a class method
with arguments. Eventually, I figured out how to make that happen.

However, the decorator `add_heuristic_score` was more difficult because I had to figure
out how to add the decorator dynamically as required and how to make it work with the
different instances of the `SantoriniBoard` class once undo/redo/next was allowed.

The current usage of `add_heuristic_score` with the `base_get_description` and normal
`get_description` methods does not seem optimal, but it is functional.

## Memento

Like with the Decorator pattern, I knew I would need some sort of Memento pattern
to fulfill the fourth command line argument for the history and undo/redo/next commands.
The Memento interface and its caretaker and originator classes allowed me to store
the current state of the game (all encapsulated in the current turn and the board)
before every turn and to create the history necessary for undo/redo/next to work.

I had a few issues with the Memento pattern. The first issue was figuring out what state
to store in the `SantoriniMemento`, which ended up being the turn and the board state.
The second issue was determining how to implement the `undo()` and `redo()` methods
on the `SantoriniCaretaker` to make sure I could only `undo()` and `redo()` as much as
allowed. The third issue was that it seemed the board was not updating on an `undo()`
or a `redo()` operation, which I fixed by making a deep copy of the board on `save()`
using the `deepcopy()` method from the Python standard library `copy` package.
