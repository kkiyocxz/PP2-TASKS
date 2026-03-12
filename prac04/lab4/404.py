def squares_gen(a,b):
    for i in range(a, b + 1):
        yield i ** 2
        
a, b =map(int,input().split())
for x in squares_gen(a,b):
    print(x)