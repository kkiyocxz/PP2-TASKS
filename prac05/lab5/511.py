import re

text = input()

regex = r"[A-Z]"
arr = re.findall(regex, text)
print(len(arr))