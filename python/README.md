# /python — Exercism Python Track

40+ completed exercises from the [Exercism Python track](https://exercism.org/tracks/python), organized by concept. Every solution is tested against the official bats suite and written with type hints and clean Python idioms.

---

## Completed Exercises by Category

### Fundamentals & Math
| Exercise | Key Concept |
|---|---|
| `leap` | Modular arithmetic, boolean logic |
| `grains` | Powers of 2, bit shifting |
| `collatz-conjecture` | Recursion vs iteration |
| `raindrops` | String building, modular conditions |
| `pangram` | Set membership, string ops |
| `armstrong-numbers` | Digit decomposition, exponentiation |
| `perfect-numbers` | Divisor sums, number classification |
| `darts` | Euclidean distance, scoring zones |
| `triangle` | Geometric validation |
| `killer-sudoku-helper` | Combinatorics, itertools |

### Strings
| Exercise | Key Concept |
|---|---|
| `reverse-string` | Slicing, string manipulation |
| `bob` | String analysis, conditional dispatch |
| `isogram` | Character uniqueness, sets |
| `rna-transcription` | String translation, `str.maketrans` |
| `rotational-cipher` | Caesar cipher, modular char shifting |
| `little-sisters-essay` | String methods — `capitalize`, `replace`, `strip` |
| `little-sisters-vocab` | String construction — `join`, `startswith` |

### Data Structures — Collections
| Exercise | Key Concept |
|---|---|
| `binary-search` | Iterative bisection, index arithmetic |
| `binary-search-tree` | BST insert, search, in/pre/post-order traversal |
| `all-your-base` | Radix conversion, arbitrary base arithmetic |
| `card-games` | List methods — `pop`, `insert`, `index`, `count` |
| `chaitanas-colossal-coaster` | List mutation — `append`, `extend`, `remove`, `sort` |
| `cater-waiter` | Set operations — union, intersection, difference, symmetric diff |
| `inventory-management` | Dict methods — `get`, `update`, `setdefault`, `pop` |
| `mecha-munch-management` | Dict merging, copying, iteration |
| `tisbury-treasure-hunt` | Tuple indexing, searching, iteration |

### OOP & Classes
| Exercise | Key Concept |
|---|---|
| `ellens-alien-game` | Class definition, `__init__`, instance methods |
| `black-jack` | Conditional logic, value comparison, game state |

### Loops, Iterators & Generators
| Exercise | Key Concept |
|---|---|
| `making-the-grade` | List comprehensions, `filter`-style loops |
| `locomotive-engineer` | Unpacking, `*args`, `**kwargs` |
| `plane-tickets` | Generator functions, `yield`, lazy evaluation |

### Logic & Control Flow
| Exercise | Key Concept |
|---|---|
| `meltdown-mitigation` | Nested conditionals, early return |
| `ghost-gobble-arcade-game` | Boolean expressions, operator precedence |
| `currency-exchange` | Float arithmetic, floor division |

### Intro / Onboarding
| Exercise | Key Concept |
|---|---|
| `guidos-gorgeous-lasagna` | Constants, basic functions, docstrings |

---

## Running Tests

Each exercise includes Exercism's official test suite:

```bash
cd python/<exercise-name>
python <exercise>_test.py
```

Or with pytest for cleaner output:

```bash
pip install pytest
pytest python/<exercise-name>/
```

---

## Notes

- `__pycache__/` directories are gitignored going forward — clean your local tree with `find . -type d -name __pycache__ -exec rm -rf {} +`
- Each solution file contains only the implementation — test files are Exercism's unmodified suite
- Type hints are added where Exercism's stub doesn't include them
