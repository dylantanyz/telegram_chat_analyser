# import relevant modules: JSON parser, datetime
import json
import datetime

# open and read telegram history
inp = input("Input file name:")
nocommonwords = input()
data = open(inp, "r", encoding="utf8")
file = data.read()
data.close()
lines = json.loads(file)

meta = {
    "Sender":{},
    "Date":{}
}

worddict = {}

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

    # word counts (lowercase)
    msg = i.get("text")
    msg = str(msg).split()
    for word in msg:
        if word.lower() in worddict:
            worddict[word.lower()] += 1
        else:
            worddict[word.lower()] = 1



# print results
print("Total Messages: ", msgcount)
print(meta)
wordlist = sorted(worddict.items(), key = lambda x: x[1], reverse=True)
print(wordlist)

# further idea: list of words per person