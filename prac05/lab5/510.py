import re

text = input()

regex = r"cat|dog"
if re.search(regex, text):
    print("Yes")
else:
    print("No")