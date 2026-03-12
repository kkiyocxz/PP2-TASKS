import re

text = input()

#   \S non-space пробелы жоқ    только 1 символ
#   \S+ non-space пробелы жоқ >= 1 символ
#   \. точка

regex = r"\S+@\S+\.\S+"

arr = re.search(regex, text)
if arr:
    print(arr.group())  # .group substring тартып береды
else:
    print("No email")