def fibo(n):
    a = 0
    b = 1
    cnt = 0
    while cnt < n:
        yield a
        a, b = b , a + b
        cnt += 1
        
n = int(input())
first = True
for x in fibo(n):
    if first:
        print(f"{x}", end="")
        first = False
    else:
        print(f",{x}", end="")


        