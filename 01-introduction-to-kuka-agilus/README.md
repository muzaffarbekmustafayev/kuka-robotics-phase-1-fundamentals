# Introduction to KUKA KR AGILUS Manipulator & Safety Standards
## KUKA KR AGILUS manipulyatoriga kirish va xavfsizlik standartlari | Введение в манипулятор KUKA KR AGILUS и стандарты безопасности

[![Phase](https://img.shields.io/badge/Phase-kuka-robotics-phase-1-fundamentals-blue.svg)](#)
[![Robot: KUKA KR 6 R900-2](https://img.shields.io/badge/KUKA-KR%206%20R900--2%20(AGILUS)-orange.svg)](https://www.kuka.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)

---

### 🌐 Overview & Multilingual Summary

#### 🇺🇿 O'zbekcha:
KR 6 R900-2 mexanik anatomiyasi, o'qlar joylashuvi (A1..A6), KRC4/KRC5 kontrollerlari va ISO 10218 xalqaro xavfsizlik normalari.

#### 🇷🇺 Русский:
Механическая анатомия KR 6 R900-2, кинематическая схема осей (A1..A6), контроллеры KRC4/KRC5 и нормы безопасности ISO 10218.

#### 🇬🇧 English:
Mechanical anatomy of KR 6 R900-2, axis layout (A1..A6), KRC4/KRC5 controllers, and ISO 10218 industrial safety standards.

---

### 🗂️ Directory Structure (Mandatory Boilerplate)
```
01-introduction-to-kuka-agilus/
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
