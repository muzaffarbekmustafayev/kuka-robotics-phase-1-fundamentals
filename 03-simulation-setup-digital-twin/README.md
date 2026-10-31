# Virtual Simulation & Digital Twin Setup (KUKA.Sim Pro & OfficeLite)
## Virtual simulyatsiya va Digital Twin (KUKA.Sim Pro & OfficeLite) | Виртуальная симуляция и Цифровой Двойник (KUKA.Sim Pro и OfficeLite)

[![Phase](https://img.shields.io/badge/Phase-kuka-robotics-phase-1-fundamentals-blue.svg)](#)
[![Robot: KUKA KR 6 R900-2](https://img.shields.io/badge/KUKA-KR%206%20R900--2%20(AGILUS)-orange.svg)](https://www.kuka.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)

---

### 🌐 Overview & Multilingual Summary

#### 🇺🇿 O'zbekcha:
KUKA.Sim Pro va KUKA OfficeLite VRC ko'prigi, KR 6 R900-2 uchun raqamli egizak (Digital Twin) muhitini sozlash.

#### 🇷🇺 Русский:
Мост взаимодействия KUKA.Sim Pro и KUKA OfficeLite VRC, развертывание цифрового двойника для KR 6 R900-2.

#### 🇬🇧 English:
Communication bridge between KUKA.Sim Pro and KUKA OfficeLite VRC, deploying the KR 6 R900-2 digital twin environment.

---

### 🗂️ Directory Structure (Mandatory Boilerplate)
```
03-simulation-setup-digital-twin/
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
