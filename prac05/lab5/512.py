import re

text = input()

#   \d digit
#   {2,}   [2;+inf] times
regex = r"\d{2,}"
arr = re.findall(regex, text)
if arr:
    print(*arr)
else:
    print()