# 3-Dars: Virtual Simulyatsiya va Digital Twin (KUKA.Sim Pro & OfficeLite)
## 1-Bob: Asoslar va Simulyatsiya | KUKA KR 6 R900-2

[![Faza: 1-Asoslar](https://img.shields.io/badge/Faza-1--Asoslar-blue.svg)](../README.md)
[![Simulyatsiya: KUKA.Sim Pro](https://img.shields.io/badge/Simulyatsiya-KUKA.Sim%20Pro%204.x-purple.svg)](https://www.kuka.com)
[![Kontroller: OfficeLite VRC](https://img.shields.io/badge/VRC-OfficeLite%20KSS%208.6-red.svg)](https://www.kuka.com)

---

## 🎯 Darsning Maqsadi va Natijasi

* **Maqsad:** KUKA KR 6 R900-2 manipulyatori uchun 3D virtual hujayra qurish, KUKA.Sim Pro va KUKA OfficeLite VRC (Virtual Robot Controller) o'rtasidagi real vaqtli sinxronizatsiya mexanizmini va $12\text{ ms}$ lik interpolatsiya siklini matematik modellashtirish.
* **Natija:** VRC paketlarini generatsiya qiluvchi, tarmoq kechikishi va jitterini hisoblovchi hamda real vaqt talablariga mosligini tekshiruvchi Python moduli (`digital_twin_sync.py`), to'liq unit testlar va KUKA.Sim Pro sozlamalari konspekti.

---

## 🧮 Matematik Apparat: Diskret Vaqtli Traektoriya Interpolatsiyasi

KUKA KSS kontrolleri bo'g'in burchaklarini uzluksiz emas, balki qat'iy deterministik diskret qadamlar bilan hisoblab boradi.

> **Teorema (Diskret Traektoriya Integrali):**
> KSS ning asosiy interpolatsiya sikli $T_s = 12\text{ ms} = 0.012\text{ s}$ bo'lsin. Har bir $k$-qadamdagi bo'g'in burchagi $\vec{q}_k$ oldingi qadam $\vec{q}_{k-1}$ va buyurilgan burchak tezligi $\dot{\vec{q}}_k$ orqali hisoblanadi:
> $$\vec{q}_k = \vec{q}_{k-1} + \int_{t_{k-1}}^{t_k} \dot{\vec{q}}(t) dt \approx \vec{q}_{k-1} + \dot{\vec{q}}_k \cdot T_s$$
> Real vaqtli sinxronizatsiya sharti (Jitter Compliance):
> $$\sigma_{latency} < \frac{T_s}{2} = 6.0\text{ ms}$$

---

## 💻 Python Dasturiy Moduli va Test Natijalari

* Kod: [`src/scripts/digital_twin_sync.py`](./src/scripts/digital_twin_sync.py)
* Test: [`src/scripts/test_digital_twin.py`](./src/scripts/test_digital_twin.py)

```bash
uv run --with numpy python src/scripts/digital_twin_sync.py
uv run --with numpy --with pytest pytest src/scripts/test_digital_twin.py
```
**Chiqish Natijasi:**
```text
==============================================================================
 KUKA DIGITAL TWIN 12ms VRC INTERPOLATION & JITTER BENCHMARK
==============================================================================
 Initial Home Joints (deg): [  0. -90.  90.   0.   0.   0.]
 Executed 50 VRC cycles (0.600 s):
 Final Joint Angles (deg): [ 18.  -84.   87.    0.    0.    0.]

VRC Communication Metrics:
 Mean Latency:   2.71 ms
 Latency Jitter: 1.25 ms
 Real-time Compliant (KSS < 6ms jitter): True
==============================================================================
```

---
🔗 **[Bosh Mundarijaga Qaytish](https://github.com/muzaffarbekmustafayev/kuka-industrial-robotics-syllabus)**
