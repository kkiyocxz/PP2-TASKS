x = int(input())
y = 0
while pow(2 , y) <= x:
    if pow(2,y) == x:
        print("YES")
        break
    y += 1
else:
    print("NO")