
my_list = ["apple", "banana", "cherry"]
my_it = iter(my_list)

print(next(my_it)) # apple
print(next(my_it)) # banana

def my_generator():
    yield "Первый"
    yield "Второй"
    yield "Третий"

for val in my_generator():
    print(val)