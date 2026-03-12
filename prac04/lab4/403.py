def div_gen(n):
    for i in range(0 , n + 1):
        if i % 12 == 0 :
            yield i
            
n = int(input())
for x in div_gen(n):
    print(x,end=" ")