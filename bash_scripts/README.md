# /bash_scripts — Bash Scripting Curriculum

A structured progression through the Bash language, built as a hands-on curriculum. The `done/` folder contains ~30 completed scripts organized by topic. Scripts in the repo root are active development or supporting files.

---

## Structure

```
bash_scripts/
├── done/              # completed, tested scripts
├── files/             # sample files for script exercises (foo/bar/baz .txt/.jpg)
├── lib/               # shared library functions (greetings)
├── empty/             # edge case testing directory
├── armstrong          # WIP — Armstrong number checker
├── check-terminal     # WIP — terminal detection
├── format_00          # CSV formatter
├── data.txt           # sample data for stream scripts
└── log.txt            # sample log for parsing scripts
```

---

## `done/` — Completed Scripts by Topic

### I/O & Stream Processing
| Script | Demonstrates |
|---|---|
| `read-input` | `read` builtin, prompts, variable capture |
| `00-while-read` | `while read` loop for line-by-line processing |
| `01-forever-read` | Persistent read loop with exit condition |
| `00-basic-reader` | Basic file reading via redirection |
| `char-by-char` | Character-level iteration with `fold` / `read -n1` |
| `02-client-writer` | Writing structured output, client simulation |

### Arrays
| Script | Demonstrates |
|---|---|
| `indexed-arrays` | Declaration, indexing, slicing, iteration |
| `associative-arrays` | `declare -A`, key-value ops, iteration patterns |
| `01-mapfile` | `mapfile`/`readarray` — safe multi-line input into arrays |

### Control Flow
| Script | Demonstrates |
|---|---|
| `conditionals` | `if/elif/else`, `[[ ]]` tests, file/string/numeric checks |
| `for-loops` | `for` over lists, ranges, arrays, globs |
| `loop` | `while` and `until` with counters |
| `case` | `case` statement, pattern matching |
| `01-case` | `case` with multiple patterns and fall-through |

### String & Parameter Operations
| Script | Demonstrates |
|---|---|
| `parameter-expansion` | `${var:-default}`, `${#var}`, `${var:offset:len}`, `${var//pat/rep}` |
| `curly-brace-expansion` | `{a,b,c}`, `{1..10}`, nested brace expansion |
| `braces-numeric` | Numeric sequences with step `{0..100..5}` |
| `command-substitution` | `$(...)` vs backticks, capturing output |
| `process-substitution` | `<(...)` and `>(...)` — treating process output as files |
| `curly-vs-parens` | Brace groups `{ }` vs subshells `( )` — scope and performance |

### Arithmetic
| Script | Demonstrates |
|---|---|
| `arithmetic-expression` | `$(( ))`, `let`, `(( ))` — all three arithmetic forms |

### Functions & Script Structure
| Script | Demonstrates |
|---|---|
| `00-simple` | Minimal correct script skeleton |
| `00-simple-script` | Hardened template: `set -euo pipefail`, IFS, usage, exit codes |
| `01-better` | Refactored structure — functions, local vars, return values |
| `03-all-in-one` | Full script combining I/O, arrays, functions, error handling |
| `greeter` | Function with arguments, `$@` / `$*` handling |
| `say-hi` / `say-bye` | Library-style functions sourced via `lib/` |
| `hello` | Entry-point script sourcing from `lib/greetings` |

### Error Handling & Debugging
| Script | Demonstrates |
|---|---|
| `return-codes` | `$?`, explicit `exit N`, error propagation |
| `01-syntax-error` | Intentional syntax error — `bash -n` and debugging |
| `02-undefined` | `set -u` behavior with unbound variables |
| `04-trap-info` | `trap`, `ERR`, `EXIT`, `SIGINT` — cleanup and signal handling |

### Terminal & Output Formatting
| Script | Demonstrates |
|---|---|
| `256-colors` | ANSI escape codes, 256-color palette display |
| `move-cursor` | Cursor positioning with `tput` / escape sequences |

### Data Processing
| Script | Demonstrates |
|---|---|
| `format_00` | CSV parsing — field splitting, `IFS`, output formatting |

---

## Coding Standards

Every script in `done/` meets these requirements before it's committed:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

- Zero `shellcheck` warnings at `--severity=warning`
- No useless `cat` — redirect from files directly
- `mapfile` for array ingestion, never `for i in $(command)`
- All errors to `stderr` (`>&2`), all output to `stdout`
- Every variable expansion is quoted: `"${var}"`
- Functions use `local` for all variables
