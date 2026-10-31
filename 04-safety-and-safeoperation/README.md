# 04-Dars: Sanoat xavfsizligi va KUKA SafeOperation texnologiyasi
## Industrial Safety & KUKA SafeOperation Technology

[![Phase](https://img.shields.io/badge/Phase-kuka-robotics-phase-1-fundamentals-blue.svg)](#)
[![Robot: KUKA KR 6 R900-2](https://img.shields.io/badge/KUKA-KR%206%20R900--2%20(AGILUS)-orange.svg)](https://www.kuka.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)

---

### 🎯 1. Maqsad (Goal)
ISO 13849-1 (PL e, Cat 4), ISO 10218-1/2 va ISO/TS 15066 xalqaro xavfsizlik standartlari talablari asosida KUKA SafeOperation tizimida robotning 6 ta o'qining kinematik harakat diapazonlarini, 3D kartesian fazoviy monitoring zonalarini (Inclusion/Exclusion Zones) va favqulodda to'xtash trayektoriyasi masofasini ($S_p$) real vaqt rejimida dasturiy nazorat qilish.

---

### 📊 2. Natija (Result)
Ushbu dars yakunida quyidagi aniq natijalarga erishiladi:
1. **Python SafeOperation Supervisor (`safe_zones_monitor.py`):**
   - Robot TCP nuqtasi uchun 3D kuboid fazoviy monitoring (AABB inclusion/exclusion zonalar).
   - Safe Reduced Speed (SRS) nazorati ($v_{max} \le 250 \text{ mm/s}$ T1 rejimi uchun).
   - Reaksiya vaqti ($t_r = 20\text{ ms}$) va tormozlanish tezlanishi ($a_{brake} = 8000\text{ mm/s}^2$) hisobga olingan holda to'xtash masofasini hisoblash.
2. **Pytest Unit Testlari (`test_safe_zones.py`):**
   - Bo'g'in chegaralari, to'xtash masofasi formulasi va fazoviy cheklovlar uchun 100% muvaffaqiyatli testlar to'plami.
3. **KRL Ishlab chiqarish dasturi (`SAFE_ZONE.src` va `SAFE_ZONE.dat`):**
   - SafeOperation xavfsizlik signallari (`$IN[10]`, `$OUT[15]`), Safe Stop 1 (SS1) reaksiyasi va sekinlashtirilgan tezlik profili.

---

### 🧮 3. Matematik apparat va Teoremalar (Mathematics)

#### 3.1. Favqulodda to'xtash masofasi (Stopping Distance Model):
Robot $v$ tezlik bilan harakatlanayotganda favqulodda xavfsizlik to'xtashi uchun talab etiladigan masofa:

$$S_p = v \cdot t_r + \frac{v^2}{2 \cdot a_{max}} + C$$

bu yerda:
- $t_r = 0.020 \text{ s}$ — xavfsizlik shinasi va rele reaksiyasi vaqti;
- $a_{max} = 8000 \text{ mm/s}^2$ — maksimal favqulodda tormozlanish;
- $C = 50.0 \text{ mm}$ — xavfsizlik zaxira masofasi (margin).

Masalan, $v = 250 \text{ mm/s}$ bo'lganda:
$$S_p = (250 \cdot 0.02) + \frac{250^2}{16000} + 50 = 5.0 + 3.91 + 50.0 = 58.91 \text{ mm}$$

#### 3.2. Fazoviy kuboid cheklovi:
Fazodagi $P = [x, y, z]^T$ koordinatasi uchun ruxsat etilgan ish kamerasi:
$$x_{min} \le x \le x_{max} \land y_{min} \le y \le y_{max} \land z_{min} \le z \le z_{max}$$

To'liq matematik isbotlar [**docs/derivations.md**](./docs/derivations.md) da berilgan.

---

### 💻 4. Ishga tushirish va tekshirish (Execution & Verification)

Python skriptini ishga tushirish:
```bash
uv run --with numpy python src/scripts/safe_zones_monitor.py
```

Konsol chiqishi:
```
=================================================================
KUKA KR 6 R900-2 SafeOperation Supervisor Simulator
=================================================================

[Test 1] Pos: [450.   0. 500.], Vel: 200.0 mm/s
  Stopping distance: 56.50 mm
  Safe: True

[Test 2] Pos: [750. 100. 400.], Vel: 220.0 mm/s (In Exclusion Area)
  Safe: False (Violation detected!)

[Test 3] Pos: [450.   0. 500.], Vel: 450.0 mm/s (Excessive velocity)
  Speed safe: False, Overall safe: False
```

Avtomatlashtirilgan unit testlarni bajarish:
```bash
uv run --with numpy --with pytest pytest src/scripts/test_safe_zones.py
```

Natija: `4 passed in 0.11s`.

---

🔗 **[Bosh Mundarija / Return to Master Syllabus](https://github.com/muzaffarbekmustafayev/kuka-industrial-robotics-syllabus)**
