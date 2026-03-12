def my_generator(n):
    i = n + 1
    while i != 0:
        i -= 1
        yield i
        
n = int(input())
for x in my_generator(n):
    print(x)         