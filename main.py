# import relevant modules: JSON parser, datetime
import json
import datetime

# open and read telegram history
inp = input("Input file name:")
data = open(inp, "r", encoding="utf8")
file = data.read()
data.close()
lines = json.loads(file)

# defining data variables
calls = memremoved = memadded = photoedit = msgcount = int()
groupnames = list()
pinned = list()
worddict = dict()
meta = {
    "Sender":{},
    "Date":{},
    "Time":{}
}

# retrieved from http://xpo6.com/list-of-english-stop-words/
stopwords = ["i'm", "',", "'", "[{'type':", "{'type':", "u", "i", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

# loop through message lines in file
msgdict = lines["messages"]
for i in msgdict:
    msgcount += 1

    if i.get("type") == "service":
        action = i.get("action")
        if action == "edit_group_title":
            groupnames.append(i.get("title"))
            continue
        elif action == "pin_message":
            id = i.get("message_id")
            tempdict = next(item for item in msgdict if item["id"] == id)
            pinned.append(tempdict.get("text"))
            continue
        elif action == "group_call" or action == "phone_call":
            calls += 1
            continue
        elif action == "edit_group_photo" or action == "delete_group_photo":
            photoedit += 1
            continue
        elif action == "remove_members":
            memremoved += 1
            continue
        elif action == "invite_members":
            memadded += 1
            continue
        elif action == "create_group" or action == "invite_to_group_call": continue
        else: print(action)

    # sender counts
    name = i.get("from")
    if name in meta["Sender"]:
        meta["Sender"][name] += 1
    else: meta["Sender"][name] = 1

    msg = i.get("text")
    msg = str(msg).split()
    for word in msg:
        if word.lower() in worddict:
            worddict[word.lower()] += 1
        else:
            worddict[word.lower()] = 1

    for g in stopwords:
        if g in worddict.keys(): del worddict[g]

    # date counts, by year
    datestring = i.get("date")
    date = datetime.datetime.fromisoformat(datestring)
    time = datetime.datetime.time(date)

    if time.hour in meta["Time"]:
        meta["Time"][time.hour] += 1
    else: meta["Time"][time.hour] = 1

    if date.year in meta["Date"]:
        meta["Date"][date.year] += 1
    else: meta["Date"][date.year] = 1

    # word counts across all messages, regardless of sender
    msg = i.get("text")
    msg = str(msg).split()
    for word in msg:
        if word.lower() in worddict:
            worddict[word.lower()] += 1
        else:
            worddict[word.lower()] = 1

    for i in stopwords:
        if i in worddict.keys(): del worddict[i]

wordlist = sorted(worddict.items(), key = lambda x: x[1], reverse=True)

# print results
print("Total Messages: ", msgcount)
if len(groupnames) > 0:
    print("Total Group Title Changes: ", len(groupnames))
    print("Previous Names: ", groupnames)
if calls > 0:
    print("Total Calls: ", calls)
if len(pinned) > 0:
    print("Total Pinned Messages: ", len(pinned))
    # print("Pinned Messages: ", pinned)
if photoedit > 0: print("Total Group Photo Edits: ", photoedit)
if memadded > 0: print("Members Added: ", memadded)
if memremoved > 0: print("Members Removed: ", memremoved)
print("Messages Sent by Person: ", sorted(meta["Sender"].items(), key = lambda x: x[1], reverse=True))
print("Messages Sent by Year: ", meta.get("Date"))
print("Messages Sent by Hour: ", sorted(meta["Time"].items(), key = lambda x: x[1], reverse=True))

# export data
with open('exports/pinned_messages.json', 'w', encoding='utf-8') as f:
    json.dump(pinned, f, ensure_ascii=False, indent=4)
with open('exports/total_word_frequency.json', 'w', encoding='utf-8') as f:
    json.dump(wordlist, f, ensure_ascii=False, indent=4)

