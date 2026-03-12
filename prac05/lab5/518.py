import re

text = input()
pattern = input()

regex = re.escape(pattern) # string to regex    r"""
arr = re.findall(regex, text)
print(
    len(arr)
)