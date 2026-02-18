class StringHandler:
    def __init__(self): #constructor - новый объекті құру үшін қажет
        pass 
    def getString(self):
        self.word = input() #h1.word, h2.word , s.word, object
    def printString(self):
        print(self.word.upper())
        
s1 = StringHandler() #конструкторды шақырамыз
s1.getString() #input() жазаймыз
s1.printString() #вывод жасайды