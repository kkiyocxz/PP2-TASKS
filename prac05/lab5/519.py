import re

text = input()
# \b    сөздің басы/аяғы
# \w+  >=1 characters from a to Z, digits from 0-9, and the underscore _ character

regex = r"\b\w+\b"
string = re.compile(regex)
arr = string.findall(text)
print(
    len(arr)
)