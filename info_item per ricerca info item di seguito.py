import re
from proto import *

fp = open("file\item_proto_dump.xml","r")
p1 = re.compile(r'Vnum="(\d*)"?')
p2 = re.compile(r'LocalizedName="([\w\s\'\?\.\+\-\(\),±©¸¹·´£®½º¶º¼øÆ¯³­¿°»¢¥]*)"?')
p3 = re.compile(r'="([\d\.-]*)"?')
all_items = {}
i=0
for line in fp.readlines():
    vnum = p1.findall(line)
    name = p2.findall(line)
    num = p3.findall(line)
    i+=1
    
    if (not vnum):
        continue
    vnum = vnum[0]
    name = name[0]
    anti_flag = get_anti_flag(num[10])[1]
    item_type = get_item_type(num[4])[1]
    
    if ("NO_DROP_KARMA_NEGATIVO" in anti_flag):
        item = (vnum, name)

        if (item_type in all_items):
            item_list = all_items[item_type]
        else:
            item_list = []
        item_list.append(item)
        all_items[item_type] = item_list
        
fp.close()

for key in all_items.keys():
    fp = open("test/NO_DROP_KARMA__" + key + ".txt", "a")
    for item in all_items[key]:
        fp.write(item[0] + "\t\t" + item[1] + "\n")
    fp.flush()
    fp.close()



