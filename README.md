<div align="center">

```
╔══════════════════════════════════════════════════════════════════╗
║  tcrz2xc / dev-portfolio                                         ║
║  Python · Bash · AI · Cloud · Cybersecurity · Data Analytics     ║
╚══════════════════════════════════════════════════════════════════╝
```

# Thomas Cruz Jr.

### CS Instructor · Data Engineer · Systems Architect · AI Researcher

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](./python)
[![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnu-bash&logoColor=white)](./bash_scripts)
[![AI](https://img.shields.io/badge/AI%20%2F%20Search-FF6F00?style=flat-square&logo=pytorch&logoColor=white)](./ai)
[![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?style=flat-square&logo=arch-linux&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](./projects)
[![Portfolio](https://img.shields.io/badge/Portfolio-remotevault.cc-00FFAA?style=flat-square&logo=astro&logoColor=black)](https://portfolio.remotevault.cc)

[![Google Cybersecurity](https://img.shields.io/badge/Google_Cybersecurity-Completed-4285F4?style=flat-square&logo=google&logoColor=white)](#certifications)
[![Google Data Analytics](https://img.shields.io/badge/Google_Data_Analytics-Completed-4285F4?style=flat-square&logo=google&logoColor=white)](#certifications)
[![Google Advanced Analytics](https://img.shields.io/badge/Google_Advanced_Analytics-Completed-4285F4?style=flat-square&logo=google&logoColor=white)](#certifications)

</div>

---

## About

Former **Apple** and **Meta/Cognizant** data engineer turned CS instructor. I build things that run in production — homelab infrastructure on bare metal, classical AI engines grounded in formal logic, and automation tooling that holds up under real workloads. This repo is a living record of everything I'm shipping.

> Data pipelines at Apple-scale · Neural net research at UT Austin's Neuroscience Lab · B.S. Physics + B.A. Mathematics

---

## Repository Map

| Folder | Lang | Contents |
|---|---|---|
| [`/ai`](./ai) | Python | Search algorithms, propositional logic engine, maze solver, knowledge-base AI |
| [`/python`](./python) | Python | 40+ Exercism exercises — algorithms, data structures, OOP, functional patterns |
| [`/bash_scripts`](./bash_scripts) | Bash | 30+ scripting exercises + production tooling in `done/` |
| [`/bash`](./bash) | Bash | 11 Exercism track solutions — idiomatic shell from fundamentals to error handling |
| [`/projects`](./projects) | Docker · YAML · MD | Hybrid cloud homelab: Cloudflare tunnel, Ollama, SearXNG, Tailscale, Jellyfin |

---

## Featured Work

### 🧠 AI — Search & Knowledge Representation [`/ai`](./ai)

Three classical AI domains implemented from scratch:

- **`maze.py`** — Pathfinding with BFS and DFS on ASCII maze grids (`maze1.txt`, `maze2.txt`, `maze3.txt`). Visualizes the explored frontier and solution path.
- **`clue.py`** — Knowledge-base AI using propositional logic. Builds a `knowledge` base from game state and runs model-checking inference to prove which suspects, rooms, and weapons are eliminated vs. uncertain.
- **`harry.py`** — Logical deduction puzzle solver using the same `logic.py` engine.
- **`logic.py`** — Custom propositional logic library: `Symbol`, `And`, `Or`, `Not`, `Implication`, `Biconditional`, `model_check()`.

**Incoming:** Minesweeper CSP solver · Minimax Tic-Tac-Toe · PCL neural engine (SO(k) rotations, Ollama export)

---

### 🐍 Python — Exercism Track [`/python`](./python)

40+ completed exercises covering the full Python curriculum:

| Category | Exercises |
|---|---|
| **Fundamentals** | `leap`, `grains`, `collatz-conjecture`, `raindrops`, `pangram` |
| **Strings** | `reverse-string`, `bob`, `isogram`, `rna-transcription`, `rotational-cipher`, `little-sisters-*` |
| **Data Structures** | `binary-search-tree`, `binary-search`, `all-your-base` |
| **Collections** | `card-games`, `cater-waiter` (sets), `inventory-management` (dicts), `mecha-munch-management`, `tisbury-treasure-hunt` (tuples) |
| **OOP / Classes** | `ellens-alien-game`, `black-jack` |
| **Loops / Iterators** | `making-the-grade`, `chaitanas-colossal-coaster`, `plane-tickets` (generators) |
| **Math / Logic** | `armstrong-numbers`, `perfect-numbers`, `darts`, `killer-sudoku-helper`, `triangle` |
| **Systems** | `meltdown-mitigation`, `ghost-gobble-arcade-game`, `locomotive-engineer` |

---

### 🔧 Bash Scripting Curriculum [`/bash_scripts`](./bash_scripts)

30+ scripts in `done/` covering the complete Bash language — built as a structured curriculum, not a random collection:

| Topic | Scripts |
|---|---|
| **I/O & Streams** | `read-input`, `00-while-read`, `01-forever-read`, `00-basic-reader`, `char-by-char` |
| **Data Structures** | `indexed-arrays`, `associative-arrays`, `01-mapfile` |
| **Control Flow** | `conditionals`, `for-loops`, `loop`, `case`, `01-case` |
| **String / Expansion** | `parameter-expansion`, `curly-brace-expansion`, `braces-numeric`, `command-substitution`, `process-substitution`, `curly-vs-parens` |
| **Arithmetic** | `arithmetic-expression` |
| **Functions & Structure** | `00-simple`, `00-simple-script`, `01-better`, `03-all-in-one`, `greeter` |
| **Error Handling** | `return-codes`, `01-syntax-error`, `02-undefined`, `04-trap-info` |
| **Terminal / UX** | `256-colors`, `move-cursor`, `say-hi`, `say-bye`, `hello` |
| **Data Processing** | `02-client-writer`, `format_00` (CSV processing with `complex.csv`, `simple.csv`) |

---

### 📚 Bash — Exercism Track [`/bash`](./bash)

11 completed exercises with full bats test suites:

`hello-world` · `two-fer` · `hamming` · `leap` · `grains` · `reverse-string` · `binary-search` · `armstrong-numbers` · `allergies` · `error-handling` · `difference-of-squares`

---

### ☁️ Hybrid Cloud Infrastructure [`/projects`](./projects)

Self-hosted homelab stack on Arch Linux — documented with architecture diagrams, changelog, and postmortem:

**NAS Stack:** Cloudflare Tunnel · Jellyfin · Ollama · SearXNG · Tailscale
**Cloud Stack:** Separate compose stack with push workflow
**Docs:** `architecture-overview.md` · `vpn-vs-tunnel.md` · `POSTMORTEM.md` · `CHANGELOG.md`

---

## Skills

```
Languages     Python  ·  Bash/Shell  ·  POSIX sh  ·  SQL  ·  YAML
AI            Search (BFS/DFS)  ·  Propositional Logic  ·  Model Checking
              Constraint Satisfaction  ·  Hopfield Networks  ·  PCL Architecture
Data          pandas  ·  NumPy  ·  SQLite  ·  ETL Pipelines  ·  Statistical Modeling
Systems       Arch Linux  ·  Docker  ·  ZFS  ·  Btrfs  ·  systemd  ·  Nginx
Security      Snort IDS  ·  fail2ban  ·  SSH Hardening  ·  NIST Framework  ·  CIA Triad
              Google Cybersecurity Certificate curriculum
Networking    Cloudflare Tunnel  ·  Tailscale  ·  VPN/Tunnel design  ·  Reverse Proxy
Web / Dev     Astro  ·  FastAPI  ·  WebSockets  ·  Paramiko  ·  Git  ·  Neovim
Teaching      AP CS  ·  Data Structures  ·  Algorithms  ·  Python  ·  Cybersecurity
```

---

## Certifications

| Certificate | Issuer | Status |
|---|---|---|
| PCEP — Certified Entry-Level Python Programmer | Python Institute | ✅ |
| Google Cybersecurity Professional Certificate | Google / Coursera | ✅ |
| Google Data Analytics Professional Certificate | Google / Coursera | ✅ |
| Google Advanced Data Analytics Certificate | Google / Coursera | ✅ |
| RHCSA — Red Hat Certified System Administrator | Red Hat | 🔄 In Progress |

---

## Update Cadence

Monthly bundled pushes. Each push represents completed, tested work — no noise commits. **Watch** this repo to get notified of drops.

---

<div align="center">

[portfolio.remotevault.cc](https://portfolio.remotevault.cc) · [LinkedIn](https://linkedin.com/in/tom-cruz-136649ab/) · [GitHub](https://github.com/tcrz2xc/py1)

*Runs on Arch. Built from first principles.*

</div>
