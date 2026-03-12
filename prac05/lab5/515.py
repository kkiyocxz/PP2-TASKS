import re

text = input()

#   .goup() -> matches параметрін тартып береді matches=''

def new(x):
    d = x.group()
    return d * 2    # str * 2 = double str

old = r"\d"
res = re.sub(old, new, text)
print(res)