# import relevant modules JSON parser
import json

# open and read telegram history
inp = input("Input file name:")
data = open(inp, "r", encoding="utf8")
file = data.read()
data.close()
lines = json.loads(file)

meta = {
    "Sender":{}
    "Year":{}
}

msgcount = 0
print(type(lines))

msgdict = lines["messages"]

# loop through lines in file
for i in msgdict:
    msgcount += 1
    name = i.get("from")
    if name in meta["Sender"]:
        meta["Sender"][name] += 1
    else: meta["Sender"][name] = 1


print("Total Messages: ", msgcount)
print(meta)
# print information