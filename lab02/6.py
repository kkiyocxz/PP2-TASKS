x=int(input())

arr= list(map(int,input().split()))
max = arr[0]
for i in range (1,x):
    if arr[i]>max:
        max=arr[i]
print (max)