import re

text = input()

#   \d+ 1 or more digits
#   ^ start
#   $ end
regex = re.compile(r"^\d+$")

if regex.match(text):
    print("Match")
else:
    print("No match")