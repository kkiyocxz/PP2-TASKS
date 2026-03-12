import json

def compare_jsons(source, patch):
    for key, patch_value in patch.items():
        if key not in source:
            source[key] = patch_value
            continue
        if patch_value is None:
            if key in source:
                del source[key]
            continue
        source_value = source[key]
        if isinstance(patch_value,dict) and isinstance(source_value,dict):
            compare_jsons(source_value,patch_value)   #recursion
        else:
            source[key] = patch_value
            
    return source


source_line = input()
patch_line = input()

source = json.loads(source_line)
patch = json.loads(patch_line)

result = compare_jsons(source, patch)
print(json.dumps(result, separators=(',',':'), sort_keys=True))