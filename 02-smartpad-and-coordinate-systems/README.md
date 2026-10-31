# 2-Dars: smartPAD Interfeysi va Koordinata Tizimlari Mexanikasi
## 1-Bob: Asoslar va Simulyatsiya | KUKA KR 6 R900-2

[![Faza: 1-Asoslar](https://img.shields.io/badge/Faza-1--Asoslar-blue.svg)](../README.md)
[![Robot: KUKA KR 6 R900-2](https://img.shields.io/badge/Robot-KUKA%20KR%206%20R900--2-orange.svg)](https://www.kuka.com)
[![Mavzu: Koordinatalar](https://img.shields.io/badge/Mavzu-WORLD%20%7C%20BASE%20%7C%20TOOL%20%7C%20JOINT-green.svg)](#)

---

## 🎯 Darsning Maqsadi va Natijasi

* **Maqsad:** KUKA smartPAD boshqaruv pultidagi 4 xil koordinata tizimlari (WORLD, BASE, TOOL, JOINT) o'rtasidagi fazoviy bog'lanish matematikasini o'rganish va asbob uchini (TCP) bitta nuqtada saqlagan holda orientatsiyani burish hamda asbob o'qi bo'yicha siljitish algoritmini dasturlash.
* **Natija:** Koordinata transformatsiyalarini hisoblovchi, KUKA FRAME formatini $4\times 4$ bir jinsli matritsaga o'tkazuvchi va smartPAD Tool Jogging harakatini simulyatsiya qiluvchi Python moduli (`coordinate_transforms.py`) hamda sanoat KRL dasturi (`JOG_FRAMES.src`).

---

## 🧮 Matematik Apparat: Koordinatalar Zanjiri Teoremasi

Robototexnikada fazoviy transformatsiyalar Maxsus Evklid Guruhi $SE(3)$ orqali ifodalanadi.

> **Teorema (Koordinata Zanjiri Teoremasi):**
> Dunyo tizimi $\{W\}$, Robot bazasi $\{B\}$, Mexanik flanets $\{F\}$ va Asbob markazi (TCP) $\{T\}$ orasidagi bog'lanish quyidagi yopiq zanjir orqali hisoblanadi:
> $$T_{BASE}^{TOOL} = (T_{WORLD}^{BASE})^{-1} \cdot T_{WORLD}^{FLANGE} \cdot T_{FLANGE}^{TOOL}$$
> Bir jinsli transformatsiya matritsasining teskarisi ($T^{-1}$):
> $$T = \begin{bmatrix} R & \vec{p} \\ \vec{0}^T & 1 \end{bmatrix} \implies T^{-1} = \begin{bmatrix} R^T & -R^T \vec{p} \\ \vec{0}^T & 1 \end{bmatrix}$$

### 📐 KUKA Geometrik Operatori (:) Matematikasi
KRL dasturlash tilidagi `:` operatori (Frame Multiplication) ikkita fazoviy freymni matritsaviy ko'paytirish demakdir:
$$P_{new} = P_{act} : \Delta P_{tool}$$
$$T_{new} = T_{act} \cdot T_{\Delta}$$

Asbob o'qi bo'ylab $+50\text{ mm}$ siljishda:
$$\Delta T = \begin{bmatrix} I_{3\times 3} & [0, 0, 50]^T \\ \vec{0}^T & 1 \end{bmatrix}$$

---

## 💻 Python Dasturiy Moduli va Test Natijalari

* Kod: [`src/scripts/coordinate_transforms.py`](./src/scripts/coordinate_transforms.py)
* Test: [`src/scripts/test_coordinate_transforms.py`](./src/scripts/test_coordinate_transforms.py)

```bash
uv run --with numpy python src/scripts/coordinate_transforms.py
uv run --with numpy --with pytest pytest src/scripts/test_coordinate_transforms.py
```
**Chiqish Natijasi (Konsol):**
```text
==============================================================================
 KUKA KR 6 R900-2 COORDINATE SYSTEMS & JOGGING TRANSFORMATION DEMO
==============================================================================
 BASE Frame:        X=200.0, Y=100.0, Z=0.0
 TOOL Frame:        X=0.0, Y=0.0, Z=150.0
 FLANGE (in World): X=600.0, Y=300.0, Z=500.0, A=45.0°
 Computed TCP in BASE Frame:
   --> X=382.84 mm, Y=324.26 mm, Z=650.00 mm, A=45.00°

 After smartPAD Jogging +50mm along local Tool +Z axis:
   --> New TCP in BASE: X=382.84 mm, Y=324.26 mm, Z=700.00 mm
==============================================================================
```

---

## 🤖 KRL Dasturi: `JOG_FRAMES.src`

```krl
$TOOL = TOOL_DATA[1]
$BASE = BASE_DATA[1]

; Asbob Z o'qi bo'ylab +50mm siljish
LIN $POS_ACT : {X 0.0, Y 0.0, Z 50.0, A 0.0, B 0.0, C 0.0}
```

---
🔗 **[Bosh Mundarijaga Qaytish](https://github.com/muzaffarbekmustafayev/kuka-industrial-robotics-syllabus)**
