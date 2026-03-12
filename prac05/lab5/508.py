import re

text = input()
regex = input()

arr = re.split(regex, text)
result = ",".join(arr)
print(result)