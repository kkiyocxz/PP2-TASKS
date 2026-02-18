class Shape:
    def area():
        return 0
    
class Square(Shape):
    # def area(): уже бар
     # return 0
    def __init__(self,n):
        self.length = n
        
    def area(self):  #перезапись override
        return pow(self.length, 2)
    
n = int(input())
s1 = Square(n) #конструкторға n-ді передаем
print(s1.area())