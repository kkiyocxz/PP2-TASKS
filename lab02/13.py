x = int(input())
isPrime = True

for i in range(2, int(pow(x , 0.5))):
    if x % i == 0:
        isPrime = False
        break
    
if isPrime == True:
    print("Yes")
else:
    print("No")