import math
from scipy.stats import laplace
import scipy.stats

f = open("population.csv", "r")
sel = []
for i in range(0, 4):
    f.readline()
for i in range(0, 109):
    sel.append(int(f.readline().split(',')[0]))
print(sel)

# вариационный ряд
sel_v = sel.copy()
sel_v = sorted(set(sel_v))
print("----- вариационный ряд")
print(sel_v)
fr = []
for i in sel_v:
    fr.append(sel.count(i))
print(fr)
sel_vfr = sel_v.copy()
for i in range(0, len(sel_vfr)):
    sel_vfr[i] = [sel_vfr[i], fr[i], round(fr[i]/109, 2)]
print(sel_vfr)

# ранжированный ряд
sel_r = sel.copy()
sel_r.sort()
print("----- ранжированный ряд")
print(sel_r)

# интервальный ряд
s = sel.copy()
s = sorted(set(s))
print("----- интервальный ряд")
k = math.floor(1 + math.log2(109))
print("k =", k)
ma = max(s)
mi = min(s)
h = int((ma - mi)/k)
print("h =", h)
ni = []
ni += [sel.count(i) for i in range(mi, mi+h+1)]
ni = sum(ni)
ni_list = [ni]
pi_list = [round(ni/109, 2)]
int_list = [[mi, mi + h]]
print("[", mi, mi+h, "]", ni, round(ni/109, 2))
mic = mi + h
for i in range(k-1):
    ni = []
    ni += [sel.count(i) for i in range(mic + 1, mic + h + 1)]
    ni = sum(ni)
    ni_list.append(ni)
    pi_list.append(round(ni / 109, 2))
    int_list.append([mic, mic + h])
    print("(", mic, mic + h, "]", ni, round(ni / 109, 2))
    mic = mic + h

# графики абсолютных частот

# графики относительных частот

# середины интервалов и накопленные частоты
int2_list = [(i + j)/2 for i, j in int_list]
acc_ni_list = []
temp = 0
for i in ni_list:
    temp += i
    acc_ni_list.append(temp)
print("Середины интервалов: ", int2_list)
print("Накопленные частоты: ", acc_ni_list)

# условные варианты
mid = int2_list[3]
if_list = []
for i in int2_list:
    if_list.append(int((i - mid)/h))
print("Условные варианты: ", if_list)

# выборочные среднее и дисперсию. Вычислить исправленную выборочную дисперсию и исправленное СКО. Сравнить данные оценки с смещёнными оценками дисперсии и СКО.
sam_ave = 0
for i in range(len(ni_list)):
    sam_ave += int2_list[i] * ni_list[i]
sam_ave /= 109
sam_ave = round(sam_ave, 2)
print("Выборочное среднее: ", sam_ave)
sam_var = 0
for i in range(len(ni_list)):
    sam_var += ((int2_list[i] - sam_ave) ** 2) * ni_list[i]
sam_var /= 109
sam_var = round(sam_var, 2)
print("Выборочная дисперсия: ", sam_var)
com_sam_var = round(109/(109-1) * sam_var, 2)
print("Исправленная выборочная дисперсия: ", com_sam_var)
cor_sko = round(math.sqrt(109/(109-1) * sam_var), 2)
print("Исправленное СКО: ", cor_sko)
sko = round(math.sqrt(sam_var), 2)
print("Смещенная оценка СКО: ", sko)

# Найти статистическую оценку коэффициентов асимметрии и эксцесса.
v1 = 0
for i in range(len(ni_list)):
    v1 += (int2_list[i] ** 1) * ni_list[i]
v1 /= 109
v2 = 0
for i in range(len(ni_list)):
    v2 += (int2_list[i] ** 2) * ni_list[i]
v2 /= 109
v3 = 0
for i in range(len(ni_list)):
    v3 += (int2_list[i] ** 3) * ni_list[i]
v3 /= 109
v4 = 0
for i in range(len(ni_list)):
    v4 += (int2_list[i] ** 4) * ni_list[i]
v4 /= 109
m3 = v3 - 3*v2*v1 + 2*(v1**3)
m4 = v4 - 4*v3*v1 + 6*v2*(v1**2) - 3*(v1**4)
assy = round(m3/(sko**3), 3)
ecce = round(m4/(sko**4) - 3, 3)
print("Статистическая оценка коэффициента ассиметрии: ", assy)
print("Статистическая оценка коэффициента эксцесса: ", ecce)

# Вычислить моду, медиану и коэффициент вариации для заданного распределения.
x_m0 = int2_list[3]
m0 = x_m0 + h*((ni_list[3] - ni_list[2])/((ni_list[3] - ni_list[2]) + (ni_list[3] - ni_list[4])))
print("Мода: ", m0)
x_me = int2_list[3]
me = round(x_me + h/pi_list[3]*(0.5 - acc_ni_list[2]/109), 2)
print("Медиана: ", me)

# Вычислить точность и доверительный интервал для математического ожидания при неизвестном среднеквадратичном отклонении при заданном объёме выборки для доверительной точности 𝛾 ∈ {0.95, 0.99}.
gamma1 = 0.95
gamma2 = 0.99
tg1 = 1.9822
tg2 = 2.6221
accuracy1 = round(tg1*cor_sko/math.sqrt(109)*math.sqrt(1-(109/400)), 2)
accuracy2 = round(tg2*cor_sko/math.sqrt(109)*math.sqrt(1-(109/400)), 2)
print("Точность доверительного интервала (0.95): ", accuracy1)
print("Точность доверительного интервала (0.99): ", accuracy2)
print("Доверительный интервал (0.95): xг принадлежит (", sam_ave - accuracy1, sam_ave + accuracy1, ")")
print("Доверительный интервал (0.99): xг принадлежит (", sam_ave - accuracy2, sam_ave + accuracy2, ")")

# Для вычисления границ доверительного интервала для среднеквадратичного отклонения определить значение 𝑞 при заданных 𝛾 и 𝑛.
q1 = 1.9822
q2 = 2.6221
print("Доверительный интервал для среднеквадратического отклонения (0.95): (", 0, cor_sko + cor_sko*q1, ")")
print("Доверительный интервал для среднеквадратического отклонения (0.99): (", 0, cor_sko + cor_sko*q2, ")")

# Проверить гипотезу о нормальности заданного распределения с помощью критерия 𝜒2 (Пирсона). Для этого необходимо найти тео-
# ретические частоты и вычислить наблюдаемое значение критерия. Далее по заданному уровню значимости 𝛼 = 0.05 и числу степе-
# ней свободы найти критическую точку и сравнить с наблюдаемым значением.
pi_f = []
pi_f.append(round(scipy.stats.norm.cdf((359 - sam_ave)/cor_sko) - 0.5 + 0.5, 4))
for i in range(1, len(int_list) - 1):
    pi_f.append(round(scipy.stats.norm.cdf((int_list[i][1] - sam_ave)/cor_sko) - 0.5 - (scipy.stats.norm.cdf((int_list[i][0] - sam_ave)/cor_sko) - 0.5), 4))
pi_f.append(round(-scipy.stats.norm.cdf((554 - sam_ave)/cor_sko) + 0.5 + 0.5, 4))
ni_f = [round(i*109, 2) for i in pi_f]
print("pi     ni'")
for i in range(0, len(pi_f)):
    print(pi_f[i], ni_f[i])
nini_f = []
for i in range(0, len(ni_list)):
    nini_f.append((ni_list[i] - ni_f[i])**2)
nini_f_ni_f = []
for i in range(0, len(nini_f)):
    nini_f_ni_f.append(nini_f[i]/ni_f[i])
x_obs = round(sum(nini_f_ni_f), 1)
print("Xнабл^2 = ", x_obs)
alpha = 0.05
count = 4
x_crit = 9.5
print("Xкрит^2 = ", x_crit)
print("Проверена гипотеза о нормальности заданного распределения с помощью критерия Пирсона: ", x_obs < x_crit)

f.close()