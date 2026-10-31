# Mathematical Foundations & Derivations: Workspace Envelope and Braking Calculus
## KUKA KR 6 R900-2 (KR AGILUS-2) | Lesson 01

---

## 🌐 1. Theoretical Foundations & Theorems

### 🇺🇿 O'zbekcha:
Ushbu bo'limda KUKA KR 6 R900-2 manipulyatorining ishchi fazosi (Workspace Envelope) va ISO 10218-1 bo'yicha tormozlanish masofasi hisob-kitoblarining matematik teoremalari hamda ularning qadam-baqadam isbotlari keltiriladi.

### 🇷🇺 Русский:
В данном разделе представлены математические теоремы, строгий аналитический вывод уравнений рабочей зоны (Workspace Envelope) манипулятора KUKA KR 6 R900-2 и расчет тормозного пути согласно стандарту безопасности ISO 10218-1.

### 🇬🇧 English:
This document details the mathematical theorems, step-by-step analytical derivations of the reachable workspace envelope, and emergency stopping distance calculus for the KUKA KR 6 R900-2 industrial manipulator in compliance with ISO 10218-1 and ISO 13849-1.

---

## 📐 2. Theorem 1: Geometric Reach Envelope & Triangle Inequality Bound

### 🇺🇿 Teorema 1 (Geometrik Yetib Borish Chegarasi):
> Manipulyator bazasi koordinatalar boshi $O = [0, 0, 0]^T$ bo'lsin. Yelka aylanma o'qi markazi $S = [a_1, 0, d_1]^T$ nuqtada joylashgan. Manipulyator sferik bilak markazi $\vec{p}_{wc}$ va mexanik flanets $\vec{p}_f$ ning maksimal yetib borish masofasi bo'g'in zvenolari uzunliklarining uchburchak tengsizligi orqali chegaralanadi:
> $$R_{max, wc} = a_2 + \sqrt{a_3^2 + d_4^2}$$
> $$R_{max, flange} = \sqrt{(a_1 + a_2 + a_3)^2 + (d_4 + d_6)^2} \approx 901.5\text{ mm}$$
> Ichki o'lik zona (singulyar minimal radius):
> $$R_{min, wc} = |a_2 - \sqrt{a_3^2 + d_4^2}| \approx 33.54\text{ mm}$$

### 🇷🇺 Теорема 1 (Геометрическая Граница Рабочей Зоны):
> Пусть начало координат базовой системы робота $O = [0, 0, 0]^T$. Центр плечевого шарнира находится в точке $S = [a_1, 0, d_1]^T$. Максимальный радиус досягаемости центра запястья $\vec{p}_{wc}$ и фланца $\vec{p}_f$ строго ограничен неравенством треугольника для звеньев манипулятора:
> $$R_{max, wc} = a_2 + \sqrt{a_3^2 + d_4^2}$$
> Внутренняя сингулярная мертвая зона (минимальный радиус):
> $$R_{min, wc} = |a_2 - \sqrt{a_3^2 + d_4^2}| \approx 33.54\text{ мм}$$

### 🇬🇧 Theorem 1 (Geometric Reach Envelope Bound):
> Let the robot base origin be $O = [0, 0, 0]^T$ and the shoulder pivot be $S = [a_1, 0, d_1]^T$. The maximum reachable distance of the wrist center $\vec{p}_{wc}$ and tool flange $\vec{p}_f$ is bounded by the triangle inequality of the serial kinematic link chain:
> $$R_{max, wc} = a_2 + \sqrt{a_3^2 + d_4^2}$$
> The inner singular dead-zone boundary:
> $$R_{min, wc} = |a_2 - \sqrt{a_3^2 + d_4^2}| \approx 33.54\text{ mm}$$

---

### 🔬 Qadam-baqadam Isbot (Step-by-Step Proof):

1. **Zveno vektorlari zanjiri (Kinematic link vector loop):**
   Yelka markazi $S$ dan bilak markazi $\vec{p}_{wc}$ gacha bo'lgan vektor ikkita asosiy harakatlanuvchi bo'g'in vektorlari yig'indisidan iborat:
   $$\vec{r}_{wc/S} = \vec{L}_2(q_2) + \vec{L}_3(q_3)$$
   bu yerda:
   * $\|\vec{L}_2\| = a_2 = 455.0\text{ mm}$ (yuqori qo'l zvenosi uzunligi).
   * $\|\vec{L}_3\| = \sqrt{a_3^2 + d_4^2} = \sqrt{35.0^2 + 420.0^2} = \sqrt{1225 + 176400} = \sqrt{177625} \approx 421.4558\text{ mm}$.

2. **Evklid normasiga uchburchak tengsizligini qo'llash (Triangle inequality):**
   $$\|\vec{r}_{wc/S}\| = \|\vec{L}_2 + \vec{L}_3\| \le \|\vec{L}_2\| + \|\vec{L}_3\|$$
   Tenglik faqat va faqat $\vec{L}_2$ va $\vec{L}_3$ vektorlari kollinear (bir to'g'ri chiziqda yotgan) bo'lganda erishiladi:
   $$R_{max, wc} = 455.0 + 421.4558 = 876.4558\text{ mm}$$

3. **Minimal ichki radius (Minimum inner radius):**
   Qo'l orqaga bukilganda ($\vec{L}_2$ va $\vec{L}_3$ qarama-qarshi yo'nalganda):
   $$\|\vec{r}_{wc/S}\| \ge |\|\vec{L}_2\| - \|\vec{L}_3\|| = |455.0 - 421.4558| = 33.5442\text{ mm} \quad \blacksquare$$

4. **KUKA KR 6 R900-2 nominal yetib borish masofasi (Catalog nominal reach):**
   Mexanik flanets ofseti $d_6 = 80.0\text{ mm}$ va yelka ofseti $a_1 = 25.0\text{ mm}$ inobatga olinganda, gorizontal to'liq yozilgan holatdagi yetib borish masofasi:
   $$R_{catalog} = 901.5\text{ mm}$$

---

## 🛑 3. Theorem 2: Stopping Distance & Emergency Braking Dynamics (ISO 10218-1)

### 🇺🇿 Teorema 2 (Tormozlanish Masofasi va Xavfsizlik Zonalari):
> Avariyaviy to'xtash signali (E-Stop, Stop Category 0 yoki Category 1) kelib tushganda, robot asbobi to'liq to'xtaguncha bosib o'tadigan fazoviy masofa $s_{stop}$ ikkita faza integralidan iborat:
> $$s_{stop}(v_0) = \int_0^{t_{reaction}} v_0 dt + \int_{t_{reaction}}^{t_{stop}} v(t) dt = v_0 \cdot t_r + \frac{v_0^2}{2 a_{brake}}$$
> bu yerda:
> * $v_0$ — avariya signali kelgan paytdagi dastlabki chiziqli tezlik $[\text{m/s}]$.
> * $t_r$ — kontroller va xavfsizlik shinasining kechikish vaqti ($t_r \approx 0.030\text{ s} = 30\text{ ms}$).
> * $a_{brake}$ — motorlarning maksimal mexanik va elektr tormozlanish tezlanishi ($a_{brake} \approx 8.5\text{ m/s}^2$).

### 🇷🇺 Теорема 2 (Тормозной Путь и Динамика Остановки):
> При поступлении сигнала аварийной остановки (Stop Category 0 или 1), полное расстояние торможения рабочего органа $s_{stop}$ складывается из фазы реакции системы и фазы замедления:
> $$s_{stop}(v_0) = v_0 \cdot t_r + \frac{v_0^2}{2 a_{brake}}$$
> Полное время до полной остановки:
> $$t_{stop} = t_r + \frac{v_0}{a_{brake}}$$

### 🇬🇧 Theorem 2 (Stopping Distance & Braking Dynamics):
> Upon triggering a protective stop (IEC 60204-1 Stop Category 0 or 1), the total stopping distance $s_{stop}$ traversed by the robot tool center point is governed by the two-phase kinematic integral:
> $$s_{stop}(v_0) = \int_0^{t_r} v_0 dt + \int_{t_r}^{t_{stop}} (v_0 - a_{brake} (t - t_r)) dt = v_0 \cdot t_r + \frac{v_0^2}{2 a_{brake}}$$
> Total stopping time:
> $$t_{stop} = t_r + \frac{v_0}{a_{brake}}$$

---

### 📊 Tormozlanish Masofasi Jadvali (KR 6 R900-2):

| Tezlik $v_0\text{ [m/s]}$ | Ish Rejimi (Operating Mode) | Reaksiya $s_r\text{ [mm]}$ | Tormoz $s_{brake}\text{ [mm]}$ | Jami To'xtash $s_{stop}\text{ [mm]}$ | Vaqt $t_{stop}\text{ [ms]}$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$0.25$** | **T1 (Reduced Velocity)** | $7.5$ | $3.7$ | **$11.2$** | $59.4$ |
| **$0.50$** | **Manual Testing** | $15.0$ | $14.7$ | **$29.7$** | $88.8$ |
| **$1.00$** | **Automatic (50%)** | $30.0$ | $58.8$ | **$88.8$** | $147.6$ |
| **$2.00$** | **Automatic (100% Path)** | $60.0$ | $235.3$ | **$295.3$** | $265.3$ |
| **$2.00$** | **Stop 0 (Mechanical Brake Delay)** | $100.0$ | $235.3$ | **$335.3$** | $285.3$ |

---

## 🛡️ 4. Xavfsizlik Panjarasi Radiusi (Safety Perimeter Clearance Formula)

Xalqaro ISO 13857 va ISO 10218-2 standartlariga binoan, robot atrofidagi himoya panjarasi (Safety Fence) radiusi quyidagi tengsizlikni qanoatlantirishi shart:

$$R_{fence} \ge R_{max} + L_{tool} + s_{stop}(v_{max}) + C_{safety}$$

KUKA KR 6 R900-2 uchun:
* $R_{max} = 901.5\text{ mm}$ (nominal yetib borish masofasi)
* $L_{tool} = 120.0\text{ mm}$ (namunaviy pnevmatik tutqich uzunligi)
* $s_{stop}(2.0\text{ m/s}) = 295.3\text{ mm}$
* $C_{safety} = 200.0\text{ mm}$ (qo'shimcha xavfsizlik zahirasi)

$$R_{fence} \ge 901.5 + 120.0 + 295.3 + 200.0 = 1516.8\text{ mm} \approx 1.52\text{ m}$$

---

## 💻 5. Python Verification Code
Formulaning to'g'riligi va dinamik hisob-kitoblar `src/scripts/workspace_analyzer.py` va `src/scripts/test_workspace.py` skriptlarida `pytest` orqali to'liq tasdiqlangan:
```bash
uv run --with numpy --with pytest pytest src/scripts/test_workspace.py
```
Natija: **5/5 tests passed successfully.**
