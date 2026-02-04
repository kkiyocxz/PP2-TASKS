num = {}
x = int(input())
arr = list(map(int, input().split()))

for x in arr:
    if x not in num:
        num[x] = 1
    else:
        num[x] += 1
        
max_frequency = max(num.values())
arr = []
for key in num:
    if max_frequency == num[key]:
        arr.append(key)

print(min(arr))