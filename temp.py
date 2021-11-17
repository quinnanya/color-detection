import json

with open ("manifest3.json", "r") as f:
    data = json.load(f)

with open ('manifest4.json', "w") as f:
    json.dump(data, f, indent=4)
