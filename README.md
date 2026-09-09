# Mancala AI Development Guide

A console-based Mancala game framework where you can create custom AI players to compete against each other.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Creating Your AI](#creating-your-ai)
- [The MancalaBoard API](#the-mancalaboard-api)
- [Board Layout Reference](#board-layout-reference)
- [Game Rules](#game-rules)
- [Testing Your AI](#testing-your-ai)
- [Available AIs](#available-ais)

---

## Architecture Overview

The project consists of several modules:

| File | Description |
|------|-------------|
| `main.py` | Game engine, menu system, and game loop |
| `MancalaBoard.py` | Board representation and game logic |
| `console_screen.py` | Terminal display rendering |
| `ansi_lib.py` | Low-level ANSI escape code utilities |
| `util.py` | Helper functions (file loading, name formatting) |
| `getch.py` | Blocking keyboard input |
| `screen_templates.py` | Text templates for menus and board display |
| `players/MancalaAI.py` | Base class all AIs must extend |
| `players/*.py` | Example AI implementations |

The game flow for an AI player is:

1. `main.py` loads your AI module via `importlib` (see [util.py](util.py) `load_player_files`)
2. The AI's constructor receives the player number (`1` or `2`)
3. During the game loop, `get_move(board)` is called with the current `MancalaBoard` instance
4. The AI returns an integer move (1-6) representing which pit to sow from

## Creating Your AI

### Step 1: Create Your File

Create a new `.py` file in the `players/` directory. The filename determines the class name and display name automatically.

- **File**: `players/my_clever_bot.py` → **Class**: `MyCleverBot` → **Display**: `My Clever Bot`

The conversion is handled by `util.py`:
- `get_class_name()`: Title-cases the filename and removes underscores → `MyCleverBot`
- `get_printable_name()`: Title-cases and replaces underscores with spaces → `My Clever Bot`

### Step 2: Implement the Base Class

Every AI must import and extend `MancalaAI` from `players.MancalaAI`:

```python
from players.MancalaAI import MancalaAI

class MyCleverBot(MancalaAI):
    def get_move(self, board):
        # Your logic here
        return 1  # Must return a valid move: 1-6
```

### Required Interface

Your class must:

1. **Inherit from `MancalaAI`** (which stores `self.player_num`)
2. **Implement `get_move(self, board)`** — receives a `MancalaBoard` instance, returns an integer 1-6

Your `get_move` will be called once per turn. The `board` argument reflects the state **before** your move is applied.

### Important Notes on Naming

The file name controls the class discovery mechanism in `main.py`:

```python
module_name = importlib.import_module('players.' + players[i])     # players.my_clever_bot
class_name = get_class_name(players[i])                          # MyCleverBot
ai_class = getattr(module_name, class_name)                       # MyCleverBot
ai_instance = ai_class(i+1)                                       # Constructor gets player number
```

This means the class name **must exactly match** the title-cased, underscore-stripped version of your filename. Failure to match will cause an `AttributeError` at load time.

---

## The MancalaBoard API

All AIs interact with the game through the `MancalaBoard` class ([MancalaBoard.py](MancalaBoard.py)). Here are the key methods:

### Core Methods

#### `board.get_valid_moves()`
Returns a list of valid move integers (1-6) for the **current** player (`board.player_num`).

```python
moves = board.get_valid_moves()
# Example: [1, 3, 5, 6]
```

#### `board.get_test_board(move_num)`
Returns a **new** `MancalaBoard` with the given move applied. The original board is not modified. This is the primary way to look ahead.

```python
for move in board.get_valid_moves():
    future = board.get_test_board(move)
    # Analyze future board state...
```

**Important**: The returned board's `player_num` is updated to reflect whose turn it is after the move. If `future.player_num == self.player_num`, your AI gets to move again.

#### `board.make_move(move_num)`
Applies a move to the board in-place. Raises `InvalidMoveException` if the move is invalid. AIs should use `get_test_board()` for analysis and avoid calling this on the real board.

#### `board.clone()`
Returns a deep copy of the board. Equivalent to `get_test_board` but without applying a move.

### Board State Inspection

#### `board.board`
The 14-element list representing the game state:

```
Index: 0  1  2  3  4  5  6  7  8  9 10 11 12 13
       P2 P2 P2 P2 P2 P2 P2 P1 P1 P1 P1 P1 P1 P1
       M  6  5  4  3  2  1  M  6  5  4  3  2  1
```

- Index 0: Player 2's mancala (end pit)
- Indices 1-6: Player 2's side pits
- Index 7: Player 1's mancala (end pit)
- Indices 8-13: Player 1's side pits

**Access directly as `board.board[index]`.**

#### `board.player_num`
The current player number (`1` or `2`).

#### `board.get_my_mancala_idx(player_num)`
Returns the index of the given player's mancala.

```python
my_idx = board.get_my_mancala_idx(self.player_num)  # 7 for P1, 0 for P2
```

#### `board.get_stones()`
Returns the board list (equivalent to `board.board`).

#### `board.is_game_over()`
Returns `True` if either player has no stones left in their side pits.

#### `board.get_winner()`
Returns `0` (no winner yet), `1` (Player 1 wins), `2` (Player 2 wins), or `-1` (tie).

#### `board.get_moves()`
Returns the move history as a list of two lists: `[[player1_moves], [player2_moves]]`.

### Utility Methods

#### `board.index_on_my_side(idx)`
Returns `True` if the given index belongs to the current player's side.

---

## Board Layout Reference

```
Player 1 (goes first, bottom):
╔═══════════════════════════════════════════════════╗
║ ┌────┐ ┌─1─┐ ┌─2─┐ ┌─3─┐ ┌─4─┐ ┌─5─┐ ┌─6─┐ ┌────┐ ║
║ │    │ │[6]│ │[5]│ │[4]│ │[3]│ │[2]│ │[1]│ │    │ ║
║ │    │ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ │    │ ║
║ │[7] │                                     │[0] │ ║
║ │    │ ┌─6─┐ ┌─5─┐ ┌─4─┐ ┌─3─┐ ┌─2─┐ ┌─1─┐ │    │ ║
║ │    │ │[8]│ │[9]│ │[10] │[11] │[12] │[13] │    │ ║
║ └────┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └────┘ ║
╚═══════════════════════════════════════════════════╝
                              Player 2
```

**Key observations**:
- A move number `n` corresponds to the `n`-th pit from the right on your side
- `get_index_from_move(n)` = `(7 * player_num) - n`
- After sowing, if the last stone lands in your mancala, you get another turn
- If the last stone lands in an empty pit on your side (and the opposite pit has stones), you capture those stones

---

## Game Rules

1. Each player starts with 6 pits containing 4 stones each, plus a mancala with 0 stones
2. On your turn, pick up all stones from any of your non-empty pits
3. Sow them one by one counterclockwise, skipping the opponent's mancala
4. If the last stone lands in your own mancala, take another turn
5. If the last stone lands in an empty pit on your side, capture it and all stones opposite that pit
6. The game ends when one player has no stones in their side pits
7. Players collect remaining stones into their mancalas
8. The player with more stones in their mancala wins

### Move Numbering

Moves are numbered 1-6. For Player 1, move 1 is index 1 (closest to Player 2's mancala), move 6 is index 6. For Player 2, move 1 is index 8, move 6 is index 13.

Use `board.get_valid_moves()` to always get the correct list for the current player.

---

## Testing Your AI

### Manual Testing

Run the game:

```bash
python main.py
```

Select option `(2)` to pit two custom AIs against each other. This lets you test your AI against any other AI in the players folder.

You can also use option `(3)` to play against your AI yourself (if you modify the menu).

### Automated Tournament

Select option `(2)` then `(2)` to run 500 games with AI vs AI. The game will:
1. Run 500 games with your selected player order
2. Run 500 games with the reversed order
3. Display a comparison of wins/losses/ties

### Writing Debug Logs

You can add logging to your AI for debugging. See the commented-out logging in `players/deep_purple.py` for an example.

---

## Available AIs

| File | Class | Strategy |
|------|-------|----------|
| `random_idiot.py` | `RandomIdiot` | Picks a random valid move |
| `seq_dummy.py` | `SeqDummy` | Always picks the lowest-numbered valid move |
| `easy_peasy.py` | `EasyPeasy` | Greedy: maximizes immediate mancala stones + bonus for extra turns |
| `deep_purple.py` | `DeepPurple` | Minimax-style with depth-limited lookahead |
| `the_hunter.py` | `TheHunter` | Heuristic-based with immediate captures and extra-turn bonus |
| `skinny.py` | `Skinny` | Heuristic-based with capture, extra-turn, and empty-pit strategies |
| `Mimancalaplayer.py` | `Mimancalaplayer` | Recursive lookahead evaluating opponent responses |
| `squweekers.py` | `Squweekers` | See player file for details |
| `stone_oven_v2.py` | `StoneOvenV2` | See player file for details |
| `new.py` | `New` | See player file for details |
| `shayne.py` | `Shayne` | See player file for details |

---

## Key Methods for AI Development

### `get_test_board(move_num, player_num=None)`

**Critical for lookahead/search algorithms.** Creates a copy of the board and applies the move without modifying the original.

```python
def get_move(self, board):
    best_move = None
    best_score = -999
    
    for move in board.get_valid_moves():
        test_board = board.get_test_board(move)
        
        # Check if we'd get another turn
        if test_board.player_num == self.player_num:
            # We go again - this is valuable!
            score = 10
        else:
            # Evaluate mancala difference
            my_mancala = test_board.get_my_mancala_idx(self.player_num)
            score = test_board.board[my_mancala]
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move
```

### Reading the Board Directly

Since `board.board` is a list, you can analyze it directly:

```python
# Player 1's side pits (indices 1-6)
p1_pits = board.board[1:7]

# Player 2's side pits (indices 8-13)
p2_pits = board.board[8:14]

# Mancalas
p1_mancala = board.board[7]
p2_mancala = board.board[0]

# Total stones (sanity check - should always be 48)
total = sum(board.board)
```

### Understanding Turn Flow

After `get_test_board(move)` returns:
- If `test_board.player_num == self.player_num` → you get another turn
- If `test_board.player_num != self.player_num` → opponent's turn

This lets you implement multi-turn strategies (like DeepPurple's recursive lookahead).

---

## Common Pitfalls

1. **Invalid move return**: Always return a value from `board.get_valid_moves()`. If you return an invalid move, `InvalidMoveException` is raised and your game is forfeited.

2. **Performance**: For deep search, use iterative deepening or caching. The minimax-style AIs can be slow with deep recursion.

3. **Name matching**: The class name must exactly match the title-cased, underscore-stripped filename. `my_bot.py` → `MyBot`.

4. **Modifying the board**: Never call `board.make_move()` on the real board object passed to `get_move()`. Use `board.get_test_board()` for analysis.

5. **Board index reference**: Remember that Player 1's mancala is at index 7, Player 2's at index 0.

---

## API Method Summary

| Method | Returns | Description |
|--------|---------|-------------|
| `get_valid_moves()` | `list[int]` | Valid moves (1-6) for current player |
| `get_test_board(move)` | `MancalaBoard` | New board with move applied |
| `make_move(move)` | `self` | Apply move in-place (use with caution) |
| `clone()` | `MancalaBoard` | Deep copy of board |
| `is_game_over()` | `bool` | True if any player lacks side-pit stones |
| `get_winner()` | `int` | 0 (ongoing), 1/2 (winner), -1 (tie) |
| `get_my_mancala_idx(player_num)` | `int` | Index of player's mancala |
| `index_on_my_side(idx)` | `bool` | Whether idx is on current player's side |
| `get_stones()` | `list[int]` | The board array |
| `get_moves()` | `list[list]` | Move history for both players |

---

## Contributing

1. Create your AI file in `players/`
2. Ensure the class name matches the filename convention
3. Test against existing AIs using the tournament mode
4. All AIs must extend `players.MancalaAI.MancalaAI`
5. All AIs must implement `get_move(self, board)` returning a valid move 1-6