import re

text = input()
old = input()
new = input()

print(re.sub(old, new, text))