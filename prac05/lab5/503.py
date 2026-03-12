import re

text = input()
sub = input()

# через findall
arr = re.findall(sub, text) # findall массив қайтарады
print(len(arr))

# через finditer
# counter = 0
# for i in re.finditer(sub, text):
#    counter += 1
# print(counter)