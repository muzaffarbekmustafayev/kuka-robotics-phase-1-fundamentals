# Sanoat xavfsizligi va SafeOperation matematik asoslari

## 1. Favqulodda to'xtash masofasi (Stopping Distance Calculation)

ISO 13855 va ISO/TS 15066 standartlariga asosan sanoat robotining xavfsizlik perimetri ichida to'liq to'xtashi uchun zarur minimal masofa $S_p$ quyidagi formula bilan aniqlanadi:

$$S_p = S_{reaction} + S_{braking} + C$$

bu yerda:
- $S_{reaction} = v \cdot t_r$ : Xavfsizlik signali aniqlanishi (safety PLC bus cycle, controller latency) davridagi bosib o'tilgan yo'l.
- $t_r$ : Umumiy reaksiya vaqti ($t_r \approx 0.020 \text{ s} = 20\text{ ms}$).
- $S_{braking} = \frac{v^2}{2 \cdot a_{max}}$ : Mexanik va elektrodinamik tormozlanish masofasi.
- $a_{max}$ : Maksimal ruxsat etilgan favqulodda tormoz sekinlanishi (KR 6 R900-2 uchun $a_{max} \approx 8000 \text{ mm/s}^2$).
- $C$ : Zaxira xavfsizlik masofasi (penetration depth factor, odatda $C \ge 50\text{ mm}$).

### Teorema 1 (Kritik xavfsiz masofa sharti):
Agar robot TCP nuqtasining chetga masofasi $d_{boundary}$ quyidagi shartni qanoatlantirsa:
$$d_{boundary} < v(t) \cdot t_r + \frac{v(t)^2}{2 a_{max}} + C$$
u holda SafeOperation tizimi darhol Safe Stop 1 (SS1) yoki Safe Stop 2 (SS2) to'xtash komandasini ishga tushirishi shart, aks holda chegara buzilishi muqarrar bo'ladi.

---

## 2. Fazoviy kuboid soha tekshiruvi (AABB Point Containment)

Fazoda robotning $P = [x, y, z]^T \in \mathbb{R}^3$ nuqtasi berilgan $B = [x_{min}, x_{max}] \times [y_{min}, y_{max}] \times [z_{min}, z_{max}]$ kuboid zonasiga tegishliligi:

$$\chi_B(P) = \begin{cases} 
1, & \text{agar } x_{min} \le x \le x_{max} \land y_{min} \le y \le y_{max} \land z_{min} \le z \le z_{max} \\
0, & \text{aksincha}
\end{cases}$$

Taqiqlangan hudud (Exclusion Zone) uchun xavfsizlik qoidasi:
$$\text{Safe}_{exclusion}(P) \iff \chi_B(P) = 0$$

Ruxsat etilgan ishchi kamera (Inclusion Zone) uchun:
$$\text{Safe}_{inclusion}(P) \iff \chi_B(P) = 1$$
