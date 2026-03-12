g = 0

def outer(commands):
    n = 0   # non local

    def inner(command, x):
        global g
        nonlocal n
        if command == "global":
            g += x
        elif command == "nonlocal":
            n += x
        elif command == "local":
            x = 0

    for command, value in commands:
        inner(command, value)
    return n

q = int(input())
commands = []
for i in range(q):
    command, value = input().split()
    commands.append(
        (command, int(value))
    )
k = outer(commands)
print(g, k)