import json

x = '{"name":"Altemir", "age":18, "city":"Almaty"}'
y = json.loads(x)
print(y["age"])


student = {"name": "Altemir", "major": "Automation"}
json_string = json.dumps(student)
print(json_string)