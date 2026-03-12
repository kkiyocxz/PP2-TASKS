import math

def isIntersect(r, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx ** 2 + dy ** 2)

    a = dx ** 2 + dy ** 2
    b = 2 * (x1 * dx + y1 * dy)
    c = x1 ** 2 + y1 ** 2 - r ** 2
    
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        pointA = x1 ** 2 + y1 ** 2
        pointB = x2 ** 2 + y2 ** 2
        if pointA <= r ** 2 and pointB <= r ** 2:
            return length
        else:
            return 0
    sqrtDiscriminant = math.sqrt(discriminant)
    t1 = (-b - sqrtDiscriminant) / (2.0 * a)
    t2 = (-b + sqrtDiscriminant) / (2.0 * a)
    if t1 > t2:
        t1, t2 = t2, t1
    
    left = max(0.0, t1)
    right = min(1.0, t2)
    if left >= right:
        return 0
    return (right - left) * length

def shortest_path(r, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx ** 2 + dy ** 2)
    if isIntersect(r, x1, y1, x2, y2) <= 0:
        return length
    
    ao = math.sqrt(x1 ** 2 + y1 ** 2)
    bo = math.sqrt(x2 ** 2 + y2 ** 2)
    alpha = math.acos(r / ao)
    beta = math.acos(r / bo)
    gamma = math.acos((x1 * x2 + y1 * y2) / (ao * bo))
    arc_phi = gamma - alpha - beta
    arc = r * arc_phi
    lines = math.sqrt(ao ** 2 - r ** 2) + math.sqrt(bo ** 2 - r ** 2) 
    return lines + arc

r = int(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())
result = shortest_path(r, x1, y1, x2, y2)
print(f"{result:.10f}")