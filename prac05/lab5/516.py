import re

text = input()
#   ()  Capture and group
#   .   any symbol
#   .+  one or more any symbol
regex = r"Name: (.+), Age: (.+)"
match = re.search(regex, text)

print(
        match.group(1), match.group(2)
)