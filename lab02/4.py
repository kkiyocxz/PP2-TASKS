x = int(input())
count = 0
arr = list(map(int, input().split()))
for i in arr:
    if i > 0:
        count += 1
print(count)
