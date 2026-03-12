def even_numbers_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i
            
            
n = int(input())
first = True
for x in even_numbers_generator(n):
    if first :
        print(f"{x}",end="")
        first = False
    else:
        print(f",{x}",end="")