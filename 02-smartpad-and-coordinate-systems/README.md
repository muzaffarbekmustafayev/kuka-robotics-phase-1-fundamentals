# SmartPAD Interface & Mechanics of Coordinate Systems
## SmartPAD interfeysi va koordinata tizimlari mexanikasi | Интерфейс SmartPAD и механика систем координат

[![Phase](https://img.shields.io/badge/Phase-kuka-robotics-phase-1-fundamentals-blue.svg)](#)
[![Robot: KUKA KR 6 R900-2](https://img.shields.io/badge/KUKA-KR%206%20R900--2%20(AGILUS)-orange.svg)](https://www.kuka.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)

---

### 🌐 Overview & Multilingual Summary

#### 🇺🇿 O'zbekcha:
smartPAD boshqaruvi, 6D Space Mouse fizikasi. WORLD, BASE, TOOL va JOINT koordinata tizimlari transformatsiyasi.

#### 🇷🇺 Русский:
Управление через smartPAD, физика 6D Space Mouse. Трансформация систем координат WORLD, BASE, TOOL и JOINT.

#### 🇬🇧 English:
smartPAD operations, 6D Space Mouse mechanics. Kinematic transformations between WORLD, BASE, TOOL, and JOINT frames.

---

### 🗂️ Directory Structure (Mandatory Boilerplate)
```
02-smartpad-and-coordinate-systems/
├── src/
│   ├── krl/            # Production KRL code (.src, .dat) [All code & comments in English]
│   └── scripts/        # Python verification scripts (.py) [All code & comments in English]
├── sim/                # KUKA.Sim Pro layouts (.vcmx), URDF and CAD models
├── docs/               # Theoretical diagrams, figures, and proofs
├── CLAUDE.md           # AI developer instructions
└── README.md           # Trilingual guide (Uzbek, Russian, English)
```

---

### 🧮 Mathematical Foundations & Verification
All formulas, derivations, and theorems for this lesson are detailed in [**docs/derivations.md**](./docs/derivations.md).
Runnable Python verification scripts are provided in `src/scripts/verify_theorem.py`.

To run the verification test:
```bash
uv run --with numpy python src/scripts/verify_theorem.py
```

---
🔗 **[Return to Master Syllabus / Bosh Mundarija](https://github.com/muzaffarbekmustafayev/kuka-industrial-robotics-syllabus)**
