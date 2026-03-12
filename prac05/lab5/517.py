import re

text = input()

#   \d digit
#   {2} 2 times

regex = r"\d{2}/\d{2}/\d{4}"
arr = re.findall(regex, text)
print(
    len(arr)
)