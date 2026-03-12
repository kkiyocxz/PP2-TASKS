import re

text = input()
sub = input()

if re.search(sub, text):
    print("Yes")
else:
    print("No")