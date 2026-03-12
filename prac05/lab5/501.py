import re

line = input()

if re.match("Hello", line): # тек басынан тексереді
    print("Yes")
else:
    print("No")