# Phase Control Layer (PCL) — Mini Neural Engine

> **Status:** Early draft / active development · Not yet production-ready

A lightweight neural architecture layer built on **SO(k) rotation geometry**. The PCL inserts structured, mathematically grounded rotation matrices between standard neural layers — adding directional phase coherence to weight updates without the overhead of a full attention mechanism.

This is the AI backend powering the game engines on [portfolio.remotevault.cc](https://portfolio.remotevault.cc).

---

## What Is This?

Most neural network weight updates are unconstrained — gradients push weights in arbitrary directions, which works but discards geometric structure. The PCL constrains weight updates to lie on the **SO(k) manifold** (the group of k×k rotation matrices with determinant 1), so each update is a *rotation* rather than an arbitrary nudge.

The result is a layer that:
- Preserves vector norms through the rotation (no vanishing/exploding gradient contribution from the PCL itself)
- Introduces structured directional bias via **Givens rotation** composition
- Adds ~0.27% parameter overhead over a baseline dense layer
- Runs as a drop-in wrapper — no changes to the surrounding architecture required

---

## Mathematical Foundation

### SO(k) Rotation Matrices

A rotation matrix **R ∈ SO(k)** satisfies:

```
R^T R = I    (orthogonality)
det(R) = 1   (proper rotation, no reflection)
```

The PCL parameterizes **R** as a product of **Givens rotations** — elementary 2D rotations embedded in k-dimensional space:

```
G(i, j, θ) =  I  except at positions:
    [i,i] = cos(θ)
    [j,j] = cos(θ)
    [i,j] = -sin(θ)
    [j,i] =  sin(θ)
```

A full SO(k) matrix is built by composing k(k-1)/2 Givens rotations — one per independent rotation plane. Each angle θ is a learnable parameter.

### Forward Pass

```
y = R(θ) · x
```

Where:
- `x` is the input vector of dimension k
- `R(θ)` is the composed Givens rotation matrix parameterized by learned angles `θ`
- `y` is the phase-rotated output, same dimension as `x`

### Parameter Count

For a layer of dimension k:
- Standard dense layer: k²
- PCL overhead: k(k-1)/2 angles
- Overhead ratio: `(k(k-1)/2) / k²` → approaches 0.5 as k → ∞, but in practice ~0.27% at tested dimensions

---

## Architecture

```
Input x (dim k)
     │
     ▼
┌─────────────────────────┐
│  Givens Rotation Stack  │  ← k(k-1)/2 learnable angles θ
│  G(0,1,θ₀₁) ·          │
│  G(0,2,θ₀₂) ·          │
│  G(1,2,θ₁₂) · ...      │
└─────────────────────────┘
     │
     ▼
R(θ) · x   (SO(k) rotation applied)
     │
     ▼
Output y (dim k)  →  downstream layer
```

The PCL sits *between* standard layers. It does not replace them — it modulates the direction of activations passing through, introducing learned rotational structure.

---

## Implementation

### Core Components

| File | Description |
|---|---|
| `pcl_engine/pcl_layer.py` | `PCLLayer` — PyTorch `nn.Module` implementing Givens rotation stack |
| `pcl_engine/givens.py` | Givens rotation matrix construction and SO(k) composition |
| `pcl_engine/model.py` | `PCLModel` — baseline network with PCL inserted between layers |
| `pcl_engine/benchmark.py` | Parameter overhead and CPU compute overhead benchmarks |
| `pcl_engine/ollama_export.py` | Export pipeline for Ollama-compatible streaming inference |

### PCLLayer (sketch)

```python
import torch
import torch.nn as nn
import math

class PCLLayer(nn.Module):
    """
    Phase Control Layer using SO(k) Givens rotation matrices.

    Args:
        dim (int): Dimension of the rotation space k.
    """
    def __init__(self, dim: int) -> None:
        super().__init__()
        self.dim = dim
        # One learnable angle per rotation plane
        n_angles = dim * (dim - 1) // 2
        self.angles = nn.Parameter(torch.zeros(n_angles))

    def _build_rotation(self) -> torch.Tensor:
        """Compose k(k-1)/2 Givens rotations into a single SO(k) matrix."""
        R = torch.eye(self.dim, device=self.angles.device)
        idx = 0
        for i in range(self.dim):
            for j in range(i + 1, self.dim):
                theta = self.angles[idx]
                G = torch.eye(self.dim, device=self.angles.device)
                G[i, i] =  torch.cos(theta)
                G[j, j] =  torch.cos(theta)
                G[i, j] = -torch.sin(theta)
                G[j, i] =  torch.sin(theta)
                R = G @ R
                idx += 1
        return R

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        R = self._build_rotation()
        return x @ R.T
```

---

## Benchmarks

Tested against a baseline two-layer MLP (dim=64) on CPU:

| Metric | Value |
|---|---|
| Parameter overhead | ~0.27% |
| CPU compute overhead | ~71% |
| Output norm preservation | ✅ Exact (‖Rx‖ = ‖x‖) |
| Gradient flow | ✅ Clean (no vanishing/exploding from PCL) |

The compute overhead is expected — full Givens stack construction is O(k³) per forward pass. Optimization via cached rotation matrices and sparse composition is on the roadmap.

---

## Ollama Export

The PCL model exports to an Ollama-compatible format for local LLM-style streaming inference. The export pipeline in `ollama_export.py` serializes the full model state (base weights + PCL angles) into a format the Ollama runtime can serve.

This is what powers the AI game backends on [portfolio.remotevault.cc](https://portfolio.remotevault.cc) — the Tic-Tac-Toe minimax engine and the Minesweeper constraint solver both route through the PCL inference layer.

---

## Status & Roadmap

This is an **early draft** — the mathematics is correct and benchmarked, but the implementation is being cleaned up for public release.

| Item | Status |
|---|---|
| Givens rotation stack | ✅ Implemented |
| SO(k) orthogonality verified | ✅ Benchmarked |
| Parameter overhead measured | ✅ ~0.27% |
| PyTorch `nn.Module` wrapper | ✅ Working |
| Ollama export pipeline | ✅ Working |
| Sparse/cached rotation optimization | 🔄 In progress |
| Full test suite | 🔄 In progress |
| Game engine integration (Minesweeper, TTT) | 🔄 In progress |
| Production-ready release | 📋 Planned |

---

## Research Context

This architecture was developed alongside Hopfield network research at UT Austin's Neuroscience Lab. The core idea — using SO(k) geometry to impose structure on neural updates — draws from:

- Geometric deep learning (Bronstein et al.)
- Lie group methods in neural ODEs
- Orthogonal RNN research (Arjovsky et al., *Unitary Evolution RNNs*)

The PCL is not claiming to replicate any of these — it's a practical engineering layer that borrows the geometric intuition and applies it at inference time in a lightweight, composable form.

---

## Dependencies

```bash
pip install torch          # PCL layer and model
pip install numpy          # benchmarking utilities
# ollama                   # required for export pipeline (install separately)
```

---

## Citation / Use

This is original work. If you build on it, a credit to [tcrz2xc](https://github.com/tcrz2xc) / [portfolio.remotevault.cc](https://portfolio.remotevault.cc) is appreciated but not required under the MIT license.
