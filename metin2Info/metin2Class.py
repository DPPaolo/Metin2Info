# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
import metin2Data
import QtMetin2
import proto
import re

class gestore_opzioni():
    def __init__(self):
        #Creazione file di Opzioni
        self.setting = QtCore.QSettings(proto.cur_dir + "/config.ini", QtCore.QSettings.IniFormat)
        self.setting.setFallbacksEnabled(False)

    def create_config(self):
        self.set_option("Version", "3") #Versione Programma
        self.set_option("SubVersion", "3") #Versione Programma
        self.set_option("FirstInit", 0) #Prima Installazione
        self.set_option("Debug", 0) #Debug
        self.set_option("Platform", 0) #Lingua File: 0 IT, 1 Test Server
        self.set_option("TradMob", 0) #Traduzione dei Nomi: 0 No, 1 Si
        self.set_option("Update/AutoUpdate", 1) #Aggiornamento Automatico

    def get_option(self, option, *tipo):
        if (tipo):
            val = self.setting.value(option, "testo")
            return val
        else:
            val = self.setting.value(option, 0)
            return int(val)

    def set_option(self, option, value):
        self.setting.setValue(option, value)

    def change_option(self, name, value):
        value = int(value)
        self.set_option(name, value)
        if (name == "Platform"):
            proto.change_download_file(value)
            QtMetin2.change_suggest_list(value)

class item_data():
    def __init__(self, file1, file2):
        self.item_data_vnum, self.item_data_name, self.item_set_up = self.create_dictionary_xml(file1)
        self.item_data_vnum_en, self.item_data_name_en, self.item_set_up_en =  self.create_dictionary_xml(file2)


    def create_dictionary_xml(self, file):
        item_data_vnum = {}
        item_data_name = {}
        item_set_up = []
        try:
            fp = open(file,"r")
        except:
            proto.err("Errore nell'apertura del file item_proto")
            proto.stampa_errore("Errore nell'apertura del file item_proto")
            return item_data_vnum, item_data_name, []

        p1 = re.compile(metin2Data.VNUM_PARSER)
        p2 = re.compile(metin2Data.NAME_PARSER)
        p3 = re.compile(metin2Data.DATA_PARSER)
        vnum = name = None
        for line in fp.readlines():
            vnum = p1.findall(line)
            if (not vnum):
                continue
            name = p2.findall(line)
            num = p3.findall(line)
            vnum = vnum[0]
            name = name[0]
            item_info = {}
            item_info['vnum'] = vnum
            item_info['name'] = name.title()
            item_info['VnumRange'] = num[1]
            item_info['Type'] = num[4]
            item_info['SubType'] = num[5]
            item_info['TypeMask'] = num[6]
            item_info['SubTypeMask'] = num[7]
            item_info['Weight'] = num[8]
            item_info['Size'] = num[9]
            item_info['AntiFlags'] = num[10]
            item_info['Flags'] = num[11]
            item_info['WearFlags'] = num[12]
            item_info['ImmuneFlags'] = num[13]
            item_info['Gold'] = num[14]
            item_info['ShopBuyPrice'] = num[15]
            item_info['LimitType0'] = num[16]
            item_info['LimitValue0'] = num[17]
            item_info['LimitType1'] = num[18]
            item_info['LimitValue1'] = num[19]
            item_info['ApplyType0'] = num[20]
            item_info['ApplyValue0'] = num[21]
            item_info['ApplyType1'] = num[22]
            item_info['ApplyValue1'] = num[23]
            item_info['ApplyType2'] = num[24]
            item_info['ApplyValue2'] = num[25]
            item_info['ApplyType3'] = num[26]
            item_info['ApplyValue3'] = num[27]
            item_info['Value0'] = num[28]
            item_info['Value1'] = num[29]
            item_info['Value2'] = num[30]
            item_info['Value3'] = num[31]
            item_info['Value4'] = num[32]
            item_info['Value5'] = num[33]
            item_info['Socket0'] = num[34]
            item_info['Socket1'] = num[35]
            item_info['Socket2'] = num[36]
            item_info['Socket3'] = num[37]
            item_info['Socket4'] = num[38]
            item_info['Socket5'] = num[39]
            item_info['RefineElementApplyType'] = num[40]
            item_info['RefineElementBonus'] = num[41]
            item_info['RefinedVnum'] = num[42]
            item_info['RefineSet'] = num[43]
            item_info['67_Material'] = num[44]
            item_info['AlterToMagicItemPercent'] = num[45]
            item_info['Specular'] = num[46]
            item_info['GainSocketPercent'] = num[47]
            item_data_vnum[vnum] = item_info
            if (item_info['RefineSet'] not in item_set_up):
                item_set_up.append(item_info['RefineSet'])
            if (name.title() in item_data_name):
                temp = item_data_name[name.title()]
                if (type(temp) == dict):
                    item_data_name[name.title()] = []
                    item_data_name[name.title()].append(temp)
                item_data_name[name.title()].append(item_info)
            else:
                item_data_name[name.title()] = item_info

        return item_data_vnum, item_data_name, item_set_up

    def get_vnum_list(self):
        return list(self.item_data_vnum.keys()), list(self.item_data_vnum_en.keys())

    def get_name_list(self):
        return list(self.item_data_name.keys()), list(self.item_data_name_en.keys())
    
class mob_data():
    def __init__(self, file1, file2):
        self.mob_data_vnum, self.mob_data_name = self.create_dictionary(file1)
        self.mob_data_vnum_en, self.mob_data_name_en =  self.create_dictionary(file2)
        self.mob_name_it = self.create_mob_name_it()

    def create_dictionary(self, file):
        mob_data_vnum = {}
        mob_data_name = {}
        try:
            fp = open(file,"r")
        except:
            proto.err("Errore nell'apertura del file mob_proto")
            proto.stampa_errore("Errore nell'apertura del file mob_proto")
            return mob_data_vnum, mob_data_name

        p1 = re.compile(metin2Data.VNUM_PARSER)
        p2 = re.compile(metin2Data.NAME_PARSER)
        p3 = re.compile(metin2Data.DATA_PARSER)
        p4 = re.compile(metin2Data.FOLDER_PARSER)
        vnum = name = num = folder = mult = None
        for line in fp.readlines():
            vnum = p1.findall(line)
            if (not vnum):
                continue
            name = p2.findall(line)
            num = p3.findall(line)
            folder = p4.findall(line)
            vnum = vnum[0]
            name = name[0]
            folder = folder[0]
            mob_info = {}
            mob_info['vnum'] = vnum
            mob_info['name'] = name.title()
            mob_info['Type'] = num[3]
            mob_info['Rank'] = num[4]
            mob_info['BattleType'] = num[5]
            mob_info['Level'] = num[6]
            mob_info['ScalePct'] = num[7]
            mob_info['Size'] = num[8]
            mob_info['DropGoldMin'] = num[9]
            mob_info['DropGoldMax'] = num[10]
            mob_info['Experience'] = num[11]
            mob_info['SungMaExperience'] = num[12]
            mob_info['MaxHP'] = num[13]
            mob_info['RegenCycle'] = num[14]
            mob_info['RegenPercent'] = num[15]
            mob_info['Defense'] = num[16]
            mob_info['AIFlags'] = num[17]
            mob_info['RaceFlag'] = num[18]
            mob_info['ImmuneFlag'] = num[19]
            mob_info['Str'] = num[20]
            mob_info['Dex'] = num[21]
            mob_info['Con'] = num[22]
            mob_info['Int'] = num[23]
            mob_info['SungMaStr'] = num[24]
            mob_info['SungMaDex'] = num[25]
            mob_info['SungMaCon'] = num[26]
            mob_info['SungMaInt'] = num[27]
            mob_info['DamageMin'] = num[28]
            mob_info['DamageMax'] = num[29]
            mob_info['AttackSpeed'] = num[30]
            mob_info['MovingSpeed'] = num[31]
            mob_info['AggressiveHPPct'] = num[32]
            mob_info['AggressiveSight'] = num[33]
            mob_info['AttackRange'] = num[34]
            mob_info['EnchantCurse'] = num[35]
            mob_info['EnchantSlow'] = num[36]
            mob_info['EnchantPoison'] = num[37]
            mob_info['EnchantStun'] = num[38]
            mob_info['EnchantCritical'] = num[39]
            mob_info['EnchantPenetrate'] = num[40]
            mob_info['ResistFist'] = num[41]
            mob_info['ResistSword'] = num[42]
            mob_info['ResistTwohand'] = num[43]
            mob_info['ResistDagger'] = num[44]
            mob_info['ResistBell'] = num[45]
            mob_info['ResistFan'] = num[46]
            mob_info['ResistBow'] = num[47]
            mob_info['ResistClaw'] = num[48]
            mob_info['ResistFire'] = num[49]
            mob_info['ResistElect'] = num[50]
            mob_info['ResistMagic'] = num[51]
            mob_info['ResistWind'] = num[52]
            mob_info['ResistPoison'] = num[53]
            mob_info['ResistBleeding'] = num[54]
            mob_info['AttElec'] = num[55]
            mob_info['AttFire'] = num[56]
            mob_info['AttIce'] = num[57]
            mob_info['AttWind'] = num[58]
            mob_info['AttEarth'] = num[59]
            mob_info['AttDark'] = num[60]
            mob_info['ResistDark'] = num[61]
            mob_info['ResistIce'] = num[62]
            mob_info['ResistEarth'] = num[63]
            mob_info['ResurrectionVnum'] = num[64]
            mob_info['DropItemVnum'] = num[65]
            mob_info['MountCapacity'] = num[66]
            mob_info['OnClickType'] = num[67]
            mob_info['Empire'] = num[68]
            mob_info['Folder'] = folder
            mob_info['DamMultiply'] = num[70]
            mob_info['SummonVnum'] = num[71]
            mob_info['DrainSP'] = num[72]
            mob_info['MonsterColor'] = num[73]
            mob_info['PolymorphItemVnum'] = num[74]
            mob_info['SkillVnum0'] = num[75]
            mob_info['SkillLevel0'] = num[76]
            mob_info['SkillVnum1'] = num[77]
            mob_info['SkillLevel1'] = num[78]
            mob_info['SkillVnum2'] = num[79]
            mob_info['SkillLevel2'] = num[80]
            mob_info['SkillVnum3'] = num[81]
            mob_info['SkillLevel3'] = num[82]
            mob_info['SkillVnum4'] = num[83]
            mob_info['SkillLevel4'] = num[84]
            mob_info['BerserkPoint'] = num[85]
            mob_info['StoneSkinPoint'] = num[86]
            mob_info['GodSpeedPoint'] = num[87]
            mob_info['DeathBlowPoint'] = num[88]
            mob_info['RevivePoint'] = num[89]
            mob_info['HealPoint'] = num[90]
            mob_info['ReverseAttackSpeedPoint'] = num[91]
            mob_info['ReverseCastSpeedPoint'] = num[92]
            mob_info['ReverseHPRegenPoint'] = num[93]
            mob_info['HitRange'] = num[94]
            mob_data_vnum[vnum] = mob_info
            if (name.title() in mob_data_name):
                temp = mob_data_name[name.title()]
                if (type(temp) == dict):
                    mob_data_name[name.title()] = []
                    mob_data_name[name.title()].append(temp)
                mob_data_name[name.title()].append(mob_info)
            else:
                mob_data_name[name.title()] = mob_info

        return mob_data_vnum, mob_data_name

    def create_mob_name_it(self):
        data = {}
        try:
            fp = open(proto.DOWNLOAD_FILE[4],"r")
        except:
            proto.err("Errore nell'apertura del file mob_list")
            proto.stampa_errore("Errore nell'apertura del file mob_list")
            return []
        for line in fp.readlines():
            line = line.replace("\n", "")
            line = line.split("\t")
            
            if (line[1].title() in data):
                if (type(data[line[1].title()]) == list):
                    data[line[1].title()].append(line[0])
                else:
                    temp = data[line[1].title()]
                    data[line[1].title()] = []
                    data[line[1].title()].append(temp)
                    data[line[1].title()].append(line[0])
            else:
                data[line[1].title()] = line[0]
        return data

    def get_vnum_list(self):
        return list(self.mob_data_vnum.keys()), list(self.mob_data_vnum_en.keys())

    def get_name_list(self):
        return list(self.mob_data_name.keys()), list(self.mob_data_name_en.keys())

    def get_name_list_it(self):
        return list(self.mob_name_it.keys())

class search_box():

    def __init__(self, tipo):
        self.tipo = tipo
        SearchVnumLab = QtWidgets.QLabel("Vnum: ")
        SearchBoxVnum = QtWidgets.QLineEdit()
        SearchNameLab = QtWidgets.QLabel("Nome: ")
        SearchBoxName = QtWidgets.QLineEdit()
        SearchBoxStampa = QtWidgets.QPushButton("Stampa")
        
        self.ItemIcon = item_icon()
        self.ItemIcon.icon.setAlignment(QtCore.Qt.AlignLeft)

        self.NameLab = QtWidgets.QLabel("Nome: ")
        self.Name = QtWidgets.QLabel("N/D")
        self.VnumLab = QtWidgets.QLabel("Vnum: ")
        self.Vnum = QtWidgets.QLabel("N/D")
        self.ItemDesc = QtWidgets.QLabel("")

        self.ItemDesc.setAlignment(QtCore.Qt.AlignLeft)

        completerVnum = QtWidgets.QCompleter()
        completerName = QtWidgets.QCompleter()

        self.modelVnum = QtCore.QStringListModel()
        self.modelName = QtCore.QStringListModel()

        completerVnum.setModel(self.modelVnum)
        completerName.setModel(self.modelName)
        
        SearchBoxVnum.setCompleter(completerVnum)
        SearchBoxName.setCompleter(completerName)

        self.SearchBar = QtWidgets.QHBoxLayout()
        self.NameVnumBox = QtWidgets.QHBoxLayout()
        self.IconBox = QtWidgets.QHBoxLayout()

        self.InfoBox = QtWidgets.QVBoxLayout()
        self.SearchBox = QtWidgets.QVBoxLayout()

        self.SearchBar.addWidget(SearchVnumLab)
        self.SearchBar.addWidget(SearchBoxVnum)
        self.SearchBar.addWidget(SearchNameLab)
        self.SearchBar.addWidget(SearchBoxName)
        self.SearchBar.addWidget(SearchBoxStampa)

        self.NameVnumBox.addWidget(self.NameLab)
        self.NameVnumBox.addWidget(self.Name)
        self.NameVnumBox.addWidget(self.VnumLab)
        self.NameVnumBox.addWidget(self.Vnum)

        self.InfoBox.addLayout(self.NameVnumBox)
        self.InfoBox.addWidget(self.ItemDesc)        

        self.IconBox.addStretch(1)
        self.IconBox.addWidget(self.ItemIcon.icon)
        self.IconBox.addLayout(self.InfoBox)
        self.IconBox.addStretch(1)

        self.SearchBox.addLayout(self.SearchBar)
        self.SearchBox.addLayout(self.IconBox)

        #self.SearchBox.addStretch(1)

        self.set_tooltip()

        self.list_item_vnum = proto.item_data.get_vnum_list()
        self.list_item_name = proto.item_data.get_name_list()

        self.list_mob_vnum = proto.mob_data.get_vnum_list()
        self.list_mob_name = proto.mob_data.get_name_list()
        self.list_mob_name_it = proto.mob_data.get_name_list_it()

        if (self.tipo == 1):
            SearchBoxVnum.returnPressed.connect(lambda: QtMetin2.update_item_info_by_vnum(SearchBoxVnum.text()))
            SearchBoxName.returnPressed.connect(lambda: QtMetin2.update_item_info_by_name(SearchBoxName.text()))
            SearchBoxStampa.clicked.connect(lambda: QtMetin2.stampa_item_data(SearchBoxVnum.text(), SearchBoxName.text()))
            if (int(proto.gestore_opzioni.get_option("Platform")) == 0):
                self.modelVnum.setStringList(list(str(self.list_item_vnum[0].sort(key=int))))
                self.modelName.setStringList(sorted(self.list_item_name[0]))
            else:
                self.modelVnum.setStringList(list(str(self.list_item_vnum[1].sort(key=int))))
                self.modelName.setStringList(sorted(self.list_item_name[1]))

        elif (self.tipo == 2):
            SearchBoxVnum.returnPressed.connect(lambda: QtMetin2.update_mob_info_by_vnum(SearchBoxVnum.text()))
            SearchBoxName.returnPressed.connect(lambda: QtMetin2.update_mob_info_by_name(SearchBoxName.text()))
            SearchBoxStampa.clicked.connect(lambda: QtMetin2.stampa_mob_data(SearchBoxVnum.text(), SearchBoxName.text()))
            if (int(proto.gestore_opzioni.get_option("Platform")) == 0):
                self.modelVnum.setStringList(list(str(self.list_mob_vnum[0].sort(key=int))))
                self.modelName.setStringList(sorted(self.list_mob_name_it))
            else:
                self.modelVnum.setStringList(list(str(self.list_mob_vnum[1].sort(key=int))))
                self.modelName.setStringList(sorted(self.list_mob_name[1]))

    def set_suggest_list(self, value):
        if (value == 0):
            if (self.tipo == 1):
                self.modelVnum.setStringList(self.list_item_vnum[0])
                self.modelName.setStringList(self.list_item_name[0])
            else:
                self.modelVnum.setStringList(self.list_mob_vnum[0])
                self.modelName.setStringList(self.list_mob_name_it)
        else:
            if (self.tipo == 1):
                self.modelVnum.setStringList(self.list_item_vnum[1])
                self.modelName.setStringList(self.list_item_name[1])
            else:
                self.modelVnum.setStringList(self.list_mob_vnum[1])
                self.modelName.setStringList(self.list_mob_name[1])

    def set_tooltip(self):
        if (self.tipo == 1):
            self.ItemIcon.setToolTip("Icona dell'oggetto")
            self.NameLab.setToolTip("Nome dell'oggetto in gioco")
            self.Name.setToolTip("Nome dell'oggetto in gioco")
            self.VnumLab.setToolTip("Vnum dell'oggetto.\nPer creare questo oggetto basta usare il comando /i con questo valore")
            self.Vnum.setToolTip("Vnum dell'oggetto.\nPer creare questo oggetto basta usare il comando /i con questo valore")
        elif (self.tipo == 2):
            self.NameLab.setToolTip("Nome del mostro in gioco")
            self.Name.setToolTip("Nome del mostro in gioco")
            self.VnumLab.setToolTip("Vnum del mostro.\nPer far apparire questo mostro basta usare il comando /m con questo valore")
            self.Vnum.setToolTip("Vnum del mostro.\nPer far apparire questo mostro basta usare il comando /m con questo valore")

    def set_name_vnum(self, name, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            if (self.tipo == 1):
                item = proto.item_data.item_data_vnum[vnum]
            else:
                item = proto.mob_data.mob_data_vnum[vnum]
        else:
            if (self.tipo == 1):
                item = proto.item_data.item_data_vnum_en[vnum]
            else:
                item = proto.mob_data.mob_data_vnum_en[vnum]
        self.Name.setText(str(name))
        if (self.tipo == 1):
            self.ItemIcon.setToolTip("Icona dell'oggetto.\nIcona corrispondente: " + proto.get_icon_vnum(vnum) + ".png")  
            self.ItemIcon.set_icon(vnum)
            if (str(item['VnumRange']) == "0"):
                self.Vnum.setText(str(vnum))
            else:
                self.Vnum.setText(str(vnum) + " ~ " + str(item['VnumRange']))
        else:
            self.Vnum.setText(str(vnum))

    def set_desc(self, desc):
        self.ItemDesc.setText(proto.divide_message(desc))

    def set_no_data(self):
        self.Name.setText("Non Trovato")
        self.Vnum.setText("N/D")
        self.ItemDesc.setText(" ")
        self.ItemIcon.hide()       

class pre_flag_item_box():

    def __init__(self):
        self.ItemTypeLab = QtWidgets.QLabel("Tipo: ")
        self.ItemType = QtWidgets.QLabel("N/D")
        self.ItemSubTypeLab = QtWidgets.QLabel("Sotto Tipo: ")
        self.ItemSubType = QtWidgets.QLabel("N/D")
        self.ItemMaskTypeLab = QtWidgets.QLabel("Maschera Tipo: ")
        self.ItemMaskType = QtWidgets.QLabel("N/D")
        self.ItemMaskSubTypeLab = QtWidgets.QLabel("Maschera Sotto Tipo: ")
        self.ItemMaskSubType = QtWidgets.QLabel("N/D")
        self.ItemPesoLab = QtWidgets.QLabel("Peso: ")
        self.ItemPeso = QtWidgets.QLabel("N/D")
        self.ItemSpazioLab = QtWidgets.QLabel("Spazi Occupati: ")
        self.ItemSpazio = QtWidgets.QLabel("N/D")
        self.ItemSpace = QtWidgets.QLabel(" ")
        
        self.set_tooltip(False)

        self.pre_flag_box1 = QtWidgets.QHBoxLayout()
        self.pre_flag_box2 = QtWidgets.QHBoxLayout()
        self.pre_flag_box3 = QtWidgets.QHBoxLayout()
        
        self.pre_flag_Box = QtWidgets.QVBoxLayout()

        self.pre_flag_box1.addWidget(self.ItemTypeLab)
        self.pre_flag_box1.addWidget(self.ItemType)
        self.pre_flag_box1.addWidget(self.ItemSubTypeLab)
        self.pre_flag_box1.addWidget(self.ItemSubType)

        self.pre_flag_box2.addWidget(self.ItemMaskTypeLab)
        self.pre_flag_box2.addWidget(self.ItemMaskType)
        self.pre_flag_box2.addWidget(self.ItemMaskSubTypeLab)
        self.pre_flag_box2.addWidget(self.ItemMaskSubType)
        
        self.pre_flag_box3.addWidget(self.ItemPesoLab)
        self.pre_flag_box3.addWidget(self.ItemPeso)
        self.pre_flag_box3.addWidget(self.ItemSpazioLab)
        self.pre_flag_box3.addWidget(self.ItemSpazio)

        self.pre_flag_Box.addWidget(self.ItemSpace)
        self.pre_flag_Box.addLayout(self.pre_flag_box1)
        self.pre_flag_Box.addLayout(self.pre_flag_box2)
        self.pre_flag_Box.addLayout(self.pre_flag_box3)

    def set_tooltip(self, vnum):
        self.ItemPesoLab.setToolTip("Peso dell'oggetto. Valore non usato in gioco")
        self.ItemPeso.setToolTip("Peso dell'oggetto. Valore non usato in gioco")
        self.ItemSpazioLab.setToolTip("Numero di slot occupati in verticale dell'inventario.\nGli oggetti con spazio uguale a 0 servono da placeholder\nper determinate funzioni, come l'autocaccia.")
        self.ItemSpazio.setToolTip("Numero di slot occupati in verticale dell'inventario.\nGli oggetti con spazio uguale a 0 servono da placeholder\nper determinate funzioni, come l'autocaccia.")

        if (vnum == False):
            self.ItemTypeLab.setToolTip("Tipo dell'oggetto. Il Tipo determina parte delle\nsue funzioni e il significato dei campi value.")
            self.ItemType.setToolTip("Tipo dell'oggetto. Il Tipo determina parte delle\nsue funzioni e il significato dei campi value.")
            self.ItemSubTypeLab.setToolTip("Sotto Tipo dell'oggetto. Specifica una sotto funzione\nspecifica. Solo alcuni tipi di oggetti ne hanno uno.")
            self.ItemSubType.setToolTip("Sotto Tipo dell'oggetto. Specifica una sotto funzione\nspecifica. Solo alcuni tipi di oggetti ne hanno uno.")
            self.ItemMaskTypeLab.setToolTip("Tipo Maschera dell'oggetto. Serve a determinarne il comportamento\nnei vari slot del personaggio.")
            self.ItemMaskType.setToolTip("Tipo Maschera dell'oggetto. Serve a determinarne il comportamento\nnei vari slot del personaggio.")
            self.ItemMaskSubTypeLab.setToolTip("Sotto Tipo Maschera dell'oggetto. Specifica ancora di piu'\nil comportamento dell'oggetto. Pochi oggetti ne possiedono uno.")
            self.ItemMaskSubType.setToolTip("Sotto Tipo Maschera dell'oggetto. Specifica ancora di piu'\nil comportamento dell'oggetto. Pochi oggetti ne possiedono uno.")
        else:
            if (proto.gestore_opzioni.get_option("Platform") == 0):
                item = proto.item_data.item_data_vnum[vnum]
            else:
                item = proto.item_data.item_data_vnum_en[vnum]
            self.ItemTypeLab.setToolTip("Tipo dell'oggetto. Il Tipo determina parte delle\nsue funzioni e il significato dei campi value.\nValore Originale: " + proto.get_item_type(item['Type'])[0])
            self.ItemType.setToolTip("Tipo dell'oggetto. Il Tipo determina parte delle\nsue funzioni e il significato dei campi value.\nValore Originale: " + proto.get_item_type(item['Type'])[0])
            self.ItemSubTypeLab.setToolTip("Sotto Tipo dell'oggetto. Specifica una sotto funzione\nspecifica. Solo alcuni tipi di oggetti ne hanno uno.\nValore Originale: " + proto.get_item_subtype(item['Type'],item['SubType'])[0])
            self.ItemSubType.setToolTip("Sotto Tipo dell'oggetto. Specifica una sotto funzione\nspecifica. Solo alcuni tipi di oggetti ne hanno uno.\nValore Originale: " + proto.get_item_subtype(item['Type'],item['SubType'])[0])
            self.ItemMaskTypeLab.setToolTip("Tipo Maschera dell'oggetto. Serve a determinarne il comportamento\nnei vari slot del personaggio.\nValore Originale: " + proto.get_item_mask(item['TypeMask'])[0])
            self.ItemMaskType.setToolTip("Tipo Maschera dell'oggetto. Serve a determinarne il comportamento\nnei vari slot del personaggio.\nValore Originale: " + proto.get_item_mask(item['TypeMask'])[0])
            self.ItemMaskSubTypeLab.setToolTip("Sotto Tipo Maschera dell'oggetto. Specifica ancora di piu'\nil comportamento dell'oggetto. Pochi oggetti ne possiedono uno.\nValore Originale: " + proto.get_item_sub_mask(item['TypeMask'], item['SubTypeMask'])[0])
            self.ItemMaskSubType.setToolTip("Sotto Tipo Maschera dell'oggetto. Specifica ancora di piu'\nil comportamento dell'oggetto. Pochi oggetti ne possiedono uno.\nValore Originale: " + proto.get_item_sub_mask(item['TypeMask'], item['SubTypeMask'])[0])   

    def set_pre_flag_data(self, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            item = proto.item_data.item_data_vnum[vnum]
        else:
            item = proto.item_data.item_data_vnum_en[vnum]
        self.ItemType.setText(proto.get_item_type(item['Type'])[1])
        self.ItemSubType.setText(proto.get_item_subtype(item['Type'],item['SubType'])[1])
        self.ItemMaskType.setText(proto.get_item_mask(item['TypeMask'])[1])
        self.ItemMaskSubType.setText(proto.get_item_sub_mask(item['TypeMask'],item['SubTypeMask'])[1])
        self.ItemPeso.setText(item['Weight'])
        self.ItemSpazio.setText(item['Size'])
        self.set_tooltip(vnum)

    def set_pre_flag_no_data(self):
        self.ItemType.setText("N/D")
        self.ItemSubType.setText("N/D")
        self.ItemMaskType.setText("N/D")
        self.ItemMaskSubType.setText("N/D")
        self.ItemPeso.setText("N/D")
        self.ItemSpazio.setText("N/D")
        self.set_tooltip(False)

class flag_item_box():

    def __init__(self):
        self.ItemFlagWikiLab = QtWidgets.QLabel("Flag Wiki: ")
        self.ItemFlagWiki = QtWidgets.QLabel("N/D")
        self.ItemAntiFlagLab = QtWidgets.QLabel("Anti Flag: ")
        self.ItemAntiFlag = QtWidgets.QLabel("N/D")
        self.ItemFlagLab = QtWidgets.QLabel("Flag: ")
        self.ItemFlag = QtWidgets.QLabel("N/D")
        self.ItemFlagUsoLab = QtWidgets.QLabel("Flag Uso: ")
        self.ItemFlagUso = QtWidgets.QLabel("N/D")
        self.ItemFlagImmLab = QtWidgets.QLabel("Flag Immunita': ")
        self.ItemFlagImm = QtWidgets.QLabel("N/D")
        self.Item67BonusLab = QtWidgets.QLabel("Item per 6° e 7° Bonus: ")
        self.Item67Bonus = QtWidgets.QLabel("N/D")
        self.ItemBuyLab = QtWidgets.QLabel("Prezzo di Acquisto: ")
        self.ItemBuy = QtWidgets.QLabel("N/D")
        self.ItemSellImmLab = QtWidgets.QLabel("Prezzo di Vendita: ")
        self.ItemSellImm = QtWidgets.QLabel("N/D")

        self.ItemSpace1 = QtWidgets.QLabel(" ")
        self.ItemSpace2 = QtWidgets.QLabel(" ")
        self.ItemSpace3 = QtWidgets.QLabel(" ")
        self.ItemSpace4 = QtWidgets.QLabel(" ")
        self.ItemSpace5 = QtWidgets.QLabel(" ")
        self.ItemSpace6 = QtWidgets.QLabel(" ")
        self.ItemSpace7 = QtWidgets.QLabel(" ")
        self.ItemSpace8 = QtWidgets.QLabel(" ")
        self.ItemSpace9 = QtWidgets.QLabel(" ")
        self.ItemSpace10 = QtWidgets.QLabel(" ")
        self.ItemSpace11 = QtWidgets.QLabel(" ")
        self.ItemSpace12 = QtWidgets.QLabel(" ")

        self.set_tooltip(False)

        self.flag_box1 = QtWidgets.QHBoxLayout()
        self.flag_box2 = QtWidgets.QHBoxLayout()
        self.flag_box3 = QtWidgets.QHBoxLayout()
        self.flag_box4 = QtWidgets.QHBoxLayout()
        self.flag_box5 = QtWidgets.QHBoxLayout()
        self.flag_box6 = QtWidgets.QHBoxLayout()
        self.flag_box7 = QtWidgets.QHBoxLayout()
        
        self.flag_Box = QtWidgets.QVBoxLayout()

        self.flag_box1.addWidget(self.ItemFlagWikiLab)
        self.flag_box1.addWidget(self.ItemFlagWiki)
        self.flag_box1.addWidget(self.ItemSpace1)
        self.flag_box1.addWidget(self.ItemSpace2)

        self.flag_box2.addWidget(self.ItemAntiFlagLab)
        self.flag_box2.addWidget(self.ItemAntiFlag)
        self.flag_box2.addWidget(self.ItemSpace3)
        self.flag_box2.addWidget(self.ItemSpace4)

        self.flag_box3.addWidget(self.ItemFlagLab)
        self.flag_box3.addWidget(self.ItemFlag)
        self.flag_box3.addWidget(self.ItemSpace5)
        self.flag_box3.addWidget(self.ItemSpace6)

        self.flag_box4.addWidget(self.ItemFlagUsoLab)
        self.flag_box4.addWidget(self.ItemFlagUso)
        self.flag_box4.addWidget(self.ItemSpace7)
        self.flag_box4.addWidget(self.ItemSpace8)

        self.flag_box5.addWidget(self.ItemFlagImmLab)
        self.flag_box5.addWidget(self.ItemFlagImm)
        self.flag_box5.addWidget(self.ItemSpace9)
        self.flag_box5.addWidget(self.ItemSpace10)

        self.flag_box6.addWidget(self.Item67BonusLab)
        self.flag_box6.addWidget(self.Item67Bonus)
        self.flag_box6.addWidget(self.ItemSpace10)
        self.flag_box6.addWidget(self.ItemSpace11)
        
        self.flag_box7.addWidget(self.ItemBuyLab)
        self.flag_box7.addWidget(self.ItemBuy)
        self.flag_box7.addWidget(self.ItemSellImmLab)
        self.flag_box7.addWidget(self.ItemSellImm)

        self.flag_Box.addLayout(self.flag_box1)
        self.flag_Box.addLayout(self.flag_box2)
        self.flag_Box.addLayout(self.flag_box3)
        self.flag_Box.addLayout(self.flag_box4)
        self.flag_Box.addLayout(self.flag_box5)
        self.flag_Box.addLayout(self.flag_box6)
        self.flag_Box.addLayout(self.flag_box7)

    def set_tooltip(self, vnum):
        self.ItemFlagWikiLab.setToolTip("Parametro da inserire nel Template Interazioni")
        self.ItemFlagWiki.setToolTip("Parametro da inserire nel Template Interazioni")
        self.ItemBuyLab.setToolTip("Prezzo di acquisto base dell'oggetto nei negozi.")
        self.ItemBuy.setToolTip("Prezzo di acquisto base dell'oggetto nei negozi.")
        self.ItemSellImmLab.setToolTip("Prezzo di vendita dell'oggetto nei negozi.")
        self.ItemSellImm.setToolTip("Prezzo di Vendita dell'oggetto nei negozi.")
        self.Item67BonusLab.setToolTip("Oggetto richiesto per aggiungere il 6° e 7° bonus")
        self.Item67Bonus.setToolTip("Oggetto richiesto per aggiungere il 6° e 7° bonus")

        if (vnum == False):
            self.ItemAntiFlagLab.setToolTip("Anti Flag dell'oggetto. Indicano cosa non si puo' fare con l'oggetto.")
            self.ItemAntiFlag.setToolTip("Anti Flag dell'oggetto. Indicano cosa non si puo' fare con l'oggetto.")
            self.ItemFlagLab.setToolTip("Flag dell'oggetto. Indica cosa e' possibile fare con\nl'oggettoe che caratteristiche possiede. ")
            self.ItemFlag.setToolTip("Flag dell'oggetto. Indica cosa e' possibile fare con\nl'oggetto e che caratteristiche possiede. ")
            self.ItemFlagUsoLab.setToolTip("Flag del tipo di uso dell'oggetto nell'equipaggiamento.\nIndica in quale posizione della finestra personaggio deve essere\nposizionato l'oggetto.")
            self.ItemFlagUso.setToolTip("Flag del tipo di uso dell'oggetto nell'equipaggiamento.\nIndica in quale posizione della finestra personaggio deve essere\nposizionato l'oggetto.")
            self.ItemFlagImmLab.setToolTip("Flag Immunita' dell'oggetto. Indica quale immunita' possiede l'oggetto\n riferita ai vari status negativi. Nessun oggetto presenta valore diverso da 0.")
            self.ItemFlagImm.setToolTip("Flag Immunita' dell'oggetto. Indica quale immunita' possiede l'oggetto\n riferita ai vari status negativi. Nessun oggetto presenta valore diverso da 0.")
        else:
            if (proto.gestore_opzioni.get_option("Platform") == 0):
                item = proto.item_data.item_data_vnum[vnum]
            else:
                item = proto.item_data.item_data_vnum_en[vnum]
            self.ItemAntiFlagLab.setToolTip("Anti Flag dell'oggetto. Indicano cosa non si puo' fare con l'oggetto.\nValore Originale: " + proto.get_anti_flag(int(item['AntiFlags']))[0])
            self.ItemAntiFlag.setToolTip("Anti Flag dell'oggetto. Indicano cosa non si puo' fare con l'oggetto.\nValore Originale: " + proto.get_anti_flag(int(item['AntiFlags']))[0])
            self.ItemFlagLab.setToolTip("Flag dell'oggetto. Indica cosa e' possibile fare con\nl'oggettoe che caratteristiche possiede. \nValore Originale: " + proto.get_item_flag(int(item['Flags']))[0])
            self.ItemFlag.setToolTip("Flag dell'oggetto. Indica cosa e' possibile fare con\nl'oggetto e che caratteristiche possiede. \nValore Originale: " + proto.get_item_flag(int(item['Flags']))[0])
            self.ItemFlagUsoLab.setToolTip("Flag del tipo di uso dell'oggetto nell'equipaggiamento.\nIndica in quale posizione della finestra personaggio deve essere\nposizionato l'oggetto.\nValore Originale: " + proto.get_wear_flag(int(item['WearFlags']))[0])
            self.ItemFlagUso.setToolTip("Flag del tipo di uso dell'oggetto nell'equipaggiamento.\nIndica in quale posizione della finestra personaggio deve essere\nposizionato l'oggetto.\nValore Originale: " + proto.get_wear_flag(int(item['WearFlags']))[0])
            self.ItemFlagImmLab.setToolTip("Flag Immunita' dell'oggetto. Indica quale immunita' possiede l'oggetto\n riferita ai vari status negativi. Nessun oggetto presenta valore diverso da 0.\nValore Originale: " + proto.get_item_immune_flag(int(item['ImmuneFlags']))[0])
            self.ItemFlagImm.setToolTip("Flag Immunita' dell'oggetto. Indica quale immunita' possiede l'oggetto\n riferita ai vari status negativi. Nessun oggetto presenta valore diverso da 0.\nValore Originale: " + proto.get_item_immune_flag(int(item['ImmuneFlags']))[0])        

    def set_flag_data(self, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            item = proto.item_data.item_data_vnum[vnum]
        else:
            item = proto.item_data.item_data_vnum_en[vnum]
        self.ItemFlagWiki.setText(proto.get_wiki_anti_flag(int(item['AntiFlags']), int(item['Flags'])))
        self.ItemAntiFlag.setText(proto.get_anti_flag(int(item['AntiFlags']))[1])
        self.ItemFlag.setText(proto.get_item_flag(int(item['Flags']))[1])
        self.ItemFlagUso.setText(proto.get_wear_flag(int(item['WearFlags']))[1])
        self.ItemFlagImm.setText(proto.get_item_immune_flag(int(item['ImmuneFlags']))[1])
        self.Item67Bonus.setText(item['67_Material'] + " (" + proto.get_item_name(item['67_Material']) + ")")
        self.ItemBuy.setText(item['Gold'] + " Yang")
        self.ItemSellImm.setText(str(int(item['ShopBuyPrice'])//5) + " Yang")
        self.set_tooltip(vnum)

    def set_flag_no_data(self):
        self.ItemFlagWiki.setText("N/D")
        self.ItemAntiFlag.setText("N/D")
        self.ItemFlag.setText("N/D")
        self.ItemFlagUso.setText("N/D")
        self.ItemFlagImm.setText("N/D")
        self.Item67Bonus.setText("N/D")
        self.ItemBuy.setText("N/D")
        self.ItemSellImm.setText("N/D")
        self.set_tooltip(False)

class bonus_item_box():

    def __init__(self):
        self.ItemLimit0Lab = QtWidgets.QLabel("Restrizione 1: ")
        self.ItemLimit0 = QtWidgets.QLabel("N/D")
        self.ItemLimit1Lab = QtWidgets.QLabel("Restrizione 2: ")
        self.ItemLimit1 = QtWidgets.QLabel("N/D")
        self.ItemBonus0Lab = QtWidgets.QLabel("Bonus 1: ")
        self.ItemBonus0 = QtWidgets.QLabel("N/D")
        self.ItemBonus1Lab = QtWidgets.QLabel("Bonus 2: ")
        self.ItemBonus1 = QtWidgets.QLabel("N/D")
        self.ItemBonus2Lab = QtWidgets.QLabel("Bonus 3: ")
        self.ItemBonus2 = QtWidgets.QLabel("N/D")
        self.ItemBonus3Lab = QtWidgets.QLabel("Bonus 4: ")
        self.ItemBonus3 = QtWidgets.QLabel("N/D")
        self.ItemValue0Lab  = QtWidgets.QLabel("Valore 0: ")
        self.ItemValue0  = QtWidgets.QLabel("N/D")
        self.ItemValue1Lab  = QtWidgets.QLabel("Valore 1: ")
        self.ItemValue1  = QtWidgets.QLabel("N/D")
        self.ItemValue2Lab  = QtWidgets.QLabel("Valore 2: ")
        self.ItemValue2  = QtWidgets.QLabel("N/D")
        self.ItemValue3Lab  = QtWidgets.QLabel("Valore 3: ")
        self.ItemValue3  = QtWidgets.QLabel("N/D")
        self.ItemValue4Lab  = QtWidgets.QLabel("Valore 4: ")
        self.ItemValue4  = QtWidgets.QLabel("N/D")
        self.ItemValue5Lab  = QtWidgets.QLabel("Valore 5: ")
        self.ItemValue5  = QtWidgets.QLabel("N/D")

        self.ItemFisValLab = QtWidgets.QLabel("Attacco Fisico: ")
        self.ItemFisVal = QtWidgets.QLabel("N/D")
        self.ItemMagValLab = QtWidgets.QLabel("Attacco Magico: ")
        self.ItemMagVal = QtWidgets.QLabel("N/D")
        self.ItemArmorLab = QtWidgets.QLabel("Difesa: ")
        self.ItemArmor = QtWidgets.QLabel("N/D")

        self.ItemSpace1  = QtWidgets.QLabel(" ")
        self.ItemSpace2  = QtWidgets.QLabel(" ")

        self.bonus_box1 = QtWidgets.QHBoxLayout()
        self.bonus_box2 = QtWidgets.QHBoxLayout()
        self.bonus_box3 = QtWidgets.QHBoxLayout()
        self.bonus_box4 = QtWidgets.QHBoxLayout()
        self.bonus_box5 = QtWidgets.QHBoxLayout()
        self.bonus_box6 = QtWidgets.QHBoxLayout()
        self.bonus_box7 = QtWidgets.QHBoxLayout()

        self.bonus_Box = QtWidgets.QVBoxLayout()
        
        self.bonus_box1.addWidget(self.ItemLimit0Lab)
        self.bonus_box1.addWidget(self.ItemLimit0)
        self.bonus_box1.addWidget(self.ItemLimit1Lab)
        self.bonus_box1.addWidget(self.ItemLimit1)

        self.bonus_box2.addWidget(self.ItemBonus0Lab)
        self.bonus_box2.addWidget(self.ItemBonus0)
        self.bonus_box2.addWidget(self.ItemBonus1Lab)
        self.bonus_box2.addWidget(self.ItemBonus1)

        self.bonus_box3.addWidget(self.ItemBonus2Lab)
        self.bonus_box3.addWidget(self.ItemBonus2)
        self.bonus_box3.addWidget(self.ItemBonus3Lab)
        self.bonus_box3.addWidget(self.ItemBonus3)

        self.bonus_box4.addWidget(self.ItemArmorLab)
        self.bonus_box4.addWidget(self.ItemArmor)
        self.bonus_box4.addWidget(self.ItemSpace1)
        self.bonus_box4.addWidget(self.ItemSpace2)
        self.bonus_box4.addWidget(self.ItemFisValLab)
        self.bonus_box4.addWidget(self.ItemFisVal)
        self.bonus_box4.addWidget(self.ItemMagValLab)
        self.bonus_box4.addWidget(self.ItemMagVal)
        
        self.bonus_box5.addWidget(self.ItemValue0Lab)
        self.bonus_box5.addWidget(self.ItemValue0)
        self.bonus_box5.addWidget(self.ItemValue1Lab)
        self.bonus_box5.addWidget(self.ItemValue1)
        
        self.bonus_box6.addWidget(self.ItemValue2Lab)
        self.bonus_box6.addWidget(self.ItemValue2)
        self.bonus_box6.addWidget(self.ItemValue3Lab)
        self.bonus_box6.addWidget(self.ItemValue3)

        self.bonus_box7.addWidget(self.ItemValue4Lab)
        self.bonus_box7.addWidget(self.ItemValue4)
        self.bonus_box7.addWidget(self.ItemValue5Lab)
        self.bonus_box7.addWidget(self.ItemValue5)

        self.bonus_Box.addLayout(self.bonus_box1)
        self.bonus_Box.addLayout(self.bonus_box2)
        self.bonus_Box.addLayout(self.bonus_box3)
        self.bonus_Box.addLayout(self.bonus_box4)
        self.bonus_Box.addLayout(self.bonus_box5)
        self.bonus_Box.addLayout(self.bonus_box6)
        self.bonus_Box.addLayout(self.bonus_box7)

        self.ItemFisValLab.hide()
        self.ItemFisVal.hide()
        self.ItemMagValLab.hide()
        self.ItemMagVal.hide()
        self.ItemArmorLab.hide()
        self.ItemArmor.hide()
        self.ItemSpace1.show()
        self.ItemSpace2.show()
        
        self.set_tooltip(False)
            
    def set_tooltip(self, vnum):
        self.ItemValue0Lab.setToolTip("Valore 0 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue0.setToolTip("Valore 0 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue1Lab.setToolTip("Valore 1 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue1.setToolTip("Valore 1 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue2Lab.setToolTip("Valore 2 dell'oggetto")
        self.ItemValue2.setToolTip("Valore 2 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue3Lab.setToolTip("Valore 3 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue3.setToolTip("Valore 3 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue4Lab.setToolTip("Valore 4 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue4.setToolTip("Valore 4 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue5Lab.setToolTip("Valore 5 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        self.ItemValue5.setToolTip("Valore 5 dell'oggetto. Indica le caratteristiche dell'oggetto.\nIl significato del valore varia in base al tipo dell'oggetto.")
        if (vnum == False):
            self.ItemLimit0Lab.setToolTip("Primo requisito per equipaggiare o usare l'oggetto, in genere\n si tratta del livello minimo.")
            self.ItemLimit0.setToolTip("Primo requisito per equipaggiare o usare l'oggetto, in genere\n si tratta del livello minimo.")
            self.ItemLimit1Lab.setToolTip("Secondo requisito per equipaggiare o usare l'oggetto.")
            self.ItemLimit1.setToolTip("Secondo requisito per equipaggiare o usare l'oggetto.")
            self.ItemBonus0Lab.setToolTip("Primo Bonus base dell'oggetto.")
            self.ItemBonus0.setToolTip("Primo Bonus base dell'oggetto.")
            self.ItemBonus1Lab.setToolTip("Secondo Bonus base dell'oggetto.")
            self.ItemBonus1.setToolTip("Secondo Bonus base dell'oggetto.")
            self.ItemBonus2Lab.setToolTip("Terzo Bonus base dell'oggetto.")
            self.ItemBonus2.setToolTip("Terzo Bonus base dell'oggetto.")
            self.ItemBonus2Lab.setToolTip("Quarto Bonus base dell'oggetto.")
            self.ItemBonus2.setToolTip("Quarto Bonus base dell'oggetto.")
            self.ItemFisValLab.setToolTip("Valore di Attacco Fisico dell'arma ")
            self.ItemFisVal.setToolTip("Valore di Attacco Fisico dell'arma")
            self.ItemMagValLab.setToolTip("Valore di Attacco Magico dell'arma, se lo possiede.")
            self.ItemMagVal.setToolTip("Valore di Attacco Magico dell'arma, se lo possiede.")
            self.ItemArmorLab.setToolTip("Valore di Difesa dell'oggetto.")
            self.ItemArmor.setToolTip("Valore di Difesa dell'oggetto.")
        else:
            if (proto.gestore_opzioni.get_option("Platform") == 0):
                item = proto.item_data.item_data_vnum[vnum]
            else:
                item = proto.item_data.item_data_vnum_en[vnum]
            self.ItemLimit0Lab.setToolTip("Primo requisito per equipaggiare o usare l'oggetto, in genere\n si tratta del livello minimo.\nValore Originale: " + str(proto.get_limit_type(int(item['LimitType0']))[0]))
            self.ItemLimit0.setToolTip("Primo requisito per equipaggiare o usare l'oggetto, in genere\n si tratta del livello minimo.\nValore Originale: "  + str(proto.get_limit_type(int(item['LimitType0']))[0]))
            self.ItemLimit1Lab.setToolTip("Secondo requisito per equipaggiare o usare l'oggetto.\nValore Originale: " + str(proto.get_limit_type(int(item['LimitType1']))[0]))
            self.ItemLimit1.setToolTip("Secondo requisito per equipaggiare o usare l'oggetto.\nValore Originale: " + str(proto.get_limit_type(int(item['LimitType1']))[0]))
            self.ItemBonus0Lab.setToolTip("Primo Bonus base dell'oggetto.\nValore Originale: " + str(proto.get_apply_type(int(item['ApplyType0']))[0]))
            self.ItemBonus0.setToolTip("Primo Bonus base dell'oggetto.\nValore Originale: " + str(proto.get_apply_type(int(item['ApplyType0']))[0]))
            self.ItemBonus1Lab.setToolTip("Secondo Bonus base dell'oggetto.\nValore Originale: " + str(proto.get_apply_type(int(item['ApplyType1']))[0]))
            self.ItemBonus1.setToolTip("Secondo Bonus base dell'oggetto.\nValore Originale: " + str(proto.get_apply_type(int(item['ApplyType1']))[0]))
            self.ItemBonus2Lab.setToolTip("Terzo Bonus base dell'oggetto.\nValore Originale: " + str(proto.get_apply_type(int(item['ApplyType2']))[0]))
            self.ItemBonus2.setToolTip("Terzo Bonus base dell'oggetto.\nValore Originale: " + str(proto.get_apply_type(int(item['ApplyType2']))[0]))
            self.ItemBonus3Lab.setToolTip("Quarto Bonus base dell'oggetto.\nValore Originale: " + str(proto.get_apply_type(int(item['ApplyType3']))[0]))
            self.ItemBonus3.setToolTip("Quarto Bonus base dell'oggetto.\nValore Originale: " + str(proto.get_apply_type(int(item['ApplyType3']))[0]))
            self.ItemFisValLab.setToolTip("Valore di Attacco Fisico dell'arma.\nValore calcolato nel seguente modo:\nAttacco Fisico Minimo: Valore 3 + Valore 5\nAttacco Fisico Massimo: Valore 4 + Valore 5")
            self.ItemFisVal.setToolTip("Valore di Attacco Fisico dell'arma.\nValore calcolato nel seguente modo:\nAttacco Fisico Minimo: Valore 3 + Valore 5\nAttacco Fisico Massimo: Valore 4 + Valore 5")
            self.ItemMagValLab.setToolTip("Valore di Attacco Magico dell'arma, se lo possiede.\nValore calcolato nel seguente modo:\nAttacco Magico Minimo: Valore 1 + Valore 5\nAttacco Magico Massimo: Valore 2 + Valore 5")
            self.ItemMagVal.setToolTip("Valore di Attacco Magico dell'arma, se lo possiede.\nValore calcolato nel seguente modo:\nAttacco Magico Minimo: Valore 1 + Valore 5\nAttacco Magico Massimo: Valore 2 + Valore 5")
            self.ItemArmorLab.setToolTip("Valore di Difesa dell'oggetto.\nValore calcolato nel seguente modo:\nDifesa: Valore 1 + 2*Valore 5")
            self.ItemArmor.setToolTip("Valore di Difesa dell'oggetto.\nValore calcolato nel seguente modo:\nDifesa: Valore 1 + 2*Valore 5")

    def set_bonus_data(self, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            item = proto.item_data.item_data_vnum[vnum]
        else:
            item = proto.item_data.item_data_vnum_en[vnum]
        if (str(item['LimitType0']) == "0" and str(item['LimitValue0']) == "0"):
            self.ItemLimit0.setText(proto.get_limit_type(int(item['LimitType0']))[1])
        else:
            if (str(item['LimitType0']) in ["7", "8", "9"]):
                self.ItemLimit0.setText(proto.get_limit_type(int(item['LimitType0']))[1] + " " + proto.get_time(item['LimitValue0']))
            else:
                self.ItemLimit0.setText(proto.get_limit_type(int(item['LimitType0']))[1] + " " + item['LimitValue0'])
        if (str(item['LimitType1']) == "0" and str(item['LimitValue1']) == "0"):
            self.ItemLimit1.setText(proto.get_limit_type(int(item['LimitType1']))[1])
        else:
            if (str(item['LimitType1']) in ["7", "8", "9"]):
                self.ItemLimit1.setText(proto.get_limit_type(int(item['LimitType1']))[1] + " " + proto.get_time(item['LimitValue1']))
            else:
                self.ItemLimit1.setText(proto.get_limit_type(int(item['LimitType1']))[1] + " " + item['LimitValue1'])
        if (str(item['ApplyType0']) == "0" and str(item['ApplyValue0']) == "0"):
            self.ItemBonus0.setText(proto.get_apply_type(int(item['ApplyType0']))[1])
        else:
            self.ItemBonus0.setText(proto.get_apply_type(int(item['ApplyType0']))[1] + " " + item['ApplyValue0'])
        if (str(item['ApplyType1']) == "0" and str(item['ApplyValue1']) == "0"):
            self.ItemBonus1.setText(proto.get_apply_type(int(item['ApplyType1']))[1])
        else:
            self.ItemBonus1.setText(proto.get_apply_type(int(item['ApplyType1']))[1] + " " + item['ApplyValue1'])
        if (str(item['ApplyType2']) == "0" and str(item['ApplyValue2']) == "0"):
            self.ItemBonus2.setText(proto.get_apply_type(int(item['ApplyType2']))[1])
        else:
            self.ItemBonus2.setText(proto.get_apply_type(int(item['ApplyType2']))[1]  + " " + item['ApplyValue2'])
        if (str(item['ApplyType3']) == "0" and str(item['ApplyValue3']) == "0"):
            self.ItemBonus3.setText(proto.get_apply_type(int(item['ApplyType3']))[1])
        else:
            self.ItemBonus3.setText(proto.get_apply_type(int(item['ApplyType3']))[1]  + " " + item['ApplyValue3'])

        self.ItemValue0Lab.setText("Valore 0: ")
        self.ItemValue1Lab.setText("Valore 1: ")
        self.ItemValue2Lab.setText("Valore 2: ")
        self.ItemValue3Lab.setText("Valore 3: ")
        self.ItemValue4Lab.setText("Valore 4: ")
        self.ItemValue5Lab.setText("Valore 5: ")
        self.ItemValue0.setText(item['Value0'])
        self.ItemValue1.setText(item['Value1'])
        self.ItemValue2.setText(item['Value2'])
        self.ItemValue3.setText(item['Value3'])
        self.ItemValue4.setText(item['Value4'])
        self.ItemValue5.setText(item['Value5'])

        self.ItemFisValLab.hide()
        self.ItemFisVal.hide()
        self.ItemMagValLab.hide()
        self.ItemMagVal.hide()
        self.ItemArmorLab.hide()
        self.ItemArmor.hide()
        self.ItemSpace1.hide()
        self.ItemSpace2.hide()

        itemtype2 = proto.get_item_type(item['Type'])[0]
        subtype2 = proto.get_item_subtype(item['Type'], item['SubType'])[0]

        if (itemtype2 == 'ITEM_WEAPON'):
            self.ItemFisValLab.show()
            self.ItemFisVal.show()
            self.ItemMagValLab.show()
            self.ItemMagVal.show()
            self.ItemFisVal.setText(str(int(item['Value3'])+ int(item['Value5'])) + " - " + str(int(item['Value4'])+ int(item['Value5'])))
            if (int(item['Value2']) != 0):
                self.ItemMagVal.setText(str(int(item['Value1'])+ int(item['Value5'])) + " - " + str(int(item['Value2'])+ int(item['Value5'])))
            else:
                self.ItemMagVal.setText("Non Presente")
            self.ItemValue0Lab.setText("Valore 0: ")
            self.ItemValue1Lab.setText("Min Magico: ")
            self.ItemValue2Lab.setText("Max Magico: ")
            self.ItemValue3Lab.setText("Min Fisico: ")
            self.ItemValue4Lab.setText("Max Fisico: ")
            self.ItemValue5Lab.setText("Incremento: ")
        elif (itemtype2 == 'ITEM_ARMOR'):
            self.ItemArmorLab.show()
            self.ItemArmor.show()
            self.ItemSpace1.show()
            self.ItemSpace2.show()
            self.ItemArmor.setText(str(int(item['Value1']) + 2*int(item['Value5'])))
            self.ItemValue0Lab.setText("Valore 0: ")
            self.ItemValue1Lab.setText("Difesa Base: ")
            self.ItemValue2Lab.setText("Valore 2: ")
            self.ItemValue3Lab.setText("Index Skin: ")
            self.ItemValue4Lab.setText("Valore 4: ")
            self.ItemValue5Lab.setText("Meta' Incremento: ")
        elif (itemtype2 == 'ITEM_USE'):
            if (subtype2 == 'USE_POTION' or subtype2 == 'USE_POTION_NODELAY'):
                self.ItemValue0Lab.setText("HP Ripristinati: ")
                self.ItemValue1Lab.setText("MP Rpristinati: ")
            elif (subtype2 == 'USE_TALISMAN'):
                self.ItemValue0Lab.setText("Tipo Teletrasporto: ")
            elif (subtype2 == 'USE_TUNING'):
                self.ItemValue0Lab.setText("Tipo Pergamena Up: ")
            elif (subtype2 == 'USE_BAIT'):
                self.ItemValue0Lab.setText("Aumento % Pesca: ")
            elif (subtype2 == 'USE_ABILITY_UP'):
                self.ItemValue0Lab.setText("Bonus Fornito: ")
                self.ItemValue0.setText(proto.get_apply_type(item['Value0'])[1])
                self.ItemValue1Lab.setText("Durata: ")
                self.ItemValue2Lab.setText("Valore Bonus: ")
            elif (subtype2 == 'USE_AFFECT'):
                self.ItemValue0Lab.setText("ID Icona HUD: ")
                self.ItemValue1Lab.setText("Bonus Fornito: ")
                self.ItemValue1.setText(proto.get_apply_type(item['Value1'])[1])
                self.ItemValue2Lab.setText("Valore Bonus: ")
                self.ItemValue3Lab.setText("Durata: ")
                self.ItemValue4Lab.setText("Incremento Bonus: ")
            elif (subtype2 == 'USE_INVISIBILITY'):
                self.ItemValue1Lab.setText("Durata: ")
            elif (subtype2 == 'USE_DETACHMENT'):
                self.ItemValue0Lab.setText("Num. Pietre da Rimuovere: ")
            elif (subtype2 == 'USE_RECIPE'):
                self.ItemValue0Lab.setText("Risultato: ")
                self.ItemValue0.setText(proto.get_item_name(item['Value0']))
                self.ItemValue1Lab.setText("Materiale 1: ")
                self.ItemValue1.setText(proto.get_item_name(item['Value1']))
                self.ItemValue2Lab.setText("Quantita' Mat. 1: ")
                self.ItemValue3Lab.setText("Materiale 2: ")
                self.ItemValue3.setText(proto.get_item_name(item['Value3']))
                self.ItemValue4Lab.setText("Quantita' Mat. 2: ")
            elif (subtype2 == 'USE_TIME_CHARGE_PER'):
                self.ItemValue0Lab.setText("Percentuale Incremento: ")
            elif (subtype2 == 'USE_TIME_CHARGE_FIX'):
                self.ItemValue0Lab.setText("Incremento in Minuti: ")
            elif (subtype2 == 'USE_FLOWER_SEED'):
                self.ItemValue0Lab.setText("Oggetto Ottenibile: ")
                self.ItemValue0.setText(proto.get_item_name(item['Value0']))
                self.ItemValue1Lab.setText("Quantita' Richiesta: ")
        elif (itemtype2 == 'ITEM_METIN'):
            self.ItemValue5Lab.setText("Index Pietra: ")
        elif (itemtype2 == 'ITEM_FISH'):
            self.ItemValue0Lab.setText("Index Pesce: ")
        elif (itemtype2 == 'ITEM_ROD'):
            self.ItemValue0Lab.setText("Incremento Pesca: ")
            self.ItemValue1Lab.setText("Diminuzione Tempo Pesca: ")
            self.ItemValue2Lab.setText("Punti per Potenziare: ")
            self.ItemValue3Lab.setText("Percentuale Up: ")
            self.ItemValue4Lab.setText("Item conserva Punti: ")
            self.ItemValue4.setText(proto.get_item_name(item['Value4']))
            self.ItemValue5Lab.setText("Percentuale Punti Persi: ")
        elif (itemtype2 == 'ITEM_UNIQUE'):
            self.ItemValue0Lab.setText("Durata: ")
            self.ItemValue2Lab.setText("Scade se non usato: ")
            self.ItemValue2.setText(proto.inttosino(item['Value2']))
        elif (itemtype2 == 'ITEM_QUEST'):
            if (subtype2 == 'QUEST_PET_PAY'):
                self.ItemValue0Lab.setText("Tipo Pet: ")
        elif (itemtype2 == 'ITEM_SKILLBOOK'):
            self.ItemValue0Lab.setText("ID Abiita': ")
        elif (itemtype2 == 'ITEM_TREASURE_BOX' or itemtype2 == 'ITEM_TREASURE_KEY'):
            self.ItemValue0Lab.setText("Tipo Chiave/Forziere: ")
        elif (itemtype2 == 'ITEM_GIFTBOX'):
            self.ItemValue0Lab.setText("Spazi Vuoti Richiesti: ")
        elif (itemtype2 == 'ITEM_PICK'):
            self.ItemValue0Lab.setText("Incremento Minerali: ")
            self.ItemValue1Lab.setText("Diminuzione Tempo Piccone: ")
            self.ItemValue2Lab.setText("Punti per Potenziare: ")
            self.ItemValue3Lab.setText("Percentuale Up: ")
            self.ItemValue4Lab.setText("Item conserva Punti: ")
            self.ItemValue4.setText(proto.get_item_name(item['Value4']))
            self.ItemValue5Lab.setText("Percentuale Punti Persi: ")
        elif (itemtype2 == 'ITEM_COSTUME' and subtype2 != "COSTUME_ACCE"):
            if (subtype2 == 'COSTUME_WEAPON'):
                self.ItemValue0Lab.setText("Valore 0: ")
                self.ItemValue1Lab.setText("Valore 1: ")
                self.ItemValue2Lab.setText("Valore 2: ")
                self.ItemValue3Lab.setText("Tipo Arma: ")
                self.ItemValue3.setText(proto.get_item_subtype(1, item['Value3'])[1])
                self.ItemValue4Lab.setText("Valore 4: ")
                self.ItemValue5Lab.setText("Valore 5: ")
            elif (subtype2 == 'COSTUME_MOUNT'):
                self.ItemValue0Lab.setText("Valore 0: ")
                self.ItemValue1Lab.setText("Valore 1: ")
                self.ItemValue2Lab.setText("Valore 2: ")
                self.ItemValue3Lab.setText("Valore 3: ")
                self.ItemValue4Lab.setText("Valore 4: ")
                self.ItemValue5Lab.setText("Valore 5: ")
            else:
                self.ItemValue0Lab.setText("Valore 0: ")
                self.ItemValue1Lab.setText("Valore 1: ")
                self.ItemValue2Lab.setText("Valore 2: ")
                self.ItemValue3Lab.setText("Index Skin: ")
                self.ItemValue4Lab.setText("Valore 4: ")
                self.ItemValue5Lab.setText("Valore 5: ")
        elif (itemtype2 == 'ITEM_EXTRACT'):
            self.ItemValue0Lab.setText("Incremento Percentuale: ")
        elif (itemtype2 == 'ITEM_BELT'):
            self.ItemValue0Lab.setText("Num. Slot Aperti: ")
            self.ItemValue0.setText(proto.get_belt_slot(item['Value0']))
        elif (itemtype2 == 'ITEM_PET'):
            if (subtype2 == 'PET_EGG'):
                self.ItemValue0Lab.setText("Sigillo: ")
                self.ItemValue0.setText(proto.get_item_name(item['Value0']))
                self.ItemValue1Lab.setText("Valore 1: ")
                self.ItemValue2Lab.setText("Valore 2: ")
                self.ItemValue3Lab.setText("Prezzo Schiusura: ")
                self.ItemValue4Lab.setText("Valore 4: ")
                self.ItemValue5Lab.setText("Valore 5: ")
            elif (subtype2 == 'PET_UPBRINGING'):
                self.ItemValue0Lab.setText("Vnum Pet: ")
                self.ItemValue1Lab.setText("Valore 1: ")
                self.ItemValue2Lab.setText("Valore 2: ")
                self.ItemValue3Lab.setText("Vnum Pet Eroe: ")
                self.ItemValue4Lab.setText("Valore 4: ")
                self.ItemValue5Lab.setText("Valore 5: ")
            elif (subtype2 == 'PET_SKILL_BOOK'):
                self.ItemValue0Lab.setText("ID Skill: ")
            elif (subtype2 == 'PET_OLD'):
                self.ItemValue0Lab.setText("Vnum Pet: ")
        elif (itemtype2 == 'ITEM_SOUL'):
            self.ItemValue0Lab.setText("Value 0: ")
            self.ItemValue1Lab.setText("Up Anima: ")
            self.ItemValue2Lab.setText("Colpi Potenziati: ")
            self.ItemValue3Lab.setText("Moltiplicatore 1: ")
            self.ItemValue4Lab.setText("Moltiplicatore 2: ")
            self.ItemValue5Lab.setText("Moltiplicatore 3: ")
        else:
            self.ItemValue0Lab.setText("Valore 0: ")
            self.ItemValue1Lab.setText("Valore 1: ")
            self.ItemValue2Lab.setText("Valore 2: ")
            self.ItemValue3Lab.setText("Valore 3: ")
            self.ItemValue4Lab.setText("Valore 4: ")
            self.ItemValue5Lab.setText("Valore 5: ")
            
        self.set_tooltip(vnum)

    def set_bonus_no_data(self):
        self.ItemLimit0.setText("N/D")
        self.ItemLimit1.setText("N/D")
        self.ItemBonus0.setText("N/D")
        self.ItemBonus1.setText("N/D")
        self.ItemBonus2.setText("N/D")
        self.ItemValue0.setText("N/D")
        self.ItemValue1.setText("N/D")
        self.ItemValue2.setText("N/D")
        self.ItemValue3.setText("N/D")
        self.ItemValue4.setText("N/D")
        self.ItemValue5.setText("N/D")
        self.ItemValue0Lab.setText("Valore 0: ")
        self.ItemValue1Lab.setText("Valore 1: ")
        self.ItemValue2Lab.setText("Valore 2: ")
        self.ItemValue3Lab.setText("Valore 3: ")
        self.ItemValue4Lab.setText("Valore 4: ")
        self.ItemValue5Lab.setText("Valore 5: ")
        self.ItemFisValLab.hide()
        self.ItemFisVal.hide()
        self.ItemMagValLab.hide()
        self.ItemMagVal.hide()
        self.ItemArmorLab.hide()
        self.ItemArmor.hide()
        self.ItemSpace1.show()
        self.ItemSpace2.show()
        self.set_tooltip(False)

class other_item_box():

    def __init__(self):
        self.UpWidget = QtMetin2.widget_up(self)
        
        self.ItemSocket0Lab = QtWidgets.QLabel("Socket0: ")
        self.ItemSocket0 = QtWidgets.QLabel("N/D")
        self.ItemSocket1Lab = QtWidgets.QLabel("Socket1: ")
        self.ItemSocket1 = QtWidgets.QLabel("N/D")
        self.ItemSocket2Lab = QtWidgets.QLabel("Socket2: ")
        self.ItemSocket2 = QtWidgets.QLabel("N/D")
        self.ItemVnumUpLab = QtWidgets.QLabel("Vnum Up: ")
        self.ItemVnumUp = QtWidgets.QLabel("N/D")
        self.ItemSetUpLab = QtWidgets.QLabel("Set di Up: ")
        self.ItemSetUp = QtWidgets.QPushButton("N/D")
        self.ItemPossBonusLab = QtWidgets.QLabel("% Comparsa Bonus Extra: ")
        self.ItemPossBonus = QtWidgets.QLabel("N/D")
        self.ItemLuccLab = QtWidgets.QLabel("% Luccichio: ")
        self.ItemLucc = QtWidgets.QLabel("N/D")
        self.ItemSocketLab = QtWidgets.QLabel("Socket Disponibili: ")
        self.ItemSocket = QtWidgets.QLabel("N/D")

        self.Up = 0

        self.ItemSetUp.clicked.connect(self.open_set_up)
        
        self.set_tooltip()

        self.other_box1 = QtWidgets.QHBoxLayout()
        self.other_box2 = QtWidgets.QHBoxLayout()
        self.other_box3 = QtWidgets.QHBoxLayout()
        self.other_box4 = QtWidgets.QHBoxLayout()
        
        self.other_Box = QtWidgets.QVBoxLayout()

        self.other_box1.addWidget(self.ItemSocket0Lab)
        self.other_box1.addWidget(self.ItemSocket0)
        self.other_box1.addWidget(self.ItemSocket1Lab)
        self.other_box1.addWidget(self.ItemSocket1)

        self.other_box2.addWidget(self.ItemSocket2Lab)
        self.other_box2.addWidget(self.ItemSocket2)
        self.other_box2.addWidget(self.ItemLuccLab)
        self.other_box2.addWidget(self.ItemLucc)

        self.other_box3.addWidget(self.ItemVnumUpLab)
        self.other_box3.addWidget(self.ItemVnumUp)
        self.other_box3.addWidget(self.ItemSetUpLab)
        self.other_box3.addWidget(self.ItemSetUp)

        self.other_box4.addWidget(self.ItemPossBonusLab)
        self.other_box4.addWidget(self.ItemPossBonus)
        self.other_box4.addWidget(self.ItemSocketLab)
        self.other_box4.addWidget(self.ItemSocket)

        self.other_Box.addLayout(self.other_box1)
        self.other_Box.addLayout(self.other_box2)
        self.other_Box.addLayout(self.other_box3)
        self.other_Box.addLayout(self.other_box4)

    def open_set_up(self):
        item = proto.get_item_set_up(self.Up)       
        if (item):
            if ("Non" in item):
                pass
            else:
                self.item_up.set_up(item)
                self.UpWidget.setWindowTitle("Oggetti per Uppare Richiesti")
                self.UpWidget.show() 

    def set_tooltip(self):
        self.ItemSocket0Lab.setToolTip("Vnum dell'oggetto presente di base nel primo slot")
        self.ItemSocket0.setToolTip("Vnum dell'oggetto presente di base nel primo slot")
        self.ItemSocket1Lab.setToolTip("Vnum dell'oggetto presente di base nel secondo slot")
        self.ItemSocket1.setToolTip("Vnum dell'oggetto presente di base nel secondo slot")
        self.ItemSocket2Lab.setToolTip("Vnum dell'oggetto presente di base nel terzo slot")
        self.ItemSocket2.setToolTip("Vnum dell'oggetto presente di base nel terzo slot")
        self.ItemVnumUpLab.setToolTip("Vnum dell'item che si otterrebbe potenziando l'oggetto dal fabbro")
        self.ItemVnumUp.setToolTip("Vnum dell'item che si otterrebbe potenziando l'oggetto dal fabbro")
        self.ItemSetUpLab.setToolTip("Identificatore degli oggetti richiesti per l'up")
        self.ItemSetUp.setToolTip("Identificatore degli oggetti richiesti per l'up.\nClicca per saperne di piu'")
        self.ItemPossBonusLab.setToolTip("Possibilita' in percentuale che all'ottenimento\ndell'oggetto vengano aggiunti bonus extra a quelli\nbase (l'oggetto avra' il nome giallo invece che bianco)")
        self.ItemPossBonus.setToolTip("Possibilita' in percentuale che all'ottenimento\ndell'oggetto vengano aggiunti bonus extra a quelli\nbase (l'oggetto avra' il nome giallo invece che bianco)")
        self.ItemLuccLab.setToolTip("Percentuale dei particellari da visualizzare nell'oggetto. Percentuali\nbasse faranno apparire l'oggetto piu' lucido. Valori sopra al 60\naggiungeranno particellari visibili in quantita' e colore diversi")
        self.ItemLucc.setToolTip("Percentuale dei particellari da visualizzare nell'oggetto. Percentuali\nbasse faranno apparire l'oggetto piu' lucido. Valori sopra al 60\naggiungeranno particellari visibili in quantita' e colore diversi")
        self.ItemSocketLab.setToolTip("Numero di slot vuoti disponibili dell'oggetto\nper l'inserimento di pietre o raffinati")
        self.ItemSocket.setToolTip("Numero di slot vuoti disponibili dell'oggetto\nper l'inserimento di pietre o raffinati")

    def set_other_data(self, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            item = proto.item_data.item_data_vnum[vnum]
        else:
            item = proto.item_data.item_data_vnum_en[vnum]
        self.Up = int(item['RefineSet'])
        self.ItemSocket0.setText(item['Socket0'])
        self.ItemSocket1.setText(item['Socket1'])
        self.ItemSocket2.setText(item['Socket2'] )
        self.ItemVnumUp.setText(item['RefinedVnum'] + " (" + proto.get_item_name(item['RefinedVnum']) + ")")
        self.ItemSetUpLab.setText("Set di Up: ")
        self.ItemSetUp.setText(item['RefineSet'])
        self.ItemPossBonus.setText(item['AlterToMagicItemPercent'] + "%")
        self.ItemLucc.setText(item['Specular'])
        self.ItemSocket.setText(item['GainSocketPercent'])

    def set_other_no_data(self):
        self.Up = 0
        self.ItemSocket0.setText("N/D")
        self.ItemSocket1.setText("N/D")
        self.ItemSocket2.setText("N/D")
        self.ItemVnumUp.setText("N/D")
        self.ItemSetUpLab.setText("Set di Up: N/D")
        self.ItemSetUp.setText("N/D")
        self.ItemPossBonus.setText("N/D")
        self.ItemLucc.setText("N/D")
        self.ItemSocket.setText("N/D")

class pre_flag_mob_box():
    def __init__(self):
        self.MobType = QtWidgets.QLabel("Tipo: N/D")
        self.MobGrade = QtWidgets.QLabel("Grado: N/D")
        self.MobAttack = QtWidgets.QLabel("Tipo Attacco: N/D")
        self.MobLevel = QtWidgets.QLabel("Livello: N/D")
        self.MobScale = QtWidgets.QLabel("Punti Scala: N/D")
        self.MobDim = QtWidgets.QLabel("Dimensione: N/D")
        self.MobYang = QtWidgets.QLabel("Yang Droppati: N/D")
        self.MobExp = QtWidgets.QLabel("Exp: N/D")
        self.MobExpCampione = QtWidgets.QLabel("Exp Campione: N/D")
        self.MobHP = QtWidgets.QLabel("HP: N/D")
        self.MobDifesa = QtWidgets.QLabel("Difesa: N/D")
        self.MobRegHPCicle = QtWidgets.QLabel("Ciclo Rig. HP: N/D")
        self.MobRegHPPerc = QtWidgets.QLabel("Quantita' HP Curati: N/D")

        self.pre_flag_box0 = QtWidgets.QHBoxLayout()
        self.pre_flag_box1 = QtWidgets.QHBoxLayout()
        self.pre_flag_box2 = QtWidgets.QHBoxLayout()
        self.pre_flag_box3 = QtWidgets.QHBoxLayout()

        self.pre_flag_Box = QtWidgets.QVBoxLayout()
        
        self.pre_flag_box0.addWidget(self.MobLevel)
        self.pre_flag_box0.addWidget(self.MobGrade)
        self.pre_flag_box0.addWidget(self.MobType)
        self.pre_flag_box1.addWidget(self.MobAttack)
        self.pre_flag_box1.addWidget(self.MobScale)
        self.pre_flag_box1.addWidget(self.MobDim)
        self.pre_flag_box2.addWidget(self.MobYang)
        self.pre_flag_box2.addWidget(self.MobExp)
        self.pre_flag_box2.addWidget(self.MobExpCampione)
        self.pre_flag_box2.addWidget(self.MobDifesa)
        self.pre_flag_box3.addWidget(self.MobHP)
        self.pre_flag_box3.addWidget(self.MobRegHPCicle)
        self.pre_flag_box3.addWidget(self.MobRegHPPerc)

        self.pre_flag_Box.addLayout(self.pre_flag_box0)
        self.pre_flag_Box.addLayout(self.pre_flag_box1)
        self.pre_flag_Box.addLayout(self.pre_flag_box2)
        self.pre_flag_Box.addLayout(self.pre_flag_box3)

        self.set_tooltip(False)

    def set_pre_flag_data(self, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            mob = proto.mob_data.mob_data_vnum[vnum]
        else:
            mob = proto.mob_data.mob_data_vnum_en[vnum]
        self.MobType.setText("Tipo: " + proto.get_mob_type(mob['Type'])[1])
        self.MobGrade.setText("Grado: " + proto.get_mob_grade(mob['Rank'])[1])
        self.MobAttack.setText("Tipo Attacco: " + proto.get_mob_battle_type(mob['BattleType'])[1])
        self.MobLevel.setText("Livello: " + mob['Level'])
        self.MobScale.setText("Punti Scala: " + mob['ScalePct'] + "%")
        self.MobDim.setText("Dimensione: " + proto.get_mob_size(mob['Size'])[1])
        self.MobYang.setText("Yang Droppati: " + mob['DropGoldMin'] + " ~ " + mob['DropGoldMax'])
        self.MobExp.setText("Exp: " + mob['Experience'])
        self.MobExpCampione.setText("Exp Campione: " + mob['SungMaExperience'])
        self.MobDifesa.setText("Difesa: " + mob['Defense'])
        self.MobHP.setText("HP: " + mob['MaxHP'])
        self.MobRegHPCicle.setText("Ciclo Rig. HP: " + mob['RegenCycle'] + "s")
        self.MobRegHPPerc.setText("Quantita' HP Curati: " + mob['RegenPercent'] + "%")
        self.set_tooltip(vnum)

    def set_pre_flag_no_data(self):
        self.MobType.setText("Tipo: N/D")
        self.MobGrade.setText("Grado: N/D")
        self.MobAttack.setText("Tipo Attacco: N/D")
        self.MobLevel.setText("Livello: N/D")
        self.MobScale.setText("Punti Scala: N/D")
        self.MobDim.setText("Dimensione: N/D")
        self.MobYang.setText("Yang Droppati: N/D")
        self.MobExp.setText("Exp: N/D")
        self.MobExpCampione.setText("Exp Campione: N/D")
        self.MobHP.setText("HP: N/D")
        self.MobDifesa.setText("Difesa:N/D")
        self.MobRegHPCicle.setText("Ciclo Rig. HP: N/D")
        self.MobRegHPPerc.setText("Quantita' HP Curati:N/D")
        self.set_tooltip(False)

    def set_tooltip(self, vnum):
        self.MobLevel.setToolTip("Indica il livello del mostro.")
        self.MobScale.setToolTip("Indica il fattore in percentuale di scala da applicare alle dimensioni\nbase del mostro.")
        self.MobYang.setToolTip("Quantita' di Yan droppati dal mostro, il valore e' compreso tra\n il valore minimo e massimo.")
        self.MobExp.setToolTip("Exp ottenuta uccidendo il mostro.")
        self.MobExpCampione.setToolTip("Exp Campione ottenuta uccidendo il mostro.")
        self.MobHP.setToolTip("HP del mostro.")
        self.MobDifesa.setToolTip("Difesa del mostro.")
        self.MobRegHPCicle.setToolTip("Periodo del ciclo di rigenerazione HP del mostro.")
        self.MobRegHPPerc.setToolTip("Quantita' di HP rigenerati per ogni ciclo di rigenerazione.")
        if (vnum == False):
            self.MobType.setToolTip("Indica il tipo associato al mostro.\nNe determina il comportamento realtivo al personaggio.")
            self.MobGrade.setToolTip("Indica il grado del mostro.")
            self.MobAttack.setToolTip("Indica il tipo di attacco del mostro. In base al tipo\ncambiera' il tipo di danno che effettua.")
            self.MobDim.setToolTip("Dimensione del mostro.")
        else:
            if (proto.gestore_opzioni.get_option("Platform") == 0):
                mob = proto.mob_data.mob_data_vnum[vnum]
            else:
                mob = proto.mob_data.mob_data_vnum_en[vnum]
            self.MobType.setToolTip("Indica il tipo associato al mostro.\nNe determina il comportamento realtivo al personaggio.\nValore Originale: " + proto.get_mob_type(mob['Type'])[0])
            self.MobGrade.setToolTip("Indica il grado del mostro.\nValore Originale: " + proto.get_mob_type(mob['Rank'])[0])
            self.MobAttack.setToolTip("Indica il tipo di attacco del mostro. In base al tipo\ncambiera' il tipo di danno che effettua.\nValore Originale: " + proto.get_mob_battle_type(mob['BattleType'])[1])
            self.MobDim.setToolTip("Dimensione del mostro.\nValore originale: " + proto.get_mob_size(mob['Size'])[0])

class flag_mob_box():
    
    def __init__(self):
        self.MobFlagWikiLab = QtWidgets.QLabel("Flag Wiki:")
        self.MobFlagWiki = QtWidgets.QLabel("N/D")
        self.MobFlagAILab = QtWidgets.QLabel("Flag AI:")
        self.MobFlagAI = QtWidgets.QLabel("N/D")
        self.MobFlagRazzaLab = QtWidgets.QLabel("Flag Razza:")
        self.MobFlagRazza = QtWidgets.QLabel("N/D")
        self.MobFlagImmLab = QtWidgets.QLabel("Flag Immunita':")
        self.MobFlagImm = QtWidgets.QLabel("N/D")
        self.MobSTR = QtWidgets.QLabel("STR: N/D")
        self.MobDEX = QtWidgets.QLabel("DEX: N/D")
        self.MobVIT = QtWidgets.QLabel("VIT: N/D")
        self.MobINT = QtWidgets.QLabel("INT: N/D")
        self.MobSungMaSTR = QtWidgets.QLabel("SungMa STR: N/D")
        self.MobSungMaDEX = QtWidgets.QLabel("SungMa RES: N/D")
        self.MobSungMaVIT = QtWidgets.QLabel("SungMa VIT: N/D")
        self.MobSungMaINT = QtWidgets.QLabel("SungMa INT: N/D")
        self.MobDam = QtWidgets.QLabel("Danno Mostro: N/D")
        self.MobRangeATT = QtWidgets.QLabel("Range Mostro: N/D")
        self.MobVelAtt = QtWidgets.QLabel("Vel. Attacco: N/D")
        self.MobVelMov = QtWidgets.QLabel("Vel. Movimento: N/D")
        self.MobHPAggro = QtWidgets.QLabel("Perc. HP Aggro: N/D")
        self.MobRagAggro = QtWidgets.QLabel("Raggio Aggro: N/D")
        self.MobMultAtt = QtWidgets.QLabel("Molt. Danno: N/D")
        self.MobMPSteal = QtWidgets.QLabel("MP Rubati: N/D")

        self.MobSpace1 = QtWidgets.QLabel(" ")
        self.MobSpace2 = QtWidgets.QLabel(" ")
        self.MobSpace3 = QtWidgets.QLabel(" ")
        self.MobSpace4 = QtWidgets.QLabel(" ")
        self.MobSpace5 = QtWidgets.QLabel(" ")
        self.MobSpace6 = QtWidgets.QLabel(" ")
        self.MobSpace7 = QtWidgets.QLabel(" ")
        self.MobSpace8 = QtWidgets.QLabel(" ")

        self.flag_box0 = QtWidgets.QHBoxLayout()
        self.flag_box1 = QtWidgets.QHBoxLayout()
        self.flag_box2 = QtWidgets.QHBoxLayout()
        self.flag_box3 = QtWidgets.QHBoxLayout()
        self.flag_box4 = QtWidgets.QHBoxLayout()
        self.flag_box5 = QtWidgets.QHBoxLayout()
        self.flag_box6 = QtWidgets.QHBoxLayout()
        self.flag_box7 = QtWidgets.QHBoxLayout()

        self.flag_Box = QtWidgets.QVBoxLayout()

        self.flag_box0.addWidget(self.MobFlagWikiLab)
        self.flag_box0.addWidget(self.MobFlagWiki)
        self.flag_box0.addWidget(self.MobSpace1)
        self.flag_box0.addWidget(self.MobSpace2)
        
        self.flag_box1.addWidget(self.MobFlagAILab)
        self.flag_box1.addWidget(self.MobFlagAI)
        self.flag_box1.addWidget(self.MobSpace3)
        self.flag_box1.addWidget(self.MobSpace4)

        self.flag_box2.addWidget(self.MobFlagRazzaLab)
        self.flag_box2.addWidget(self.MobFlagRazza)
        self.flag_box2.addWidget(self.MobSpace5)
        self.flag_box2.addWidget(self.MobSpace6)

        self.flag_box3.addWidget(self.MobFlagImmLab)
        self.flag_box3.addWidget(self.MobFlagImm)
        self.flag_box3.addWidget(self.MobSpace7)
        self.flag_box3.addWidget(self.MobSpace8)

        self.flag_box4.addWidget(self.MobSTR)
        self.flag_box4.addWidget(self.MobDEX)
        self.flag_box4.addWidget(self.MobVIT)
        self.flag_box4.addWidget(self.MobINT)

        self.flag_box5.addWidget(self.MobSungMaSTR)
        self.flag_box5.addWidget(self.MobSungMaDEX)
        self.flag_box5.addWidget(self.MobSungMaVIT)
        self.flag_box5.addWidget(self.MobSungMaINT)

        self.flag_box6.addWidget(self.MobDam)
        self.flag_box6.addWidget(self.MobMultAtt)
        self.flag_box6.addWidget(self.MobVelAtt)
        self.flag_box6.addWidget(self.MobVelMov)
        
        self.flag_box7.addWidget(self.MobRangeATT)
        self.flag_box7.addWidget(self.MobHPAggro)
        self.flag_box7.addWidget(self.MobRagAggro)
        self.flag_box7.addWidget(self.MobMPSteal)

        self.flag_Box.addLayout(self.flag_box0)
        self.flag_Box.addLayout(self.flag_box1)
        self.flag_Box.addLayout(self.flag_box2)
        self.flag_Box.addLayout(self.flag_box3)
        self.flag_Box.addLayout(self.flag_box4)
        self.flag_Box.addLayout(self.flag_box5)
        self.flag_Box.addLayout(self.flag_box6)
        self.flag_Box.addLayout(self.flag_box7)

    def set_flag_data(self, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            mob = proto.mob_data.mob_data_vnum[vnum]
        else:
            mob = proto.mob_data.mob_data_vnum_en[vnum]
        self.MobFlagWiki.setText(proto.get_wiki_mob_flag(vnum))
        self.MobFlagAI.setText(str(proto.get_mob_ai_flag(int(mob['AIFlags']))[1]))
        self.MobFlagRazza.setText(str(proto.get_mob_race_flag(int(mob['RaceFlag']))[1]))
        self.MobFlagImm.setText(str(proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[1]))
        self.MobSTR.setText("STR: " + str(mob['Str']))
        self.MobDEX.setText("DEX: " + str(mob['Dex']))
        self.MobVIT.setText("VIT: " + str(mob['Con']))
        self.MobINT.setText("INT: " + str(mob['Int']))
        self.MobSungMaSTR.setText("SungMa STR: " + str(mob['SungMaStr']))
        self.MobSungMaDEX.setText("SungMa RES: " + str(mob['SungMaDex']))
        self.MobSungMaVIT.setText("SungMa VIT: " + str(mob['SungMaCon']))
        self.MobSungMaINT.setText("SungMa INT: " + str(mob['SungMaInt']))
        self.MobDam.setText("Danno Mostro: " + str(mob['DamageMin']) + " - " + str(mob['DamageMax']))
        self.MobVelAtt.setText("Vel. Attacco: " + str(mob['AttackSpeed']))
        self.MobVelMov.setText("Vel. Movimento: " + str(mob['MovingSpeed']))
        self.MobHPAggro.setText("Perc. HP Aggro: " + str(mob['AggressiveHPPct']))
        self.MobRagAggro.setText("Raggio Aggro: " + str(mob['AggressiveSight']))
        self.MobRangeATT.setText("Range Mostro: " + str(mob['AttackRange']))
        self.MobMultAtt.setText("Molt. Danno: " + str(mob['DamMultiply']))
        self.MobMPSteal.setText("MP Rubati: " + str(mob['DrainSP']))

        self.set_tooltip(vnum)
        
    def set_flag_no_data(self):
        self.MobFlagWiki.setText("N/D")
        self.MobFlagAI.setText("N/D")
        self.MobFlagRazza.setText("N/D")
        self.MobFlagImm.setText("N/D")
        self.MobSTR.setText("STR: N/D")
        self.MobDEX.setText("DEX: N/D")
        self.MobVIT.setText("VIT: N/D")
        self.MobINT.setText("INT: N/D")
        self.MobSungMaSTR.setText("SungMa STR: N/D")
        self.MobSungMaDEX.setText("SungMa RES: N/D")
        self.MobSungMaVIT.setText("SungMa VIT: N/D")
        self.MobSungMaINT.setText("SungMa INT: N/D")
        self.MobDam.setText("Danno Mostro: N/D")
        self.MobVelAtt.setText("Vel. Attacco: N/D")
        self.MobVelMov.setText("Vel. Movimento: N/D")
        self.MobHPAggro.setText("Perc. HP Aggro: N/D")
        self.MobRagAggro.setText("Raggio Aggro: N/D")
        self.MobRangeATT.setText("Range Mostro: N/D")
        self.MobMultAtt.setText("Molt. Danno: N/D")
        self.MobMPSteal.setText("MP Rubati: N/D")
        self.set_tooltip(False)

    def set_tooltip(self, vnum):
        self.MobFlagWikiLab.setToolTip("Flag da mettere nella wiki nel parametro Interazioni.")
        self.MobFlagWiki.setToolTip("Flag da mettere nella wiki nel parametro Interazioni.")
        self.MobSTR.setToolTip("Statistica di STR del mostro.")
        self.MobDEX.setToolTip("Statistica di DEX del mostro.")
        self.MobVIT.setToolTip("Statistica di VIT del mostro.")
        self.MobINT.setToolTip("Statistica di INT del mostro.")
        self.MobSungMaSTR.setToolTip("Statistica di Volontà STR del mostro.")
        self.MobSungMaDEX.setToolTip("Statistica di Volontà RES del mostro.")
        self.MobSungMaVIT.setToolTip("Statistica di Volontà VIT del mostro.")
        self.MobSungMaINT.setToolTip("Statistica di Volontà INT del mostro.")
        self.MobDam.setToolTip("Danno Massimo e Minimo del mostro. Il suo danno minimo e massimo e'\ncalcolato a partire da questo valore.:")
        self.MobVelAtt.setToolTip("Velocita' d'Attacco del mostro.")
        self.MobVelMov.setToolTip("Velocita' di Movimento del mostro.")
        self.MobHPAggro.setToolTip("Percentuale HP sotto la quale il mostro attacchera' chiunque\nnel suo raggio di aggressivita'")
        self.MobRagAggro.setToolTip("Raggio di aggressivita' del mostro.")
        self.MobRangeATT.setToolTip("Range di attacco del mostro.")
        self.MobMultAtt.setToolTip("Moltiplicatore del Danno del mostro.")
        self.MobMPSteal.setToolTip("Quantita' di MP rubati dal mostro ad ogni suo attacco base.")
        
        if (vnum == False):
            self.MobFlagAILab.setToolTip("Flag AI del mostro. Indica il comportamento del mostro rispetto al giocatore e agli altri mostro.")
            self.MobFlagAI.setToolTip("Flag AI del mostro. Indica il comportamento del mostro rispetto al giocatore e agli altri mostro.")
            self.MobFlagRazzaLab.setToolTip("Flag Razza del mostro. Indica la sua razza e il tipo di elemento ad esso associato.")
            self.MobFlagRazza.setToolTip("Flag Razza del mostro. Indica la sua razza e il tipo di elemento ad esso associato.")
            self.MobFlagImmLab.setToolTip("Flag Immunita' del mostro. Indica le resistenza all'attivazione degli status alterati.")
            self.MobFlagImm.setToolTip("Flag Immunita' del mostro. Indica le resistenza all'attivazione degli status alterati.")
        else:
            if (proto.gestore_opzioni.get_option("Platform") == 0):
                mob = proto.mob_data.mob_data_vnum[vnum]
            else:
                mob = proto.mob_data.mob_data_vnum_en[vnum]
            self.MobFlagAILab.setToolTip("Flag AI del mostro. Indica il comportamento del mostro rispetto al giocatore e agli altri mostro.\nValore Originale: " + str(proto.get_mob_ai_flag(int(mob['AIFlags']))[0]))
            self.MobFlagAI.setToolTip("Flag AI del mostro. Indica il comportamento del mostro rispetto al giocatore e agli altri mostro.\nValore Originale: " + str(proto.get_mob_ai_flag(int(mob['AIFlags']))[0]))
            self.MobFlagRazzaLab.setToolTip("Flag Razza del mostro. Indica la sua razza e il tipo di elemento ad esso associato.\nValore Originale: " + str(proto.get_mob_race_flag(int(mob['RaceFlag']))[0]))
            self.MobFlagRazza.setToolTip("Flag Razza del mostro. Indica la sua razza e il tipo di elemento ad esso associato.\nValore Originale: " + str(proto.get_mob_race_flag(int(mob['RaceFlag']))[0]))
            self.MobFlagImmLab.setToolTip("Flag Immunita' del mostro. Indica le resistenza all'attivazione degli status alterati.\nValore Originale: " + str(proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[0]))
            self.MobFlagImm.setToolTip("Flag Immunita' del mostro. Indica le resistenza all'attivazione degli status alterati.\nValore Originale: " + str(proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[0]))

class skill_mob_box():
    
    def __init__(self):
        self.MobPosMal = QtWidgets.QLabel("Poss. Maledire: N/D")
        self.MobPosRal = QtWidgets.QLabel("Poss. Rallentare: N/D")
        self.MobPosVel = QtWidgets.QLabel("Poss. Veleno: N/D")
        self.MobPosStun = QtWidgets.QLabel("Poss. Stun: N/D")
        
        self.MobPosCrit = QtWidgets.QLabel("Poss. Critico: N/D")
        self.MobPosPerf = QtWidgets.QLabel("Poss. Trafiggente: N/D")
        self.MobResSword = QtWidgets.QLabel("Res. Spada: N/D")
        self.MobRes2HSword = QtWidgets.QLabel("Res. Spadone: N/D")

        self.MobResDagger = QtWidgets.QLabel("Res. Pugnale: N/D")
        self.MobResBell = QtWidgets.QLabel("Res. Campana: N/D")
        self.MobResFan = QtWidgets.QLabel("Res. Ventaglio: N/D")
        self.MobResBow = QtWidgets.QLabel("Res. Arco: N/D")

        self.MobResClaw = QtWidgets.QLabel("Res. Artiglio: N/D")
        self.MobResFuoco = QtWidgets.QLabel("Res. Fuoco: N/D")
        self.MobResLampo = QtWidgets.QLabel("Res. Lampo: N/D")
        self.MobResMagia = QtWidgets.QLabel("Res. Magia: N/D")

        self.MobResVento = QtWidgets.QLabel("Res. Vento: N/D")
        self.MobResVeleno = QtWidgets.QLabel("Res. Veleno: N/D")
        self.MobResSang = QtWidgets.QLabel("Res. Sanguinamento: N/D")
        self.MobResFist = QtWidgets.QLabel("Res. Pugni: N/D")

        self.MobResGhiaccio = QtWidgets.QLabel("Res. Ghiaccio: N/D")
        self.MobResTerra = QtWidgets.QLabel("Res. Terra: N/D")
        self.MobResOsc = QtWidgets.QLabel("Res. Oscurita': N/D")
        self.MobElem = QtWidgets.QLabel("Elemento : N/D")


        self.skill_mob_box0 = QtWidgets.QHBoxLayout()
        self.skill_mob_box1 = QtWidgets.QHBoxLayout()
        self.skill_mob_box2 = QtWidgets.QHBoxLayout()
        self.skill_mob_box3 = QtWidgets.QHBoxLayout()
        self.skill_mob_box4 = QtWidgets.QHBoxLayout()
        self.skill_mob_box5 = QtWidgets.QHBoxLayout()
        
        self.skil_Box = QtWidgets.QVBoxLayout()

        self.skill_mob_box0.addWidget(self.MobPosMal)
        self.skill_mob_box0.addWidget(self.MobPosRal)
        self.skill_mob_box0.addWidget(self.MobPosVel)
        self.skill_mob_box0.addWidget(self.MobPosStun)

        self.skill_mob_box1.addWidget(self.MobPosCrit)
        self.skill_mob_box1.addWidget(self.MobPosPerf)
        self.skill_mob_box1.addWidget(self.MobResSword)
        self.skill_mob_box1.addWidget(self.MobRes2HSword)

        self.skill_mob_box2.addWidget(self.MobResDagger)
        self.skill_mob_box2.addWidget(self.MobResBell)
        self.skill_mob_box2.addWidget(self.MobResFan)
        self.skill_mob_box2.addWidget(self.MobResBow)

        self.skill_mob_box3.addWidget(self.MobResClaw)
        self.skill_mob_box3.addWidget(self.MobResFist)
        self.skill_mob_box3.addWidget(self.MobResVeleno)
        self.skill_mob_box3.addWidget(self.MobResSang)
        
        self.skill_mob_box4.addWidget(self.MobResMagia)
        self.skill_mob_box4.addWidget(self.MobResFuoco)
        self.skill_mob_box4.addWidget(self.MobResLampo)
        self.skill_mob_box4.addWidget(self.MobResVento)
        
        self.skill_mob_box5.addWidget(self.MobResGhiaccio)
        self.skill_mob_box5.addWidget(self.MobResOsc)
        self.skill_mob_box5.addWidget(self.MobResTerra)
        self.skill_mob_box5.addWidget(self.MobElem)        

        self.skil_Box.addLayout(self.skill_mob_box0)
        self.skil_Box.addLayout(self.skill_mob_box1)
        self.skil_Box.addLayout(self.skill_mob_box2)
        self.skil_Box.addLayout(self.skill_mob_box3)
        self.skil_Box.addLayout(self.skill_mob_box4)
        self.skil_Box.addLayout(self.skill_mob_box5)
        
        self.set_tooltip()

    def set_skill_mob_data(self, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            mob = proto.mob_data.mob_data_vnum[vnum]
        else:
            mob = proto.mob_data.mob_data_vnum_en[vnum]
        self.MobPosMal.setText("Poss. Maledire: " + str(mob['EnchantCurse']) + "%")
        self.MobPosRal.setText("Poss. Rallentare: " +str(mob['EnchantSlow']) + "%")
        self.MobPosVel.setText("Poss. Veleno: " + str(mob['EnchantPoison']) + "%")
        self.MobPosStun.setText("Poss. Stun: " + str(mob['EnchantStun']) + "%")
        self.MobPosCrit.setText("Poss. Critico: " + str(mob['EnchantCritical']) + "%")
        self.MobPosPerf.setText("Poss. Trafiggente: " + str(mob['EnchantPenetrate']) + "%")
        self.MobResSword.setText("Res. Spada: " + str(mob['ResistSword']) + "%")
        self.MobRes2HSword.setText("Res. Spadone: " + str(mob['ResistTwohand']) + "%")
        self.MobResDagger.setText("Res. Pugnale:" + str(mob['ResistDagger']) + "%")
        self.MobResBell.setText("Res. Campana:" + str(mob['ResistBell']) + "%")
        self.MobResFan.setText("Res. Ventaglio: " + str(mob['ResistFan']) + "%")
        self.MobResBow.setText("Res. Arco:" + str(mob['ResistBow']) + "%")
        self.MobResClaw.setText("Res. Artiglio:" + str(mob['ResistClaw']) + "%")
        self.MobResFuoco.setText("Res. Fuoco:" + str(mob['ResistFire']) + "%")
        self.MobResLampo.setText("Res. Lampo:" + str(mob['ResistElect']) + "%")
        self.MobResMagia.setText("Res. Magia:" + str(mob['ResistMagic']) + "%")
        self.MobResVento.setText("Res. Vento:" + str(mob['ResistWind']) + "%")
        self.MobResVeleno.setText("Res. Veleno:" + str(mob['ResistPoison']) + "%")
        self.MobResSang.setText("Res. Sanguinamento:" + str(mob['ResistBleeding']) + "%")
        self.MobResFist.setText("Res. Pugni: " + mob['ResistFist'] + "%")
        self.MobResGhiaccio.setText("Res. Ghiaccio: " + mob['ResistIce'] + "%")
        self.MobResTerra.setText("Res. Terra: " + mob['ResistEarth'] + "%")
        self.MobResOsc.setText("Res. Oscurita': " + mob['ResistDark'] + "%")
        self.MobElem.setText("% Att. Elem.: " + proto.get_mob_att_element(vnum) + "%")

    def set_skill_mob_no_data(self):
        self.MobPosMal.setText("Poss. Maledire: N/D")
        self.MobPosRal.setText("Poss. Rallentare: N/D")
        self.MobPosVel.setText("Poss. Veleno: N/D")
        self.MobPosStun.setText("Poss. Stun: N/D")
        self.MobPosCrit.setText("Poss. Critico: N/D")
        self.MobPosPerf.setText("Poss. Trafiggente: N/D")
        self.MobResSword.setText("Res. Spada: N/D")
        self.MobRes2HSword.setText("Res. Spadone: N/D")
        self.MobResDagger.setText("Res. Pugnale: N/D")
        self.MobResBell.setText("Res. Campana: N/D")
        self.MobResFan.setText("Res. Ventaglio: N/D")
        self.MobResBow.setText("Res. Arco: N/D")
        self.MobResClaw.setText("Res. Artiglio: N/D")
        self.MobResFuoco.setText("Res. Fuoco: N/D")
        self.MobResLampo.setText("Res. Lampo: N/D")
        self.MobResMagia.setText("Res. Magia: N/D")
        self.MobResVento.setText("Res. Vento: N/D")
        self.MobResVeleno.setText("Res. Veleno: N/D")
        self.MobResSang.setText("Res. Sanguinamento: N/D")
        self.MobResFist.setText("Res. Pugni: N/D")
        self.MobResGhiaccio.setText("Res. Ghiaccio: N/D" )
        self.MobResTerra.setText("Res. Terra: N/D")
        self.MobResOsc.setText("Res. Oscurita': N/D")
        self.MobElem.setText("Elemento: N/D")

    def set_tooltip(self):
        self.MobPosMal.setToolTip("Possibilita' del mostro di infliggere lo status Maledizione")
        self.MobPosRal.setToolTip("Possibilita' del mostro di infliggere lo status Rallentamento")
        self.MobPosVel.setToolTip("Possibilita' del mostro di infliggere lo status Avvelenamento")
        self.MobPosStun.setToolTip("Possibilita' del mostro di infliggere lo status Stordimento")
        self.MobPosCrit.setToolTip("Possibilita' del mostro di infliggere un colpo critico")
        self.MobPosPerf.setToolTip("Possibilita' del mostro di infliggere un colpo trafiggente")
        self.MobResSword.setToolTip("Resistenza del mostro agli attacchi con la spada.")
        self.MobRes2HSword.setToolTip("Resistenza del mostro agli attacchi con lo spadone.")
        self.MobResDagger.setToolTip("Resistenza del mostro agli attacchi con i pugnali.")
        self.MobResBell.setToolTip("Resistenza  del mostro agli attacchi con la campana.")
        self.MobResFan.setToolTip("Resistenza  del mostro agli attacchi con il ventaglio.")
        self.MobResBow.setToolTip("Resistenza  del mostro agli attacchi con l'arco.")
        self.MobResClaw.setToolTip("Resistenza  del mostro agli attacchi con gli artigli.")
        self.MobResFuoco.setToolTip("Resistenza del mostro agli attacchi di elemento fuoco.")
        self.MobResLampo.setToolTip("Resistenza del mostro agli attacchi di elemento lampo.")
        self.MobResMagia.setToolTip("Resistenza del mostro agli attacchi magici.")
        self.MobResVento.setToolTip("Resistenza del mostro agli attacchi di elemento vento.")
        self.MobResVeleno.setToolTip("Resistenza del mostro al danno del veleno.\n Il danno del veleno verra' ridotto dal valore standard.")
        self.MobResSang.setToolTip("Resistenza del mostro al danno del sanguinamento.\nIl danno del sanguinamento verra' ridotto dal valore standard.")
        self.MobResFist.setToolTip("Resistenza del mostro agli attacchi con i pugni.")
        self.MobResGhiaccio.setToolTip("Resistenza del mostro agli attacchi di elemento ghiaccio.")
        self.MobResTerra.setToolTip("Resistenza del mostro agli attacchi di elemento terra.")
        self.MobResOsc.setToolTip("Resistenza del mostro agli attacchi di elemento oscurita'.")
        self.MobElem.setText("Elemento del mostro.")
                                  
class other_mob_box():
    
    def __init__(self):
        self.MobVnumRespawn = QtWidgets.QLabel("Mob in cui Respawna: N/D")
        self.MobVnumSpawn = QtWidgets.QLabel("Mob Evocato: N/D")
        self.MobFolder = QtWidgets.QLabel("Cartella File Mob: N/D")
        self.MobColour = QtWidgets.QLabel("Colore Mostro: N/D")
        self.MobItemDrop = QtWidgets.QLabel("Item Droppato: N/D")
        self.MobPolyItem = QtWidgets.QLabel("Sfera Droppata: N/D")
        self.MobMount = QtWidgets.QLabel("Capacita' Mount: N/D")
        self.MobTypeOnClick = QtWidgets.QLabel("Tipo On Click: N/D")
        self.MobRegno = QtWidgets.QLabel("Regno: N/D")
        self.MobMobCurato = QtWidgets.QLabel("Mob Curato: N/D")
        self.MobHitRange = QtWidgets.QLabel("Range Colpo: N/D")
        self.MobPtBerserk = QtWidgets.QLabel("Punti Berserk: N/D")
        self.MobPtStoneSkin = QtWidgets.QLabel("Punti StoneSkin: N/D")
        self.MobPtGodSpeed = QtWidgets.QLabel("Punti GodSpeed: N/D")
        self.MobPtDeathBlow = QtWidgets.QLabel("Punti DeathBlow: N/D")
        self.MobPtRevive = QtWidgets.QLabel("Punti Revive: N/D")

        self.other_box0 = QtWidgets.QHBoxLayout()
        self.other_box1 = QtWidgets.QHBoxLayout()
        self.other_box2 = QtWidgets.QHBoxLayout()
        self.other_box3 = QtWidgets.QHBoxLayout()
        self.other_box4 = QtWidgets.QHBoxLayout()
        
        self.other_Box = QtWidgets.QVBoxLayout()

        self.other_box0.addWidget(self.MobVnumRespawn)
        self.other_box0.addWidget(self.MobVnumSpawn)
        self.other_box0.addWidget(self.MobFolder)
        self.other_box0.addWidget(self.MobColour)

        self.other_box1.addWidget(self.MobItemDrop)
        self.other_box1.addWidget(self.MobPolyItem)
        self.other_box1.addWidget(self.MobMount)
        self.other_box1.addWidget(self.MobTypeOnClick)

        self.other_box2.addWidget(self.MobRegno)
        self.other_box2.addWidget(self.MobMobCurato)
        self.other_box2.addWidget(self.MobHitRange)
        self.other_box2.addWidget(self.MobPtBerserk)

        self.other_box3.addWidget(self.MobPtStoneSkin)
        self.other_box3.addWidget(self.MobPtGodSpeed)
        self.other_box3.addWidget(self.MobPtDeathBlow)
        self.other_box3.addWidget(self.MobPtRevive)

        self.other_Box.addLayout(self.other_box0)
        self.other_Box.addLayout(self.other_box1)
        self.other_Box.addLayout(self.other_box2)
        self.other_Box.addLayout(self.other_box3)
        self.other_Box.addLayout(self.other_box4)

        self.set_tooltip(False)

    def set_other_mob_data(self, vnum):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            mob = proto.mob_data.mob_data_vnum[vnum]
        else:
            mob = proto.mob_data.mob_data_vnum_en[vnum]
        self.MobVnumRespawn.setText("Mob in cui Respawna: " + str(mob['ResurrectionVnum']))
        self.MobVnumSpawn.setText("Mob Evocato: " + str(mob['SummonVnum']))
        self.MobFolder.setText("Cartella File Mob: " + str(mob['Folder']))
        self.MobColour.setText("Colore Mostro: " + str(mob['MonsterColor']))
        self.MobItemDrop.setText("Item Droppato: " + str(mob['DropItemVnum']))
        self.MobPolyItem.setText("Sfera Droppata: " + str(mob['PolymorphItemVnum']))
        self.MobMount.setText("Capacita' Mount: " + str(mob['MountCapacity']))
        self.MobTypeOnClick.setText("Tipo On Click: " + str(proto.get_mob_type_on_click(mob['OnClickType'])[1]))
        self.MobRegno.setText("Regno: " + mob['Empire'] + " (" + proto.get_regno(mob['Empire'])[1] + ")")
        self.MobHitRange.setText("Range Colpo: "+ str(mob['HitRange']))
        self.MobPtBerserk.setText("Punti Berserk: "+ str(mob['BerserkPoint']))
        self.MobPtStoneSkin.setText("Punti StoneSkin: "+ str(mob['StoneSkinPoint']))
        self.MobPtGodSpeed.setText("Punti GodSpeed: "+ str(mob['GodSpeedPoint']))
        self.MobPtDeathBlow.setText("Punti DeathBlow: "+ str(mob['DeathBlowPoint']))
        self.MobPtRevive.setText("Punti Revive: "+ str(mob['RevivePoint']))
        self.set_tooltip(vnum)
    
    def set_other_mob_no_data(self):
        self.MobVnumRespawn.setText("Mob in cui Respawna: N/D")
        self.MobVnumSpawn.setText("Mob Evocato: N/D")
        self.MobFolder.setText("Cartella File Mob: N/D")
        self.MobColour.setText("Colore Mostro: N/D")
        self.MobItemDrop.setText("Item Droppato: N/D")
        self.MobPolyItem.setText("Sfera Droppata: N/D")
        self.MobMount.setText("Capacita' Mount: N/D")
        self.MobTypeOnClick.setText("Tipo On Click: N/D")
        self.MobRegno.setText("Regno: N/D")
        self.MobMobCurato.setText("Mob Curato: N/D")
        self.MobHitRange.setText("Range Colpo: N/D")
        self.MobPtBerserk.setText("Punti Berserk: N/D")
        self.MobPtStoneSkin.setText("Punti StoneSkin: N/D")
        self.MobPtGodSpeed.setText("Punti GodSpeed: N/D")
        self.MobPtDeathBlow.setText("Punti DeathBlow: N/D")
        self.MobPtRevive.setText("Punti Revive: N/D")
        self.set_tooltip(False)

    def set_tooltip(self, vnum):
        self.MobFolder.setToolTip("Nome della cartella del client contenente i file del mostro.")
        self.MobColour.setToolTip("Colore del Mostro che sara' applicato dopo la renderizzazione delle sue texture.")
        self.MobPolyItem.setToolTip("Vnum sfera trasformazione droppata dal mostro alla sua morte.")
        self.MobMount.setToolTip("Capacita' del mostro di essere cavalcato.")
        self.MobRegno.setToolTip("Regno del mostro.")
        self.MobMobCurato.setToolTip("Vnum bersaglio che viene curato da questo mostro.")
        self.MobHitRange.setToolTip("Range aggiuntivo ai colpi e abilita' del mostro.")
        self.MobPtBerserk.setToolTip("Punti Berserk del mostro.")
        self.MobPtStoneSkin.setToolTip("Punti StoneSkin del mostro. Quando la percentuale degli HP attuali del mostro\ne' inferiore a questo valore allora il mostro subira' meta' del danno.")
        self.MobPtGodSpeed.setToolTip("Punti GodSpeed del mostro. Quando la percentuale degli HP attuali del mostro\ne' inferiore a questo valore, la velocita' d'attacco del mostro aumenta considerevolmente\nconsentendo al mostro di infliggere danni prima di raggiungere il personaggio.")
        self.MobPtDeathBlow.setToolTip("Punti DeathBlow del mostro. Il mostro ha una probabilita' (circa il 25%) che il colpo\ninfligga quattro volte il danno normale.")
        self.MobPtRevive.setToolTip("Punti Revive del mostro. Consentono al mostro di essere rianimato dopo la morte se vi\ne' nel suo gruppo un mostro con il potere di rianimare.")

        if (vnum == False):
            self.MobVnumRespawn.setToolTip("Vnum del mostro in cui respawna dopo essere stato ucciso.")
            self.MobVnumSpawn.setToolTip("Vnum del mostro che viene spawnato (massimo 3).")
            self.MobItemDrop.setToolTip("Vnum dell'item droppato quando il mostro viene ucciso.")
            self.MobTypeOnClick.setToolTip("Tipo di comportamento speciale quando si clicca con\nil tasto sinistro del mouse sul mostro.")
        else:
            if (proto.gestore_opzioni.get_option("Platform") == 0):
                mob = proto.mob_data.mob_data_vnum[vnum]
            else:
                mob = proto.mob_data.mob_data_vnum_en[vnum]
            self.MobVnumRespawn.setToolTip("Vnum del mostro in cui respawna dopo essere stato ucciso.\nIl Vnum corrisponde a " + QtMetin2.get_mob_name(mob['ResurrectionVnum']))
            self.MobVnumSpawn.setToolTip("Vnum del mostro che viene spawnato (massimo 3).\nIl Vnum corrisponde a " + QtMetin2.get_mob_name(mob['SummonVnum']))
            self.MobItemDrop.setToolTip("Vnum dell'item droppato quando il mostro viene ucciso.\nIl Vnum corrisponde a " + proto.get_item_name(mob['DropItemVnum']))
            self.MobTypeOnClick.setToolTip("Tipo di comportamento speciale quando si clicca con\nil tasto sinistro del mouse sul mostro.\nValore Originale: " + str(proto.get_mob_type_on_click(mob['OnClickType'])[0]))            
 

class item_icon():
    
    def __init__(self):
        self.icon = QtWidgets.QLabel("")

    def set_icon(self, vnum):
        self.icon.show()
        cur_dir = proto.cur_dir
        icon = QtMetin2.download_icon(vnum)
        if (icon == ""):
            self.icon.hide()
        else:
            self.icon.setPixmap(QtGui.QPixmap(cur_dir + "\\images\\" + icon + ".png").scaled(32, 96, QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))

    def setToolTip(self, stringa):
        self.icon.setToolTip(stringa)

    def hide(self):
        self.icon.hide()

    def show(self):
        self.icon.show()

class item_up_box():
    
    def __init__(self):
        self.ItemIcon1 = item_icon()
        self.ItemIcon2 = item_icon()
        self.ItemIcon3 = item_icon()

        self.Item1 = QtWidgets.QLabel("")
        self.Item2 = QtWidgets.QLabel("")
        self.Item3 = QtWidgets.QLabel("")

        self.YangLab = QtWidgets.QLabel("Yang Richiesti")
        self.Yang = QtWidgets.QLabel("")

        self.ItemIcon1.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemIcon2.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemIcon3.icon.setAlignment(QtCore.Qt.AlignCenter)

        self.upvbox1 = QtWidgets.QVBoxLayout()
        self.upvbox2 = QtWidgets.QVBoxLayout()
        self.upvbox3 = QtWidgets.QVBoxLayout()
        self.upvbox4 = QtWidgets.QVBoxLayout()
        self.UpBox = QtWidgets.QHBoxLayout()

        self.upvbox1.addWidget(self.ItemIcon1.icon)
        self.upvbox1.addWidget(self.Item1)

        self.upvbox2.addWidget(self.ItemIcon2.icon)
        self.upvbox2.addWidget(self.Item2)

        self.upvbox3.addWidget(self.ItemIcon3.icon)
        self.upvbox3.addWidget(self.Item3)

        self.upvbox4.addWidget(self.YangLab)
        self.upvbox4.addWidget(self.Yang)

        self.UpBox.addLayout(self.upvbox1)
        self.UpBox.addLayout(self.upvbox2)
        self.UpBox.addLayout(self.upvbox3)
        self.UpBox.addLayout(self.upvbox4)

    def set_up(self, item):
        self.ItemIcon1.show()
        self.ItemIcon2.show()
        self.ItemIcon3.show()
        self.Item1.show()
        self.Item2.show()
        self.Item3.show()
        if (not str(item[0][0]).isdigit()):
            self.ItemIcon1.hide()
            self.Item1.setText(str(item[0][1]) + " x " + str(item[0][0]))
        elif (item[0][0] == 0):
            self.ItemIcon1.hide()
            self.Item1.hide()
        else:
            self.ItemIcon1.set_icon(str(item[0][0]))
            self.Item1.setText(str(item[0][1]) + " x " + proto.get_item_name(str(item[0][0])))
        if (not str(item[1][0]).isdigit()):
            self.ItemIcon2.hide()
            self.Item2.setText(str(item[1][1]) + " x " + str(item[1][0]))
        elif (item[1][0] == 0):
            self.ItemIcon2.hide()
            self.Item2.hide()
        else:
            self.ItemIcon2.set_icon(str(item[1][0]))
            self.Item2.setText(str(item[1][1]) + " x " + proto.get_item_name(str(item[1][0])))
        if (not str(item[2][0]).isdigit()):
            self.ItemIcon3.hide()
            self.Item3.setText(str(item[2][1]) + " x " + str(item[2][0]))
        elif (item[2][0] == 0):
            self.ItemIcon3.hide()
            self.Item3.hide()
        else:
            self.ItemIcon3.set_icon(str(item[2][0]))
            self.Item3.setText(str(item[2][1]) + " x " + proto.get_item_name(str(item[2][0])))
        self.Yang.setText(item[3])
