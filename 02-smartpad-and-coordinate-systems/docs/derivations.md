# Homogeneous Frame Transformation and Kinematic Tree Composition Theorem
## Matematik Isbot va KUKA KR 6 R900-2 uchun Hisoblash

### Asosiy Formula:
$$T_{BASE}^{TOOL} = (T_{WORLD}^{BASE})^{-1} \cdot T_{WORLD}^{FLANGE} \cdot T_{FLANGE}^{TOOL}$$

---

### 1. Nazariy Asos va Teorema (Theoretical Foundation & Theorem)
Robot manipulyatorida fazoviy koordinatalar zanjiri Maxsus Evklid Guruhi $SE(3)$ elementlari orqali bog'lanadi.
smartPAD pultida turli koordinata tizimlarida (WORLD, BASE, TOOL, JOINT) harakatlanish (Jogging) quyidagi fundamental teoremaga asoslanadi:

> **Teorema (Koordinata Zanjiri Teoremasi):** 
> Ixtiyoriy $A, B, C$ koordinatalar tizimlari uchun $T_C^A = T_B^A \cdot T_C^B$. Har bir bir jinsli transformatsiya matritsasi $T \in SE(3)$ ortogonal aylanish $R \in SO(3)$ va siljish vektoridan $ec{p} \in \mathbb{R}^3$ iborat:
> $$T = \begin{bmatrix} R & \vec{p} \\ \vec{0}^T & 1 \end{bmatrix}, \quad T^{-1} = \begin{bmatrix} R^T & -R^T \vec{p} \\ \vec{0}^T & 1 \end{bmatrix}$$

### 2. Formulaning Qadam-baqadam Keltirib Chiqarilishi (Derivation & Proof)
1. Dunyo koordinata tizimi $\{W\}$ ga nisbatan robot bazasi $\{B\}$ va flanets $\{F\}$ o'rnatilgan:
   $$P^W = T_B^W P^B, \quad P^W = T_F^W P^F$$
2. Flanetsga asbob (Tool Center Point — TCP) $\{T\}$ mahkamlangan: $P^F = T_T^F P^T$.
3. Operator BASE tizimiga nisbatan asbob uchini boshqarganda, asbob koordinatalari $P^B$ quyidagicha topiladi:
   $$P^B = (T_B^W)^{-1} P^W = (T_B^W)^{-1} T_F^W T_T^F P^T$$
4. Natijada KUKA kontrolleridagi `$POS_ACT` ($T_T^B$) transformatsiyasi hosil bo'ladi:
   $$T_T^B = (T_B^W)^{-1} \cdot T_F^W \cdot T_T^F$$

### 3. KUKA KR 6 R900-2 Manipulyatori uchun Tatbiqi
* KUKA tizimida `$BASE` koordinatalari: $\{X, Y, Z, A, B, C\}$
* Asbob koordinatalari `$TOOL`: $\{X, Y, Z, A, B, C\}$
* Flanes koordinatalari: `$FLANGE` (o'q $A_6$ ning mexanik uchi)
* O'qlar bo'yicha harakatda (JOINT Jogging): har bir bo'g'in burchagi $\Delta q_i$ mustaqil o'zgaradi.
* Dekart harakatida (WORLD/BASE Jogging): kontroller har bir interpolatsiya qadamida (12ms) teskari kinematikani hisoblab, barcha 6 ta motorga bir vaqtda mos burchak tezliklarini $\dot{\vec{q}}$ uzatadi.

