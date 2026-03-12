def powers_generator(n):
    for i in range(n + 1):
        yield 2 ** i
        
n = int(input())
for x in powers_generator(n):
    print(x,end=" ")