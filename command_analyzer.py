import csv

def getKey(item):
    return item[1]

command_data = []
with open("command_data.csv", "r", encoding = "utf8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
    for row in spamreader:
        command_data.append(row)

command_counter = {} # dict 생성, 아이디를 key값, 입력줄수를 value값
for data in command_data:
    if data[1] in command_counter.keys(): # 아이디가 이미 key값으로 변경되었을 때
        command_counter[data[1]] += 1 # 기존 출현한 아이디
    else:
        command_counter[data[1]] = 1 # 처음 나온 아이디

print(command_counter)

dictlist = []
for key, value in command_counter.items():
    temp = [key, value]
    dictlist.append(temp)
    
sorted_dict = sorted(dictlist, key = getKey, reverse=True)
print(sorted_dict[:10])