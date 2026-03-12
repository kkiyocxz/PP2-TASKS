import re

text = input()

# \b    сөздің басы/аяғы
# \w    characters from a to Z, digits from 0-9, and the underscore _ character

regex = r"\b\w{3}\b"
arr = re.findall(regex, text)
print(len(arr))
# counter = 0
# for x in re.split(" ", text):
#    if len(x) == 3:
#        counter += 1
# print(counter)    