def cycle(text, amount):
    i = 0
    while i < amount:
        yield text
        i += 1
        
text = input()
amount = int(input())

for x in cycle(text, amount):
    print(x,end=" ")