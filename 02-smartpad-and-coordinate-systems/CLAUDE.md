# AI Developer Instructions: 02-smartpad-and-coordinate-systems

## 🎯 Lesson Context: SmartPAD interfeysi va fazoviy koordinata tizimlari
Belongs to **Phase 1: Asoslar, Xavfsizlik va Digital Twin** of the KUKA Industrial Robotics Course.
Target Manipulator: **KUKA KR 6 R900-2 (KR AGILUS-2)**.

## 📁 Internal Boilerplate Structure
* `src/krl/`: Industrial KRL files (`.src`, `.dat`) strictly formatted for KSS 8.3+.
* `src/scripts/`: Python 3.10+ verification scripts with type hinting and `pytest` tests.
* `sim/`: Simulation scenes (`.vcmx`, `.urdf`).
* `docs/`: Mathematical derivations and schematics.
* `README.md`: Comprehensive student guide in Uzbek/English with formulas and tasks.

## 📐 Mathematical Standards
Follow the notation defined in the course master cheatsheet:
* Skew-symmetric operator: $[\vec{k}]_\times$
* Rodrigues formula: $R(\vec{k}, \theta) = I + \sin\theta K + (1-\cos\theta)K^2$
* KUKA Euler convention: Tait-Bryan $Z-Y'-X''$ ($A, B, C$)
