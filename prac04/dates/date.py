import datetime

#  датa и временя
now = datetime.datetime.now()
print(now)          # 2026-02-19 ...
print(now.year)     # 2026
print(now.strftime("%A")) # Название дня недели


x = datetime.datetime(2020, 5, 17)
print(x) # 2020-05-17 00:00:00


print(x.strftime("%B")) 