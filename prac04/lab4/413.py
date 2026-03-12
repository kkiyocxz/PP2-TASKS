import json

def parsing(database,q):
    isFound = True
    curr = database
    i = 0
    n = len(q)
    while i < n:
        if q[i].isalpha():
            j = i
            while j<n and (q[j].isalpha()):
                j += 1
            key = q[i:j]
            
            if not isinstance(curr, dict) or key not in curr:
                return None,False        
            
            curr = curr[key]
            i = j
        elif q[i] == '[':
            i += 1 #skip [
            index = 0
            while i < n and q[i].isdigit():
                index = index * 10 +    (ord(q[i]) - ord('0'))
                i += 1
                
            i += 1 #skip ]
            
            if not isinstance(curr, list) or index >= len(curr):
                isFound = False
            else:
                curr = curr[index]
        elif q[i] == '.':
            i += 1
    return curr, isFound       
def to_dict(v):
    return json.dumps(v , separators=(',',':'),sort_keys=True)
                
data_base = json.loads(input())  #str to dict
queries = int(input())
while queries > 0:
    q = input()
    value, isFound = parsing(data_base, q)
    if not isFound:
        print("NOT_FOUND")
    else:
        print(to_dict(value))
    queries -= 1