# /ai — Search Algorithms & Knowledge Representation

Classical AI implementations built from scratch. No ML frameworks — every behavior is the result of formal logic, graph search, or constraint reasoning that can be read, traced, and proven correct.

---

## Contents

### `logic.py` — Propositional Logic Engine
The foundation for all knowledge-base programs in this folder. Implements:

| Class / Function | Description |
|---|---|
| `Symbol(name)` | Atomic proposition |
| `And(*conjuncts)` | Logical conjunction — supports `.add()` for incremental KB building |
| `Or(*disjuncts)` | Logical disjunction |
| `Not(operand)` | Logical negation |
| `Implication(a, b)` | `a → b` |
| `Biconditional(a, b)` | `a ↔ b` |
| `model_check(kb, query)` | Exhaustive model enumeration — returns `True` if KB entails query |

No external dependencies. Pure Python.

---

### `clue.py` — Deductive Reasoning (Clue/Cluedo Solver)
Builds a propositional knowledge base from game state — known cards in hand, partial reveals from other players — and runs `model_check()` to determine which suspects, rooms, and weapons are definitively eliminated (`YES`) vs. still possible (`MAYBE`).

```bash
pip install termcolor
python clue.py
```

**Concepts:** knowledge-base AI, model enumeration, deductive elimination under partial information

---

### `harry.py` — Logic Puzzle Solver
Uses the same `logic.py` engine to solve a classic logic deduction puzzle (Hogwarts house assignments). Demonstrates how the same inference infrastructure generalizes across problem domains.

**Concepts:** propositional encoding of constraints, entailment as proof

---

### `maze.py` — Pathfinding on ASCII Grids
Solves mazes defined as text files (`maze1.txt`, `maze2.txt`, `maze3.txt`) using both **BFS** (breadth-first search, shortest path) and **DFS** (depth-first search). Generates a visual PNG output (`maze.png`) showing the explored frontier and solution path.

```bash
python maze.py maze1.txt
```

**Concepts:** graph search, BFS vs DFS trade-offs, frontier/explored sets, state space representation

---

## Maze Files

| File | Description |
|---|---|
| `maze1.txt` | Simple maze — good for verifying correctness |
| `maze2.txt` | Medium complexity |
| `maze3.txt` | Larger grid — highlights BFS vs DFS path length differences |
| `maze.png` | Generated output (gitignored in future — run locally) |

---

## Incoming 🔄

| Project | Concepts |
|---|---|
| `minesweeper.py` | Constraint propagation, subset inference, probabilistic fallback |
| `tictactoe.py` | Minimax, alpha-beta pruning, zero-sum adversarial search |
| `pcl_engine/` | SO(k) rotation matrices, Givens rotations, Ollama-compatible export |

---

## Architecture Philosophy

```
Search          maze.py      →  BFS / DFS  →  Optimal path on state graph
Knowledge       clue.py      →  KB + model_check  →  Deductive proof
                harry.py     →  Constraint encoding  →  Puzzle solving
Constraint      minesweeper  →  CSP inference  →  Safe cell identification  [incoming]
Adversarial     tictactoe    →  Minimax  →  Optimal game play              [incoming]
Neural          pcl_engine   →  SO(k) geometry  →  Phase control layer     [incoming]
```

All engines here prioritize **explainability and mathematical grounding**. The goal is AI you can reason about formally.

---

## Dependencies

```bash
pip install termcolor pillow   # termcolor for clue.py, pillow for maze.py PNG output
# logic.py — zero deps, pure Python stdlib
```
