# /bash — Exercism Bash Track

11 completed exercises from the [Exercism Bash track](https://exercism.org/tracks/bash). Each solution is idiomatic Bash, tested against the official bats suite, and held to production scripting standards.

---

## Completed Exercises

| Exercise | Concepts |
|---|---|
| `hello-world` | Script skeleton, `echo`, exit codes |
| `two-fer` | Default parameter handling, string interpolation |
| `hamming` | String iteration, character comparison, counter logic |
| `leap` | Modular arithmetic, `(( ))` arithmetic conditions |
| `grains` | Bit shifting `$(( 1 << n ))`, boundary validation |
| `reverse-string` | String reversal, parameter expansion vs `rev` |
| `binary-search` | Iterative bisection, index arithmetic, `(( ))` guards |
| `armstrong-numbers` | Digit decomposition, exponentiation in Bash |
| `allergies` | Bitmask operations, bitwise AND in Bash arithmetic |
| `error-handling` | Exit codes, `trap`, error propagation patterns |
| `difference-of-squares` | Arithmetic series formulas, `(( ))` |

---

## Solution Standards

All solutions follow the same baseline:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

- `[[ ]]` for all conditionals — not `[ ]`
- `(( ))` for arithmetic — not `expr` or `let`
- Errors to `stderr` via `>&2`, not mixed with `stdout`
- No unnecessary subshells — prefer builtins and parameter expansion
- `mapfile` / `readarray` for multi-line input where needed

---

## Running Tests

Each exercise ships with [bats-core](https://github.com/bats-core/bats-core) tests:

```bash
# Install bats (Arch)
sudo pacman -S bash-bats

# Run an exercise
cd bash/binary-search
bats binary_search.bats
```

---

## Track Progress

11 / ~90 exercises complete. New exercises added in monthly batches once polished.

Full track: [exercism.org/tracks/bash](https://exercism.org/tracks/bash)
