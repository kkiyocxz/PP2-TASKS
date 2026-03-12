class Reverse:
    def __init__(self , t): #constructor
        self.text = t
        
    def __iter__(self):
        i = len(self.text) - 1
        while i >= 0:
            yield self.text[i]
            i -= 1
            
s = input()
r = Reverse(s) #объект құрамын, конструктор шақырылады
for x in r.__iter__(): #объект итерациялаймын
    print(x,end="")
    
    