# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
from metin2Data import *

import metin2Class
import os
import proto
import re
import sys
import urllib
import urllib.request

def widget_item(self):
    ItemWidget = QtWidgets.QWidget()

    self.ItemGrid = QtWidgets.QGridLayout(ItemWidget)

    ItemWidget.setLayout(self.ItemGrid)

    self.ItemGrid.setAlignment(QtCore.Qt.AlignTop)

    global search_item
    global Ibox1
    global Ibox2
    global Ibox3
    global Ibox4

    #Creo gli oggetti
    search_item = metin2Class.search_box(1)

    Ibox1 = metin2Class.pre_flag_item_box()
    Ibox2 = metin2Class.flag_item_box()
    Ibox3 = metin2Class.bonus_item_box()
    Ibox4 = metin2Class.other_item_box()

    self.ItemGrid.addLayout(search_item.SearchBox, 0,0)
    self.ItemGrid.addLayout(Ibox1.pre_flag_Box, 1,0)
    self.ItemGrid.addLayout(Ibox2.flag_Box, 2,0)
    self.ItemGrid.addLayout(Ibox3.bonus_Box, 3,0)
    self.ItemGrid.addLayout(Ibox4.other_Box, 4,0)

    return ItemWidget

def widget_XML_item(self):
    ItemXMLWidget = QtWidgets.QWidget()  

    self.CercaItem = QtWidgets.QLabel("Ricerca per:")
    self.ComboBoxItem = QtWidgets.QComboBox(ItemXMLWidget)
    self.ComboBoxItem.addItem("Tipo")
    self.ComboBoxItem.addItem("Maschera")
    self.ComboBoxItem.addItem("Anti Flag")
    self.ComboBoxItem.addItem("Item Flag")
    self.ComboBoxItem.addItem("Wear Flag")
    self.ComboBoxItem.addItem("Immune Flag")
    self.ComboBoxItem.addItem("Restrizioni")
    self.ComboBoxItem.addItem("Bonus")
    self.ComboBoxItem.addItem("Set di Up")
    self.ComboBoxItem.addItem("Altro")

    self.ComboBoxTipoItem = QtWidgets.QComboBox(ItemXMLWidget)
    self.ComboBoxSottoTipoItem = QtWidgets.QComboBox(ItemXMLWidget)
    self.ButtonSearchItem = QtWidgets.QPushButton("Cerca")
    self.ButtonInterazioni = QtWidgets.QPushButton("Stampa Interazioni")
    self.ButtonItemDoppioni = QtWidgets.QPushButton("Stampa Item Doppioni")
    self.ButtonItemColOrig = QtWidgets.QPushButton("Stampa Dati Originali")
    self.ButtonItemColTrad = QtWidgets.QPushButton("Stampa Dati Tradotti")
    self.ButtonItemOnlyFlag = QtWidgets.QPushButton("Stampa Solo Flag Item")

    self.CercaItem.setAlignment(QtCore.Qt.AlignLeft)
    self.ComboBoxItem.setSizeAdjustPolicy(0)#AdjustToContents
    self.ComboBoxTipoItem.setSizeAdjustPolicy(0)#AdjustToContents
    self.ComboBoxSottoTipoItem.setSizeAdjustPolicy(0)#AdjustToContents
    
    for i in range(0, len(ITEM_TYPE.keys())):
        self.ComboBoxTipoItem.addItem(ITEM_TYPE[i][1])

    for i in range(0, len(ITEM_SUB_TYPE[ITEM_TYPE[self.ComboBoxTipoItem.currentIndex()][0]].keys())):
        self.ComboBoxSottoTipoItem.addItem(ITEM_SUB_TYPE[ITEM_TYPE[self.ComboBoxTipoItem.currentIndex()][0]][i][1])

    self.ButtonSearchItem.clicked.connect(lambda: cerca_item_by_combobox(self))
    self.ComboBoxItem.currentIndexChanged[str].connect(lambda: change_combo_box_item(self))
    self.ComboBoxTipoItem.currentIndexChanged[str].connect(lambda: change_combo_box_tipo_item(self))
    self.ButtonInterazioni.clicked.connect(lambda: stampa_interazioni(self))
    self.ButtonItemDoppioni.clicked.connect(lambda: stampa_item_doppioni(self))
    self.ButtonItemColOrig.clicked.connect(lambda: stampa_item_col_orig(self))
    self.ButtonItemColTrad.clicked.connect(lambda: stampa_item_col_trad(self))
    self.ButtonItemOnlyFlag.clicked.connect(lambda: stampa_item_only_flag(self))

    self.ItemLineEdit = QtWidgets.QTextEdit(ItemXMLWidget)

    self.ItemXMLGrid = QtWidgets.QGridLayout(ItemXMLWidget)

    ItemXMLWidget.setLayout(self.ItemXMLGrid)

    self.ItemXMLGrid.setAlignment(QtCore.Qt.AlignTop)

    self.ItemXMLGrid.addWidget(self.CercaItem, 0, 0)
    self.ItemXMLGrid.addWidget(self.ComboBoxItem, 0, 1)
    self.ItemXMLGrid.addWidget(self.ComboBoxTipoItem, 0, 2)
    self.ItemXMLGrid.addWidget(self.ComboBoxSottoTipoItem, 0, 3)
    self.ItemXMLGrid.addWidget(self.ButtonSearchItem, 0, 4)
    self.ItemXMLGrid.addWidget(self.ItemLineEdit, 1, 0, 1, 5)
    self.ItemXMLGrid.addWidget(self.ButtonInterazioni, 2, 0, 1, 1)
    self.ItemXMLGrid.addWidget(self.ButtonItemDoppioni, 2, 1, 1, 1)
    self.ItemXMLGrid.addWidget(self.ButtonItemColOrig, 2, 2, 1, 1)
    self.ItemXMLGrid.addWidget(self.ButtonItemColTrad, 2, 3, 1, 1)
    self.ItemXMLGrid.addWidget(self.ButtonItemOnlyFlag, 2, 4, 1, 1)

    return ItemXMLWidget

def change_combo_box_item(self):
    IndexTipo = self.ComboBoxItem.currentIndex()
    self.ComboBoxSottoTipoItem.show()

    if (IndexTipo == 0): #Tipo
        self.ComboBoxTipoItem.clear()
        for i in range(0, len(ITEM_TYPE.keys())):
            self.ComboBoxTipoItem.addItem(ITEM_TYPE[i][1])

    elif (IndexTipo == 1): #Maschera
        self.ComboBoxTipoItem.clear()
        for i in range(0, len(ITEM_MASK_TYPE.keys())):
            self.ComboBoxTipoItem.addItem(ITEM_MASK_TYPE[i][1])

    elif (IndexTipo == 2): #Anti Flag
        self.ComboBoxSottoTipoItem.hide()
        self.ComboBoxTipoItem.clear()
        for i in range(0, len(ITEM_ANTI_FLAG)):
            self.ComboBoxTipoItem.addItem(ITEM_ANTI_FLAG[i][1])

    elif (IndexTipo == 3): #Item Flag
        self.ComboBoxSottoTipoItem.hide()
        self.ComboBoxTipoItem.clear()
        for i in range(0, len(ITEM_FLAG)):
            self.ComboBoxTipoItem.addItem(ITEM_FLAG[i][1])

    elif (IndexTipo == 4): #Wear Flag
        self.ComboBoxSottoTipoItem.hide()
        self.ComboBoxTipoItem.clear()
        for i in range(0, len(ITEM_WEAR_FLAG)):
            self.ComboBoxTipoItem.addItem(ITEM_WEAR_FLAG[i][1])

    elif (IndexTipo == 5): #Immune Flag
        self.ComboBoxSottoTipoItem.hide()
        self.ComboBoxTipoItem.clear()
        for i in range(0, len(ITEM_IMMUNE_FLAG)):
            self.ComboBoxTipoItem.addItem(ITEM_IMMUNE_FLAG[i][1])

    elif (IndexTipo == 6): #Restrizione
        self.ComboBoxSottoTipoItem.hide()
        self.ComboBoxTipoItem.clear()
        for i in range(0, len(ITEM_LIMIT_TYPE)):
            self.ComboBoxTipoItem.addItem(ITEM_LIMIT_TYPE[i][1])

    elif (IndexTipo == 7): #Bonus
        self.ComboBoxSottoTipoItem.hide()
        self.ComboBoxTipoItem.clear()
        for i in range(0, len(ITEM_APPLY_TYPE)):
            self.ComboBoxTipoItem.addItem(ITEM_APPLY_TYPE[i][1])

    elif (IndexTipo == 8): #Set Up
        self.ComboBoxSottoTipoItem.hide()
        self.ComboBoxTipoItem.clear()
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            file = proto.item_data.item_set_up
        else:
            file = proto.item_data.item_set_up_en
        for elem in sorted(int(x) for x in file):
            self.ComboBoxTipoItem.addItem(str(elem))  

    elif (IndexTipo == 9): #Altro
        self.ComboBoxTipoItem.clear()
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            key = list(proto.item_data.item_data_vnum["101"].keys())
        else:
            key = list(proto.item_data.item_data_vnum_en["101"].keys())
        key.remove("name")          #Nome
        key.remove("vnum")          #Vnum
        key.remove("Type")          #Tipo
        key.remove("SubType")       #SottoTipo
        key.remove("TypeMask")      #Tipo Maschera
        key.remove("SubTypeMask")   #Sotto Tipo Maschera
        key.remove("AntiFlags")     #AntiFlag
        key.remove("Flags")         #Flag
        key.remove("WearFlags")     #Wear Flag
        key.remove("ImmuneFlags")   #ImmuneFlag
        key.remove("LimitType0")    #Restrizione 0
        key.remove("LimitValue0")   #Valore Limite 0
        key.remove("LimitType1")    #Restrizione 1
        key.remove("LimitValue1")   #Valore Limite 1
        key.remove("ApplyType0")    #Bonus 0
        key.remove("ApplyValue0")   #Valore Bonus 0
        key.remove("ApplyType1")    #Bonus 1
        key.remove("ApplyValue1")   #Valore Bonus 1
        key.remove("ApplyType2")    #Bonus 2
        key.remove("ApplyValue2")   #Valore Bonus 2
        key.remove("ApplyType3")    #Bonus 2
        key.remove("ApplyValue3")   #Valore Bonus 2
        key.remove("RefineSet")     #Set Up
        
        for elem in sorted(key):
          self.ComboBoxTipoItem.addItem(elem)  
            
    else:                   #Errore
        pass

def change_combo_box_tipo_item(self):
    IndexTipo = self.ComboBoxItem.currentIndex()
    IndexSottoTipo = self.ComboBoxTipoItem.currentIndex()
    if (IndexSottoTipo == -1):
        return

    if (IndexTipo == 0): #Tipo
        IndexSottoTipo = ITEM_TYPE[IndexSottoTipo][0]
        self.ComboBoxSottoTipoItem.clear()
        for i in sorted(ITEM_SUB_TYPE[IndexSottoTipo].keys()):
            self.ComboBoxSottoTipoItem.addItem(ITEM_SUB_TYPE[IndexSottoTipo][i][1])
            
    elif (IndexTipo == 1): #Maschera
        IndexSottoTipo = ITEM_MASK_TYPE[IndexSottoTipo][0]
        self.ComboBoxSottoTipoItem.clear()
        for i in sorted(ITEM_SUB_MASK_TYPE[IndexSottoTipo].keys()):
            self.ComboBoxSottoTipoItem.addItem(ITEM_SUB_MASK_TYPE[IndexSottoTipo][i][1])

    if (IndexTipo == 9): #Altro
        self.ComboBoxSottoTipoItem.clear()
        DATA_LIST = get_all_item_info_by_name(self.ComboBoxTipoItem.currentText())
        for i in range(0, len(DATA_LIST)):
            self.ComboBoxSottoTipoItem.addItem(DATA_LIST[i])


def cerca_item_by_combobox(self):
    data = ""
    IndexTipo = self.ComboBoxItem.currentIndex()
    IndexSottoTipo = self.ComboBoxTipoItem.currentText()
    Valore = self.ComboBoxSottoTipoItem.currentText()
    
    data = search_item_data_from_type(str(IndexTipo), str(IndexSottoTipo), str(Valore))
    self.ItemLineEdit.clear()
    self.ItemLineEdit.append(data)
    self.ItemLineEdit.moveCursor(QtGui.QTextCursor.Start)
    self.ItemLineEdit.ensureCursorVisible()


def widget_mob(self):
    MobWidget = QtWidgets.QWidget()

    self.MobGrid = QtWidgets.QGridLayout(MobWidget)

    MobWidget.setLayout(self.MobGrid)

    self.MobGrid.setAlignment(QtCore.Qt.AlignTop)

    global search_mob
    global Mbox1
    global Mbox2
    global Mbox3
    global Mbox4

    #Creo gli oggetti
    search_mob = metin2Class.search_box(2)

    Mbox1 = metin2Class.pre_flag_mob_box()
    Mbox2 = metin2Class.flag_mob_box()
    Mbox3 = metin2Class.skill_mob_box()
    Mbox4 = metin2Class.other_mob_box()

    self.MobGrid.addLayout(search_mob.SearchBox, 0,0)
    self.MobGrid.addLayout(Mbox1.pre_flag_Box, 1,0)
    self.MobGrid.addLayout(Mbox2.flag_Box, 2,0)
    self.MobGrid.addLayout(Mbox3.skil_Box, 3,0)
    self.MobGrid.addLayout(Mbox4.other_Box, 4,0)

    return MobWidget

def widget_XML_mob(self):
    MobXMLWidget = QtWidgets.QWidget()

    CercaMob = QtWidgets.QLabel("Ricerca per:")
    
    self.ComboBoxMob = QtWidgets.QComboBox(MobXMLWidget)
    self.ComboBoxMob.addItem("Tipo")
    self.ComboBoxMob.addItem("Grado")
    self.ComboBoxMob.addItem("Tipo Battaglia")
    self.ComboBoxMob.addItem("Size")
    self.ComboBoxMob.addItem("Ai Flag")
    self.ComboBoxMob.addItem("Race Flag")
    self.ComboBoxMob.addItem("Immune Flag")
    self.ComboBoxMob.addItem("Status Inflitti")
    self.ComboBoxMob.addItem("Altro")

    self.ComboBoxTipoMob = QtWidgets.QComboBox(MobXMLWidget)
    self.ComboBoxSottoTipoMob = QtWidgets.QComboBox(MobXMLWidget)
    ButtonSearchMob = QtWidgets.QPushButton("Cerca")
    ButtonMobInterazioni = QtWidgets.QPushButton("Stampa Interazioni")
    ButtonMobDoppioni = QtWidgets.QPushButton("Stampa Mob Doppioni")
    ButtonMobColOrig = QtWidgets.QPushButton("Stampa Dati Originali")
    ButtonMobColTrad = QtWidgets.QPushButton("Stampa Dati Tradotti")
    ButtonMobOnlyFlag = QtWidgets.QPushButton("Stampa Solo Flag Mob")

    CercaMob.setAlignment(QtCore.Qt.AlignLeft)
    self.ComboBoxMob.setSizeAdjustPolicy(0)#AdjustToContents
    self.ComboBoxTipoMob.setSizeAdjustPolicy(0)#AdjustToContents

    for i in sorted(MOB_TYPE.keys()):
        self.ComboBoxTipoMob.addItem(MOB_TYPE[i][1])

    self.ComboBoxSottoTipoMob.hide()
    
    ButtonSearchMob.clicked.connect(lambda: cerca_mob_by_combobox(self))
    self.ComboBoxMob.currentIndexChanged[str].connect(lambda: change_combo_box_mob(self))
    self.ComboBoxTipoMob.currentIndexChanged[str].connect(lambda: change_combo_box_tipo_mob(self))
    ButtonMobInterazioni.clicked.connect(lambda: stampa_mob_interazioni(self))
    ButtonMobDoppioni.clicked.connect(lambda: stampa_mob_doppioni(self))
    ButtonMobColOrig.clicked.connect(lambda: stampa_mob_col_orig(self))
    ButtonMobColTrad.clicked.connect(lambda: stampa_mob_col_trad(self))
    ButtonMobOnlyFlag.clicked.connect(lambda: stampa_mob_only_flag(self))

    self.MobLineEdit = QtWidgets.QTextEdit(MobXMLWidget)

    MobXMLGrid = QtWidgets.QGridLayout(MobXMLWidget)

    MobXMLGrid.addWidget(CercaMob, 0, 0)
    MobXMLGrid.addWidget(self.ComboBoxMob, 0, 1)
    MobXMLGrid.addWidget(self.ComboBoxTipoMob, 0, 2)
    MobXMLGrid.addWidget(self.ComboBoxSottoTipoMob, 0, 3)
    MobXMLGrid.addWidget(ButtonSearchMob, 0, 4)
    MobXMLGrid.addWidget(self.MobLineEdit, 1, 0, 1, 5)
    MobXMLGrid.addWidget(ButtonMobInterazioni, 2, 0, 1, 1)
    MobXMLGrid.addWidget(ButtonMobDoppioni, 2, 1, 1, 1)
    MobXMLGrid.addWidget(ButtonMobColOrig, 2, 2, 1, 1)
    MobXMLGrid.addWidget(ButtonMobColTrad, 2, 3, 1, 1)
    MobXMLGrid.addWidget(ButtonMobOnlyFlag, 2, 4, 1, 1)

    MobXMLWidget.setLayout(MobXMLGrid)

    MobXMLGrid.setAlignment(QtCore.Qt.AlignTop)

    return MobXMLWidget

def change_combo_box_mob(self):
    IndexTipo = self.ComboBoxMob.currentIndex()
    self.ComboBoxSottoTipoMob.show()

    if (IndexTipo == 0): #Tipo
        self.ComboBoxTipoMob.clear()
        self.ComboBoxSottoTipoMob.hide()
        for i in sorted(MOB_TYPE.keys()):
            self.ComboBoxTipoMob.addItem(MOB_TYPE[i][1])

    elif (IndexTipo == 1): #Grado
        self.ComboBoxTipoMob.clear()
        self.ComboBoxSottoTipoMob.hide()
        for i in range(0, len(MOB_GRADE.keys())):
            self.ComboBoxTipoMob.addItem(MOB_GRADE[i][1])

    elif (IndexTipo == 2): #Tipo Attacco
        self.ComboBoxTipoMob.clear()
        self.ComboBoxSottoTipoMob.hide()
        for i in range(0, len(MOB_BATTLE_TYPE)):
            self.ComboBoxTipoMob.addItem(MOB_BATTLE_TYPE[i][1])

    elif (IndexTipo == 3): #Size
        self.ComboBoxTipoMob.clear()
        self.ComboBoxSottoTipoMob.hide()
        for i in range(0, len(MOB_SIZE)):
            self.ComboBoxTipoMob.addItem(MOB_SIZE[i][1])

    elif (IndexTipo == 4): #Ai Flag
        self.ComboBoxTipoMob.clear()
        self.ComboBoxSottoTipoMob.hide()
        for i in range(0, len(MOB_AI_FLAG)):
            self.ComboBoxTipoMob.addItem(MOB_AI_FLAG[i][1])

    elif (IndexTipo == 5): #Race Flag
        self.ComboBoxTipoMob.clear()
        self.ComboBoxSottoTipoMob.hide()
        for i in range(0, len(MOB_RACE_FLAG)):
            self.ComboBoxTipoMob.addItem(MOB_RACE_FLAG[i][1])

    elif (IndexTipo == 6): #Immune Flag
        self.ComboBoxTipoMob.clear()
        self.ComboBoxSottoTipoMob.hide()
        for i in range(0, len(MOB_IMMUNE_FLAG)):
            self.ComboBoxTipoMob.addItem(MOB_IMMUNE_FLAG[i][1])
            
    elif (IndexTipo == 7): #Poss. Infliggere Status
        self.ComboBoxTipoMob.clear()
        self.ComboBoxSottoTipoMob.hide()
        self.ComboBoxTipoMob.addItem("Maledire")
        self.ComboBoxTipoMob.addItem("Rallentare")
        self.ComboBoxTipoMob.addItem("Avvelenare")
        self.ComboBoxTipoMob.addItem("Stordire")
        self.ComboBoxTipoMob.addItem("Critico")
        self.ComboBoxTipoMob.addItem("Trafiggenti")

    elif (IndexTipo == 8): #Altro
        self.ComboBoxTipoMob.clear()
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            key = list(proto.mob_data.mob_data_vnum["101"].keys())
        else:
            key = list(proto.mob_data.mob_data_vnum_en["101"].keys())
        key.remove("name")          #Nome
        key.remove("vnum")          #Vnum
        key.remove("Type")          #Tipo
        key.remove("Rank")          #Grado
        key.remove("BattleType")    #Tipo Battaglia
        key.remove("Size")          #Dimensione
        key.remove("AIFlags")       #AIFlag
        key.remove("RaceFlag")      #RaceFlag
        key.remove("ImmuneFlag")    #ImmuneFlag
        for elem in sorted(key):
          self.ComboBoxTipoMob.addItem(elem)  

    else:                   #Errore
        pass

def change_combo_box_tipo_mob(self):
    IndexTipo = self.ComboBoxMob.currentIndex()
    IndexSottoTipo = self.ComboBoxTipoMob.currentText()
    
    if (IndexTipo == 8): #Altro
        self.ComboBoxSottoTipoMob.clear()
        DATA_LIST = get_all_mob_info_by_name(IndexSottoTipo)
        for i in range(0, len(DATA_LIST)):
            self.ComboBoxSottoTipoMob.addItem(DATA_LIST[i])

def cerca_mob_by_combobox(self):
    data = ""
    IndexTipo = self.ComboBoxMob.currentIndex()
    IndexSottoTipo = self.ComboBoxTipoMob.currentText()
    Valore = self.ComboBoxSottoTipoMob.currentText()
    
    data = search_mob_data_from_type(str(IndexTipo), str(IndexSottoTipo), str(Valore))
    self.MobLineEdit.clear()
    self.MobLineEdit.append(data)
    self.MobLineEdit.moveCursor(QtGui.QTextCursor.Start)
    self.MobLineEdit.ensureCursorVisible()

def widget_up(self):
    UpWidget = QtWidgets.QWidget()

    self.UpGrid = QtWidgets.QGridLayout(UpWidget)

    UpWidget.setLayout(self.UpGrid)

    self.UpGrid.setAlignment(QtCore.Qt.AlignTop)

    self.item_up = metin2Class.item_up_box()
    self.UpGrid.addLayout(self.item_up.UpBox, 0,0)

    return UpWidget

def update_item_info_by_vnum(vnum):
    name = desc = ""
    res, vnum, name = search_item_data(vnum, "")
    if (res == -1):
        set_item_not_found()
        return
    update_item_data(name, vnum)

def update_item_info_by_name(name):
    vnum = 0
    desc = ""
    res, vnum, name = search_item_data(0, name)
    if (res == -1):
        set_item_not_found()
        return
    update_item_data(name, vnum)

def update_item_data(name, vnum):
    global search_item
    global Ibox1
    global Ibox2
    global Ibox3
    global Ibox4
    desc = proto.get_desc(vnum)
    try:
        search_item.set_name_vnum(name, vnum)
        search_item.set_desc(desc)
    except Exception as er:
        search_item.set_no_data()
        proto.err("Errore nel settare nome e vnum degli item: " + str(er))
        proto.stampa_errore("Errore nel settare nome e vnum degli item: " + str(er))
    try:
        Ibox1.set_pre_flag_data(vnum)
    except Exception as er:
        Ibox1.set_pre_flag_no_data()
        proto.err("Errore nel cercare i dati pre flag degli item: " + str(er))
        proto.stampa_errore("Errore nel cercare i dati pre flag degli item: " + str(er))
    try:
        Ibox2.set_flag_data(vnum)
    except Exception as er:
        Ibox2.set_flag_no_data()
        proto.err("Errore nel cercare i dati delle flag degli item: " + str(er))
        proto.stampa_errore("Errore nel cercare i dati delle flag degli item: " + str(er))
    try:
        Ibox3.set_bonus_data(vnum)
    except Exception as er:
        Ibox3.set_bonus_no_data()
        proto.err("Errore nel cercare i dati dei bonus degli item: " + str(er))
        proto.stampa_errore("Errore nel cercare i dati dei bonus degli item: " + str(er))
    try:
        Ibox4.set_other_data(vnum)
    except Exception as er:
        Ibox4.set_other_no_data()
        proto.err("Errore nel cercare gli altri dati degli item: " + str(er))
        proto.stampa_errore("Errore nel cercare gli altri dati degli item: " + str(er))

def set_item_not_found():
    global search_item
    global Ibox1
    global Ibox2
    global Ibox3
    global Ibox4
    search_item.set_no_data()
    Ibox1.set_pre_flag_no_data()
    Ibox2.set_flag_no_data()
    Ibox3.set_bonus_no_data()
    Ibox4.set_other_no_data()

def stampa_item_data(vnum, name):
    if (vnum.isnumeric()):
        res, vnum, name = search_item_data(vnum, "")
    else:
        res, vnum, name = search_item_data(0, name)
    if (res == 1):
        proto.stampa_info_item(vnum, name)
    else:
        return

def update_mob_info_by_vnum(vnum):
    name = ""
    res, vnum, name = search_mob_data(vnum, "")
    if (res == -1):
        set_mob_not_found()
        return
    if (proto.gestore_opzioni.get_option("TradMob") == 1):
        name = get_mob_name_it(vnum)
    update_mob_data(name, vnum)
    
def update_mob_info_by_name(name):
    global search_mob
    vnum = 0
    res, vnum, name = search_mob_data(0, name)
    if (res == -1):
        set_mob_not_found()
        return
    if (proto.gestore_opzioni.get_option("TradMob") == 1):
        name = get_mob_name_it(vnum)
    update_mob_data(name, vnum)

def update_mob_data(name, vnum):
    global search_mob
    global Mbox1
    global Mbox2
    global Mbox3
    global Mbox4
    try:
        search_mob.set_name_vnum(name, vnum)
    except Exception as er:
        search_mob.set_no_data()
        proto.err("Errore nel settare nome e vnum dei mob: " + str(er))
        proto.stampa_errore("Errore nel settare nome e vnum dei mob: " + str(er))
    try:
        Mbox1.set_pre_flag_data(vnum)
    except Exception as er:
        Mbox1.set_pre_flag_no_data()
        proto.err("Errore nel cercare i dati pre flag dei mostri: " + str(er))
        proto.stampa_errore("Errore nel cercare i dati pre flag dei mostri: " + str(er))
    try:
        Mbox2.set_flag_data(vnum)
    except Exception as er:
        Mbox2.set_flag_no_data()
        proto.err("Errore nel cercare i dati delle flag dei mostri: " + str(er))
        proto.stampa_errore("Errore nel cercare i dati delle flag dei mostri:" + str(er))
    try:
        Mbox3.set_skill_mob_data(vnum)
    except Exception as er:
        Mbox3.set_skill_mob_no_data()
        proto.err("Errore nel cercare i dati delle abilita' dei mostri: " + str(er))
        proto.stampa_errore("Errore nel cercare i dati delle abilita' dei mostri: " + str(er))
    try:
        Mbox4.set_other_mob_data(vnum)
    except Exception as er:
        Mbox4.set_other_mob_no_data()
        proto.err("Errore nel cercare gli altri dati dei mostri: " + str(er))
        proto.stampa_errore("Errore nel cercare gli altri dati dei mostri: " + str(er))   

def set_mob_not_found():
    global search_mob
    global Mbox1
    global Mbox2
    global Mbox3
    global Mbox4
    search_mob.set_no_data()
    Mbox1.set_pre_flag_no_data()
    Mbox2.set_flag_no_data()
    Mbox3.set_skill_mob_no_data()
    Mbox4.set_other_mob_no_data()

def stampa_mob_data(vnum, name):
    if (vnum.isnumeric()):
        res, vnum, name = search_mob_data(vnum, "")
    else:
        res, vnum, name = search_mob_data(0, name)
    if (res == 1):
        if (proto.gestore_opzioni.get_option("TradMob") == 1):
            name = get_mob_name_it(vnum)
        proto.stampa_info_mob(vnum, name)
    else:
        return

def search_item_data(vnum, name):
    if (proto.gestore_opzioni.get_option("Platform") == 0):
        file_vnum = proto.item_data.item_data_vnum
        file_name = proto.item_data.item_data_name
    else:
        file_vnum = proto.item_data.item_data_vnum_en
        file_name = proto.item_data.item_data_name_en
    if (name == ""):
        if (vnum in file_vnum):
            return 1, vnum, file_vnum[vnum]['name']
    elif (vnum == 0):
        if (name in file_name):
            if (type(file_name[name]) == dict):
                return 1, file_name[name]['vnum'], name
            else:
                data = ""
                for item in file_name[name]:
                    data = data + item['vnum'] + "\n"
                info("Esiste piu' di un vnum con questo nome. Usa la ricerca per uno di questi vnum:\n" + data)
                return 1, file_name[name][0]['vnum'], name
    return -1, 0, ""

def search_mob_data(vnum, name):
    if (proto.gestore_opzioni.get_option("Platform") == 0):
        file_vnum = proto.mob_data.mob_data_vnum
        file_name = proto.mob_data.mob_data_name
    else:
        file_vnum = proto.mob_data.mob_data_vnum_en
        file_name = proto.mob_data.mob_data_name_en
    if (name == ""):
        if (vnum in file_vnum):
            if (proto.gestore_opzioni.get_option("Platform") == 0):
                if (proto.gestore_opzioni.get_option("TradMob") == 1):
                    return 1, vnum, get_mob_name_it(file_vnum[vnum])
                else:
                    return 1, vnum, file_vnum[vnum]['name']
            else:
                return 1, vnum, file_vnum[vnum]['name']
    elif (vnum == 0):
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            if (name in proto.mob_data.mob_name_it):
                if (type(proto.mob_data.mob_name_it[name]) == list):
                    data = ""
                    for mob in proto.mob_data.mob_name_it[name]:
                        data = data + mob + "\n"
                    info("Esiste piu' di un vnum con questo nome. Usa la ricerca per uno di questi vnum:\n" + data)
                    return 1, proto.mob_data.mob_name_it[name][0], name
                else:
                    return 1, proto.mob_data.mob_name_it[name], name
        else:
            vnum = get_vnum_mob_from_name(name)
            if (name in file_name):
                name = file_vnum[vnum]['name']
            else:
                return -1, 0, ""
            if (name in file_name):
                if (type(file_name[name]) == dict):
                    return 1, file_name[name]['vnum'], name
                else:
                    data = ""
                    for mob in file_name[name]:
                        data = data + mob['vnum'] + "\n"
                    info("Esiste piu' di un vnum con questo nome. Usa la ricerca per uno di questi vnum:\n" + data)
                    return 1, file_name[name][0]['vnum'], name
    return -1, 0, ""

def get_mob_name_it(vnum):
    for mob in proto.mob_data.mob_name_it:
        if (type(proto.mob_data.mob_name_it[mob]) == list):
            for elem in proto.mob_data.mob_name_it[mob]:
                if (str(elem) == str(vnum)):
                    return mob
        else:
            if (str(proto.mob_data.mob_name_it[mob]) == str(vnum)):
                return mob
    return "???"

def get_mob_name(num):
    if (num == '0'):
        return "Nessuno"
    if (num in proto.mob_data.mob_data_vnum):
        if (proto.gestore_opzioni.get_option("TradMob") == 1):
            return get_mob_name_it(num)
        else:
            return proto.mob_data.mob_data_vnum[num]['name']
    else:
        return "Mob non Trovato"

def get_vnum_mob_from_name(name):
    if (proto.gestore_opzioni.get_option("Platform") == 0):
        if (name in proto.mob_data.mob_name_it):
            if (type(proto.mob_data.mob_name_it[name]) == list):
                return proto.mob_data.mob_name_it[name][0]
            else:
                return proto.mob_data.mob_name_it[name]
    else:
        if (name in proto.mob_data.mob_data_name_en):
            if (type(proto.mob_data.mob_data_name[name]) == dict):
                return proto.mob_data.mob_data_name_en[name]['vnum']
            else:
                return proto.mob_data.mob_data_name_en[name][0]['vnum']
    return 0

def search_item_data_from_type(scelta, item_type, sub_type):
    scelta = str(scelta)
    trovato = 0
    data = ""
    if (proto.gestore_opzioni.get_option("Platform") == 0):
        file = proto.item_data.item_data_vnum
    else:
        file = proto.item_data.item_data_vnum_en
    for item in sorted(int(x) for x in file):
        item = file[str(item)]

        if (scelta == "0"): #Tipo
            i_type = proto.get_item_type(item['Type'])[1]
            subtype = proto.get_item_subtype(item['Type'],item['SubType'])[1]
            if (i_type == str(item_type)):
                if (subtype == str(sub_type)):
                    trovato = 1
                    data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tTipo: " + str(item_type) + "\tSotto Tipo: " + str(sub_type) + "\n"
        elif (scelta == "1"): #Mask
            i_mask = proto.get_item_mask(item['TypeMask'])[1]
            submask = proto.get_item_sub_mask(item['TypeMask'],item['SubTypeMask'])[1]
            if (i_mask == str(item_type)):
                if (submask == str(sub_type)):
                    trovato = 1
                    data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tMaschera: " + str(item_type) + "\tSotto Maschera: " + str(sub_type) + "\n"
        elif (scelta == "2"): #Anti Flag
            anti_flag = proto.get_anti_flag(int(item['AntiFlags']))[1]
            if (item_type in anti_flag):
                trovato = 1
                data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tAnti Flag: " + item['AntiFlags'] + "\n"
        elif (scelta == "3"): #Item Flag
            item_flag = proto.get_item_flag(int(item['Flags']))[1]
            if (item_type in item_flag):
                trovato = 1
                data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tItem Flag: " + item['Flags'] + "\n"
        elif (scelta == "4"): #Wear Flag
            wear_flag = proto.get_wear_flag(int(item['WearFlags']))[1]
            if (item_type in wear_flag):
                trovato = 1
                data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tWear Flag: " + item['WearFlags'] + "\n"
        elif (scelta == "5"): #Immune Flag
            immune_flag = proto.get_item_immune_flag(int(item['ImmuneFlags']))[1]
            if (item_type in immune_flag):
                trovato = 1
                data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tImmune Flag: " + item['ImmuneFlags'] + "\n"
        elif (scelta == "6"): #Restrizione
            limit_1 = proto.get_limit_type(int(item['LimitType0']))[1]
            limit_2 = proto.get_limit_type(int(item['LimitType1']))[1]
            if (limit_1 == str(item_type) or limit_2 == str(item_type)):
                trovato = 1
                data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tRestrizione 1: " + limit_1 + "\tRestrizione 2: " + limit_2 + "\n"   
        elif (scelta == "7"): #Bonus
            bonus_1 = proto.get_apply_type(int(item['ApplyType0']))[1]
            bonus_2 = proto.get_apply_type(int(item['ApplyType1']))[1]
            bonus_3 = proto.get_apply_type(int(item['ApplyType2']))[1]
            bonus_4 = proto.get_apply_type(int(item['ApplyType3']))[1]
            if (bonus_1 == str(item_type) or bonus_2 == str(item_type) or bonus_3 == str(item_type) or bonus_4 == str(item_type)):
                trovato = 1
                data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tBonus 1: " + bonus_1 + "\tBonus 2: " + bonus_2 + "\tBonus 3: " + bonus_3 + "\tBonus 4: " + bonus_4 + "\n"
        elif (scelta == "8"): #Set Up
            set_up = item['RefineSet']
            if (str(set_up) == str(item_type)):
                trovato = 1
                data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\tSet Up: " + set_up + "\n"
        elif (scelta == "9"): #Altro
            if (item_type in item):
                if (str(item[item_type]) == str(sub_type)):
                    trovato = 1
                    data = data + item['vnum'] + "\t" + item['name'] + proto.spazio(item['name']) + "\t" + item_type + ": " + sub_type + "\n"
    if (trovato == 0):
        data =  "Nessun oggetto trovato con queste chiavi di ricerca"
    return data

def search_mob_data_from_type(scelta, mob_type, valore):
    trovato = 0
    data = ""
    if (proto.gestore_opzioni.get_option("Platform") == 0):
        file = proto.mob_data.mob_data_vnum
    else:
        file = proto.mob_data.mob_data_vnum_en
    for mob in sorted(int(x) for x in file):
        mob = file[str(mob)]

        if (scelta == "0"):     #Tipo
            mobtype = proto.get_mob_type(mob['Type'])[1]
            if (mobtype == mob_type):
                trovato = 1
                if (proto.gestore_opzioni.get_option("TradMob") == 1):
                    name = get_mob_name_it(mob['vnum'])
                else:
                    name = mob['name']
                data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tTipo: " + str(mob['Type']) + "\n"
        elif (scelta == "1"):   #Grado
            grade = proto.get_mob_grade(mob['Rank'])[1]
            if (grade == mob_type):
                trovato = 1
                if (proto.gestore_opzioni.get_option("TradMob") == 1):
                    name = get_mob_name_it(mob['vnum'])
                else:
                    name = mob['name']
                data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tGrado: " + str(mob['Rank']) + "\n"
        elif (scelta == "2"):   #Tipo Attacco
            battle_type = proto.get_mob_battle_type(mob['BattleType'])[1]
            if (battle_type == mob_type):
                trovato = 1
                if (proto.gestore_opzioni.get_option("TradMob") == 1):
                    name = get_mob_name_it(mob['vnum'])
                else:
                    name = mob['name']
                data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tBattle Type: " + str(mob['BattleType']) + "\n"
        elif (scelta == "3"):   #Size
            size = proto.get_mob_size(mob['Size'])[1]
            if (size == mob_type):
                trovato = 1
                if (proto.gestore_opzioni.get_option("TradMob") == 1):
                    name = get_mob_name_it(mob['vnum'])
                else:
                    name = mob['name']
                data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tSize: " + str(mob['Size']) + "\n"
        elif (scelta == "4"):   #Ai Flag
            ai_flag = proto.get_mob_ai_flag(int(mob['AIFlags']))[1]
            if (mob_type in ai_flag):
                trovato = 1
                if (proto.gestore_opzioni.get_option("TradMob") == 1):
                    name = get_mob_name_it(mob['vnum'])
                else:
                    name = mob['name']
                data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tAI Flag: " + str(mob['AIFlags']) + "\n"
        elif (scelta == "5"):   #Race Flag
            race_flag = proto.get_mob_race_flag(int(mob['RaceFlag']))[1]
            if (mob_type in race_flag):
                trovato = 1
                if (proto.gestore_opzioni.get_option("TradMob") == 1):
                    name = get_mob_name_it(mob['vnum'])
                else:
                    name = mob['name']
                data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tRace Flag: " + str(mob['RaceFlag']) + "\n"
        elif (scelta == "6"):   #Immune Flag
            immune_flag = proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[1]
            if (mob_type in immune_flag):
                trovato = 1
                if (proto.gestore_opzioni.get_option("TradMob") == 1):
                    name = get_mob_name_it(mob['vnum'])
                else:
                    name = mob['name']
                data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tImmune Flag: " + str(mob['ImmuneFlag']) + "\n"
        elif (scelta == "7"):   #Poss. Infliggere Status
            if (mob_type == "Maledire"):
                maledizione = mob['EnchantCurse']
                if (int(maledizione) > 0):
                    trovato = 1
                    if (proto.gestore_opzioni.get_option("TradMob") == 1):
                        name = get_mob_name_it(mob['vnum'])
                    else:
                        name = mob['name']
                    data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tPoss. Maledire: " + str(mob['EnchantCurse']) + "%\n"
            elif (mob_type == "Rallentare"):
                rallentare = mob['EnchantSlow']
                if (int(rallentare)> 0):
                    trovato = 1
                    if (proto.gestore_opzioni.get_option("TradMob") == 1):
                        name = get_mob_name_it(mob['vnum'])
                    else:
                        name = mob['name']
                    data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tPoss. Rallentare: " + str(mob['EnchantSlow']) + "%\n"
            elif (mob_type == "Avvelenare"):
                veleno = mob['EnchantPoison']
                if (int(veleno)> 0):
                    trovato = 1
                    if (proto.gestore_opzioni.get_option("TradMob") == 1):
                        name = get_mob_name_it(mob['vnum'])
                    else:
                        name = mob['name']
                    data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tPoss. Avvelenare: " + str(mob['EnchantPoison']) + "%\n"
            elif (mob_type == "Stordire"):
                stun = mob['EnchantStun']
                if (int(stun)> 0):
                    trovato = 1
                    if (proto.gestore_opzioni.get_option("TradMob") == 1):
                        name = get_mob_name_it(mob['vnum'])
                    else:
                        name = mob['name']
                    data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tPoss. Stordire: " + str(mob['EnchantStun']) + "%\n"
            elif (mob_type == "Critico"):
                critico = mob['EnchantCritical']
                if (int(critico)> 0):
                    trovato = 1
                    if (proto.gestore_opzioni.get_option("TradMob") == 1):
                        name = get_mob_name_it(mob['vnum'])
                    else:
                        name = mob['name']
                    data = data + mob['vnum'] + "\t" + name + proto.spazio(name) + "\tPoss. Critico: " + str(mob['EnchantCritical']) + "%\n"
            elif (mob_type == "Trafiggenti"):
                trafi = mob['EnchantPenetrate']
                if (int(trafi)> 0):
                    trovato = 1
                    if (proto.gestore_opzioni.get_option("TradMob") == 1):
                        name = get_mob_name_it(mob['vnum'])
                    else:
                        name = mob['name']
                    data = data + mob['vnum']+ "\t" + name + proto.spazio(name) + "\tPoss. Trafiggenti: " + str(mob['EnchantPenetrate']) + "%\n"
        elif (scelta == "8"):   #Altro
            if (mob_type in mob):
                if (str(mob[mob_type]) == str(valore)):
                    trovato = 1
                    if (proto.gestore_opzioni.get_option("TradMob") == 1):
                        name = get_mob_name_it(mob['vnum'])
                    else:
                        name = mob['name']
                    data = data + mob['vnum']+ "\t" + name + proto.spazio(name) + "\t" + mob_type + ": "+  str(valore) + "\n"
    if (trovato == 0):
        data =  "Nessun mostro trovato con queste chiavi di ricerca"
    return data

def info(message):
    new = QtWidgets.QWidget()
    QtWidgets.QMessageBox.information(new, "Info", message)

def errore(message, *boolean):
    if (boolean):
        proto.err(message)
    new = QtWidgets.QWidget()
    QtWidgets.QMessageBox.critical(new , "Errore", message)

def change_suggest_list(value):
    global search_item
    global search_mob
    search_item.set_suggest_list(value)
    search_mob.set_suggest_list(value)

def check_file(name):
    return os.path.exists(proto.cur_dir + "/" + name)

def check_dir(name):
    if (not check_file(name)):
        os.makedirs(proto.cur_dir + "/" + name)

def create_folders():
    d = proto.cur_dir
    if (not os.path.isdir(d + "/images")):
        os.makedirs(d + "/images")

def download(url, path):
    create_folders()
    urllib.request.urlretrieve(url, path)

def download_bar(self, url, path):
    fp = open(path, 'wb')
    response = urllib.request.urlopen(url)
    size = int(response.info()['Content-Length'])
    scaricato = 0
    while True:
        chunk = response.read(2048)
        if (not chunk):
            break
        scaricato += len(chunk)
        fp.write(chunk)
        per = (float(scaricato)/size) * 100
        self.UpdatePer.setProperty("value", per)

def download_icon(vnum):
    icon = proto.get_icon_vnum(vnum)
    if (icon != ""):
        check_dir("images")
        if (not check_file("images/" + icon + ".png")):
            try:
                print("Download dell'icona " + icon + " dell'oggetto con vnum " + vnum)
                download(proto.UPDATE_SITE + "images/" + icon + ".png", proto.cur_dir + "/images/" + icon + ".png")
            except:
                print("Icona non trovata: " + icon + " dell'oggetto con vnum " + vnum)
                proto.err("Icona non trovata: " + icon + " con vnum " + vnum)
                return ""
    return icon

def download_all_icon():
    try:
        fp = open(proto.DOWNLOAD_FILE[3], "r")
    except:
        return "Errore"
    print("Download delle icone iniziato")
    for line in fp.readlines():
        if (line == "\n"):
            continue
        line = line.split("\t")
        download_icon(line[0])
    print("Download delle icone terminato")

def check_set_up():
    for item in proto.item_data.item_data_vnum:
        item = proto.item_data.item_data_vnum[item]
        up = int(item['RefineSet'])
        
        itemtype = proto.get_item_type(item['Type'])[0]
        if (itemtype == 'ITEM_WEAPON' or itemtype == 'ITEM_ARMOR'):
            item = proto.get_item_set_up(up)

def check_all_item_type():
    print("Controllo Dati Item")
    for item in sorted(int(x) for x in proto.item_data.item_data_vnum):
        item = proto.item_data.item_data_vnum[str(item)]

        itemtype = proto.get_item_type(item['Type'])[0]
        sub_type = proto.get_item_subtype(item['Type'],item['SubType'])[0]
        itemmask = proto.get_item_mask(item['TypeMask'])[0]
        submask = proto.get_item_sub_mask(item['TypeMask'],item['SubTypeMask'])[0]

        flagwiki = proto.get_wiki_anti_flag(int(item['AntiFlags']), int(item['Flags']))
        antiflag = proto.get_anti_flag(int(item['AntiFlags']))[0]
        itemflag = proto.get_item_flag(int(item['Flags']))[0]
        wearflag = proto.get_wear_flag(int(item['WearFlags']))[0]
        immuneflag = proto.get_item_immune_flag(int(item['ImmuneFlags']))[0]

        limit_type_0 = proto.get_limit_type(int(item['LimitType0']))[0]
        limit_type_1 = proto.get_limit_type(int(item['LimitType1']))[0]
        bonus_0 = proto.get_apply_type(int(item['ApplyType0']))[0]
        bonus_1 = proto.get_apply_type(int(item['ApplyType1']))[0]
        bonus_2= proto.get_apply_type(int(item['ApplyType2']))[0]
        bonus_3= proto.get_apply_type(int(item['ApplyType3']))[0]

    print("Controllo Dati Item EN")

    for item in sorted(int(x) for x in proto.item_data.item_data_vnum_en):
        item = proto.item_data.item_data_vnum_en[str(item)]

        itemtype = proto.get_item_type(item['Type'])[0]
        sub_type = proto.get_item_subtype(item['Type'],item['SubType'])[0]
        itemmask = proto.get_item_mask(item['TypeMask'])[0]
        submask = proto.get_item_sub_mask(item['TypeMask'],item['SubTypeMask'])[0]

        flagwiki = proto.get_wiki_anti_flag(int(item['AntiFlags']), int(item['Flags']))
        antiflag = proto.get_anti_flag(int(item['AntiFlags']))[0]
        itemflag = proto.get_item_flag(int(item['Flags']))[0]
        wearflag = proto.get_wear_flag(int(item['WearFlags']))[0]
        immuneflag = proto.get_item_immune_flag(int(item['ImmuneFlags']))[0]

        limit_type_0 = proto.get_limit_type(int(item['LimitType0']))[0]
        limit_type_1 = proto.get_limit_type(int(item['LimitType1']))[0]
        bonus_0 = proto.get_apply_type(int(item['ApplyType0']))[0]
        bonus_1 = proto.get_apply_type(int(item['ApplyType1']))[0]
        bonus_2= proto.get_apply_type(int(item['ApplyType2']))[0]
        bonus_3= proto.get_apply_type(int(item['ApplyType3']))[0]

    print("Controllo Terminato")


def check_all_mob_type():
    print("Controllo Dati Mob")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum):
        mob = proto.mob_data.mob_data_vnum[str(mob)]
        
        mob_type = proto.get_mob_type(mob['Type'])[0]
        grade = proto.get_mob_grade(mob['Rank'])[0]
        battle_type = proto.get_mob_battle_type(mob['BattleType'])[0]
        mob_size = proto.get_mob_size(mob['Size'])[0]

        flagwiki = proto.get_wiki_mob_flag(mob['vnum'])
        aiflag = proto.get_mob_ai_flag(int(mob['AIFlags']))[0]
        raceflag = proto.get_mob_race_flag(int(mob['RaceFlag']))[0]
        immuneflag = proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[0]

        empire = proto.get_regno(mob['Empire'])[0]
        TypeOnClick = proto.get_mob_type_on_click(mob['OnClickType'])[0]

    print("Controllo Dati Mob EN")

    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum_en):
        mob = proto.mob_data.mob_data_vnum_en[str(mob)]
        
        mob_type = proto.get_mob_type(mob['Type'])[0]
        grade = proto.get_mob_grade(mob['Rank'])[0]
        battle_type = proto.get_mob_battle_type(mob['BattleType'])[0]
        mob_size = proto.get_mob_size(mob['Size'])[0]

        flagwiki = proto.get_wiki_mob_flag(mob['vnum'])
        aiflag = proto.get_mob_ai_flag(int(mob['AIFlags']))[0]
        raceflag = proto.get_mob_race_flag(int(mob['RaceFlag']))[0]
        immuneflag = proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[0]

        empire = proto.get_regno(mob['Empire'])[0]
        TypeOnClick = proto.get_mob_type_on_click(mob['OnClickType'])[0]

    print("Controllo Terminato")

def stampa_interazioni(self):
    print("Elaborazione Interazioni Item")
    out = open("Interazioni.txt", "w")
    for item in sorted(int(x) for x in proto.item_data.item_data_vnum):
        item = proto.item_data.item_data_vnum[str(item)]
        name = item['vnum']
        try:
            data = item['vnum'] + "\t" + name + proto.spazio(name) + "\t" + proto.get_wiki_anti_flag(int(item['AntiFlags']), int(item['Flags'])) + "\n"
            out.write(data)
        except:
            data = item['vnum'] + "\t" + "Errore nel Nome" + proto.spazio("Errore nel Nome") + "\t" + proto.get_wiki_anti_flag(int(item['AntiFlags']), int(item['Flags'])) + "\n"
            out.write(data)
        out.flush()
    out.close()

    print("Elaborazione Interazioni Item EN")
    out2 = open("Interazioni_en.txt", "w")
    for item in sorted(int(x) for x in proto.item_data.item_data_vnum_en):
        item = proto.item_data.item_data_vnum_en[str(item)]
        name = item['vnum']
        try:
            data = item['vnum'] + "\t" + name + proto.spazio(name) + "\t" + proto.get_wiki_anti_flag(int(item['AntiFlags']), int(item['Flags'])) + "\n"
            out.write(data)
        except:
            data = item['vnum'] + "\t" + "Errore nel Nome" + proto.spazio("Errore nel Nome") + "\t" + proto.get_wiki_anti_flag(int(item['AntiFlags']), int(item['Flags'])) + "\n"
            out2.write(data)
        out2.flush()
    out2.close()

def stampa_mob_interazioni(self):
    print("Elaborazione Interazioni Mostri")
    out = open("Interazioni_mob.txt", "w")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum):
        mob = proto.mob_data.mob_data_vnum[str(mob)]
        if (proto.gestore_opzioni.get_option("TradMob") == 1):
            name = get_mob_name_it(mob['vnum'])
        else:
            name = mob['name']
        try:
            data = mob['vnum'] + "\t" + name + proto.spazio(name) + "\t" + proto.get_wiki_mob_flag(mob['vnum']) + "\t" + proto.get_mob_element(mob['vnum']) + "\n"
            out.write(data)
        except:
            data = mob['vnum'] + "\t" + "Errore nel Nome" + proto.spazio("Errore nel Nome") + "\t" + proto.get_wiki_mob_flag(mob['vnum']) + "\t" + proto.get_mob_element(mob['vnum']) + "\n"
            out.write(data)
        out.flush()
        
    print("Elaborazione Interazioni Mostri EN")
    out.close()
    out2 = open("Interazioni_mob_en.txt", "w")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum_en):
        mob = proto.mob_data.mob_data_vnum_en[str(mob)]
        try:
            data = mob['vnum'] + "\t" + mob['name'] + proto.spazio(mob['name']) + "\t" + proto.get_wiki_mob_flag(mob['vnum']) + "\t" + proto.get_mob_element(mob['vnum']) + "\n"
            out2.write(data)
        except:
            data = mob['vnum'] + "\t" + "Errore nel Nome" + proto.spazio("Errore nel Nome") + "\t" + proto.get_wiki_mob_flag(mob['vnum']) + "\t" + proto.get_mob_element(mob['vnum']) + "\n"
            out2.write(data)
        out2.flush()
    out2.close()        

    print("Stampa Finita")
    
def stampa_item_doppioni(self):
    item_doppioni = {}
    out = open("lista item doppioni.txt", "w")
    print("Ricerca Item Doppioni Iniziata")
    for item in sorted(proto.item_data.item_data_name):
        if (type(proto.item_data.item_data_name[item]) != dict):
            item_doppioni[item] = proto.item_data.item_data_name[item]

    for item in item_doppioni:
        try:
            out.write(item_doppioni[item][0]['name'] + "\t")
        except:
            out.write("Errore nel Nome" + "\t")
        for elem in item_doppioni[item]:
            out.write(elem['vnum'] + "\t")
            out.flush()
        out.write("\n")
    out.close()
    print("Stampa Finita")

    item_doppioni = {}
    out = open("lista item doppioni en.txt", "w")
    print("Ricerca Item Doppioni EN Iniziata")
    for item in sorted(proto.item_data.item_data_name_en):
        if (type(proto.item_data.item_data_name_en[item]) != dict):
            item_doppioni[item] = proto.item_data.item_data_name_en[item]

    for item in item_doppioni:
        try:
            out.write(item_doppioni[item][0]['vnum'] + "\t")
        except:
            out.write("Errore nel Nome" + "\t")
        for elem in item_doppioni[item]:
            out.write(elem['vnum'] + "\t")
            out.flush()
        out.write("\n")
    out.close()
    print("Stampa Finita")

def stampa_mob_doppioni(self):
    mob_doppioni = {}
    out = open("lista mob doppioni.txt", "w")
    print("Ricerca Mob Doppioni Iniziata")
    for mob in sorted(proto.mob_data.mob_data_name):
        if (type(proto.mob_data.mob_data_name[mob]) != dict):
            mob_doppioni[mob] = proto.mob_data.mob_data_name[mob]

    for mob in mob_doppioni:
        try:
            if (proto.gestore_opzioni.get_option("TradMob") == 1):
                name = get_mob_name_it(mob_doppioni[mob][0]['vnum'])
            else:
                name = mob_doppioni[mob][0]['name']
            out.write(name + "\t")
        except:
            out.write("Errore nel Nome" + "\t")
        for elem in mob_doppioni[mob]:
            out.write(elem['vnum'] + "\t")
            out.flush()
        out.write("\n")
    out.close()
    print("Stampa Finita")

    mob_doppioni_en = {}
    out = open("lista mob doppioni en.txt", "w")
    print("Ricerca Mob Doppioni EN Iniziata")
    for mob in sorted(proto.mob_data.mob_data_name_en):
        if (type(proto.mob_data.mob_data_name_en[mob]) != dict):
            mob_doppioni_en[mob] = proto.mob_data.mob_data_name_en[mob]

    for mob in mob_doppioni_en:
        try:
            out.write(mob_doppioni_en[mob][0]['name'] + "\t")
        except:
            out.write("Errore nel Nome" + "\t")
        for elem in mob_doppioni_en[mob]:
            out.write(elem['vnum'] + "\t")
            out.flush()
        out.write("\n")
    out.close()
    print("Stampa Finita")


def stampa_item_col_orig(self):
    fout = open("item.txt", "w")
    fout.write("Vnum\tName\t\tType\tSubType\tTypeMask\tSubTypeMask\tWeight\tSize\tAntiFlags\tFlags\tWearFlags\tImmuneFlags\tGold\tShopBuyPrice\tLimitType0\tLimitValue0\tLimitType1\tLimitValue1\tApplyType0\tApplyValue0\tApplyType1\tApplyValue1\tApplyType2\tApplyValue2\tValue0\tValue1\tValue2\tValue3\tValue4\tValue5\tSocket0\tSocket1\tSocket2\tRefinedVnum\tRefineSet\tAlterToMagicItemPercent\tSpecular\tGainSocketPercent\n")
    
    print("Ricerca Iniziata Item")

    for item_info in sorted(int(x) for x in proto.item_data.item_data_vnum):
        item_info = proto.item_data.item_data_vnum[str(item_info)]
        if (str(item_info['vnum']) != "0"):
            data = item_info['vnum'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        else:
            data = item_info['vnum'] + "~" + item_info['VnumRange'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        fout.write(data)
        data = '\t' + item_info['Type'] + '\t' + item_info['SubType'] + '\t' + item_info['TypeMask'] + '\t'
        data = data + '\t' + item_info['SubTypeMask'] + '\t' + item_info['Weight'] + '\t' +  item_info['Size'] + "\t" + item_info['AntiFlags']
        data = data + '\t' + item_info['Flags'] + '\t' + item_info['WearFlags'] + '\t' + "\t" + item_info['ImmuneFlags']
        data = data + '\t' + item_info['Gold'] + '\t' + item_info['ShopBuyPrice'] + '\t' +  item_info['LimitType0'] + "\t" + item_info['LimitValue0'] 
        data = data + '\t' + item_info['LimitType1'] + '\t' + item_info['LimitValue1'] + '\t' +  item_info['ApplyType0'] + "\t" + item_info['ApplyValue0']
        data = data + '\t' + item_info['ApplyType1'] + '\t' + item_info['ApplyValue1'] + '\t' +  item_info['ApplyType2'] + "\t" + item_info['ApplyValue2'] + item_info['ApplyType3'] + "\t" + item_info['ApplyValue3']    
        data = data + '\t' + item_info['Value0'] + '\t' + item_info['Value1'] + '\t' +  item_info['Value2'] + "\t" + item_info['Value3']   
        data = data + '\t' + item_info['Value4'] + '\t' + item_info['Value5'] + '\t' +  item_info['Socket0'] + "\t" + item_info['Socket1']        
        data = data + '\t' + item_info['Socket2'] + '\t' + item_info['RefinedVnum'] + '\t' +  item_info['RefineSet'] + "\t" + item_info['AlterToMagicItemPercent'] + "\t" + item_info['67_Material']
        data = data + '\t' + item_info['Specular'] + '\t' + item_info['GainSocketPercent']

        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")

    fout = open("item_en.txt", "w")
    fout.write("Vnum\tName\t\tType\tSubType\tTypeMask\tSubTypeMask\tWeight\tSize\tAntiFlags\tFlags\tWearFlags\tImmuneFlags\tGold\tShopBuyPrice\tLimitType0\tLimitValue0\tLimitType1\tLimitValue1\tApplyType0\tApplyValue0\tApplyType1\tApplyValue1\tApplyType2\tApplyValue2\tValue0\tValue1\tValue2\tValue3\tValue4\tValue5\tSocket0\tSocket1\tSocket2\tRefinedVnum\tRefineSet\tAlterToMagicItemPercent\tSpecular\tGainSocketPercent\n")
    
    print("Ricerca Iniziata Item EN")

    for item_info in sorted(int(x) for x in proto.item_data.item_data_vnum_en):
        item_info = proto.item_data.item_data_vnum_en[str(item_info)]
        if (str(item_info['vnum']) != "0"):
            data = item_info['vnum'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        else:
            data = item_info['vnum'] + "~" + item_info['VnumRange'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        fout.write(data)
        data = '\t' + item_info['Type'] + '\t' + item_info['SubType'] + '\t' + item_info['TypeMask'] + '\t'
        data = data + '\t' + item_info['SubTypeMask'] + '\t' + item_info['Weight'] + '\t' +  item_info['Size'] + "\t" + item_info['AntiFlags']
        data = data + '\t' + item_info['Flags'] + '\t' + item_info['WearFlags'] + '\t' + "\t" + item_info['ImmuneFlags']
        data = data + '\t' + item_info['Gold'] + '\t' + item_info['ShopBuyPrice'] + '\t' +  item_info['LimitType0'] + "\t" + item_info['LimitValue0'] 
        data = data + '\t' + item_info['LimitType1'] + '\t' + item_info['LimitValue1'] + '\t' +  item_info['ApplyType0'] + "\t" + item_info['ApplyValue0']
        data = data + '\t' + item_info['ApplyType1'] + '\t' + item_info['ApplyValue1'] + '\t' +  item_info['ApplyType2'] + "\t" + item_info['ApplyValue2'] +  item_info['ApplyType3'] + "\t" + item_info['ApplyValue3']         
        data = data + '\t' + item_info['Value0'] + '\t' + item_info['Value1'] + '\t' +  item_info['Value2'] + "\t" + item_info['Value3']   
        data = data + '\t' + item_info['Value4'] + '\t' + item_info['Value5'] + '\t' +  item_info['Socket0'] + "\t" + item_info['Socket1']        
        data = data + '\t' + item_info['Socket2'] + '\t' + item_info['RefinedVnum'] + '\t' +  item_info['RefineSet'] + "\t" + item_info['AlterToMagicItemPercent'] + "\t" + item_info['67_Material']
        data = data + '\t' + item_info['Specular'] + '\t' + item_info['GainSocketPercent']

        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")


def stampa_mob_col_orig(self):
    fout = open("mob.txt", "w")
    fout.write("VNUM\tNOME\t\t\tType\tRank\tBattleType\tLevel\tScalePct\tSize\tDropGoldMin\tDropGoldMax\tExperience\tMaxHP\tRegenCycle\tRegenPercent\tDefense\tAIFlags\tRaceFlag\tImmuneFlag\tStr\tDex\tCon\tInt\tDamageMin\tDamageMax\tAttackSpeed\tMovingSpeed\tAggressiveHPPct\tAggressiveSight\tAttackRange\tEnchantCurse\tEnchantSlow\tEnchantPoison\tEnchantStun\tEnchantCritical\tEnchantPenetrate\tResistFist\tResistSword\tResistTwohand\tResistDagger\tResistBell\tFesistFan\tResistBow\tResistClaw\tResistFire\tResistElect\tResistMagic\tResistWind\tResistEarth\tResistDark\tResistIce\tResistPoison\tResistBleeding\tAttElec\tAttWind\tAttFire\tAttIce\tAttDark\tAttEarth\tResurrectionVnum\tDropItemVnum\tMountCapacity\tOnClickType\tEmpire\tFolder\tDamMultiply\tSummonVnum\tDrainSP\tMonsterColor\tPolymorphItemVnum\tSkillVnum0\tSkillLevel0\tSkillVnum1\tSkillLevel1\tSkillVnum2\tSkillLevel2\tSkillVnum3\tSkillLevel3\tSkillVnum4\tSkillLevel4\tBerserkPoint\tStoneSkinPoint\tGodSpeedPoint\tDeathBlowPoint\tRevivePoint\tHealVnum\tHitRange\n")
    
    print("Ricerca Iniziata Mob")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum):
        mob = proto.mob_data.mob_data_vnum[str(mob)]
        try:
            if (proto.gestore_opzioni.get_option("TradMob") == 1):
                name = get_mob_name_it(mob['vnum'])
            else:
                name = mob['name']
            data = mob['vnum'] + '\t' + name + proto.spazio(name)
            fout.write(data)
        except:
            data = mob['vnum'] + '\t' + "Errore nel Nome" + proto.spazio("Errore nel Nome")
            fout.write(data)
        data = '\t' + mob['Type'] + '\t' + mob['Rank'] + '\t' + mob['BattleType'] 
        data = data + '\t' + mob['Level'] + '\t' + mob['ScalePct'] + '\t' +  mob['Size'] + "\t" + mob['DropGoldMin'] + "\t" + mob['DropGoldMax']
        data = data + '\t' + mob['Experience'] + '\t' + mob['MaxHP'] + '\t' + mob['RegenCycle'] + "\t" + mob['RegenPercent']
        data = data + '\t' + mob['Defense'] + '\t' + mob['AIFlags'] + '\t' + mob['RaceFlag'] + '\t' + mob['ImmuneFlag'] + '\t' + mob['Str'] + "\t" + mob['Dex'] + "\t" + mob['Con'] + "\t" + mob['Int']
        data = data + '\t' + mob['DamageMin'] + "\t" + mob['DamageMax'] + '\t' + mob['AttackSpeed'] + "\t" + mob['MovingSpeed'] + "\t" + mob['AggressiveHPPct'] + "\t" + mob['AggressiveSight']
        data = data + '\t' + mob['AttackRange'] + "\t" + mob['EnchantCurse'] + "\t" + mob['EnchantSlow'] + "\t" + mob['EnchantPoison'] + "\t" + mob['EnchantStun'] + "\t" + mob['EnchantCritical'] + "\t" + mob['EnchantPenetrate'] + "\t" + mob['ResistFist'] + "\t" + mob['ResistSword']
        data = data + '\t' + mob['ResistTwohand'] + "\t" + mob['ResistDagger'] + "\t" + mob['ResistBell'] + "\t" + mob['ResistFan']
        data = data + '\t' + mob['ResistBow'] + "\t" + mob['ResistClaw'] + "\t" + mob['ResistFire'] + "\t" + mob['ResistElect']
        data = data + '\t' + mob['ResistMagic'] + "\t" + mob['ResistWind'] + "\t" + mob['ResistEarth'] + "\t" + mob['ResistDark'] + "\t" + mob['ResistIce'] + "\t" +  mob['ResistPoison']
        data = data + '\t' + mob['ResistBleeding'] + "\t" + mob['AttElec'] + "\t" + mob['AttWind'] + "\t" + mob['AttFire'] + "\t" + mob['AttIce'] + "\t" + mob['AttDark'] + "\t" + mob['AttEarth']
        data = data + '\t' + mob['ResurrectionVnum'] + "\t" + mob['DropItemVnum'] + "\t" + mob['MountCapacity'] + "\t" + mob['OnClickType'] + "\t" + mob['Empire']
        data = data + '\t' + mob['Folder'] + "\t" + mob['DamMultiply'] + "\t" + mob['SummonVnum'] + "\t" + mob['DrainSP'] + "\t" + mob['MonsterColor'] + "\t" + mob['PolymorphItemVnum']
        data = data + '\t' + mob['SkillVnum0'] + "\t" + mob['SkillLevel0'] + "\t" + mob['SkillVnum1'] + "\t" + mob['SkillLevel1'] + "\t" + mob['SkillVnum2'] + "\t" + mob['SkillLevel2'] + "\t" + mob['SkillVnum3'] + "\t" + mob['SkillLevel3']
        data = data + '\t' + mob['BerserkPoint'] + "\t" + mob['StoneSkinPoint'] + "\t" + mob['GodSpeedPoint'] + "\t" + mob['DeathBlowPoint'] + "\t" + mob['RevivePoint'] + "\t" + mob['HealVnum'] + "\t" + mob['HitRange']
        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")
    
    fout = open("mob_en.txt", "w")
    fout.write("VNUM\tNOME\t\t\tType\tRank\tBattleType\tLevel\tScalePct\tSize\tDropGoldMin\tDropGoldMax\tExperience\tMaxHP\tRegenCycle\tRegenPercent\tDefense\tAIFlags\tRaceFlag\tImmuneFlag\tStr\tDex\tCon\tInt\tDamageMin\tDamageMax\tAttackSpeed\tMovingSpeed\tAggressiveHPPct\tAggressiveSight\tAttackRange\tEnchantCurse\tEnchantSlow\tEnchantPoison\tEnchantStun\tEnchantCritical\tEnchantPenetrate\tResistFist\tResistSword\tResistTwohand\tResistDagger\tResistBell\tFesistFan\tResistBow\tResistClaw\tResistFire\tResistElect\tResistMagic\tResistWind\tResistEarth\tResistDark\tResistIce\tResistPoison\tResistBleeding\tAttElec\tAttWind\tAttFire\tAttIce\tAttDark\tAttEarth\tResurrectionVnum\tDropItemVnum\tMountCapacity\tOnClickType\tEmpire\tFolder\tDamMultiply\tSummonVnum\tDrainSP\tMonsterColor\tPolymorphItemVnum\tSkillVnum0\tSkillLevel0\tSkillVnum1\tSkillLevel1\tSkillVnum2\tSkillLevel2\tSkillVnum3\tSkillLevel3\tSkillVnum4\tSkillLevel4\tBerserkPoint\tStoneSkinPoint\tGodSpeedPoint\tDeathBlowPoint\tRevivePoint\tHealVnum\tHitRange\n")
    
    print("Ricerca Iniziata Mob EN")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum_en):
        mob = proto.mob_data.mob_data_vnum_en[str(mob)]
        try:
            if (proto.gestore_opzioni.get_option("TradMob") == 1):
                name = get_mob_name_it(mob['vnum'])
            else:
                name = mob['name']
            data = mob['vnum'] + '\t' + name + proto.spazio(name)
            fout.write(data)
        except:
            data = mob['vnum'] + '\t' + "Errore nel Nome" + proto.spazio("Errore nel Nome")
            fout.write(data)
        data = '\t' + mob['Type'] + '\t' + mob['Rank'] + '\t' + mob['BattleType'] 
        data = data + '\t' + mob['Level'] + '\t' + mob['ScalePct'] + '\t' + mob['Size'] + "\t" + mob['DropGoldMin'] + "\t" + mob['DropGoldMax']
        data = data + '\t' + mob['Experience'] + '\t' + mob['MaxHP'] + '\t' + mob['RegenCycle'] + "\t" + mob['RegenPercent']
        data = data + '\t' + mob['Defense'] + '\t' + mob['AIFlags'] + '\t' + mob['RaceFlag'] + '\t' + mob['ImmuneFlag'] + '\t' + mob['Str'] + "\t" + mob['Dex'] + "\t" + mob['Con'] + "\t" + mob['Int']
        data = data + '\t' + mob['DamageMin'] + "\t" + mob['DamageMax'] + '\t' + mob['AttackSpeed'] + "\t" + mob['MovingSpeed'] + "\t" + mob['AggressiveHPPct'] + "\t" + mob['AggressiveSight']
        data = data + '\t' + mob['AttackRange'] + "\t" + mob['EnchantCurse'] + "\t" + mob['EnchantSlow'] + "\t" + mob['EnchantPoison'] + "\t" + mob['EnchantStun'] + "\t" + mob['EnchantCritical'] + "\t" + mob['EnchantPenetrate'] + "\t" + mob['ResistFist'] + "\t" + mob['ResistSword']
        data = data + '\t' + mob['ResistTwohand'] + "\t" + mob['ResistDagger'] + "\t" + mob['ResistBell'] + "\t" + mob['ResistFan']
        data = data + '\t' + mob['ResistBow'] + "\t" + mob['ResistClaw'] + "\t" + mob['ResistFire'] + "\t" + mob['ResistElect']
        data = data + '\t' + mob['ResistMagic'] + "\t" + mob['ResistWind'] + "\t" + mob['ResistEarth'] + "\t" + mob['ResistDark'] + "\t" + mob['ResistIce'] + "\t" +  mob['ResistPoison']
        data = data + '\t' + mob['ResistBleeding'] + "\t" + mob['AttElec'] + "\t" + mob['AttWind'] + "\t" + mob['AttFire'] + "\t" + mob['AttIce'] + "\t" + mob['AttDark'] + "\t" + mob['AttEarth']
        data = data + '\t' + mob['ResurrectionVnum'] + "\t" + mob['DropItemVnum'] + "\t" + mob['MountCapacity'] + "\t" + mob['OnClickType'] + "\t" + mob['Empire']
        data = data + '\t' + mob['Folder'] + "\t" + mob['DamMultiply'] + "\t" + mob['SummonVnum'] + "\t" + mob['DrainSP'] + "\t" + mob['MonsterColor'] + "\t" + mob['PolymorphItemVnum']
        data = data + '\t' + mob['SkillVnum0'] + "\t" + mob['SkillLevel0'] + "\t" + mob['SkillVnum1'] + "\t" + mob['SkillLevel1'] + "\t" + mob['SkillVnum2'] + "\t" + mob['SkillLevel2'] + "\t" + mob['SkillVnum3'] + "\t" + mob['SkillLevel3']
        data = data + '\t' + mob['BerserkPoint'] + "\t" + mob['StoneSkinPoint'] + "\t" + mob['GodSpeedPoint'] + "\t" + mob['DeathBlowPoint'] + "\t" + mob['RevivePoint'] + "\t" + mob['HealVnum'] + "\t" + mob['HitRange']
        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")


def stampa_item_col_trad(self):

    fout = open("dati_item_tradotti.txt", "w")
    fout.write("Vnum\tName\t\tType\tSubType\tTypeMask\tSubTypeMask\tWeight\tSize\tAntiFlags\tFlags\tWearFlags\tImmuneFlags\tGold\tShopBuyPrice\tLimitType0\tLimitValue0\tLimitType1\tLimitValue1\tApplyType0\tApplyValue0\tApplyType1\tApplyValue1\tApplyType2\tApplyValue2\tValue0\tValue1\tValue2\tValue3\tValue4\tValue5\tSocket0\tSocket1\tSocket2\tRefinedVnum\tRefineSet\tAlterToMagicItemPercent\tSpecular\tGainSocketPercent\n")
    
    print("Ricerca Iniziata Item Tradotti")

    for item_info in sorted(int(x) for x in proto.item_data.item_data_vnum):
        item_info = proto.item_data.item_data_vnum[str(item_info)]
        if (str(item_info['vnum']) != "0"):
            data = item_info['vnum'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        else:
            data = item_info['vnum'] + "~" + item_info['VnumRange'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        fout.write(data)
        data = '\t' + proto.get_item_type(item_info['Type'])[1] + '\t' + proto.get_item_subtype(item_info['Type'],item_info['SubType'])[1] + '\t' + proto.get_item_mask(item_info['TypeMask'])[1] + '\t'
        data = data + '\t' + proto.get_item_sub_mask(item_info['TypeMask'],item_info['SubTypeMask'])[1] + '\t' + item_info['Weight'] + '\t' +  item_info['Size'] + "\t" + proto.get_anti_flag(int(item_info['AntiFlags']))[1]
        data = data + '\t' + proto.get_item_flag(int(item_info['Flags']))[1]  + '\t' +  proto.get_wear_flag(int(item_info['WearFlags']))[1] + "\t" + proto.get_item_immune_flag(int(item_info['ImmuneFlags']))[1]
        data = data + '\t' + item_info['Gold'] + '\t' + item_info['ShopBuyPrice'] + '\t' +  item_info['LimitType0'] + "\t" + item_info['LimitValue0'] 
        data = data + '\t' + item_info['LimitType1'] + '\t' + item_info['LimitValue1'] + '\t' +  item_info['ApplyType0'] + "\t" + item_info['ApplyValue0']
        data = data + '\t' + item_info['ApplyType1'] + '\t' + item_info['ApplyValue1'] + '\t' +  item_info['ApplyType2'] + "\t" + item_info['ApplyValue2'] +  item_info['ApplyType3'] + "\t" + item_info['ApplyValue3']           
        data = data + '\t' + item_info['Value0'] + '\t' + item_info['Value1'] + '\t' +  item_info['Value2'] + "\t" + item_info['Value3']   
        data = data + '\t' + item_info['Value4'] + '\t' + item_info['Value5'] + '\t' +  item_info['Socket0'] + "\t" + item_info['Socket1']        
        data = data + '\t' + item_info['Socket2'] + '\t' + item_info['RefinedVnum'] + '\t' +  item_info['RefineSet'] + "\t" + item_info['AlterToMagicItemPercent'] + "\t" + item_info['67_Material']
        data = data + '\t' + item_info['Specular'] + '\t' + item_info['GainSocketPercent']

        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")

    fout = open("dati_item_tradotti_en.txt", "w")
    fout.write("Vnum\tName\t\tType\tSubType\tTypeMask\tSubTypeMask\tWeight\tSize\tAntiFlags\tFlags\tWearFlags\tImmuneFlags\tGold\tShopBuyPrice\tLimitType0\tLimitValue0\tLimitType1\tLimitValue1\tApplyType0\tApplyValue0\tApplyType1\tApplyValue1\tApplyType2\tApplyValue2\tValue0\tValue1\tValue2\tValue3\tValue4\tValue5\tSocket0\tSocket1\tSocket2\tRefinedVnum\tRefineSet\tAlterToMagicItemPercent\tSpecular\tGainSocketPercent\n")
    
    print("Ricerca Iniziata Item EN Tradotti")

    for item_info in sorted(int(x) for x in proto.item_data.item_data_vnum_en):
        item_info = proto.item_data.item_data_vnum_en[str(item_info)]
        if (str(item_info['vnum']) != "0"):
            data = item_info['vnum'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        else:
            data = item_info['vnum'] + "~" + item_info['VnumRange'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        fout.write(data)
        data = '\t' + proto.get_item_type(item_info['Type'])[1] + '\t' + proto.get_item_subtype(item_info['Type'],item_info['SubType'])[1] + '\t' + proto.get_item_mask(item_info['TypeMask'])[1] + '\t'
        data = data + '\t' + proto.get_item_sub_mask(item_info['TypeMask'],item_info['SubTypeMask'])[1] + '\t' + item_info['Weight'] + '\t' +  item_info['Size'] + "\t" + proto.get_anti_flag(int(item_info['AntiFlags']))[1]
        data = data + '\t' + proto.get_item_flag(int(item_info['Flags']))[1]  + '\t' +  proto.get_wear_flag(int(item_info['WearFlags']))[1] + "\t" + proto.get_item_immune_flag(int(item_info['ImmuneFlags']))[1]
        data = data + '\t' + item_info['Gold'] + '\t' + item_info['ShopBuyPrice'] + '\t' +  item_info['LimitType0'] + "\t" + item_info['LimitValue0'] 
        data = data + '\t' + item_info['LimitType1'] + '\t' + item_info['LimitValue1'] + '\t' +  item_info['ApplyType0'] + "\t" + item_info['ApplyValue0']
        data = data + '\t' + item_info['ApplyType1'] + '\t' + item_info['ApplyValue1'] + '\t' +  item_info['ApplyType2'] + "\t" + item_info['ApplyValue2'] +  item_info['ApplyType3'] + "\t" + item_info['ApplyValue3']
        data = data + '\t' + item_info['Value0'] + '\t' + item_info['Value1'] + '\t' +  item_info['Value2'] + "\t" + item_info['Value3']   
        data = data + '\t' + item_info['Value4'] + '\t' + item_info['Value5'] + '\t' +  item_info['Socket0'] + "\t" + item_info['Socket1']        
        data = data + '\t' + item_info['Socket2'] + '\t' + item_info['RefinedVnum'] + '\t' +  item_info['RefineSet'] + "\t" + item_info['AlterToMagicItemPercent'] + "\t" + item_info['67_Material']
        data = data + '\t' + item_info['Specular'] + '\t' + item_info['GainSocketPercent']

        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")


def stampa_mob_col_trad(self):
    fout = open("mob tradotti.txt", "w")
    fout.write("VNUM\tNOME\t\t\tType\tRank\tBattleType\tLevel\tScalePct\tSize\tDropGoldMin\tDropGoldMax\tExperience\tMaxHP\tRegenCycle\tRegenPercent\tDefense\tAIFlags\tRaceFlag\tImmuneFlag\tStr\tDex\tCon\tInt\tDamageMin\tDamageMax\tAttackSpeed\tMovingSpeed\tAggressiveHPPct\tAggressiveSight\tAttackRange\tEnchantCurse\tEnchantSlow\tEnchantPoison\tEnchantStun\tEnchantCritical\tEnchantPenetrate\tResistFist\tResistSword\tResistTwohand\tResistDagger\tResistBell\tFesistFan\tResistBow\tResistClaw\tResistFire\tResistElect\tResistMagic\tResistWind\tResistEarth\tResistDark\tResistIce\tResistPoison\tResistBleeding\tAttElec\tAttWind\tAttFire\tAttIce\tAttDark\tAttEarth\tResurrectionVnum\tDropItemVnum\tMountCapacity\tOnClickType\tEmpire\tFolder\tDamMultiply\tSummonVnum\tDrainSP\tMonsterColor\tPolymorphItemVnum\tSkillVnum0\tSkillLevel0\tSkillVnum1\tSkillLevel1\tSkillVnum2\tSkillLevel2\tSkillVnum3\tSkillLevel3\tSkillVnum4\tSkillLevel4\tBerserkPoint\tStoneSkinPoint\tGodSpeedPoint\tDeathBlowPoint\tRevivePoint\tHealVnum\tHitRange\n")
    
    print("Ricerca Iniziata Mob Tradotti")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum):
        mob = proto.mob_data.mob_data_vnum[str(mob)]
        try:
            if (proto.gestore_opzioni.get_option("TradMob") == 1):
                name = get_mob_name_it(mob['vnum'])
            else:
                name = mob['name']
            data = mob['vnum'] + '\t' + name + proto.spazio(name)
            fout.write(data)
        except:
            data = mob['vnum'] + '\t' + "Errore nel Nome" + proto.spazio("Errore nel Nome")
            fout.write(data)
        data = '\t' + proto.get_mob_type(int(mob['Type']))[1] + '\t' + proto.get_mob_grade(int(mob['Rank']))[1] + '\t' + proto.get_mob_battle_type(int(mob['BattleType']))[1] 
        data = data + '\t' + mob['Level'] + '\t' + mob['ScalePct'] + '\t' + proto.get_mob_size(int(mob['Size']))[1] + "\t" + mob['DropGoldMin'] + "\t" + mob['DropGoldMax']
        data = data + '\t' + mob['Experience'] + '\t' + mob['MaxHP'] + '\t' + mob['RegenCycle'] + "\t" + mob['RegenPercent']
        data = data + '\t' + mob['Defense'] + '\t' + proto.get_mob_ai_flag(int(mob['AIFlags']))[1] + '\t' + proto.get_mob_race_flag(int(mob['RaceFlag']))[1] + '\t' + proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[1] + '\t' + mob['Str'] + "\t" + mob['Dex'] + "\t" + mob['Con'] + "\t" + mob['Int']
        data = data + '\t' + mob['DamageMin'] + "\t" + mob['DamageMax'] + '\t' + mob['AttackSpeed'] + "\t" + mob['MovingSpeed'] + "\t" + mob['AggressiveHPPct'] + "\t" + mob['AggressiveSight']
        data = data + '\t' + mob['AttackRange'] + "\t" + mob['EnchantCurse'] + "\t" + mob['EnchantSlow'] + "\t" + mob['EnchantPoison'] + "\t" + mob['EnchantStun'] + "\t" + mob['EnchantCritical'] + "\t" + mob['EnchantPenetrate'] + "\t" + mob['ResistFist'] + "\t" + mob['ResistSword']
        data = data + '\t' + mob['ResistTwohand'] + "\t" + mob['ResistDagger'] + "\t" + mob['ResistBell'] + "\t" + mob['ResistFan']
        data = data + '\t' + mob['ResistBow'] + "\t" + mob['ResistClaw'] + "\t" + mob['ResistFire'] + "\t" + mob['ResistElect']
        data = data + '\t' + mob['ResistMagic'] + "\t" + mob['ResistWind'] + "\t" + mob['ResistEarth'] + "\t" + mob['ResistDark'] + "\t" + mob['ResistIce'] + "\t" +  mob['ResistPoison']
        data = data + '\t' + mob['ResistBleeding'] + "\t" + mob['AttElec'] + "\t" + mob['AttWind'] + "\t" + mob['AttFire'] + "\t" + mob['AttIce'] + "\t" + mob['AttDark'] + "\t" + mob['AttEarth']
        data = data + '\t' + mob['ResurrectionVnum'] + "\t" + mob['DropItemVnum'] + "\t" + mob['MountCapacity'] + "\t" + mob['OnClickType'] + "\t" + mob['Empire']
        data = data + '\t' + mob['Folder'] + "\t" + mob['DamMultiply'] + "\t" + mob['SummonVnum'] + "\t" + mob['DrainSP'] + "\t" + mob['MonsterColor'] + "\t" + mob['PolymorphItemVnum']
        data = data + '\t' + mob['SkillVnum0'] + "\t" + mob['SkillLevel0'] + "\t" + mob['SkillVnum1'] + "\t" + mob['SkillLevel1'] + "\t" + mob['SkillVnum2'] + "\t" + mob['SkillLevel2'] + "\t" + mob['SkillVnum3'] + "\t" + mob['SkillLevel3']
        data = data + '\t' + mob['BerserkPoint'] + "\t" + mob['StoneSkinPoint'] + "\t" + mob['GodSpeedPoint'] + "\t" + mob['DeathBlowPoint'] + "\t" + mob['RevivePoint'] + "\t" + mob['HealVnum'] + "\t" + mob['HitRange']
        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")

    fout = open("mob tradotti en.txt", "w")
    fout.write("VNUM\tNOME\t\t\tType\tRank\tBattleType\tLevel\tScalePct\tSize\tDropGoldMin\tDropGoldMax\tExperience\tMaxHP\tRegenCycle\tRegenPercent\tDefense\tAIFlags\tRaceFlag\tImmuneFlag\tStr\tDex\tCon\tInt\tDamageMin\tDamageMax\tAttackSpeed\tMovingSpeed\tAggressiveHPPct\tAggressiveSight\tAttackRange\tEnchantCurse\tEnchantSlow\tEnchantPoison\tEnchantStun\tEnchantCritical\tEnchantPenetrate\tResistFist\tResistSword\tResistTwohand\tResistDagger\tResistBell\tFesistFan\tResistBow\tResistClaw\tResistFire\tResistElect\tResistMagic\tResistWind\tResistEarth\tResistDark\tResistIce\tResistPoison\tResistBleeding\tAttElec\tAttWind\tAttFire\tAttIce\tAttDark\tAttEarth\tResurrectionVnum\tDropItemVnum\tMountCapacity\tOnClickType\tEmpire\tFolder\tDamMultiply\tSummonVnum\tDrainSP\tMonsterColor\tPolymorphItemVnum\tSkillVnum0\tSkillLevel0\tSkillVnum1\tSkillLevel1\tSkillVnum2\tSkillLevel2\tSkillVnum3\tSkillLevel3\tSkillVnum4\tSkillLevel4\tBerserkPoint\tStoneSkinPoint\tGodSpeedPoint\tDeathBlowPoint\tRevivePoint\tHealVnum\tHitRange\n")
    
    print("Ricerca Iniziata Mob EN Tradotti")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum_en):
        mob = proto.mob_data.mob_data_vnum_en[str(mob)]
        try:
            data = mob['vnum'] + '\t' + mob['name'] + proto.spazio(mob['name'])
            fout.write(data)
        except:
            data = mob['vnum'] + '\t' + "Errore nel Nome" + proto.spazio("Errore nel Nome")
            fout.write(data)
        data = '\t' + proto.get_mob_type(int(mob['Type']))[1] + '\t' + proto.get_mob_grade(int(mob['Rank']))[1] + '\t' + proto.get_mob_battle_type(int(mob['BattleType']))[1] 
        data = data + '\t' + mob['Level'] + '\t' + mob['ScalePct'] + '\t' + proto.get_mob_size(int(mob['Size']))[1] + "\t" + mob['DropGoldMin'] + "\t" + mob['DropGoldMax']
        data = data + '\t' + mob['Experience'] + '\t' + mob['MaxHP'] + '\t' + mob['RegenCycle'] + "\t" + mob['RegenPercent']
        data = data + '\t' + mob['Defense'] + '\t' + proto.get_mob_ai_flag(int(mob['AIFlags']))[1] + '\t' + proto.get_mob_race_flag(int(mob['RaceFlag']))[1] + '\t' + proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[1] + '\t' + mob['Str'] + "\t" + mob['Dex'] + "\t" + mob['Con'] + "\t" + mob['Int']
        data = data + '\t' + mob['DamageMin'] + "\t" + mob['DamageMax'] + '\t' + mob['AttackSpeed'] + "\t" + mob['MovingSpeed'] + "\t" + mob['AggressiveHPPct'] + "\t" + mob['AggressiveSight']
        data = data + '\t' + mob['AttackRange'] + "\t" + mob['EnchantCurse'] + "\t" + mob['EnchantSlow'] + "\t" + mob['EnchantPoison'] + "\t" + mob['EnchantStun'] + "\t" + mob['EnchantCritical'] + "\t" + mob['EnchantPenetrate'] + "\t" + mob['ResistFist'] + "\t" + mob['ResistSword']
        data = data + '\t' + mob['ResistTwohand'] + "\t" + mob['ResistDagger'] + "\t" + mob['ResistBell'] + "\t" + mob['ResistFan']
        data = data + '\t' + mob['ResistBow'] + "\t" + mob['ResistClaw'] + "\t" + mob['ResistFire'] + "\t" + mob['ResistElect']
        data = data + '\t' + mob['ResistMagic'] + "\t" + mob['ResistWind'] + "\t" + mob['ResistEarth'] + "\t" + mob['ResistDark'] + "\t" + mob['ResistIce'] + "\t" +  mob['ResistPoison']
        data = data + '\t' + mob['ResistBleeding'] + "\t" + mob['AttElec'] + "\t" + mob['AttWind'] + "\t" + mob['AttFire'] + "\t" + mob['AttIce'] + "\t" + mob['AttDark'] + "\t" + mob['AttEarth']
        data = data + '\t' + mob['ResurrectionVnum'] + "\t" + mob['DropItemVnum'] + "\t" + mob['MountCapacity'] + "\t" + mob['OnClickType'] + "\t" + mob['Empire']
        data = data + '\t' + mob['Folder'] + "\t" + mob['DamMultiply'] + "\t" + mob['SummonVnum'] + "\t" + mob['DrainSP'] + "\t" + mob['MonsterColor'] + "\t" + mob['PolymorphItemVnum']
        data = data + '\t' + mob['SkillVnum0'] + "\t" + mob['SkillLevel0'] + "\t" + mob['SkillVnum1'] + "\t" + mob['SkillLevel1'] + "\t" + mob['SkillVnum2'] + "\t" + mob['SkillLevel2'] + "\t" + mob['SkillVnum3'] + "\t" + mob['SkillLevel3']
        data = data + '\t' + mob['BerserkPoint'] + "\t" + mob['StoneSkinPoint'] + "\t" + mob['GodSpeedPoint'] + "\t" + mob['DeathBlowPoint'] + "\t" + mob['RevivePoint'] + "\t" + mob['HealVnum'] + "\t" + mob['HitRange']
        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")


def stampa_item_only_flag(self):
    fout = open("flag_item.txt", "w")
    fout.write("VNUM\tNOME\t\tANTI FLAG\tFLAG\tWEAR FLAG\tIMMUNE FLAG\n")
    
    print("Ricerca Iniziata Item Flag")

    for item_info in sorted(int(x) for x in proto.item_data.item_data_vnum):
        item_info = proto.item_data.item_data_vnum[str(item_info)]
        if (str(item_info['vnum']) != "0"):
            data = item_info['vnum'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        else:
            data = item_info['vnum'] + "~" + item_info['VnumRange'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        fout.write(data)
        data = '\t' + proto.get_anti_flag(int(item_info['AntiFlags']))[0] + '\t' + proto.get_item_flag(int(item_info['Flags']))[0]  + '\t' +  proto.get_wear_flag(int(item_info['WearFlags']))[0] + "\t" + proto.get_item_immune_flag(int(item_info['ImmuneFlags']))[0]

        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")

    fout = open("flag_item_en.txt", "w")
    fout.write("VNUM\tNOME\t\tANTI FLAG\tFLAG\tWEAR FLAG\tIMMUNE FLAG\n")
    
    print("Ricerca Iniziata Item EN Flag")

    for item_info in sorted(int(x) for x in proto.item_data.item_data_vnum_en):
        item_info = proto.item_data.item_data_vnum_en[str(item_info)]
        if (str(item_info['vnum']) != "0"):
            data = item_info['vnum'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        else:
            data = item_info['vnum'] + "~" + item_info['VnumRange'] + '\t' + item_info['name'] + proto.spazio(item_info['name'])
        fout.write(data)
        data = '\t' + proto.get_anti_flag(int(item_info['AntiFlags']))[0] + '\t' + proto.get_item_flag(int(item_info['Flags']))[0]  + '\t' +  proto.get_wear_flag(int(item_info['WearFlags']))[0] + "\t" + proto.get_item_immune_flag(int(item_info['ImmuneFlags']))[0]

        fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")


def stampa_mob_only_flag(self):
    fout = open("flag mob.txt", "w")
    fout.write("VNUM\tNOME\t\tANTI FLAG\tFLAG\tWEAR FLAG\tIMMUNE FLAG\n")
    
    print("Ricerca Iniziata Flag Mob")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum):
        mob = proto.mob_data.mob_data_vnum[str(mob)]
        ai_flag = proto.get_mob_ai_flag(int(mob['AIFlags']))[0]
        race_flag = proto.get_mob_race_flag(int(mob['RaceFlag']))[0]
        immune_flag = proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[0]
        try:
            if (proto.gestore_opzioni.get_option("TradMob") == 1):
                name = get_mob_name_it(mob['vnum'])
            else:
                name = mob['name']
            data = mob['vnum'] + '\t' + name + proto.spazio(name) +'\t' + ai_flag + '\t\t' + race_flag + '\t' + immune_flag
            fout.write(data + '\n')
        except:
            data = mob['vnum'] + '\t' + "Errore nel Nome" + proto.spazio("Errore nel Nome") +'\t' + ai_flag + '\t\t' + race_flag + '\t' + immune_flag
            fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")

    fout = open("flag mob en.txt", "w")
    fout.write("VNUM\tNOME\t\tANTI FLAG\tFLAG\tWEAR FLAG\tIMMUNE FLAG\n")
    
    print("Ricerca Iniziata Flag Mob EN")
    for mob in sorted(int(x) for x in proto.mob_data.mob_data_vnum_en):
        mob = proto.mob_data.mob_data_vnum_en[str(mob)]
        ai_flag = proto.get_mob_ai_flag(int(mob['AIFlags']))[0]
        race_flag = proto.get_mob_race_flag(int(mob['RaceFlag']))[0]
        immune_flag = proto.get_mob_immune_flag(int(mob['ImmuneFlag']))[0]
        try:
            data = mob['vnum'] + '\t' + mob['vnum'] + proto.spazio(mob['vnum']) +'\t' + ai_flag + '\t\t' + race_flag + '\t' + immune_flag
            fout.write(data + '\n')
        except:
            data = mob['vnum'] + '\t' + "Errore nel Nome" + proto.spazio("Errore nel Nome") +'\t' + ai_flag + '\t\t' + race_flag + '\t' + immune_flag
            fout.write(data + '\n')
        fout.flush()
    fout.close()
    print("Stampa Finita")

def get_all_item_info_by_name(name):
    data = []
    if (proto.gestore_opzioni.get_option("Platform") == 0):
        file =  proto.item_data.item_data_vnum
    else:
        file =  proto.item_data.item_data_vnum_en
    for item in file:
        item = file[item]
        if (name in item):
            if (item[name] not in data):
                data.append(str(item[name]))
    return sorted(data)

def get_all_mob_info_by_name(name):
    data = []
    if (proto.gestore_opzioni.get_option("Platform") == 0):
        file = proto.mob_data.mob_data_vnum
    else:
        file = proto.mob_data.mob_data_vnum_en
    for mob in file:
        mob = file[mob]
        if (name in mob):
            if (mob[name] not in data):
                data.append(str(mob[name]))
    return sorted(data)

def diff_item_proto():
    testo = QtWidgets.QFileDialog.getOpenFileName(None, "Seleziona item_proto_dump.xml", proto.cur_dir , "Xml (*.xml)")
    if (testo[0]):
        try:
            print("Inizio lettura item_proto xml")
            item = metin2Class.item_data(testo[0], testo[0])
        except Exception as er:
            print("Errore nell'analizzare il file")
            proto.err("Errore nell'analizzare il file" + str(er))
            proto.stampa_errore("Errore nell'analizzare il file" + str(er))
            return

        if (proto.gestore_opzioni.get_option("Platform") == 0):
            items = item.item_data_vnum
            file = proto.item_data.item_data_vnum
        else:
            items = item.item_data_vnum_en
            file = proto.item_data.item_data_vnum_en
            
        print("item_proto xml analizzato")
        
        fp = open("Differenze item_proto_dump.txt", "w")
        fp.write("Differenza tra Item")
        try:
            for vnum in sorted(int(x) for x in file):
                if (str(vnum) not in items):
                    print("ITEM RIMOSSO! Vnum: " + str(vnum) + "\tNome:" + str(file[str(vnum)]['name']))
                    fp.write("\nITEM RIMOSSO -> Vnum: " + str(vnum) + "\tNome:" + str(file[str(vnum)]['name']) + "\n")
                    fp.flush()
                    continue
                item = file[str(vnum)]
                #print("Analisi " + str(vnum))
                trovato = 0
                info = sorted(item.keys())
                info.remove('vnum')
                info.remove('name')
                for elem in info:
                    if (items[str(vnum)][elem] != item[elem]):
                        if (trovato == 0):
                            fp.write("\nVnum: " + str(vnum) + "\tNome:" + str(items[str(vnum)]['name']) + "\n")
                            fp.flush()
                            print("Differenza Trovata! Vnum: " + str(vnum) + "\tNome:" + str(items[str(vnum)]['name']))
                        trovato = 1
                        fp.write(str(elem) + ": " + str(item[elem]) + " --> " +  str(items[str(vnum)][elem]) + "\n")
                        fp.flush()
        except Exception as er:
            print("Errore nel confrontare i file")
            proto.err("Errore nelconfrontare i file" + str(er))
            proto.stampa_errore("Errore nelconfrontare i file" + str(er))
            return
        
        fp.write("\n\nNuovi Oggetti\n")
        for item_info in sorted(int(x) for x in items):
            if (str(item_info) not in file):
                item_info = items[str(item_info)]
                fp.write("Vnum: " + item_info['vnum'] + "\tNome: " + item_info['name']+ "\n")
                fp.flush()
                print("Nuovo Item! Vnum:  " + item_info['vnum'] + "\tNome:" + item_info['name'])
        fp.close()
        print("Stampa finita")

def diff_mob_proto():
    testo = QtWidgets.QFileDialog.getOpenFileName(None, "Seleziona mob_proto_dump.xml", proto.cur_dir , "Xml (*.xml)")
    if (testo[0]):
        try:
            mob = metin2Class.mob_data(testo[0], testo[0])
        except Exception as er:
            print("Errore nell'analizzare il file")
            proto.err("Errore nell'analizzare il file" + str(er))
            proto.stampa_errore("Errore nell'analizzare il file" + str(er))
            return
        
        if (proto.gestore_opzioni.get_option("Platform") == 0):
            mobs = mob.mob_data_vnum
            file = proto.mob_data.mob_data_vnum
        else:
            mobs = mob.mob_data_vnum_en
            file = proto.mob_data.mob_data_vnum_en

        fp = open("Differenze mob_proto_dump.txt", "w")
        fp.write("Differenza tra mob")
        for vnum in sorted(int(x) for x in file):
            mob = file[str(vnum)]
            trovato = 0
            info = sorted(mob.keys())
            info.remove('vnum')
            info.remove('name')
            for elem in info:
                if (mobs[str(vnum)][elem] != mob[elem]):
                    if (trovato == 0):
                        fp.write("\nVnum: " + str(vnum) + "\tNome:" + str(mobs[str(vnum)]['name']) + "\n")
                        fp.flush()
                        print("Differenza Trovata! Vnum: " + str(vnum) + "\tNome:" + str(mobs[str(vnum)]['name']))
                    trovato = 1
                    fp.write(str(elem) + ": " + mob[elem] + " --> " + mobs[str(vnum)][elem] + "\n")
                    fp.flush()
                    
        
        fp.write("\n\nNuovi mob\n")
        for mob_info in sorted(int(x) for x in mobs):
            if (str(mob_info) not in file):
                mob_info = mobs[str(mob_info)]
                fp.write("Vnum: " + mob_info['vnum'] + "\tNome: " + mob_info['name'] + "\n")
                fp.flush()
                print("Nuovo Mob! Vnum:  " + mob_info['vnum'] + "\tNome:" + mob_info['name'])
        fp.close()
        print("Stampa finita")

def open_info():
    QtWidgets.QMessageBox.information(None, "Info", INFO)

def open_info_aiuto(self):
    self.HelpWidget = widget_aiuto_flag(self)
    self.HelpWidget.setWindowIcon(QtGui.QIcon("images/Warframe.ico"))
    self.HelpWidget.setWindowTitle('Info sui Dati')
    self.HelpWidget.show()

def widget_aiuto_flag(self):
    HelpWidget = QtWidgets.QWidget()

    self.HelpGrid = QtWidgets.QGridLayout(HelpWidget)

    TipoInfo = QtWidgets.QLabel("Informazioni su:")
    self.ComboBoxHelp = QtWidgets.QComboBox(HelpWidget)
    self.ComboBoxHelp.addItem("Item\t")
    self.ComboBoxHelp.addItem("Mostri\t")

    self.ComboBoxTipoHelp = QtWidgets.QComboBox(HelpWidget)
    self.ComboBoxSottoTipoHelp = QtWidgets.QComboBox(HelpWidget)

    TipoInfo.setAlignment(QtCore.Qt.AlignLeft)
    self.ComboBoxHelp.setSizeAdjustPolicy(0)#AdjustToContents
    self.ComboBoxTipoHelp.setSizeAdjustPolicy(0)#AdjustToContents
    self.ComboBoxSottoTipoHelp.setSizeAdjustPolicy(0)#AdjustToContents

    self.ComboBoxTipoHelp.addItem("Tipo")
    self.ComboBoxTipoHelp.addItem("Maschera")
    self.ComboBoxTipoHelp.addItem("Anti Flag")
    self.ComboBoxTipoHelp.addItem("Flag")
    self.ComboBoxTipoHelp.addItem("Wear Flag")
    self.ComboBoxTipoHelp.addItem("Flag Immunita'")
    self.ComboBoxTipoHelp.addItem("Restrizione")
    self.ComboBoxTipoHelp.addItem("Bonus")
    self.ComboBoxTipoHelp.addItem("Attacco Fisico")
    self.ComboBoxTipoHelp.addItem("Attacco Magico")
    self.ComboBoxTipoHelp.addItem("Difesa")
    self.ComboBoxTipoHelp.addItem("Set Up")

#    for i in range(0, len(ITEM_SUB_TYPE[ITEM_TYPE[self.ComboBoxTipoItem.currentIndex()][0]].keys())):
#        self.ComboBoxSottoTipoItem.addItem(ITEM_SUB_TYPE[ITEM_TYPE[self.ComboBoxTipoItem.currentIndex()][0]][i][1])

    self.ComboBoxHelp.currentIndexChanged[str].connect(lambda: change_combo_box_help(self))
    self.ComboBoxTipoHelp.currentIndexChanged[str].connect(lambda: change_combo_box_tipo_help(self))
    self.ComboBoxSottoTipoHelp.currentIndexChanged[str].connect(lambda: cerca_help_by_combobox(self))


    self.TextHelp = QtWidgets.QLabel("\n\n\n\n\n\n\n\n")

    HelpWidget.setLayout(self.HelpGrid)


    self.HelpGrid.addWidget(TipoInfo, 0, 0)
    self.HelpGrid.addWidget(self.ComboBoxHelp, 0, 1)
    self.HelpGrid.addWidget(self.ComboBoxTipoHelp, 0, 2)
    self.HelpGrid.addWidget(self.ComboBoxSottoTipoHelp, 0, 3)
    self.HelpGrid.addWidget(self.TextHelp, 1, 0, 1, 4)

    self.HelpGrid.setAlignment(QtCore.Qt.AlignTop)

    return HelpWidget

def change_combo_box_help(self):
    IndexTipo = self.ComboBoxHelp.currentIndex()

    if (IndexTipo == 0):    #Item
        self.ComboBoxTipoHelp.clear()
        self.ComboBoxTipoHelp.addItem("Tipo")
        self.ComboBoxTipoHelp.addItem("Maschera")
        self.ComboBoxTipoHelp.addItem("Anti Flag")
        self.ComboBoxTipoHelp.addItem("Flag")
        self.ComboBoxTipoHelp.addItem("Wear Flag")
        self.ComboBoxTipoHelp.addItem("Flag Immunita'")
        self.ComboBoxTipoHelp.addItem("Restrizione")
        self.ComboBoxTipoHelp.addItem("Bonus")
        self.ComboBoxTipoHelp.addItem("Attacco Fisico")
        self.ComboBoxTipoHelp.addItem("Attacco Magico")
        self.ComboBoxTipoHelp.addItem("Difesa")
        self.ComboBoxTipoHelp.addItem("Set Up")
    elif (IndexTipo == 1):  # Mob
        self.ComboBoxTipoHelp.clear()
        self.ComboBoxTipoHelp.addItem("Tipo Attacco")
        self.ComboBoxTipoHelp.addItem("Flag AI")
        self.ComboBoxTipoHelp.addItem("Flag Razza")
        self.ComboBoxTipoHelp.addItem("Flag Immunita'")
    else:                   #Errore
        pass

def change_combo_box_tipo_help(self):
    pass
                
