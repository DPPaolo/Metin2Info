#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import re
import sys
import time
import traceback

from metin2Data import *
import QtMetin2

item_data = None
mob_data = None

LOG_FILE= 'log.log'
logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)

DOWNLOAD_FILE = ("file/item_proto_dump.xml",
                 "file/mob_proto_dump.xml",
                 "file/itemdesc.txt",
                 "file/item_list.txt",
                 "file/mob_list.txt")

INFO = "Programma Creato da Akihiko.\nTuttu i diritti riservati."


def get_time(time):
    day = hour = minute = sec = 0
    date = ""
    time = int(time)
    while (time > 0):
        if (time - 86400 >= 0):
            day += 1
            time -= 86400
            continue
        if (time - 3600 >= 0):
            hour += 1
            time -= 3600
            if (hour >= 24):
                hour = 0
                day += 1
            continue
        if (time - 60 >= 0):
            minute += 1
            time -= 60
            if (minute >= 60):
                minute = 0
                hour += 1
            continue
        else:
            sec = time
            time = 0
    if (day != 0 and day == 1):
        date = date + "1 Giorno "
    elif (day != 0):
        date = date + str(day) + " Giorni "
    if (hour != 0):
        date = date + str(hour) + "h "
    if (minute != 0):
        date = date + str(minute) + "m "
    if (str(sec) == "0"):
        return date
    else:
        return date + str(sec) + "s"

def err(stringa):
    logging.error(time.strftime('%x %X') + " - " + stringa)

def stampa_errore(mess):
    print(mess)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)

def divide_message(mess):
    if (len(mess)> 100):
        for i in range(0, len(mess)):
            if (mess[i] == " "):
                space = i
            if (i >= 100):
                return mess[:space] + "\n" + divide_message(mess[space+1:])
        return mess
    else:
        return mess

def spazio(stringa):
    l = len(stringa)
    if (l >= 16):
        return ''
    else:
        return '\t'

def abspath(path):
    cwd = os.getcwd()
    path = os.path.join(cwd, path)
    return path

def get_cur_dir():
    return os.path.dirname(abspath(os.curdir))

def int_to_binary(n):
    pot = []
    while n>0:
        if (n%2==0):
            pot.append(0)
        else:
            pot.append(1)
        n = n // 2
    return pot

def inttobool(num):
    if (num == 0):
        return False
    else:
        return True

def inttosino(num):
    if (int(num) == 0):
        return "No"
    else:
        return "Si"

def booltoint(boolean):
    if (boolean == True):
        return 1
    else:
        return 0

def change_download_file(value):
    global DOWNLOAD_FILE
    if (value == 1):
        DOWNLOAD_FILE = ("file/item_proto_dump_en.xml",
                         "file/mob_proto_dump_en.xml",
                         "file/itemdesc_en.txt",
                         "file/item_list_en.txt",
                         "file/mob_list_en.txt")
    else:
        DOWNLOAD_FILE = ("file/item_proto_dump.xml",
                         "file/mob_proto_dump.xml",
                         "file/itemdesc.txt",
                         "file/item_list.txt",
                         "file/mob_list.txt")

def get_item_name_from_itemdesc(num):
    try:
        fp = open(DOWNLOAD_FILE[2], "r")
    except:
        return false
    for line in fp.readlines():
        if (not line):
            break
        line = line.split("\t")
        if (line[0] == num):
            return line[1]
    return "Item non Trovato"

def get_item_name(num):
    if (not item_data):
        return get_item_name_from_itemdesc(num)
    if (num == '0'):
        return "Nessuno"
    if (str(num) in item_data.item_data_vnum):
        return item_data.item_data_vnum[str(num)]['name']
    else:
        name = get_item_name_from_itemdesc(num)
        if (name):
            return name
    return "Item non Trovato"


def get_desc(vnum):
    try:
        fp = open(DOWNLOAD_FILE[2],"r")
    except:
        return "Errore"
    for line in fp.readlines():
        line = line.replace("\n", "")
        line = line.split("\t")
        if (str(line[0]) == str(vnum)):
            fp.close()
            return line[3]
    fp.close()
    return "Nessuna Descrizione Disponibile"
    
def get_icon_vnum(vnum):
    try:
        fp = open(DOWNLOAD_FILE[3], "r")
    except:
        return "Errore"
    trovato = 0
    for line in fp.readlines():
        if (not line):
            continue
        line = line.split("\t")
        if (str(vnum) == str(line[0])):
            data = line[1].split("\\")
            data = data[-1].replace(".tga", "")
            data = data.replace("\n", "")
            trovato = 1
            break
    fp.close()
    if (trovato):
        return data
    else:
        return vnum

def get_item_type(item_type):
    if (int(item_type) in ITEM_TYPE):
        return ITEM_TYPE[int(item_type)]
    else:
        print("Item Type non trovato " + str(item_type))
        err("Item Type non trovato " + str(item_type))
        return "ITEM_UNKNOWN_" + str(item_type), "Sconosciuto"

def get_item_subtype(item_type, sub_type):
    item_type = get_item_type(item_type)[0]
    if (item_type in ITEM_SUB_TYPE):
        if (int(sub_type) in ITEM_SUB_TYPE[item_type]):
            return ITEM_SUB_TYPE[item_type][int(sub_type)]
        else:
            print("Item Sub Type non trovato: Item Type " + str(item_type) + ", Item Sub Type " + str(sub_type))
            err("Item Sub Type non trovato: Item Type " + str(item_type) + ", Item Sub Type " + str(sub_type))
            return "UNKNOWN_SUB_TYPE_" + str(sub_type), "Sconosciuto"
    else:
        return "NONE", "Niente"
        
def get_item_mask(mask):
    if (int(mask) in ITEM_MASK_TYPE):
        return ITEM_MASK_TYPE[int(mask)]
    else:
        print("Item Mask Type non trovato " + str(mask))
        err("Item Mask Type non trovato " + str(mask))
        return "MASK_ITEM_UNKNOWN_" + str(mask), "Sconosciuto"

def get_item_sub_mask(mask, sub_mask):
    mask = get_item_mask(mask)[0]
    if (mask in ITEM_SUB_MASK_TYPE):
        if (int(sub_mask) in ITEM_SUB_MASK_TYPE[mask]):
            return ITEM_SUB_MASK_TYPE[mask][int(sub_mask)]
        else:
            print("Item Sub Mask Type non trovato: Item Mask " + str(mask) + ", Item Sub Mask " + str(sub_mask))
            err("Item Sub Mask Type non trovato: Item Mask " + str(mask) + ", Item Sub Mask " + str(sub_mask))
            return "UNKNOWN_SUB_MASK_" + str(sub_mask), "Maschera Sconosciuta"
    else:
        return "NONE", "Nessuna"

def get_anti_flag(anti_flag):
    pot = int_to_binary(int(anti_flag))
    num=pot.count(1)
    if (not pot):
        return 'NONE', 'Niente'
    flag = flag_o = ''
    for i in range(0,len(pot)):
        if (pot[i] == 1):
            flag_o = flag_o + ITEM_ANTI_FLAG[i][0]
            flag = flag + ITEM_ANTI_FLAG[i][1]
            if (num > 1):
                flag_o = flag_o + ' | '
                flag = flag + ' | '
                num = num - 1
    return flag_o, flag

def get_item_flag(item_flag):
    pot = int_to_binary(int(item_flag))
    num=pot.count(1)
    if (not pot):
        return 'NONE', 'Niente'
    flag = flag_o = ''
    for i in range(0,len(pot)):
        if (pot[i] == 1):
            flag_o = flag_o + ITEM_FLAG[i][0]
            flag = flag + ITEM_FLAG[i][1]
            if (num > 1):
                flag_o = flag_o + ' | '
                flag = flag + ' | '
                num = num - 1
    return flag_o, flag

def get_wear_flag(wear_flag):
    pot = int_to_binary(int(wear_flag))
    num=pot.count(1)
    if (not pot):
        return 'NONE', 'Niente'
    flag = flag_o = ''
    for i in range(0,len(pot)):
        if (pot[i] == 1):
            flag_o = flag_o + ITEM_WEAR_FLAG[i][0]
            flag = flag + ITEM_WEAR_FLAG[i][1]
            if (num > 1):
                flag_o = flag_o + ' | '
                flag = flag + ' | '
                num = num - 1
    return flag_o, flag

def get_item_immune_flag(immune_flag):
    pot = int_to_binary(int(immune_flag))
    num=pot.count(1)
    if (not pot):
        return 'NONE', 'Niente'
    flag = flag_o = ''
    for i in range(0,len(pot)):
        if (pot[i] == 1):
            flag_o = flag_o + ITEM_IMMUNE_FLAG[i][0]
            flag = flag + ITEM_IMMUNE_FLAG[i][1]
            if (num > 1):
                flag_o = flag_o + ' | '
                flag = flag + ' | '
                num = num - 1
    return flag_o, flag

def get_wiki_anti_flag(anti_flag, flag):
    if (ITEM_FLAG[2][0] in get_item_flag(flag)[0]):
        if (anti_flag in ITEM_WIKI_ANTI_FLAG_IMPILABILE):
            return ITEM_WIKI_ANTI_FLAG_IMPILABILE[anti_flag]
        else:
            print("Wiki Anti Flag Non Trovata: " + str(anti_flag) + " " + get_anti_flag(anti_flag)[1])
            err("Wiki Anti Flag non trovata " + str(anti_flag) + " " + get_anti_flag(anti_flag)[1])
            return "Wiki Anti Flag Non Trovata: " + str(anti_flag)
    elif (anti_flag in ITEM_WIKI_ANTI_FLAG_NOIMPILABILE):
        return ITEM_WIKI_ANTI_FLAG_NOIMPILABILE[anti_flag]
    else:
        print("Wiki Anti Flag Non Trovata: " + str(anti_flag) + " " + get_anti_flag(anti_flag)[1])
        err("Wiki Anti Flag non trovata " + str(anti_flag) + " " + get_anti_flag(anti_flag)[1])
        return "Wiki Anti Flag Non Trovata: " + str(anti_flag)

def get_limit_type(limit_type):
    if (int(limit_type) in ITEM_LIMIT_TYPE):
        return ITEM_LIMIT_TYPE[int(limit_type)]
    else:
        print("Restrizione Item non trovata " + str(limit_type))
        err("Restrizione Item non trovata " + str(limit_type))
        return "LIMIT_UNKNOWN_" + str(item_type), "Sconosciuta"

def get_apply_type(apply_type):
    if (int(apply_type) in ITEM_APPLY_TYPE):
        return ITEM_APPLY_TYPE[int(apply_type)]
    else:
        print("Bonus Item non trovato " + str(apply_type))
        err("Bonus Item non trovato " + str(apply_type))
        return "APPLY_UNKNOWN_" + str(apply_type), "Sconosciuto"

def get_belt_slot(slot_type):
    if (int(slot_type) in BELT_TYPE_SLOT):
        return str(BELT_TYPE_SLOT[int(slot_type)])
    else:
        print("Tipo Slot Cintura non trovato " + str(slot_type))
        err("Tipo Slot Cintura non trovato " + str(slot_type))
        return str(slot_type)

def get_item_set_up(up):
    if (up in SET_UP):
        return SET_UP[up]
    elif (up == 0):
        return
    else:
        print("Set Up Non Trovato: " + str(up))
        return "Set Up Non Trovato: " + str(up)

def get_mob_grade(grade):
    if (int(grade) in MOB_GRADE):
        return MOB_GRADE[int(grade)]
    else:
        print("Grado Mostro non trovato " + str(grade))
        err("Grado Mostro non trovato " + str(grade))
        return str(grade)

def get_mob_battle_type(battle_type):
    if (int(battle_type) in MOB_BATTLE_TYPE):
        return MOB_BATTLE_TYPE[int(battle_type)]
    else:
        print("Tipo Attacco Mostro non trovato " + str(battle_type))
        err("Tipo Attacco Mostro non trovato " + str(battle_type))
        return str(battle_type)

def get_mob_type(mob_type):
    if (int(mob_type) in MOB_TYPE):
        return MOB_TYPE[int(mob_type)]
    else:
        print("Tipo Mostro non trovato " + str(mob_type))
        err("Tipo Mostro non trovato " + str(mob_type))
        return str(mob_type)

def get_mob_size(size):
    if (int(size) in MOB_SIZE):
        return MOB_SIZE[int(size)]
    else:
        print("Dimensione Mostro non trovato " + str(size))
        err("Dimensione Mostro non trovato " + str(size))
        return str(size)

def get_regno(reign):
    if (int(reign) in REGNO):
        return REGNO[int(reign)]
    else:
        print("Regno non trovato " + str(reign))
        err("Regno non trovato " + str(reign))
        return str(reign)

def get_mob_ai_flag(ai_flag):
    pot = int_to_binary(int(ai_flag))
    num=pot.count(1)
    if (not pot):
        return 'NONE', 'Niente'
    flag = flag_o = ''
    for i in range(0,len(pot)):
        if (pot[i] == 1):
            flag_o = flag_o + MOB_AI_FLAG[i][0]
            flag = flag + MOB_AI_FLAG[i][1]
            if (num > 1):
                flag_o = flag_o + ' | '
                flag = flag + ' | '
                num = num - 1
    return flag_o, flag

def get_mob_race_flag(race_flag):
    pot = int_to_binary(int(race_flag))
    num=pot.count(1)
    if (not pot):
        return 'NONE', 'Niente'
    flag = flag_o = ''
    for i in range(0,len(pot)):
        if (pot[i] == 1):
            flag_o = flag_o + MOB_RACE_FLAG[i][0]
            flag = flag + MOB_RACE_FLAG[i][1]
            if (num > 1):
                flag_o = flag_o + ' | '
                flag = flag + ' | '
                num = num - 1
    return flag_o, flag

def get_mob_immune_flag(immune_flag):
    pot = int_to_binary(int(immune_flag))
    num=pot.count(1)
    if (not pot):
        return 'NONE', 'Niente'
    flag = flag_o = ''
    for i in range(0,len(pot)):
        if (pot[i] == 1):
            flag_o = flag_o + MOB_IMMUNE_FLAG[i][0]
            flag = flag + MOB_IMMUNE_FLAG[i][1]
            if (num > 1):
                flag_o = flag_o + ' | '
                flag = flag + ' | '
                num = num - 1
    return flag_o, flag

def get_mob_element(vnum):
    if (gestore_opzioni.get_option("Platform") == 0):
        mob = mob_data.mob_data_vnum[vnum]
    else:
        mob = mob_data.mob_data_vnum_en[vnum]
    race_flag = get_mob_race_flag(int(mob['RaceFlag']))[0]
    elem = ""
    if ("ATT_ELEC" in race_flag):
        elem = elem + "Lampo"
    elif ("ATT_FIRE" in race_flag):
        elem = elem + "Fuoco"
    elif ("ATT_ICE" in race_flag):
        elem = elem + "Ghiaccio"
    elif ("ATT_WIND" in race_flag):
        elem = elem + "Vento"
    elif ("ATT_EARTH" in race_flag):
        elem = elem + "Terra"
    elif ("ATT_DARK" in race_flag):
        elem = elem + "Oscurita'"
    if (elem == ""):
        elem = "Nessuno"
    return elem

def get_mob_att_element(vnum):
    if (gestore_opzioni.get_option("Platform") == 0):
        mob = mob_data.mob_data_vnum[vnum]
    else:
        mob = mob_data.mob_data_vnum_en[vnum]
    race_flag = get_mob_race_flag(int(mob['RaceFlag']))[0]
    
    if ("ATT_ELEC" in race_flag):
        return mob['AttElec']
    elif ("ATT_FIRE" in race_flag):
        return mob['AttFire']
    elif ("ATT_ICE" in race_flag):
        return mob['AttIce']
    elif ("ATT_WIND" in race_flag):
        return mob['AttWind']
    elif ("ATT_EARTH" in race_flag):
        return mob['AttEarth']
    elif ("ATT_DARK" in race_flag):
        return mob['AttDark']
    else:
        return "0"

def get_wiki_mob_flag(vnum):
    if (len(vnum) != 0):
        if (gestore_opzioni.get_option("Platform") == 0):
            mob = mob_data.mob_data_vnum[vnum]
        else:
            mob = mob_data.mob_data_vnum_en[vnum]
        ai_flag = int(mob['AIFlags'])
        immune_flag = int(mob['ImmuneFlag'])
        slow = int(mob['EnchantSlow'])
        poison = int(mob['EnchantPoison'])
        stun = int(mob['EnchantStun'])

        proc_flag = ""

        if (MOB_AI_FLAG[0][0] in get_mob_ai_flag(ai_flag)[0]):
            proc_flag = proc_flag + "A"
        if (int(stun) > 0):
            proc_flag = proc_flag + "S"
        if (int(slow) > 0):
            proc_flag = proc_flag + "R"
        if (int(poison) > 0):
            proc_flag = proc_flag + "V"
        if (MOB_AI_FLAG[16][0] in get_mob_ai_flag(ai_flag)[0]):
            proc_flag = proc_flag + "C"
        #Utile nel caso non vengano piu' rilasciati mob_proto
        if (vnum in MOB_WIKI_FLAG_PROC):
            proc_flag = proc_flag + MOB_WIKI_FLAG_PROC[vnum]
        ##
        if (proc_flag == "ASRVC"):
            proc_flag = "TUTTE"
        elif (proc_flag == ""):
            proc_flag = "NESSUNA"

        if (immune_flag > 2**15):
            immune_flag -= 2**15
        if (immune_flag > 2**14):
            immune_flag -= 2**14
        if (immune_flag > 2**13):
            immune_flag -= 2**13
        if (immune_flag > 2**12):
            immune_flag -= 2**12
        if (immune_flag > 2**11):
            immune_flag -= 2**11
        if (immune_flag > 2**10):
            immune_flag -= 2**10
        if (immune_flag > 2**9):
            immune_flag -= 2**9
        if (immune_flag > 2**8):
            immune_flag -= 2**8
        if (immune_flag > 2**7):
            immune_flag -= 2**7
            
        if (immune_flag in MOB_WIKI_FLAG):
            return MOB_WIKI_FLAG[immune_flag] + ", " + proc_flag
        else:
            print("Wiki Mob Flag Non Trovata: " + str(immune_flag) + " " + get_mob_immune_flag(immune_flag)[1])
            err("Wiki Mob Flag non trovata " + str(immune_flag) + " " + get_mob_immune_flag(immune_flag)[1]) 
            return "Wiki Mob Flag Non Trovata: " + str(immune_flag) + ", " + proc_flag
    #Utile nel caso non vengano piu' rilasciati mob_proto
    elif (vnum in MOB_WIKI_FLAG_NEW):
        return MOB_WIKI_FLAG_NEW[vnum]
    else:
        print("Dato non disponibile per questo vnum " + str(vnum))
        return "Dato non disponibile"

def get_mob_type_on_click(click):
    if (int(click) in MOB_ON_CLICK_TYPE):
        return MOB_ON_CLICK_TYPE[int(click)]
    else:
        print("Mob On Click non trovato " + click)
        err("Mob On Click non trovato " + click) 
        return "ON_CLICK_EVENT_UNKNOWN_" + str(click), "Sconosciuto"

def stampa_info_item(vnum, name):
    filename = cur_dir + "/Info_Item_" + vnum + "_" + name + ".txt"
    fp = open(filename, "w")
    if (gestore_opzioni.get_option("Platform") == 0):
        item = item_data.item_data_vnum[vnum]
    else:
        item = item_data.item_data_vnum_en[vnum]
    
    if (str(item['VnumRange']) == "0"):
        fp.write("Vnum: " + vnum + "\n")
    else:
        fp.write("Vnum: " + vnum + " ~ " + item['VnumRange'] + "\n")
    fp.write("Nome: " + name + "\n")
    fp.write("Descrizione: " + get_desc(vnum) + "\n")
    fp.write("Vnum Range: " + item['VnumRange'] + "\n")
    fp.write("Tipo: " + get_item_type(item['Type'])[1] + " (" + get_item_type(item['Type'])[0] + ")\n")
    fp.write("Sotto Tipo: " + get_item_subtype(item['Type'],item['SubType'])[1] + " (" + get_item_subtype(item['Type'],item['SubType'])[0] + ")\n")
    fp.write("Maschera Tipo: " + get_item_mask(item['TypeMask'])[1] + " (" + get_item_mask(item['TypeMask'])[0] + ")\n")
    fp.write("Maschera Sotto Tipo: " + get_item_sub_mask(item['TypeMask'],item['SubTypeMask'])[1] + " (" + get_item_sub_mask(item['TypeMask'],item['SubTypeMask'])[0] + ")\n")
    fp.write("Peso: " + item['Weight'] + "\n")
    fp.write("Spazi Occupati: " + item['Size'] + "\n")
    fp.write("Flag Template Wiki: " + get_wiki_anti_flag(int(item['AntiFlags']), int(item['Flags'])) + "\n")
    fp.write("Anti Flag: " + get_anti_flag(int(item['AntiFlags']))[1] + " (" + get_anti_flag(int(item['AntiFlags']))[0] + ")\n")
    fp.write("Flag: " + get_item_flag(int(item['Flags']))[1] + " (" + get_item_flag(int(item['Flags']))[0] + ")\n")
    fp.write("Flag Uso: " + get_wear_flag(int(item['WearFlags']))[1] + " (" + get_wear_flag(int(item['WearFlags']))[0] + ")\n")
    fp.write("Flag Immunita': " + get_item_immune_flag(int(item['ImmuneFlags']))[1] + " (" + get_item_immune_flag(int(item['ImmuneFlags']))[0] + ")\n")
    fp.write("Prezzo Acquisto: " + item['Gold'] + "\n")
    fp.write("Prezzo Vendita (da dividere per 5): " + item['ShopBuyPrice'] + "\n")
    fp.write("Tipo Restrizione 0: " + get_limit_type(int(item['LimitType0']))[1] + " (" + get_limit_type(int(item['LimitType0']))[0] + ")\n")
    fp.write("Valore Restrizione 0: " + item['LimitValue0'] + "\n")
    fp.write("Tipo Restrizione 1: " + get_limit_type(int(item['LimitType1']))[1] + " (" + get_limit_type(int(item['LimitType1']))[0] + ")\n")
    fp.write("Valore Restrizione 1: " + item['LimitValue1'] + "\n")
    fp.write("Tipo Bonus 1: " + get_apply_type(int(item['ApplyType0']))[1] + " (" + get_apply_type(int(item['ApplyType0']))[0] + ")\n")
    fp.write("Valore Bonus 1: " + item['ApplyValue0'] + "\n")
    fp.write("Tipo Bonus 2: " + get_apply_type(int(item['ApplyType1']))[1] + " (" + get_apply_type(int(item['ApplyType1']))[0] + ")\n")
    fp.write("Valore Bonus 2: " + item['ApplyValue1'] + "\n")
    fp.write("Tipo Bonus 3: " + get_apply_type(int(item['ApplyType2']))[1] + " (" + get_apply_type(int(item['ApplyType2']))[0] + ")\n")
    fp.write("Valore Bonus 3: " + item['ApplyValue2'] + "\n")
    fp.write("Tipo Bonus 4: " + get_apply_type(int(item['ApplyType3']))[1] + " (" + get_apply_type(int(item['ApplyType3']))[0] + ")\n")
    fp.write("Valore Bonus 4: " + item['ApplyValue3'] + "\n")
    stampa_value_item(fp, vnum)
    fp.write("Socket0: " + item['Socket0'] + "\n")
    fp.write("Socket1: " + item['Socket1'] + "\n")
    fp.write("Socket2: " + item['Socket2'] + "\n")
    fp.write("Vnum Up: " + item['RefinedVnum'] + " (" + get_item_name(item['RefinedVnum']) + ")\n")
    fp.write("Set Potenziamento: " + item['RefineSet'] + "\n")
    fp.write("Item per aggiungere 6° e 7° Bonus: " + item['67_Material'] + "\n")
    fp.write("Poss. Apparizione Bonus Extra: " + item['AlterToMagicItemPercent'] + "\n")
    fp.write("Percentuale Luccichio: " + item['Specular'] + "\n")
    fp.write("Socket Disponibili " + item['GainSocketPercent'] + "\n")
    fp.flush()
    fp.close()

def stampa_value_item(fp, vnum):
    item = item_data.item_data_vnum[vnum]
    itemtype2 = get_item_type(item['Type'])[0]
    subtype2 = get_item_subtype(item['Type'], item['SubType'])[0]
    if (itemtype2 == 'ITEM_WEAPON'):
        fp.write("Valore di Attacco Fisico: " + str(int(item['Value3'])+ int(item['Value5'])) + " - " + str(int(item['Value4'])+ int(item['Value5'])) + "\n")
        if (int(item['Value2']) != 0):
            fp.write("Valore di Attacco Magico: " + str(int(item['Value1'])+ int(item['Value5'])) + " - " + str(int(item['Value2'])+ int(item['Value5'])) + "\n")
        fp.write("Valore 0: " + item['Value0'] + "\n")
        fp.write("Min Magico: " + item['Value1'] + "\n")
        fp.write("Max Magico: " + item['Value2'] + "\n")
        fp.write("Min Fisico: " + item['Value3'] + "\n")
        fp.write("Max Fisico: " + item['Value4'] + "\n")
        fp.write("Incremento: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_ARMOR'):
        fp.write("Valore di Difesa: " + str(int(item['Value1']) + int(int(item['Value5'])/2))+"\n")
        fp.write("Valore 0: " + item['Value0'] + "\n")
        fp.write("Difesa Base " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Index Skin: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Mezzo Incremento: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_USE'):
        if (subtype2 == 'USE_POTION' or subtype2 == 'USE_POTION_NODELAY'):
            fp.write("HP Ripristinati: " + item['Value0'] + "\n")
            fp.write("MP Rpristinati: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_TALISMAN'):
            fp.write("Tipo Teletrasporto: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_TUNING'):
            fp.write("Tipo Pergamena Up: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_BAIT'):
            fp.write("Aumento % Pesca: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_ABILITY_UP'):
            fp.write("Bonus Fornito: " + item['Value0'] + " (" + get_apply_type(item['Value0'])[1] + ")\n")
            fp.write("Durata: " + item['Value1'] + "\n")
            fp.write("Valore Bonus: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_AFFECT'):
            fp.write("ID Icona HUD: " + item['Value0'] + "\n")
            fp.write("Bonus Fornito: " + item['Value1'] + " (" + get_apply_type(item['Value1'])[1] + "(\n")
            fp.write("Valore Bonus: " + item['Value2'] + "\n")
            fp.write("Durata: " + item['Value3'] + "\n")
            fp.write("Incremento Bonus: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_INVISIBILITY'):
            fp.write("Valore 0: " + item['Value0'] + "\n")
            fp.write("Durata: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_DETACHMENT'):
            fp.write("Num. Pietre da Rimuovere: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_RECIPE'):
            fp.write("Risultato: " + item['Value0'] + " (" + get_item_name(item['Value0']) + ")\n")
            fp.write("Materiale 1: " + item['Value1'] + " (" + get_item_name(item['Value1']) + ")\n")
            fp.write("Quantita' Mat. 1: " + item['Value2'] + "\n")
            fp.write("Materiale 2: " + item['Value3'] + " (" + get_item_name(item['Value3']) + ")\n")
            fp.write("Quantita' Mat. 2: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_TIME_CHARGE_PER'):
            fp.write("Percentuale Incremento: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_TIME_CHARGE_FIX'):
            fp.write("Incremento in Minuti: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'USE_FLOWER_SEED'):
            fp.write("Oggetto Ottenibile: " + item['Value0'] + " (" + get_item_name(item['Value0']) + ")\n")
            fp.write("Quantita' Richiesta: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_METIN'):
        fp.write("Valore 0: " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Index Pietra: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_FISH'):
        fp.write("Index Pesce: " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_ROD'):
        fp.write("Incremento Pesca: " + item['Value0'] + "\n")
        fp.write("Diminuzione Tempo Pesca: " + item['Value1'] + "\n")
        fp.write("Punti per Potenziare: " + item['Value2'] + "\n")
        fp.write("Percentuale Up: " + item['Value3'] + "\n")
        fp.write("Item conserva Punti: " + item['Value4'] + " (" + get_item_name(item['Value4']) + ")\n")
        fp.write("Percentuale Punti Persi: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_UNIQUE'):
        fp.write("Durata: " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Scade se non usato: " + inttosino(item['Value2']) + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_QUEST'):
        if (subtype2 == 'QUEST_PET_PAY'):
            fp.write("Tipo Pet: " + item['Value0'] + "\n")
        else:
            fp.write("Valore 0: " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_SKILLBOOK'):
        fp.write("ID Abiita': " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_TREASURE_BOX' or itemtype2 == 'ITEM_TREASURE_KEY'):
        fp.write("Tipo Chiave/Forziere: " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_GIFTBOX'):
        fp.write("Spazi Vuoti Richiesti: " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_PICK'):
        fp.write("Incremento Minerali: " + item['Value0'] + "\n")
        fp.write("Diminuzione Tempo Piccone: " + item['Value1'] + "\n")
        fp.write("Punti per Potenziare: " + item['Value2'] + "\n")
        fp.write("Percentuale Up: " + item['Value3'] + "\n")
        fp.write("Item conserva Punti: " + item['Value4'] + " (" + get_item_name(item['Value4']) + ")\n")
        fp.write("Percentuale Punti Persi: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_COSTUME' and subtype2 != "COSTUME_ACCE"):
        if (subtype2 == 'COSTUME_WEAPON'):
            fp.write("Valore 0: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Tipo Arma: " + item['Value3'] + " (" + get_item_subtype(itemtype2, item['Value3'])[1] + ")\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'COSTUME_MOUNT'):
            fp.write("Valore 0: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        else:
            fp.write("Valore 0: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value2'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Index Skin: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_EXTRACT'):
        fp.write("Incremento Percentuale: " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_BELT'):
        fp.write("Num. Slot Aperti: " + get_belt_slot(item['Value0']) + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_PET'):
        if (subtype2 == 'PET_EGG'):
            fp.write("Sigillo: " + item['Value0'] + " (" + get_item_name(item['Value0']) + ")\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Prezzo Schiusura: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'PET_UPBRINGING'):
            fp.write("Vnum Pet: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Vnum Pet Eroe: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'PET_SKILL_BOOK'):
            fp.write("ID Skill: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
        elif (subtype2 == 'PET_OLD'):
            fp.write("Vnum Pet: " + item['Value0'] + "\n")
            fp.write("Valore 1: " + item['Value1'] + "\n")
            fp.write("Valore 2: " + item['Value2'] + "\n")
            fp.write("Valore 3: " + item['Value3'] + "\n")
            fp.write("Valore 4: " + item['Value4'] + "\n")
            fp.write("Valore 5: " + item['Value5'] + "\n")
    elif (itemtype2 == 'ITEM_SOUL'):
        fp.write("Value 0: " + item['Value0'] + "\n")
        fp.write("Up Anima: " + item['Value1'] + "\n")
        fp.write("Colpi Potenziati: " + item['Value2'] + "\n")
        fp.write("Moltiplicatore 1: " + item['Value3'] + "\n")
        fp.write("Moltiplicatore 2: " + item['Value4'] + "\n")
        fp.write("Moltiplicatore 3: " + item['Value5'] + "\n")
    else:
        fp.write("Valore 0: " + item['Value0'] + "\n")
        fp.write("Valore 1: " + item['Value1'] + "\n")
        fp.write("Valore 2: " + item['Value2'] + "\n")
        fp.write("Valore 3: " + item['Value3'] + "\n")
        fp.write("Valore 4: " + item['Value4'] + "\n")
        fp.write("Valore 5: " + item['Value5'] + "\n")


def stampa_info_mob(vnum, name):
    filename = cur_dir + "/Info_Mob_" + vnum + "_" + name + ".txt"
    fp = open(filename, "w")
    if (gestore_opzioni.get_option("Platform") == 0):
        mob = mob_data.mob_data_vnum[vnum]
    else:
        mob = mob_data.mob_data_vnum_en[vnum]
    fp.write("Vnum: " + vnum + "\n")
    fp.write("Nome: " + name + "\n")
    fp.write("Tipo: " + get_mob_type(mob['Type'])[1] + " (" + get_mob_type(mob['Type'])[0] + ")\n")
    fp.write("Grado: " + get_mob_grade(mob['Rank'])[1] + " (" + get_mob_grade(mob['Rank'])[0] + ")\n")
    fp.write("Tipo Attacco: " + get_mob_battle_type(mob['BattleType'])[1] + " (" + get_mob_battle_type(mob['BattleType'])[0] + ")\n")
    fp.write("Livello: " + mob['Level'] + "\n")
    fp.write("Scale Point: " + mob['ScalePct'] + "%\n")
    fp.write("Dimensione: " + get_mob_size(mob['Size'])[1] + " (" + get_mob_size(mob['Size'])[0] + ")\n")
    fp.write("Yang Droppati - Minimi: " + mob['DropGoldMin'] + " - Massimi: " + mob['DropGoldMax'] + "\n")
    fp.write("Exp: " + mob['Experience'] + "\n")
    fp.write("Max HP: " + mob['MaxHP'] + "\n")
    fp.write("Rigenerazione HP - Ciclo di " + mob['RegenCycle'] + " secondi - Percentuale Curata: " + mob['RegenPercent'] + "%\n")
    fp.write("Difesa: " + mob['Defense'] + "\n")
    fp.write("Flag Wiki Anti Flag: " + get_wiki_mob_flag(vnum))
    fp.write("Flag AI: " + get_mob_ai_flag(int(mob['AIFlags']))[1] + " (" + get_mob_ai_flag(int(mob['AIFlags']))[0] + ")\n")
    fp.write("Flag Razza: " + get_mob_race_flag(int(mob['RaceFlag']))[1] + " (" + get_mob_race_flag(int(mob['RaceFlag']))[0] + ")\n")
    fp.write("Flag Immunita': " + get_mob_immune_flag(int(mob['ImmuneFlag']))[1] + " (" + get_mob_immune_flag(int(mob['Int']))[0] + ")\n")
    fp.write("Statistiche - STR: " + mob['Str'] + " - DEX: " + mob['Dex'] + " - VIT: " + mob['Con'] + " - INT: " + mob['Int'] + "\n")
    fp.write("Danni - Minimi: " + mob['DamageMin'] + " - Massimi: " + mob['DamageMax'] + "\n")
    fp.write("Velocita' d'Attacco: " + mob['AttackSpeed'] + "\n")
    fp.write("Velocita' di Movimento: " + mob['MovingSpeed'] + "\n")
    fp.write("Aggressivita' - Percentuale HP per aggro: " + mob['AggressiveHPPct'] + "% - Raggio Aggro: " + mob['AggressiveSight'] + "\n")
    fp.write("Range Attacco: " + mob['AttackRange'] + "\n")
    fp.write("Possibilita' di\n")
    fp.write("\tMaledizione: " + mob['EnchantCurse'] + "%\n")
    fp.write("\tRallentamento: " + mob['EnchantSlow'] + "%\n")
    fp.write("\tVeleno: " + mob['EnchantPoison'] + "%\n")
    fp.write("\tStordimento: " + mob['EnchantStun'] + "%\n")
    fp.write("\tColpo Critico: " + mob['EnchantCritical'] + "%\n")
    fp.write("\tColpo Perforante: " + mob['EnchantPenetrate'] + "%\n")
    fp.write("Resistenze\n")
    fp.write("\tPugni: " + mob['ResistFist'] + "%\n")
    fp.write("\tSpada: " + mob['ResistSword'] + "%\n")
    fp.write("\tSpadone: " + mob['ResistTwohand'] + "%\n")
    fp.write("\tPugnale: " + mob['ResistDagger'] + "%\n")
    fp.write("\tCampana: " + mob['ResistBell'] + "%\n")
    fp.write("\tVentaglio: " + mob['ResistFan'] + "%\n")
    fp.write("\tArco: " + mob['ResistBow'] + "%\n")
    fp.write("\tArtiglio: " + mob['ResistClaw'] + "%\n")
    fp.write("\tFuoco: " + mob['ResistFire'] + "%\n")
    fp.write("\tLampo: " + mob['ResistElect'] + "%\n")
    fp.write("\tMagia: " + mob['ResistMagic'] + "%\n")
    fp.write("\tVento: " + mob['ResistWind'] + "%\n")
    fp.write("\tTerra: " + mob['ResistEarth'] + "%\n")
    fp.write("\tOscurita': " + mob['ResistDark'] + "%\n")
    fp.write("\tGhiaccio: " + mob['ResistIce'] + "%\n")
    fp.write("\tAvvelenamento: " + mob['ResistPoison'] + "%\n")
    fp.write("\tSanguinamento: " + mob['ResistBleeding'] + "%\n")
    fp.write("% Attacco Elementale\n")
    fp.write("\tLampo: " + mob['AttElec'] + "%\n")
    fp.write("\tVento: " + mob['AttWind'] + "%\n")
    fp.write("\tFuoco: " + mob['AttFire'] + "%\n")
    fp.write("\tGhiaccio: " + mob['AttIce'] + "%\n")
    fp.write("\tOscurita': " + mob['AttDark'] + "%\n")
    fp.write("\tTerra: " + mob['AttEarth'] + "%\n")
    fp.write("Vnum Mob in cui Respawna: " + mob['ResurrectionVnum'] + " (" + QtMetin2.get_mob_name(mob['ResurrectionVnum']) + ")\n")
    fp.write("Vnum Item Droppato: " + mob['DropItemVnum'] + " (" + get_item_name(mob['DropItemVnum']) + ")\n")
    fp.write("Capacita' Mount: " + mob['MountCapacity'] + "\n")
    fp.write("Tipo On Click: " + get_mob_type_on_click(mob['OnClickType'])[1] + " (" + get_mob_type_on_click(mob['OnClickType'])[0] + ")\n")
    fp.write("Regno: " + mob['Empire'] + " (" + get_regno(mob['Empire'])[1] + ")\n")
    fp.write("Cartella File Mob: " + mob['Folder'] + "\n")
    fp.write("Moltiplicatore Danno: " + mob['DamMultiply'] + "\n")
    fp.write("Vnum Mob Evocato: " + mob['SummonVnum'] + " (" + QtMetin2.get_mob_name(mob['SummonVnum']) + ")\n")
    fp.write("MP Rubati: " + mob['DrainSP'] + "\n")
    fp.write("Colore Mostro: " + mob['MonsterColor'] + "\n")
    fp.write("Sfera Trasformazione Droppata: " + mob['PolymorphItemVnum'] + "\n")
    fp.write("Skill Mob\n")
    fp.write("\tID Skill 1: " + mob['SkillVnum0'] + "\n")
    fp.write("\tLivello Skill 1: " + mob['SkillLevel0'] + "\n")
    fp.write("\tID Skill 2: " + mob['SkillVnum1'] + "\n")
    fp.write("\tLivello Skill 2: " + mob['SkillLevel1'] + "\n")
    fp.write("\tID Skill 3: " + mob['SkillVnum2'] + "\n")
    fp.write("\tLivello Skill 3: " + mob['SkillLevel2'] + "\n")
    fp.write("\tID Skill 4: " + mob['SkillVnum3'] + "\n")
    fp.write("\tLivello Skill 4: " + mob['SkillLevel3'] + "\n")
    fp.write("Punti Berserk: " + mob['BerserkPoint'] + "\n")
    fp.write("Punti StoneSkin: " + mob['StoneSkinPoint'] + "\n")
    fp.write("Punti GodSpeed: " + mob['GodSpeedPoint'] + "\n")
    fp.write("Punti Deathblow: " + mob['DeathBlowPoint'] + "\n")
    fp.write("Punti Revive: " + mob['RevivePoint'] + "\n")
    fp.write("Vnum Mob Curato: " + mob['HealVnum'] + " (" + QtMetin2.get_mob_name(mob['HealVnum']) + ")\n")
    fp.write("Range Colpo: " + mob['HitRange'] +  "\n")
    fp.flush()
    fp.close()


