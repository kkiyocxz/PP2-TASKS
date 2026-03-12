import re

text = input()

arr = re.findall(r"\d", text)

if arr:
    print(*arr)
else:
    print()