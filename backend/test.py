a = [
    {"id": 1, "am": 2},
    {"id": 1, "am": 1},
    {"id": 2, "am": 3},
    {"id": 3, "am": 2},
    {"id": 4, "am": 1},
    {"id": 3, "am": 3},
]
b = {}
for i in a:
    pk = i["id"]
    am = i["am"]
    b[pk] = am if pk not in b else (b[pk] + am)
print(b)
