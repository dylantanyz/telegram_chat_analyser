# import relevant modules: JSON parser, datetime
import json
import datetime

# open and read telegram history
inp = input("Input file name:")
data = open(inp, "r", encoding="utf8")
file = data.read()
data.close()
lines = json.loads(file)

meta = {
    "Sender":{},
    "Date":{}
}

msgcount = 0
print(type(lines))

msgdict = lines["messages"]

# loop through lines in file
for i in msgdict:
    msgcount += 1

    # sender counts
    name = i.get("from")
    if name in meta["Sender"]:
        meta["Sender"][name] += 1
    else: meta["Sender"][name] = 1

    # date counts, by year
    datestring = i.get("date")
    date = datetime.datetime.fromisoformat(datestring)
    if date.year in meta["Date"]:
        meta["Date"][date.year] += 1
    else: meta["Date"][date.year] = 1


print("Total Messages: ", msgcount)
print(meta)

# print information