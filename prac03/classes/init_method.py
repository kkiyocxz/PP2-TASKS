class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Ronaldo", 41)

print(p1.name)
print(p1.age)

class Person:
  pass

p1 = Person()
p1.name = "Altemir"
p1.age = 18

print(p1.name)
print(p1.age)

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Max", 28)

print(p1.name)
print(p1.age)

class Person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

p1 = Person("Bob")
p2 = Person("Alice", 39)

print(p1.name, p1.age)
print(p2.name, p2.age)

class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country

p1 = Person("Charlie", 30, "New York", "USA")