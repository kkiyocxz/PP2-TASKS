import re

text = input()

#   \w+ 1 сөз
regex = r"\w+"
arr = re.findall(regex, text)
print(
    len(arr)
)