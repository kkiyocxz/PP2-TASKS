import re

text = input()

#   ^ at the start
#   .* any char between them
#   \d digit
#   $ at the end
if re.match(r"^[A-Za-z].*\d$", text):
    print("Yes")
else:
    print("No")