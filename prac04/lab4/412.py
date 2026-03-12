import json
has_difference = False

def to_dict(a):
    return json.dumps(a,separators=(',',':'), sort_keys=True)


def compare_jsons(a,b,path):
    global has_difference
    for key, a_value in a.items():
        current = ""
        if path:
            current = f"{path}.{key}"
        else:
            current = key

        if key not in b:
            print(f"{current} : {to_dict(a_value)} -> <missing>")
            has_difference = True
            continue
        b_value = b[key]
        if isinstance(a_value,dict) and isinstance(b_value,dict):
            compare_jsons(a_value,b_value,current)
        else:
            if a_value != b_value:
                print(f"{current} : {to_dict(a_value)} -> {to_dict(b_value)}")
                has_difference = True
    for key, b_value in b.items():
        if key not in a:
            current = ""
            if path:
                current = f"{path}.{key}"
            else:
                current = key
            print(f"{current} : <missing> -> {to_dict(b_value)}")
            has_difference = True
            
                        
    


a1 = input()
a2 = input()

a = json.loads(a1) #str to dictionary
b = json.loads(a2)

compare_jsons(a,b, "")
if not has_difference:
    print("No differences")
    