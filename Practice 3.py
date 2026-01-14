import math

def time_for_save(Data):
    x = Data[0] * 3 * math.tan(math.radians(Data[5]))
    L1 = (x ** 2 + (Data[0] * 3) ** 2) ** 0.5
    L2 = ((Data[2] * 3 - x) ** 2 + Data[1] ** 2) ** 0.5
    Time = (1 / (Data[3] * 5280 / 3600)) * (L1 + Data[4] * L2)
    return Time

Data = []
Data.append(8)
Data.append(10)
Data.append(50)
Data.append(5)
Data.append(2)
Data.append(39.4)
t_min_test = {}
for i in range(100):
    Data[5] = round((Data[5] + 0.001),3)
    t = time_for_save(Data)
    print(f"Если спасатель начнёт движение под углом углом theta1, равным {Data[5]} градусам, он достигнет утопащего через {t} секунды")
    t_min_test[Data[5]] = t
min_time = min(t_min_test.items(), key=lambda item: item[1])
print(f"Минимальное время спасения на углу {min_time[0]} - {min_time[1]} ")