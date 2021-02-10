#!/usr/bin/python
# -*- coding: utf-8 -*-

UPDATE_SITE = "http://deathmt2.altervista.org/metin2/"
VNUM_PARSER = r'Vnum="(\d*)"?'
NAME_PARSER = r'LocalizedName="([\w\s\'\?\.\+\-\(\)\\\/:,`%±©¸¹·´£®½º¶º¼øÆ¯³­¿°»¢¥]*)"?'
DATA_PARSER = r'="([\d\.-]*)"?'
FOLDER_PARSER = r'Folder="([\w\s\'\?\._]*)"?'
MULT_PARSER = r'DamMultiply="([\d\.]*)"?'

#Item Type
ITEM_TYPE = {
                0: ("ITEM_NONE",        "Nessuno"),
                1: ("ITEM_WEAPON",      "Arma"),
                2: ("ITEM_ARMOR",       "Armatura"),
                3: ("ITEM_USE",         "Usabile"),
                4: ("ITEM_AUTOUSE",     "Auto Uso"),
                5: ("ITEM_MATERIAL",    "Materiale"),
                6: ("ITEM_SPECIAL",     "Speciale"),
                7: ("ITEM_TOOL",        "Strumento"),
                8: ("ITEM_LOTTERY",     "Biglietto Lotteria"),
                9: ("ITEM_ELK",         "Moneta"),
                10:("ITEM_METIN",       "Pietre Spirituali"),
                11:("ITEM_CONTAINER",   "Contenitore"),
                12:("ITEM_FISH",        "Pesce"),
                13:("ITEM_ROD",         "Canna da Pesca"),
                14:("ITEM_RESOURCE",    "Risorse"),
                15:("ITEM_CAMPFIRE",    "Falo'"),
                16:("ITEM_UNIQUE",      "Item Unico"),
                17:("ITEM_SKILLBOOK",   "Libro Abilita'"), 
                18:("ITEM_QUEST",       "Item con Quest"),
                19:("ITEM_POLYMORPH",   "Oggetto Trasformazione"),
                20:("ITEM_TREASURE_BOX","Forziere con Chiave"), 
                21:("ITEM_TREASURE_KEY","Chiave Forziere"),
                22:("ITEM_SKILLFORGET", "Libro Amnesia"),
                23:("ITEM_GIFTBOX",     "Contenitore"),
                24:("ITEM_PICK",        "Piccone"),
                25:("ITEM_HAIR",        "ITEM_HAIR"),
                26:("ITEM_TOTEM",       "ITEM_TOTEM"),
                27:("ITEM_BLEND",       "Rugiada"),
                28:("ITEM_COSTUME",     "Costume"),
                29:("ITEM_DS",          "Pietra del Drago"),
                30:("ITEM_SPECIAL_DS",  "ITEM_SPECIAL_DS"),
                31:("ITEM_EXTRACT",     "Estrazione Pietra del Drago"),
                32:("ITEM_SECONDARY_COIN","ITEM_SECONDARY_COIN"),
                33:("ITEM_RING",        "ITEM_RING"),
                34:("ITEM_BELT",        "Cintura"),
                35:("ITEM_PET",         "Pet"),     #aggiunto da me
                36:("ITEM_MEDIUM",      "Trasferisci Bonus"), #aggiunto da me (Aggiungi Bonus Costumi)
                37:("ITEM_GACHA",       "Forziere Multi Apribile"), #aggiunto da me
                38:("ITEM_SOUL",        "Anima"), #aggiunto da me
              }

#Nessun Sub Type
SUB_TYPE_NONE = {
                0: ("NONE", "Niente"),
                }

#Sub Type Weapon
SUB_TYPE_WEAPON = {
                    0:("WEAPON_SWORD",      "Spada"),
                    1:("WEAPON_DAGGER",     "Pugnale"),
                    2:("WEAPON_BOW",        "Arco"),
                    3:("WEAPON_TWO_HANDED", "Spadone"),
                    4:("WEAPON_BELL",       "Campana"),
                    5:("WEAPON_FAN",        "Ventaglio"),
                    6:("WEAPON_ARROW",      "Freccia"),
                    7:("WEAPON_MOUNT_SPEAR","Lancia per Cavallo"),
                    8:("WEAPON_CLAW",       "Artiglio"),
                    9:("WEAPON_QUIVER",     "Faretra"),
                    10:("WEAPON_WEDDING",   "Mazzo di Fiori"),
                    }

#Sub Type Armour 
SUB_TYPE_ARMOR = {
                    0:("ARMOR_BODY",        "Armatura"),
                    1:("ARMOR_HEAD",        "Elmo"),
                    2:("ARMOR_SHIELD",      "Scudo"),
                    3:("ARMOR_WRIST",       "Bracciale"),
                    4:("ARMOR_FOOTS",       "Scarpe"),
		    5:("ARMOR_NECK",        "Collana"),
                    6:("ARMOR_EAR",         "Orecchini"),
                    7:("ARMOR_PENDANT",     "Talismano"),
                }

#Sub Type Use
SUB_TYPE_USE = {
                  0: ("USE_POTION",                 "Pozione"),
                  1: ("USE_TALISMAN",               "Papiro del Luogo"),
                  2: ("USE_TUNING",                 "Per Up"),
                  3: ("USE_MOVE",                   "USE_MOVE"),
                  4: ("USE_TREASURE_BOX",           "USE_TREASURE_BOX"),
                  5: ("USE_MONEYBAG",               "USE_MONEYBAG"),
                  6: ("USE_BAIT",                   "Esca"),
                  7: ("USE_ABILITY_UP",             "Potenzia Statistiche"),
                  8: ("USE_AFFECT",                 "Potenzia Statistiche con HUD"),
                  9: ("USE_CREATE_STONE",           "Crea Pietre"),
                  10: ("USE_SPECIAL",               "Uso Speciale"),
                  11: ("USE_POTION_NODELAY",        "Pozione Istantanea"),
                  12: ("USE_CLEAR",                 "Rimuove Effetti Negativi"),
                  13: ("USE_INVISIBILITY",          "Rende Invisibile"),
                  14: ("USE_DETACHMENT",            "Rimuove Pietre"),
                  15: ("USE_BUCKET",                "Riempibile"),
                  16: ("USE_POTION_CONTINUE",       "USE_POTION_CONTINUE"),
                  17: ("USE_CLEAN_SOCKET",          "Togli Schegge"),
                  18: ("USE_CHANGE_ATTRIBUTE",      "Cambia Bonus"),
                  19: ("USE_ADD_ATTRIBUTE",         "Aggiunge Bonus"),
                  20: ("USE_ADD_ACCESSORY_SOCKET",  "Aggiunge Socket"),
                  21: ("USE_PUT_INTO_ACCESSORY_SOCKET","Riempe Socket Gioielli"),
                  22: ("USE_ADD_ATTRIBUTE2",        "Aggiungi Bonus 5+"),
                  23: ("USE_RECIPE",                "Ricetta"),
                  24: ("USE_CHANGE_ATTRIBUTE2",     "USE_CHANGE_ATTRIBUTE2"),
                  25: ("USE_BIND",                  "USE_BIND"),
                  26: ("USE_UNBIND",                "USE_UNBIND"),
                  27: ("USE_TIME_CHARGE_PER",       "Ricarica Pietra del Drago %"),
                  28: ("USE_TIME_CHARGE_FIX",       "Ricarica Pietra del Drago Fissa"),
                  29: ("USE_PUT_INTO_BELT_SOCKET",  "Riempe Socket Cintura"),
                  30: ("USE_PUT_INTO_RING_SOCKET",  "USE_PUT_INTO_RING_SOCKET"),
                  31: ("USE_CHANGE_COSTUME_ATTR",   "Cambia Bonus Costume"),
                  32: ("USE_RESET_COSTUME_ATTR",    "Cambia/Aggiunge Bonus Costume"),
                  33: ("USE_NOT_USED33",            "NOT_USED33"),
                  34: ("USE_CHANGE_BONUS_PREVIEW",  "Cambia Bonus e Anteprima"),
                  35: ("USE_FLOWER_SEED",           "Germogli Fiori"),
                  255:("USE_EMOTION",               "Sacca Emozioni"),#aggiunto da me
                  }

# USE_POTION_TOWER
# USE_POTION_NODELAY_TOWER

#Sub Type Auto Use
SUB_TYPE_AUTOUSE = {
                      0: ("AUTOUSE_POTION",         "AUTOUSE_POTION"),
                      1: ("AUTOUSE_ABILITY_UP",     "AUTOUSE_ABILITY_UP"),
                      2: ("AUTOUSE_BOMB",           "AUTOUSE_BOMB"),
                      3: ("AUTOUSE_GOLD",           "AUTOUSE_GOLD"),
                      4: ("AUTOUSE_MONEYBAG",       "AUTOUSE_MONEYBAG"),
                      5: ("AUTOUSE_TREASURE_BOX",   "AUTOUSE_TREASURE_BOX"),
                      }

#Sub Type Material
SUB_TYPE_MATERIAL = {
                      0: ("MATERIAL_LEATHER",           "Materiale"),
                      1: ("MATERIAL_BLOOD",             "MATERIAL_BLOOD"),
                      2: ("MATERIAL_ROOT",              "MATERIAL_ROOT"),
                      3: ("MATERIAL_NEEDLE",            "MATERIAL_NEEDLE"),
                      4: ("MATERIAL_JEWEL",             "MATERIAL_JEWEL"),
                      5: ("MATERIAL_DS_REFINE_NORMAL",  "Raff. Normale Pietre del Drago"),
                      6: ("MATERIAL_DS_REFINE_BLESSED", "Raff. Medio Pietre del Drago"),
                      7: ("MATERIAL_DS_REFINE_HOLLY",   "Raff. Grande Pietre del Drago"),
                      8: ("MATERIAL_DS_CHANGE_ATTR",    "Cambia Bonus Pietra del Drago"),
                    }

#Sub Type Special
SUB_TYPE_SPECIAL = {
                      0: ("SPECIAL_MAP",        "Speciale"),
                      1: ("SPECIAL_KEY",        "SPECIAL_KEY"),
                      2: ("SPECIAL_DOC",        "SPECIAL_DOC"),
                      3: ("SPECIAL_SPIRIT",     "SPECIAL_SPIRIT"),
                      }

#Sub Type Tool
SUB_TYPE_TOOL = {
                0: ("TOOL_FISHING_ROD", "Canna da Pesca"),
                }
                

#Sub Type Lottery
SUB_TYPE_LOTTERY = {
                     0: ("LOTTERY_TICKET",  "Biglietto Lotteria"),
                     1: ("LOTTERY_INSTANT", "LOTTERY_INSTANT"),
                    }

#Sub Type Metin
SUB_TYPE_METIN = {
                  0: ("METIN_NORMAL",   "Normali"),
                  1: ("METIN_GOLD",     "METIN_GOLD"),
                  }

#Sub Type Fish
SUB_TYPE_FISH = {
                  0: ("FISH_ALIVE", "Pesce Vivo"),
                  1: ("FISH_DEAD",  "Pesce Morto"),
                 }

#Sub Type Resource
SUB_TYPE_RESOURCE = {
                    0: ("RESOURCE_FISHBONE",        "Lisca"),
                    1: ("RESOURCE_WATERSTONEPIECE", "Pezzo di Pietra"),
                    2: ("RESOURCE_WATERSTONE",      "Pietra Acquatica"),
                    3: ("RESOURCE_BLOOD_PEARL",     "Perla Rossa"),
                    4: ("RESOURCE_BLUE_PEARL",      "Perla Blu"),
                    5: ("RESOURCE_WHITE_PEARL",     "Perla Bianco"),
                    6: ("RESOURCE_BUCKET",          "Bottiglia Vuota"),
                    7: ("RESOURCE_CRYSTAL",         "Cristallo"),
                    8: ("RESOURCE_GEM",             "Pietra Preziosa"),
                    9: ("RESOURCE_STONE",           "Pietra Acquatica 2"),
                    10:("RESOURCE_METIN",           "Pietra Spirituale"),
                    11:("RESOURCE_ORE",             "Minerale"),
                    12:("RESOURCE_AURA",            "Runa"),
                    }

#Sub Type Unique
SUB_TYPE_UNIQUE = {
                    0: ("UNIQUE_NONE",          "Nessuno"),
                    1: ("UNIQUE_BOOK",          "UNIQUE_BOOK"),
                    2: ("UNIQUE_SPECIAL_RIDE",  "UNIQUE_SPECIAL_RIDE"),
                    3: ("UNIQUE_3",             "UNIQUE_3"),
                    4: ("UNIQUE_4",             "UNIQUE_4"),
                    5: ("UNIQUE_5",             "UNIQUE_5"),
                    6: ("UNIQUE_6",             "UNIQUE_6"),
                    7: ("UNIQUE_7",             "UNIQUE_7"),
                    8: ("UNIQUE_8",             "UNIQUE_8"),
                    9: ("UNIQUE_9",             "UNIQUE_9"),
                    10:("USE_SPECIAL",          "Uso Speciale"),
                    }
#Sub Type Quest
SUB_TYPE_QUEST = {
                    0: ("QUEST_NONE",       "Item Missioni"),
                    1: ("QUEST_PET_PAY",    "Sigillo Pet"),
                }
  

#Sub Type Costume
SUB_TYPE_COSTUME = {
                    0:("COSTUME_BODY",      "Armatura"),
                    1:("COSTUME_HAIR",      "Capigliatura"),
                    2:("COSTUME_MOUNT",     "Cavalcatura"),
                    3:("COSTUME_ACCE",      "Stola"),
                    4:("COSTUME_WEAPON",    "Arma"),
                    5:("COSTUME_AURA",      "Veste Aura"),
                    }

#Sub Type DS
SUB_TYPE_DS = {
                0: ("DS_SLOT1", "Diamante"),
                1: ("DS_SLOT2", "Rubino"),
                2: ("DS_SLOT3", "Giada"),
                3: ("DS_SLOT4", "Zaffiro"),
                4: ("DS_SLOT5", "Granato"),
                5: ("DS_SLOT6", "Onice"),
                }

#Sub Type Extract
SUB_TYPE_EXTRACT = {
                    0: ("EXTRACT_DRAGON_SOUL",  "Estrae Pietra del Drago"),
                    1: ("EXTRACT_DRAGON_HEART", "Estrae Durata Pietra del Drago"),
                    }

#Sub Type Pet
SUB_TYPE_PET = {
                 0: ("PET_EGG",                 "Uovo"),
                 1: ("PET_UPBRINGING",          "Sigillo"),
                 2: ("PET_BAG",                 "Trasportino"),
                 3: ("PET_FEEDSTUFF",           "Boccone Proteico"),
                 4: ("PET_SKILL",               "Libro Abilita' Pet"),
                 5: ("PET_SKILL_DEL_BOOK",      "Reset Abilita' Pet"),
                 6: ("PET_NAME_CHANGE",         "Cambio Nome Pet"),
                 7: ("PET_EXPFOOD",             "Leccornia"),
                 8: ("PET_SKILL_ALL_DEL_BOOK",  "Reset Tutte Skill Pet"),
                 9: ("PET_EXPFOOD_PERC",        "Leccornia+"),
                 10:("PET_DETERMINE",           "Controllo Pet"),
                 11:("PET_ATTR_CHANGE",         "Cambia Tipo Pet"),
                 12:("PET_PAY",                 "Pet Vecchio"), #aggiunto da me
                 13:("PET_PREMIUM_FEEDSTUFF",   "Boccone Proteico Divino"),
                 }

#Sub Type Medium (Trasferisci Bonus)
SUB_TYPE_MEDIUM = {
                0: ("MEDIUM_MOVE_COSTUME_ATTR",         "Trasferisci Bonus Costume"),
                1: ("MEDIUM_MOVE_COSTUME_ACCE_ATTR",    "Trasferisci Bonus Stola"),
                }

#Sub Type Soul
SUB_TYPE_GACHA = {
                0:  ("GACHA_NONE",              "Niente"),
                1:  ("GACHA_LUCKY_BOX",         "Forziere"),            #Cassa Fortuna Blu
                2:  ("GACHA_SPECIAL_LUCKY_BOX", "Forziere Speciale"),   #Cassa Fortuna Rossa e Verde
                }
                
#Sub Type Soul
SUB_TYPE_SOUL ={ 
                0: ("RED_SOUL",     "Anima Onirica"),
                1: ("BLUE_SOUL",    "Anima Celestiale"),
                  } 

ITEM_SUB_TYPE = {
                "ITEM_NONE" : SUB_TYPE_NONE,
                "ITEM_WEAPON" : SUB_TYPE_WEAPON,
                "ITEM_ARMOR" : SUB_TYPE_ARMOR,
                "ITEM_USE" : SUB_TYPE_USE,
                "ITEM_AUTOUSE" : SUB_TYPE_AUTOUSE,
                "ITEM_MATERIAL": SUB_TYPE_MATERIAL,
                "ITEM_SPECIAL": SUB_TYPE_SPECIAL,
                "ITEM_TOOL" : SUB_TYPE_TOOL,
                "ITEM_LOTTERY" : SUB_TYPE_LOTTERY,
                "ITEM_ELK" : SUB_TYPE_NONE,
                "ITEM_METIN" : SUB_TYPE_METIN,
                "ITEM_CONTAINER" : SUB_TYPE_NONE,
                "ITEM_FISH": SUB_TYPE_FISH,
                "ITEM_ROD" : SUB_TYPE_NONE,
                "ITEM_RESOURCE" : SUB_TYPE_RESOURCE,
                "ITEM_CAMPFIRE" : SUB_TYPE_NONE,
                "ITEM_UNIQUE" : SUB_TYPE_UNIQUE,
                "ITEM_SKILLBOOK" : SUB_TYPE_NONE, 
                "ITEM_QUEST" : SUB_TYPE_QUEST,
                "ITEM_POLYMORPH" : SUB_TYPE_NONE,
                "ITEM_TREASURE_BOX" : SUB_TYPE_NONE,
                "ITEM_TREASURE_KEY" : SUB_TYPE_NONE,
                "ITEM_SKILLFORGET" : SUB_TYPE_NONE,
                "ITEM_GIFTBOX" : SUB_TYPE_NONE,
                "ITEM_PICK" : SUB_TYPE_NONE,
                "ITEM_HAIR" : SUB_TYPE_NONE,
                "ITEM_TOTEM" : SUB_TYPE_NONE,
                "ITEM_BLEND" : SUB_TYPE_NONE,
                "ITEM_COSTUME": SUB_TYPE_COSTUME,
                "ITEM_DS" : SUB_TYPE_DS,
                "ITEM_SPECIAL_DS": SUB_TYPE_NONE,
                "ITEM_EXTRACT" : SUB_TYPE_EXTRACT,
                "ITEM_SECONDARY_COIN" : SUB_TYPE_NONE,
                "ITEM_RING" : SUB_TYPE_NONE,
                "ITEM_BELT": SUB_TYPE_NONE,
                "ITEM_PET": SUB_TYPE_PET,
                "ITEM_MEDIUM" : SUB_TYPE_MEDIUM,
                "ITEM_GACHA": SUB_TYPE_GACHA,
                "ITEM_SOUL" : SUB_TYPE_SOUL,
              }

#Mask Type
ITEM_MASK_TYPE = {
                0: ("MASK_ITEM_TYPE_NONE",              "Nessuna Maschera"),
                1: ("MASK_ITEM_TYPE_MOUNT_PET",         "Maschera Cavalcatura"),
                2: ("MASK_ITEM_TYPE_EQUIPMENT_WEAPON",  "Maschera Arma"),
                3: ("MASK_ITEM_TYPE_EQUIPMENT_ARMOR",   "Maschera Armatura"),
                4: ("MASK_ITEM_TYPE_EQUIPMENT_JEWELRY", "Maschera Gioiello"),
                5: ("MASK_ITEM_TYPE_TUNING",            "Maschera Miglioramento Item"),
                6: ("MASK_ITEM_TYPE_POTION",            "Maschera Pozione"),
                7: ("MASK_ITEM_TYPE_FISHING_PICK",      "Maschera Pesci/Minerali"),
                8: ("MASK_ITEM_TYPE_DRAGON_STONE",      "Maschera Pietra del Drago"),
                9: ("MASK_ITEM_TYPE_COSTUMES",          "Maschera Costumi"),
                10:("MASK_ITEM_TYPE_SKILL",             "Maschera Abilita'"),
                11:("MASK_ITEM_TYPE_UNIQUE",            "Maschera Item Unico"),
                12:("MASK_ITEM_TYPE_ETC",               "Maschera Altro"),
              }

#Nessuna Maschera
ITEM_MASK_SUB_TYPE_NONE = {
                            0: ("NONE",     "Nessuna"),
                          }

#Mask Sub Type Mount
ITEM_MASK_SUB_TYPE_MOUNT = {
                            0: ("MASK_ITEM_SUBTYPE_MOUNT_PET_MOUNT",        "Cavalcatura"),
                            1: ("MASK_ITEM_SUBTYPE_MOUNT_PET_CHARGED_PET",  "Cavalcatura Potenziata"),
                            2: ("MASK_ITEM_SUBTYPE_MOUNT_PET_FREE_PET",     "Pet"),
                            3: ("MASK_ITEM_SUBTYPE_MOUNT_PET_EGG",          "Uovo"),
                            }

#Mask Sub Type Weapon
ITEM_MASK_SUB_TYPE_WEAPON = {
                            0: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_SWORD",    "Spada"),
                            1: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_DAGGER",   "Pugnale"),
                            2: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_BOW",      "Arco"),
                            3: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_TWO_HANDED","Spadone"),
                            4: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_BELL",     "Campana"),
                            5: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_CLAW",     "Artiglio"),
                            6: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_FAN",      "Ventaglio"),
                            7: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_MOUNT_SPEAR","Lancia da Cavallo"),
                            8: ("MASK_ITEM_SUBTYPE_WEAPON_WEAPON_ARROW",    "Freccia"),
                        }

#Mask Sub Type Armor
ITEM_MASK_SUB_TYPE_ARMOR = {0: ("MASK_ITEM_SUBTYPE_ARMOR_ARMOR_BODY",   "Armatura"),
                            1: ("MASK_ITEM_SUBTYPE_ARMOR_ARMOR_HEAD",   "Elmo"),
                            2: ("MASK_ITEM_SUBTYPE_ARMOR_ARMOR_SHIELD", "Scudo"),
                            }

#Mask Sub Type Jewel
ITEM_MASK_SUB_TYPE_JEWEL = {0: ("MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_WRIST",    "Gioiello Polso"),
                            1: ("MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_FOOTS",    "Gioiello Scarpe"),
                            2: ("MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_NECK",     "Gioiello Collo"),
                            3: ("MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_EAR",      "Gioiello Orecchie"),
                            4: ("MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_BELT",     "Gioiello Cintura"),
                            5: ("MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_PENDANT",  "Gioiello Talismano"),
                            }

#Mask Sub Type Tuning
ITEM_MASK_SUB_TYPE_TUNING = {
                            0: ("MASK_ITEM_SUBTYPE_TUNING_RESOURCE",    "Materiale Potenziamento"),
                            1: ("MASK_ITEM_SUBTYPE_TUNING_STONE",       "Pietra Spirituale"),
                            2: ("MASK_ITEM_SUBTYPE_TUNING_ETC",         "Potenziamento Altro"),
                             }

#Mask Sub Type Potion
ITEM_MASK_SUB_TYPE_POTION = {0: ("MASK_ITEM_SUBTYPE_POTION_ABILITY",    "Pozione"),
                             1: ("MASK_ITEM_SUBTYPE_POTION_HAIRDYE",    "Decolorante"),
                             2: ("MASK_ITEM_SUBTYPE_POTION_ETC",        "Pozione Altro"),
                             }

#Mask Sub Type Fishing
ITEM_MASK_SUB_TYPE_FISHING = {
                            0: ("MASK_ITEM_SUBTYPE_FISHING_PICK_FISHING_POLE",  "Canna da Pesca"),
                            1: ("MASK_ITEM_SUBTYPE_FISHING_PICK_EQUIPMENT_PICK","Piccone"),
                            2: ("MASK_ITEM_SUBTYPE_FISHING_PICK_FOOD",          "Pesce"),
                            3: ("MASK_ITEM_SUBTYPE_FISHING_PICK_STONE",         "Minerale"),
                            4: ("MASK_ITEM_SUBTYPE_FISHING_PICK_ETC",           "Altro Pesca"),
                            }

#Mask Sub Type Dragon Stone
ITEM_MASK_SUB_TYPE_DRAGON_STONE = {
                                0: ("MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_DIAMOND",    "Pietra Diamante"),
                                1: ("MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_RUBY",       "Pietra Rubino"),
                                2: ("MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_JADE",       "Pietra Giada"),
                                3: ("MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_SAPPHIRE",   "Pietra Zaffiro"),
                                4: ("MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_GARNET",     "Pietra Granato"),
                                5: ("MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_ONYX",       "Pietra Onice"),
                                6: ("MASK_ITEM_SUBTYPE_DRAGON_STONE_ETC",               "Pietra Altro"),
                                }

#Mask Sub Type Costume Originale
ITEM_MASK_SUB_TYPE_COSTUME = {
                            0: ("MASK_ITEM_SUBTYPE_COSTUMES_COSTUME_WEAPON",    "Costume Arma"),
                            1: ("MASK_ITEM_SUBTYPE_COSTUMES_COSTUME_BODY",      "Costume Armatura"),
                            2: ("MASK_ITEM_SUBTYPE_COSTUMES_COSTUME_HAIR",      "Costume Capigliatura"),
                            3: ("MASK_ITEM_SUBTYPE_COSTUMES_SASH",              "Costume Stola"),
                            4: ("MASK_ITEM_SUBTYPE_COSTUMES_ETC",               "Costume Altro"),
                            5: ("MASK_ITEM_SUBTYPE_COSTUMES_AURA",              "Item di Modifica"),
                                }

#Mask Sub Type Skill
ITEM_MASK_SUB_TYPE_SKILL = {
                            0: ("MASK_ITEM_SUBTYPE_SKILL_PAHAE",            "Baule Skill"),
                            1: ("MASK_ITEM_SUBTYPE_SKILL_SKILL_BOOK",       "Libro Abilita'"),
                            2: ("MASK_ITEM_SUBTYPE_SKILL_BOOK_OF_OBLIVION", "Libro Amnesia"),
                            3: ("MASK_ITEM_SUBTYPE_SKILL_ETC",              "Altro"),
                            }

#Mask Sub Type Skill
ITEM_MASK_SUB_TYPE_UNIQUE = {
                        0: ("MASK_ITEM_SUBTYPE_UNIQUE_ABILITY", "Abilita'"),
                        1: ("MASK_ITEM_SUBTYPE_UNIQUE_ETC",     "Altro"),
                             }

#Mask Sub Type Etc
ITEM_MASK_SUB_TYPE_ETC = {
                        0: ("MASK_ITEM_SUBTYPE_ETC_GIFTBOX",    "Forziere"),
                        1: ("MASK_ITEM_SUBTYPE_ETC_MATRIMORY",  "Matrimonio"),
                        2: ("MASK_ITEM_SUBTYPE_ETC_EVENT",      "Evento"),
                        3: ("MASK_ITEM_SUBTYPE_ETC_SEAL",       "Legame"),
                        4: ("MASK_ITEM_SUBTYPE_ETC_PARTI",      "Libri"),
                        5: ("MASK_ITEM_SUBTYPE_ETC_POLYMORPH",  "Sfera Trasformazione"),
                        6: ("MASK_ITEM_SUBTYPE_ETC_RECIPE",     "Materiale Pozioni"),
                        7: ("MASK_ITEM_SUBTYPE_ETC_ETC",        "Altro"),
                        }

#Mask Sub Type
ITEM_SUB_MASK_TYPE = {
                        "MASK_ITEM_TYPE_NONE": ITEM_MASK_SUB_TYPE_NONE,
                        "MASK_ITEM_TYPE_MOUNT_PET": ITEM_MASK_SUB_TYPE_MOUNT,
                        "MASK_ITEM_TYPE_EQUIPMENT_WEAPON": ITEM_MASK_SUB_TYPE_WEAPON,
                        "MASK_ITEM_TYPE_EQUIPMENT_ARMOR": ITEM_MASK_SUB_TYPE_ARMOR,
                        "MASK_ITEM_TYPE_EQUIPMENT_JEWELRY": ITEM_MASK_SUB_TYPE_JEWEL,
                        "MASK_ITEM_TYPE_TUNING": ITEM_MASK_SUB_TYPE_TUNING,
                        "MASK_ITEM_TYPE_POTION": ITEM_MASK_SUB_TYPE_POTION,
                        "MASK_ITEM_TYPE_FISHING_PICK": ITEM_MASK_SUB_TYPE_FISHING,
                        "MASK_ITEM_TYPE_DRAGON_STONE": ITEM_MASK_SUB_TYPE_DRAGON_STONE,
                        "MASK_ITEM_TYPE_COSTUMES": ITEM_MASK_SUB_TYPE_COSTUME,
                        "MASK_ITEM_TYPE_SKILL": ITEM_MASK_SUB_TYPE_SKILL,
                        "MASK_ITEM_TYPE_UNIQUE": ITEM_MASK_SUB_TYPE_UNIQUE,
                        "MASK_ITEM_TYPE_ETC": ITEM_MASK_SUB_TYPE_ETC,
                        }

#Anti Flag
ITEM_ANTI_FLAG = {
                    0: ("ANTI_FEMALE",      "NO_DONNA"),
                    1: ("ANTI_MALE",        "NO_UOMO"),
                    2: ("ANTI_MUSA",        "NO_WAR"),
                    3: ("ANTI_ASSASSIN",    "NO_NINJA"),
                    4: ("ANTI_SURA",        "NO_SURA"),
                    5: ("ANTI_MUDANG",      "NO_SHAMANA"),
                    6: ("ANTI_GET",         "ANTI_GET"), #Non lo so, non implementato
                    7: ("ANTI_DROP",        "NO_GETTABILE"),
                    8: ("ANTI_SELL",        "NO_NPC"),
                    9: ("ANTI_EMPIRE_A",    "NO_SHINSOO"),
                    10:("ANTI_EMPIRE_B",    "NO_CHUNJO"),
                    11:("ANTI_EMPIRE_C",    "NO_JINNO"),
                    12:("ANTI_SAVE",        "ANTI_SAVE"), #Non lo so, non implementato
                    13:("ANTI_GIVE",        "NO_PG"),
                    14:("ANTI_PKDROP",      "NO_DROP_KARMA_NEGATIVO"),
                    15:("ANTI_STACK",       "NO_IMPILABILE"),
                    16:("ANTI_MYSHOP",      "NO_FAGOTTO"),
                    17:("ANTI_SAFEBOX",     "NO_MAGAZZINO"),
                    18:("ANTI_WOLFMAN",     "NO_LICAN"),
                    19:("ANTI_PET",         "NO_PET"), # ANTIFLAG_REAL_TIME_REMOVE <- blocca la distruzione di oggetti quando il tempo scade, per questo i sigilli appaiono come scaduti.
                    20:("ANTI_QUICKSLOT",   "NO_QUICK_SLOT"),
                    21:("ANTI_CHANGELOOK",  "NO_PROIEZIONE"),
                    22:("ANTI_REINFORCE",   "NO_AGG_BONUS"),
                    23:("ANTI_ENCHANT",     "NO_GIRA_BONUS"),
                    24:("ANTI_ENERGY",      "NO_FRAM_ENERGIA"),
                    25:("ANTI_PETFEED",     "NO_CIBO_PET"),
                    26:("ANTI_APPLY",       "NO_PIETRABILE"), 
                    27:("ANTI_ACCE",        "NO_TRASF_STOLA"),
                    28:("ANTI_MAIL",        "NO_POSTA"),
                }

#Item Flag
ITEM_FLAG = {
              0: ("ITEM_TUNABLE",       "PIETRABILE"),
              1: ("ITEM_SAVE",          "ITEM_SAVE"),       #non lo so
              2: ("ITEM_STACKABLE",     "OTTENIBILE_IMPILATO"),
              3: ("COUNT_PER_1GOLD",    "CONTA_COME_1_GOLD"),
              4: ("ITEM_SLOW_QUERY",    "OGGETTO_QUERY_LENTA"),
              5: ("ITEM_UNIQUE",        "ITEM_UNIQUE"),    #non lo so
              6: ("ITEM_MAKECOUNT",     "ITEM_MAKECOUNT"), # non lo so
              7: ("ITEM_IRREMOVABLE",   "ITEM_NON_ELIMINABILE"),
              8: ("CONFIRM_WHEN_USE",   "CONFERMA_QUANDO_USATO"),
              9: ("QUEST_USE",          "USO_QUEST"), #Buoni DR
              10:("QUEST_USE_MULTIPLE", "USO_MULTIPLO_QUEST"), #Stoffe e Sigilli Cavalcature
              11:("QUEST_GIVE",         "SALVA_COORDINATE"), #Papiro del luogo e citta'
              12:("ITEM_QUEST",         "OGGETTO_QUEST"),
              13:("LOG",                "LOG"),
              14:("STACKABLE",          "USABILE_SU_UN_ALTRO"),
              15:("SLOW_QUERY",         "QUERY_LENTA"),
              16:("REFINEABLE",         "RAFFINABILE"),
              17:("IRREMOVABLE",        "NON_ELIMINABILE"),
              18:("ITEM_APPLICABLE",    "ITEM_APPLICABLE"), # non lo so
            }


#Item Wear Flag
ITEM_WEAR_FLAG = {
                    0: ("WEAR_BODY",    "Armatura"),
                    1: ("WEAR_HEAD",    "Elmo"),
                    2: ("WEAR_FOOTS",   "Scarpe"),
                    3: ("WEAR_WRIST",   "Bracciale"),
                    4: ("WEAR_WEAPON",  "Arma"),
                    5: ("WEAR_NECK",    "Collana"),
                    6: ("WEAR_EAR",     "Orecchini"),
                    7: ("WEAR_UNIQUE",  "Speciale"),
                    8: ("WEAR_SHIELD",  "Scudo"),
		    9: ("WEAR_ARROW",   "Freccia"),
                    10:("WEAR_HAIR",    "Capigliatura"),
                    11:("WEAR_ABILITY", "WEAR_ABILITY"),
                    12:("WEAR_ABILITY2","Talismano"),
                    }

#Item Immune Flag
ITEM_IMMUNE_FLAG = {
                    0: ("PARA",     "Paralisi"),
                    1: ("CURSE",    "Maledizione"),
                    2: ("STUN",     "Stordimento"),
                    3: ("SLEEP",    "Sonno"),
                    4: ("SLOW",     "Rallentamento"),
                    5: ("POISON",   "Veleno"),
                    6: ("TERROR",   "Paura"),
                    }

#Limit Type
ITEM_LIMIT_TYPE = {
                     0: ("NONE",                "Nessuno"),
                     1: ("LEVEL",               "Livello"),
                     2: ("STR",                 "Str"),
                     3: ("DEX",                 "Dex"),
                     4: ("INT",                 "Int"),
                     5: ("CON",                 "Vit"),
                     6: ("REAL_TIME",           "Tempo Rim. Reale"),
                     7: ("REAL_TIME_FIRST_USE", "Tempo Rim. Reale dal Primo Uso"),
                     8: ("TIMER_BASED_ON_WEAR", "Tempo Rim. Quando Indossato"),
                     9: ("MAX_NUM",             "Massimo Numero")
                     }

#Apply Type
ITEM_APPLY_TYPE = {
                    0:  ("APPLY_NONE",                      "Nessuno"),
                    1:  ("APPLY_MAX_HP",                    "Max HP"),
                    2:  ("APPLY_MAX_SP",                    "Max MP"),
                    3:  ("APPLY_CON",                       "Vitalita'"),
                    4:  ("APPLY_INT",                       "Intelligenza"),
                    5:  ("APPLY_STR",                       "Forza"),
                    6:  ("APPLY_DEX",                       "Destrezza"),
                    7:  ("APPLY_ATT_SPEED",                 "Velocita' d'Attacco"),
                    8:  ("APPLY_MOV_SPEED",                 "Velocita' di Movimento"),
                    9:  ("APPLY_CAST_SPEED",                "Velocita' Magia"),
                    10: ("APPLY_HP_REGEN",                  "Rigenerazione HP"),
                    11: ("APPLY_SP_REGEN",                  "Rigenerazione MP"),
                    12: ("APPLY_POISON_PCT",                "Possibilita' di Avvelenamento"),
                    13: ("APPLY_STUN_PCT",                  "Possibilita' di Svenimento"),
                    14: ("APPLY_SLOW_PCT",                  "Possibilita' di Rallentamento"),
                    15: ("APPLY_CRITICAL_PCT",              "Possibilita' Colpi Critici"),
                    16: ("APPLY_PENETRATE_PCT",             "Possibilita' Colpi Trafiggenti"),
                    17: ("APPLY_ATTBONUS_HUMAN",            "Forte contro Mezziuomini"),
                    18: ("APPLY_ATTBONUS_ANIMAL",           "Forte contro Animali"),
                    19: ("APPLY_ATTBONUS_ORC",              "Forte contro Orchi"),
                    20: ("APPLY_ATTBONUS_MILGYO",           "Forte contro Esoterici"),
                    21: ("APPLY_ATTBONUS_UNDEAD",           "Forte contro Zombie"),
                    22: ("APPLY_ATTBONUS_DEVIL",            "Forte contro Diavoli"),
                    23: ("APPLY_STEAL_HP",                  "Danni Assorbiti da HP"),
                    24: ("APPLY_STEAL_MP",                  "Danni Assorbiti da MP"),
                    25: ("APPLY_MANA_BURN_PCT",             "Possibilita' di Prendere Mp all'Avversario"),
                    26: ("APPLY_DAMAGE_SP_RECOVER",         "APPLY_DAMAGE_SP_RECOVER"),#Possibilità di Mantenere MP nei Colpi
                    27: ("APPLY_BLOCK",                     "Blocco Attacco Corporale"),
                    28: ("APPLY_DODGE",                     "Schivare Frecce"),
                    29: ("APPLY_RESIST_SWORD",              "Difesa Spada"),
                    30: ("APPLY_RESIST_TWOHAND",            "Difesa Spadone"),
                    31: ("APPLY_RESIST_DAGGER",             "Difesa Pugnale"),
                    32: ("APPLY_RESIST_BELL",               "Difesa Campana"),
                    33: ("APPLY_RESIST_FAN",                "Difesa Ventaglio"),
                    34: ("APPLY_RESIST_BOW",                "Difesa Frecce"),
                    35: ("APPLY_RESIST_FIRE",               "Resistenza Fuoco"),
                    36: ("APPLY_RESIST_ELEC",               "Resistenza Lampo"),
                    37: ("APPLY_RESIST_MAGIC",              "Resistenza Magia"),
                    38: ("APPLY_RESIST_WIND",               "Resistenza Vento"),
                    39: ("APPLY_REFLECT_MELEE",             "Riflettere Attacco Corporale"),
                    40: ("APPLY_REFLECT_CURSE",             "Riflettere Maledizioni"),
                    41: ("APPLY_POISON_REDUCE",             "Resistenza Veleno"),
                    42: ("APPLY_KILL_SP_RECOVER",           "Possibilita' di Rigenerare MP"),
                    43: ("APPLY_EXP_DOUBLE_BONUS",          "Possibilita' Exp Bonus"),
                    44: ("APPLY_GOLD_DOUBLE_BONUS",         "Possiiblita' Lasciar Cadere il Doppio degli Yang"),
                    45: ("APPLY_ITEM_DROP_BONUS",           "Possibilita' Lasciar Cadere il Doppio degli Oggetti"),
                    46: ("APPLY_POTION_BONUS",              "APPLY_POTION_BONUS"), #Aumento Effetto Pozioni
                    47: ("APPLY_KILL_HP_RECOVER",           "Possibilita' di Rigenerare HP"),
                    48: ("APPLY_IMMUNE_STUN",               "Difesa contro Svenimento"),
                    49: ("APPLY_IMMUNE_SLOW",               "Difesa contro Rallentamento"),
                    50: ("APPLY_IMMUNE_FALL",               "Difesa da Caduta"),
                    51: ("APPLY_SKILL",                     "APPLY_SKILL"), # non lo so
                    52: ("APPLY_BOW_DISTANCE",              "APPLY_BOW_DISTANCE"), #Raggio d'azione dell'arco
                    53: ("APPLY_ATT_GRADE_BONUS",           "Valore di Attacco"),
                    54: ("APPLY_DEF_GRADE_BONUS",           "Difesa"),
                    55: ("APPLY_MAGIC_ATT_GRADE",           "APPLY_MAGIC_ATT_GRADE"), #Valore d'attacco magico
                    56: ("APPLY_MAGIC_DEF_GRADE",           "APPLY_MAGIC_DEF_GRADE"), #Difesa magica
                    57: ("APPLY_CURSE_PCT",                 "APPLY_CURSE_PCT"),
                    58: ("APPLY_MAX_STAMINA",               "Resistenza+"),
                    59: ("APPLY_ATTBONUS_WARRIOR",          "Forte contro Guerrieri"),
                    60: ("APPLY_ATTBONUS_ASSASSIN",         "Forte contro Ninja"),
                    61: ("APPLY_ATTBONUS_SURA",             "Forte contro Sura"),
                    62: ("APPLY_ATTBONUS_SHAMAN",           "Forte contro Shamani"),
                    63: ("APPLY_ATTBONUS_MONSTER",          "Forte contro Mostri"),
                    64: ("APPLY_MALL_ATTBONUS",             "Valore Attacco % (Speciale)"), #% sia fisico che magico
                    65: ("APPLY_MALL_DEFBONUS",             "Difesa % (Speciale)"), #% sia fisica che magica
                    66: ("APPLY_MALL_EXPBONUS",             "Exp Bonus % (Speciale)"),
                    67: ("APPLY_MALL_ITEMBONUS",            "Drop Oggetti % (Speciale)"),
                    68: ("APPLY_MALL_GOLDBONUS",            "Drop Yang % (Speciale)"),
                    69: ("APPLY_MAX_HP_PCT",                "Max HP %"),
                    70: ("APPLY_MAX_SP_PCT",                "Max MP %"),
                    71: ("APPLY_SKILL_DAMAGE_BONUS",        "Danni Abilita'"),
                    72: ("APPLY_NORMAL_HIT_DAMAGE_BONUS",   "Danni Medi"),
                    73: ("APPLY_SKILL_DEFEND_BONUS",        "Resistenza Abilita'"),
                    74: ("APPLY_NORMAL_HIT_DEFEND_BONUS",   "Resistenza Danni Medi"),
                    75: ("APPLY_PC_BANG_EXP_BONUS",         "iCafe' Exp Bonus"),
                    76: ("APPLY_PC_BANG_DROP_BONUS",        "iCafe' Drop Bonus"),
                    77: ("APPLY_EXTRACT_HP_PCT",            "APPLY_EXTRACT_HP_PCT"),
                    78: ("APPLY_RESIST_WARRIOR",            "Resistenza contro Guerrieri"),
                    79: ("APPLY_RESIST_ASSASSIN",           "Resistenza contro Ninja"),
                    80: ("APPLY_RESIST_SURA",               "Resistenza contro Sura"),
                    81: ("APPLY_RESIST_SHAMAN",             "Resistenza contro Shamani"),
                    82: ("APPLY_ENERGY",                    "APPLY_ENERGY"), #Energia
                    83: ("APPLY_DEF_GRADE",                 "APPLY_DEF_GRADE"), #Difesa
                    84: ("APPLY_COSTUME_ATTR_BONUS",        "APPLY_COSTUME_ATTR_BONUS"), #Bonus Costume
                    85: ("APPLY_MAGIC_ATTBONUS_PER",        "APPLY_MAGIC_ATTBONUS_PER"), #Attacco % (Fisico che Magico)
                    86: ("APPLY_MELEE_MAGIC_ATTBONUS_PER",  "Attacco Fisico/Magico %"),
                    87: ("APPLY_RESIST_ICE",                "Resistenza Ghiaccio"),
                    88: ("APPLY_RESIST_EARTH",              "Resistenza Terra"),
                    89: ("APPLY_RESIST_DARK",               "Resistenza all'Oscurita'"),
                    90: ("APPLY_ANTI_CRITICAL_PCT",         "Resistenza Colpi Critici"),
                    91: ("APPLY_ANTI_PENETRATE_PCT",        "Resistenza Colpi Trafiggenti"),
                    92: ("APPLY_BLEEDING_PCT",              "Possibilita' di Sanguinamento"),
                    93: ("APLLY_BLEEDING_REDUCE",           "Resistenza al Sanguinamento"),
                    94: ("APPLY_ATTBONUS_WOLFMAN",          "Forte contro Lican"),
                    95: ("APPLY_RESIST_WOLFMAN",            "Resistenza contro Lican"),
                    96: ("APPLY_RESIST_CLAW",               "Difesa Artigli"),
                    97: ("APLLY_ACCEDRAIN_RATE",            "Tasso di Assorbimento"),
                    98: ("APLLY_RESIST_MAGIC_REDUCTION",    "Anti-Magia"),
                    99: ("APPLY_ENCHANT_ELECT",             "Forza del Fulmine"),
                    100:("APPLY_ENCHANT_FIRE",              "Forza del Fuoco"),
                    101:("APPLY_ENCHANT_ICE",               "Forza del Ghiaccio"),
                    102:("APPLY_ENCHANT_WIND",              "Forza del Vento"),
                    103:("APPLY_ENCHANT_EARTH",             "Forza della Terra"),
                    104:("APPLY_ENCHANT_DARK",              "Forza dell'Oscurita'"),
                    105:("APPLY_ATTBOUNS_CZ",               "Forte contro i mostri Zodiaco"),
                    106:("APPLY_ATTBOUNS_INSECT",           "Forte contro gli Insetti"),
                    107:("APPLY_ATTBOUNS_DESERT",           "Forte contro Mostri del Deserto"),
                    108:("APPLY_ATTBOUNS_SWORD",            "Interruzione della Difesa Spada"),
                    109:("APPLY_ATTBOUNS_TWOHAND",          "Interruzione della Difesa Spadone"),
                    110:("APPLY_ATTBOUNS_DAGGER",           "Interruzione della Difesa Pugnale"),
                    111:("APPLY_ATTBOUNS_BELL",             "Interruzione della Difesa Campana"),
                    112:("APPLY_ATTBOUNS_FAN",              "Interruzione della Difesa Ventaglio"),
                    113:("APPLY_ATTBOUNS_BOW",              "Interruzione della Difesa Frecce"),
                    114:("APPLY_ATTBOUNS_CLAW",             "Interruzione della Difesa Artigli"),
                    115:("APPLY_RESIST_HUMAN",              "Resistenza ai Mezziuomini"),
                    116:("APPLY_RESIST_FALL",               "Resistenza alla Caduta"),
                    117:("APPLY_UNKNOWN_117",               "APPLY_UNKNOWN_117"),
                    118:("APPLY_MOUNT",                     "Vnum Mount"),
                    #Sesto e Settimo Bonus
                    119: ("APPLY_SKILL_DAMAGE_SAMYEON",	                                "Danni da Taglio a Tre Vie"),
                    120: ("APPLY_SKILL_DAMAGE_TANHWAN",	                                "Danni da Sibilare"),
                    121: ("APPLY_SKILL_DAMAGE_PALBANG",	                                "Danni da Vortice di Spada"),
                    122: ("APPLY_SKILL_DAMAGE_GIGONGCHAM",                              "Danni da Penetrazione"),
                    123: ("APPLY_SKILL_DAMAGE_GYOKSAN",	                                "Danni da Colpo Potente"),
                    124: ("APPLY_SKILL_DAMAGE_GEOMPUNG",                                "Danni da Colpo di Spada"),
                    125: ("APPLY_SKILL_DAMAGE_AMSEOP",	                                "Danni da Tranello"),
                    126: ("APPLY_SKILL_DAMAGE_GUNGSIN",	                                "Danni da Attacco Lampo"),
                    127: ("APPLY_SKILL_DAMAGE_CHARYUN",	                                "Danni da Vortice del Pugnale"),
                    128: ("APPLY_SKILL_DAMAGE_SANGONG",	                                "Danni da Nuvola Velenosa"),
                    129: ("APPLY_SKILL_DAMAGE_YEONSA",	                                "Danni da Tiro Ripetuto"),
                    130: ("APPLY_SKILL_DAMAGE_KWANKYEOK",                               "Danni da Pioggia di Frecce"),
                    131: ("APPLY_SKILL_DAMAGE_GIGUNG",	                                "Danni da Freccia Avvelenata"),
                    132: ("APPLY_SKILL_DAMAGE_HWAJO",	                                "Danni da Freccia di Fuoco"),
                    133: ("APPLY_SKILL_DAMAGE_SWAERYUNG",	                        "Danni da Schiocco di Dita"),
                    134: ("APPLY_SKILL_DAMAGE_YONGKWON",	                        "Danni da Vortice del Drago"),
                    135: ("APPLY_SKILL_DAMAGE_PABEOB",	                                "Danni da Annullamento Magia"),
                    136: ("APPLY_SKILL_DAMAGE_MARYUNG",	                                "Danni da Colpo Oscuro"),
                    137: ("APPLY_SKILL_DAMAGE_HWAYEOMPOK",	                        "Danni da Colpo di Fiamma"),
                    138: ("APPLY_SKILL_DAMAGE_MAHWAN",	                                "Danni da Pietra Oscura"),
                    139: ("APPLY_SKILL_DAMAGE_BIPABU",	                                "Danni da Talismano Volante"),
                    140: ("APPLY_SKILL_DAMAGE_YONGBI",	                                "Danni da Tiro del Drago"),
                    141: ("APPLY_SKILL_DAMAGE_PAERYONG",	                        "Danni da Ruggito del Drago"),
                    142: ("APPLY_SKILL_DAMAGE_NOEJEON",	                                "Danni da Lancio di Lampi"),
                    143: ("APPLY_SKILL_DAMAGE_BYEURAK",	                                "Danni da Evocare i Lampi"),
                    144: ("APPLY_SKILL_DAMAGE_CHAIN",	                                "Danni da Artiglio di Lampo"),
                    145: ("APPLY_SKILL_DAMAGE_CHAYEOL",	                                "Danni da Dilania"),
                    146: ("APPLY_SKILL_DAMAGE_SALPOONG",	                        "Danni da Respiro del Lupo"),
                    147: ("APPLY_SKILL_DAMAGE_GONGDAB",	                                "Danni da Salto del Lupo"),
                    148: ("APPLY_SKILL_DAMAGE_PASWAE",	                                "Danni da Artiglio di Lupo"),
                    149: ("APPLY_NORMAL_HIT_DEFEND_BONUS_BOSS_OR_MORE",	                "Difesa da attacco contro boss"),
                    150: ("APPLY_SKILL_DEFEND_BONUS_BOSS_OR_MORE",	                "Difesa abilità da boss"),
                    151: ("APPLY_NORMAL_HIT_DAMAGE_BONUS_BOSS_OR_MORE",	                "Danni da attacco da boss"),
                    152: ("APPLY_SKILL_DAMAGE_BONUS_BOSS_OR_MORE",	                "Danni abilita' contro boss"),
                    153: ("APPLY_HIT_BUFF_ENCHANT_FIRE",	                        "Forza del Fuoco in battaglia"),
                    154: ("APPLY_HIT_BUFF_ENCHANT_ICE",	                                "Forza del Ghiaccio in battaglia"),
                    155: ("APPLY_HIT_BUFF_ENCHANT_ELEC",	                        "Forza del Fulmine in battaglia"),
                    156: ("APPLY_HIT_BUFF_ENCHANT_WIND",	                        "Forza del Vento in battaglia"),
                    157: ("APPLY_HIT_BUFF_ENCHANT_DARK",	                        "Forza dell'Oscurita' in battaglia"),
                    158: ("APPLY_HIT_BUFF_ENCHANT_EARTH",	                        "Forza della Terra in battaglia"),
                    159: ("APPLY_HIT_BUFF_RESIST_FIRE",	                                "Resistenza Fuoco in battaglia"),
                    160: ("APPLY_HIT_BUFF_RESIST_ICE",	                                "Resistenza Ghiaccio in battaglia"),
                    161: ("APPLY_HIT_BUFF_RESIST_ELEC",	                                "Resistenza Lampo in battaglia"),
                    162: ("APPLY_HIT_BUFF_RESIST_WIND",	                                "Resistenza Vento in battaglia"),
                    163: ("APPLY_HIT_BUFF_RESIST_DARK",	                                "Resistenza Oscurita' in battaglia"),
                    164: ("APPLY_HIT_BUFF_RESIST_EARTH",	                        "Resistenza Terra in battaglia"),
                    165: ("APPLY_USE_SKILL_CHEONGRANG_MOV_SPEED",	                "Aumenti Velocita' di Movimento usando Anima del Lupo Indaco"),
                    166: ("APPLY_USE_SKILL_CHEONGRANG_CASTING_SPEED",	                "Aumenti Velocita' della Magia usando Anima del Lupo Indaco"),
                    167: ("APPLY_USE_SKILL_CHAYEOL_CRITICAL_PCT",	                "Aumenti chance di attacco critico utilizzando Dilania"),
                    168: ("APPLY_USE_SKILL_SANGONG_ATT_GRADE_BONUS",	                "Bonus attacco utilizzando Nuvola Velenosa"),
                    169: ("APPLY_USE_SKILL_GIGUNG_ATT_GRADE_BONUS",	                "Bonus attacco utilizzando Freccia Avvelenata"),
                    170: ("APPLY_USE_SKILL_JEOKRANG_DEF_BONUS",	                        "Bonus difesa utilizzando Anima del Lupo Purpureo"),
                    171: ("APPLY_USE_SKILL_GWIGEOM_DEF_BONUS",	                        "Bonus difesa utilizzando Lama Incantata"),
                    172: ("APPLY_USE_SKILL_TERROR_ATT_GRADE_BONUS",	                "Bonus attacco utilizzando Terrore"),
                    173: ("APPLY_USE_SKILL_MUYEONG_ATT_GRADE_BONUS",	                "Bonus attacco utilizzando Spirito della Fiamma"),
                    174: ("APPLY_USE_SKILL_MANASHILED_CASTING_SPEED",	                "Aumenti Velocita' magia utilizzando Protezione Oscura"),
                    175: ("APPLY_USE_SKILL_HOSIN_DEF_BONUS",	                        "Bonus difesa utilizzando Benedizione"),
                    176: ("APPLY_USE_SKILL_GICHEON_ATT_GRADE_BONUS",	                "Bonus attacco utilizzando Aiuto del Drago"),
                    177: ("APPLY_USE_SKILL_JEONGEOP_ATT_GRADE_BONUS",	                "Bonus attacco utilizzando Cura"),
                    178: ("APPLY_USE_SKILL_JEUNGRYEOK_DEF_BONUS",	                "Bonus difesa utilizzando Attacco+"),
                    179: ("APPLY_USE_SKILL_GIHYEOL_ATT_GRADE_BONUS",	                "Bonus attacco utilizzando Volonta' di Vivere"),
                    180: ("APPLY_USE_SKILL_CHUNKEON_CASTING_SPEED",	                "Aumenti Velocita' Magia utilizzando Corpo Forte"),
                    181: ("APPLY_USE_SKILL_NOEGEOM_ATT_GRADE_BONUS",	                "Bonus attacco utilizzando Orb della Spada"),
                    182: ("APPLY_SKILL_DURATION_INCREASE_EUNHYUNG",	                "Aumento Durata Camuffamento"),
                    183: ("APPLY_SKILL_DURATION_INCREASE_GYEONGGONG",	                "Aumento Durata di Passo Piumato"),
                    184: ("APPLY_SKILL_DURATION_INCREASE_GEOMKYUNG",	                "Aumento Durata Aura della spada"),
                    185: ("APPLY_SKILL_DURATION_INCREASE_JEOKRANG",	                "Aumento Durata Anima Lupo Purpureo"),
                    186: ("APPLY_USE_SKILL_PALBANG_HP_ABSORB",	                        "Assorbi HP utilizzando Vortice di Spada"),
                    187: ("APPLY_USE_SKILL_AMSEOP_HP_ABSORB",	                        "Assorbi HP utilizzando Tranello"),
                    188: ("APPLY_USE_SKILL_YEONSA_HP_ABSORB",	                        "Assorbi HP utilizzando Tiro Ripetuto"),
                    189: ("APPLY_USE_SKILL_YONGBI_HP_ABSORB",	                        "Assorbi HP utilizzando Tiro del Drago"),
                    190: ("APPLY_USE_SKILL_CHAIN_HP_ABSORB",	                        "Assorbi HP utilizzando Artiglio di Lampo"),
                    191: ("APPLY_USE_SKILL_PASWAE_SP_ABSORB",	                        "Assorbi MP utilizzando Artiglio di Lupo"),
                    192: ("APPLY_USE_SKILL_GIGONGCHAM_STUN",	                        "Penetrazione stordisce l'avversario"),
                    193: ("APPLY_USE_SKILL_CHARYUN_STUN",	                        "Vortice del Pugnale stordisce l'avversario"),
                    194: ("APPLY_USE_SKILL_PABEOB_STUN",	                        "Annullamento Magia stordisce l'avversario"),
                    195: ("APPLY_USE_SKILL_MAHWAN_STUN",	                        "Pietra Oscura stordisce l'avversario"),
                    196: ("APPLY_USE_SKILL_GONGDAB_STUN",	                        "Salto del Lupo stordisce l'avversario"),
                    197: ("APPLY_USE_SKILL_SAMYEON_STUN",	                        "Taglio a tre Vie stordisce l'avversario"),
                    198: ("APPLY_USE_SKILL_GYOKSAN_KNOCKBACK",	                        "Colpo Potente respinge gli avversari"),
                    199: ("APPLY_USE_SKILL_SEOMJEON_KNOCKBACK",	                        "Veleno Insidioso respinge gli avversari"),
                    200: ("APPLY_USE_SKILL_SWAERYUNG_KNOCKBACK",	                "Schiocco di Dita respinge gli avversari"),
                    201: ("APPLY_USE_SKILL_HWAYEOMPOK_KNOCKBACK",	                "Colpo di Fiamma respinge gli avversari"),
                    202: ("APPLY_USE_SKILL_GONGDAB_KNOCKBACK",	                        "Salto del Lupo respinge gli avversari"),
                    203: ("APPLY_USE_SKILL_KWANKYEOK_KNOCKBACK",	                "Pioggia di Frecce respinge gli avversari"),
                    204: ("APPLY_USE_SKILL_SAMYEON_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Taglio a tre Vie"),
                    205: ("APPLY_USE_SKILL_GEOMPUNG_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Colpo di Spada"),
                    206: ("APPLY_USE_SKILL_GUNGSIN_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Attacco Lampo"),
                    207: ("APPLY_USE_SKILL_KWANKYEOK_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Pioggia di Frecce"),
                    208: ("APPLY_USE_SKILL_YONGKWON_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Vortice del Drago"),
                    209: ("APPLY_USE_SKILL_MARYUNG_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Colpo Oscuro"),
                    210: ("APPLY_USE_SKILL_BIPABU_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Talismano Volante"),
                    211: ("APPLY_USE_SKILL_NOEJEON_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Lancio di Lampi"),
                    212: ("APPLY_USE_SKILL_SALPOONG_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Respiro del Lupo"),
                    213: ("APPLY_USE_SKILL_PASWAE_NEXT_COOLTIME_DECREASE_10PER",	"10% di ridurre Tempo di ricarica Artiglio di Lupo"),
                    214: ("APPLY_ATTBONUS_STONE",	                                "Forte contro Rocce Metin"),
                    215: ("APPLY_DAMAGE_HP_RECOVERY",	                                "Assorbe % di danno come HP"),
                    216: ("APPLY_DAMAGE_SP_RECOVERY",	                                "Assorbe % di danno come MP"),
                    217: ("APPLY_ALIGNMENT_DAMAGE_BONUS",	                        "In caso di punti karma bassi, il danno provocato aumenta."),
                    218: ("APPLY_NORMAL_DAMAGE_GUARD",	                                "Probabilita' blocco danni da attacco"),
                    219: ("APPLY_MORE_THEN_HP90_DAMAGE_REDUCE",	                        "Se hai più del 90% di HP, il danno subito diminuisce"),
                    220: ("APPLY_USE_SKILL_TUSOK_HP_ABSORB",	                        "Assorbi HP utilizzando Colpo dello Spirito"),
                    221: ("APPLY_USE_SKILL_PAERYONG_HP_ABSORB",	                        "Assorbi HP utilizzando Ruggito del Drago"),
                    222: ("APPLY_USE_SKILL_BYEURAK_HP_ABSORB",	                        "Assorbi HP utilizzando Evocare i Lampi"),
                    223: ("APPLY_FIRST_ATTRIBUTE_BONUS",	                        "Incremento Bonus 1 Aggiunto"),
                    224: ("APPLY_SECOND_ATTRIBUTE_BONUS",	                        "Incremento Bonus 2 Aggiunto"),
                    225: ("APPLY_THIRD_ATTRIBUTE_BONUS",	                        "Incremento Bonus 3 Aggiunto"),
                    226: ("APPLY_FOURTH_ATTRIBUTE_BONUS",	                        "Incremento Bonus 4 Aggiunto"),
                    227: ("APPLY_FIFTH_ATTRIBUTE_BONUS",	                        "Incremento Bonus 5 Aggiunto"),
                    228: ("APPLY_USE_SKILL_SAMYEON_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Taglio a tre Vie"),
                    229: ("APPLY_USE_SKILL_GEOMPUNG_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Colpo di Spada"),
                    230: ("APPLY_USE_SKILL_GUNGSIN_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Attacco Lampo"),
                    231: ("APPLY_USE_SKILL_KWANKYEOK_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Pioggia di Frecce"),
                    232: ("APPLY_USE_SKILL_YONGKWON_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Vortice del Drago"),
                    233: ("APPLY_USE_SKILL_MARYUNG_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Colpo Oscuro"),
                    234: ("APPLY_USE_SKILL_BIPABU_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Talismano Volante"),
                    235: ("APPLY_USE_SKILL_NOEJEON_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Lancio di Lampi"),
                    236: ("APPLY_USE_SKILL_SALPOONG_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Respiro del Lupo"),
                    237: ("APPLY_USE_SKILL_PASWAE_NEXT_COOLTIME_DECREASE_20PER",	"20% di ridurre Tempo di ricarica Artiglio di Lupo"),
                    238: ("APPLY_USE_SKILL_CHAYEOL_HP_ABSORB",	                        "Assorbi HP utilizzando Dilania"),
                    }

#Tipo Slot Cinture
BELT_TYPE_SLOT = {
                    0: 0,
                    1: 1,
                    2: 2,
                    3: 4,
                    4: 6,
                    5: 9,
                    6: 12,
                    7: 16,
                    }

#Anti Flag Template Interazioni Wiki
# Quelle col Flag ITEM_IMPILABILE possono essere ricevute impilate
# mentre quelle che non lo hanno si possono ricevere solo singolarmente

#Se l'oggetto non è commerciabile (NO_P) o non è fagottabile (NO_F)
#non può essere inviato per posta per cui guadagna la NO_E automaticamente

ITEM_WIKI_ANTI_FLAG_IMPILABILE = { 0: "TUTTE",
                                   128: "NO_G",
                                   256: "NO_N", 
                                   384: "NO_NG", 
                                   8320: "NO_PG e OTTENIBILE_IMPILATO",
                                   8576: "NO_PNG",
                                   16384: "TUTTE E NO_DROP_KARMA_NEGATIVO",
                                   16512: "NO_G e NO_DROP_KARMA_NEGATIVO",
                                   16768: "NO_NG e NO_DROP_KARMA_NEGATIVO",
                                   24960: "NO_PNG e OTTENIBILE_IMPILATO E NO_DROP_KARMA_NEGATIVO",
                                   33152: "NO_ING e OTTENIBILE_IMPILATO",
                                   49536: "NO_ING e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   65536: "NO_F",
                                   65792: "NO_FN e OTTENIBILE_IMPILATO",
                                   65920: "NO_FNG",
                                   73856: "NO_FPG",
                                   74112: "NO_FPNG",
                                   82048: "NO_FG e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   82304: "NO_FNG e NO_DROP_KARMA_NEGATIVO",
                                   90240: "NO_FPG e NO_DROP_KARMA_NEGATIVO e OTTENIBILE_IMPILATO",
                                   90496: "NO_FPNG e NO_DROP_KARMA_NEGATIVO",
                                   98688: "NO_FING e OTTENIBILE_IMPILATO",
                                   106624: "NO_FIPG e OTTENIBILE_IMPILATO",
                                   106880: "NO_FIPNG e OTTENIBILE_IMPILATO",
                                   115072: "NO_FING e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   123008: "NO_FIPG e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   123264: "NO_FIPNG e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   131072: "NO_M",
                                   147840: "NO_MNG e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   196608: "NO_MF", 
                                   204928: "NO_MFPG",
                                   205184: "NO_MFPNG",
                                   221312: "NO_MFPG e OTTENIBILE_IMPILATO E NO_DROP_KARMA_NEGATIVO",
                                   221568: "NO_MFPNG e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   237952: "NESSUNA e OTTENIBILE_IMPILATO",
                                   237953: "NESSUNA, NO_D e OTTENIBILE_IMPILATO", 
                                   237954: "NESSUNA, NO_U e OTTENIBILE_IMPILATO",
                                   237696: "NO_MFIPG e OTTENIBILE_IMPILATO",
                                   254080: "NO_MFIPG e OTTENIBILE_IMPILATO e NO_DROP_NEGATIVO",
                                   254336: "NESSUNA e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   254337: "NESSUNA e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   254337: "NESSUNA, NO_D e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   254338: "NESSUNA, NO_U e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   262188: "TUTTE e NO_GNSL",
                                   262196: "TUTTE e NO_GSUSL",
                                   278580: "TUTTE, NO_GSUSL e NO_DROP_KARMA_NEGATIVO",
                                   467124: "NO_MFPG, NO_GSUSL",
                                   1065344: "NO_NGe OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   1122688: "NO_FPNG e NO_QUICK_SLOT",
                                   1138816: "NO_FPG e NO_DROP_KARMA_NEGATIVO e NO_QUICK_SLOT",
                                   1139072: "NO_FPNG e NO_QUICK_SLOT e e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO",
                                   1245312: "NO_MFG e NO_QUICK_SLOT",
                                   1253504: "NO_MFPG e NO_QUICK_SLOT",
                                   1269888: "NO_MFPG e NO_QUICK_SLOT e NO_DROP_KARMA_NEGATIVO",
                                   268525696: "NO_FPG e NO_DROP_KARMA_NEGATIVO",
                                   268525952: "NO_FPNG e NO_DROP_KARMA_NEGATIVO",
                                   269631488: "NO_ME, NO_DROP_KARMA_NEGATIVO, NO_QUICK_SLOT",
                                   269705344: "NO_MFPG e OTTENIBILE_IMPILATO e NO_DROP_KARMA_NEGATIVO, NO_QUICK_SLOT",
                        }

#l'ITEM_STACKABLE non garantisce l'impilabilita'

ITEM_WIKI_ANTI_FLAG_NOIMPILABILE = { 0: "NO_I",
                                     1: "NO_I, NO_D",
                                     2: "NO_I, NO_U",
                                     60: "NO_I, NO_GSUNS",
                                     61: "NO_I, NO_DGSUNS",
                                     128: "NO_IG",
                                     256: "NO_IN",
                                     384: "NO_ING",
                                     16384: "NO_I e NO_DROP_KARMA_NEGATIVO",
                                     16444: "NO_I e NO_DROP_KARMA_NEGATIVO, NO_GNSUS",
                                     16768: "NO_ING e NO_DROP_KARMA_NEGATIVO",
                                     32768: "NO_I",
                                     32828: "NO_I, NO_GSUNS",
                                     32896: "NO_IG",
                                     32897: "NO_IG, NO_D",
                                     32956: "NO_IG, NO_GSUNS",
                                     33024: "NO_IN",
                                     33152: "NO_ING",
                                     33153: "NO_ING, NO_D",
                                     41344: "NO_IPNG",
                                     41345: "NO_IPNG, NO_D",
                                     49212: "NO_I, NO_GSUNS e NO_DROP_KARMA_NEGATIVO",
                                     49280: "NO_IG e NO_DROP_KARMA_NEGATIVO",
                                     49281: "NO_IG, NO_D e NO_DROP_KARMA_NEGATIVO",
                                     49340: "NO_IG, NO_GSUNS e NO_DROP_KARMA_NEGATIVO",
                                     49536: "NO_ING e NO_DROP_KARMA_NEGATIVO",
                                     49537: "NO_ING, NO_D e NO_DROP_KARMA_NEGATIVO",
                                     57728: "NO_IPNG e NO_DROP_KARMA_NEGATIVO",
                                     73856: "NO_FIPG",
                                     73916: "NO_FIPG, NO_GSUNS",
                                     74112: "NO_FIPNG",
                                     82304: "NO_FNG e NO_DROP_KARMA_NEGATIVO",
                                     90240: "NO_FPG e NO_DROP_KARMA_NEGATIVO",
                                     90496: "NO_FPNG e NO_DROP_KARMA_NEGATIVO",
                                     98304: "NO_FI",
                                     98433: "NO_FIG, NO_DL",
                                     98434: "NO_FIG, NO_U",
                                     98560: "NO_FIN",
                                     98688: "NO_FING",
                                     106624: "NO_FIPG",
                                     106684: "NO_FIPG, NO_GSUNS",
                                     106880: "NO_FIPNG",
                                     106881: "NO_FIPNG, NO_D",
                                     106882: "NO_FIPNG, NO_U",
                                     106940: "NO_FIPNG, NO_GSUNS",
                                     114817: "NO_FIG, NO_DL e NO_DROP_KARMA_NEGATIVO",
                                     114818: "NO_FIG, NO_U e NO_DROP_KARMA_NEGATIVO",
                                     114944: "NO_FIN e NO_DROP_KARMA_NEGATIVO",
                                     115072: "NO_FING e NO_DROP_KARMA_NEGATIVO",
                                     123008: "NO_FIPG e NO_DROP_KARMA_NEGATIVO",
                                     123264: "NO_FIPNG e NO_DROP_KARMA_NEGATIVO",
                                     123324: "NO_FIPNG, NO_GSUNS e NO_DROP_KARMA_NEGATIVO",
                                     131072: "NO_MI",
                                     147840: "NO_MNG e NO_DROP_KARMA_NEGATIVO", 
                                     163840: "NO_MI",
                                     164096: "NO_MIN",
                                     172416: "NO_MIPNG",
                                     188800: "NO_MIPNG e NO_DROP_KARMA_NEGATIVO",
                                     196608: "NO_MIF",
                                     204928: "NO_MFIPG",
                                     205184: "NESSUNA",
                                     221312: "MFPG e NO_DRP_KARMA_NEGATIVO",
                                     221568: "NESSUNA e NO_DROP_KARMA_NEGATIVO",
                                     237696: "NO_MFIPG",
                                     237952: "NESSUNA",
                                     254080: "NO_MFIPG e NO_DROP_KARMA_NEGATIVO",
                                     254336: "NESSUNA e NO_DROP_KARMA_NEGATIVO",
                                     254337: "NESSUNA, NO_D e NO_DROP_KARMA_NEGATIVO",
                                     254337: "NESSUNA, NO_U e NO_DROP_KARMA_NEGATIVO",
                                     262172: "NO_I, NO_GSUNL",
                                     262173: "NO_I, NO_DGSUNL",
                                     262174: "NO_I, NO_UGSUNL",
                                     262176: "NO_I, NO_SL",
                                     262188: "NO_I, NO_GNSL",
                                     262189: "NO_I, NO_DGNSL",
                                     262190: "NO_I, NO_UGNSL",
                                     262196: "NO_I, NO_GSUSL",
                                     262197: "NO_I, NO_DGSUSL",
                                     262198: "NO_I, NO_UGSUSL",
                                     262200: "NO_I, NO_SUNSL",
                                     262201: "NO_I, NO_DSUNSL",
                                     262202: "NO_I, NO_USUNSL",
                                     262428: "NO_N, NO_GSUNL",
                                     278556: "NO_I e NO_DROP_KARMA_NEGATIVO, NO_GNSUL",
                                     278572: "NO_I e NO_DROP_KARMA_NEGATIVO, NO_GNSL",
                                     278580: "NO_I e NO_DROP_KARMA_NEGATIVO, NO_GSUSL",
                                     278584: "NO_I e NO_DROP_KARMA_NEGATIVO, NO_NSUSL",
                                     294940: "NO_I, NO_GSUNL",
                                     294944: "NO_I, NO_SL",
                                     294964: "NO_I, NO_GSUSL",
                                     294968: "NO_I, NO_SUNSL",
                                     295040: "NO_IG, NO_L",
                                     295041: "NO_IG, NO_DL",
                                     295042: "NO_IG, NO_UL",
                                     295068: "NO_IG, NO_SUNSL",
                                     295072: "NO_IG, NO_SL",
                                     295092: "NO_IG, NO_GSUSL",
                                     295096: "NO_IG, NO_SUNSL",
                                     295297: "NO_ING, NO_DL",
                                     295298: "NO_ING, NO_UL",
                                     303490: "NO_IPNG ,NO_UL",
                                     311324: "NO_I, NO_GSUNL e NO_DROP_KARMA_NEGATIVO",
                                     311328: "NO_I, NO_SL e NO_DROP_KARMA_NEGATIVO",
                                     311348: "NO_I, NO_GSUSL e NO_DROP_KARMA_NEGATIVO",
                                     311352: "NO_I, NO_SUNSL e NO_DROP_KARMA_NEGATIVO",
                                     311424: "NO_IG, NO_L e NO_DROP_KARMA_NEGATIVO",
                                     311425: "NO_IG, NO_DL e NO_DROP_KARMA_NEGATIVO",
                                     311426: "NO_IG, NO_UL e NO_DROP_KARMA_NEGATIVO",
                                     311452: "NO_IG, NO_SUNSL e NO_DROP_KARMA_NEGATIVO",
                                     311456: "NO_IG, NO_SL e NO_DROP_KARMA_NEGATIVO",
                                     311476: "NO_IG, NO_GSUSL e NO_DROP_KARMA_NEGATIVO",
                                     311480: "NO_IG, NO_SUNSL e NO_DROP_KARMA_NEGATIVO",
                                     311682: "NO_ING, NO_UL e NO_DROP_KARMA_NEGATIVO",
                                     360576: "NO_IPNG, NO_L",
                                     360578: "NO_FIG, NO_UL",
                                     368796: "NO_FIPG, NO_GSUNL",
                                     368800: "NO_FIPG, NO_SL",
                                     368812: "NO_FIPG, NO_GNSL",
                                     368820: "NO_FIPG, NO_GSUSL",
                                     368824: "NO_FIPG, NO_SUNSL",
                                     369024: "NO_FIPNG, NO_L",
                                     369025: "NO_FIPNG, NO_DL",
                                     369026: "NO_FIPNG, NO_UL",
                                     369052: "NO_FIPNG, NO_GSUNL",
                                     369056: "NO_FIPNG, NO_SL",
                                     369068: "NO_FIPNG, NO_GNSL",
                                     369076: "NO_FIPNG, NO_GSUSL",
                                     369080: "NO_FIPNG, NO_SUNSL",
                                     376960: "NO_IPNG, NO_L e NO_DROP_KARMA_NEGATIVO",
                                     376962: "NO_FIG, NO_UL e NO_DROP_KARMA_NEGATIVO",
                                     385440: "NO_FIPNG, NO_SL e NO_DROP_KARMA_NEGATIVO",
                                     385460: "NO_FIPNG, NO_GSUSL e NO_DROP_KARMA_NEGATIVO",
                                     385464: "NO_FIPNG, NO_SUNSL e NO_DROP_KARMA_NEGATIVO",
                                     385436: "NO_FIPNG, NO_GSUNL e NO_DROP_KARMA_NEGATIVO",
                                     622976: "NO_FING e NO_PET",
                                     630912: "NO_FIPG e NO_PET",
                                     639360: "NO_FING e NO_PET e NO_DROP_KARMA_NEGATIVO",
                                     647296: "NO_FIPG e NO_PET e NO_DROP_KARMA_NEGATIVO",
                                     1048576: "NO_I e NO_QUICK_SLOT", 
                                     1081472: "NO_IG e NO_QUICK_SLOT",
                                     1097856: "NO_IG e NO_QUICK_SLOT e NO_DROP_KARMA_NEGATIVO",
                                     1139072: "NO_FPNG e NO_QUICK_SLOT e NO_DROP_KARMA_NEGATIVO",
                                     1253504: "NO_MFIPG e NO_QUICK_SLOT",
                                     266543292: "NO_MFIPG, NO_GNSUS e NO_PROIEZIONE, NO_AGG_BONUS, NO_GIRA_BONUS, NO_FRAM_ENERGIA, NO_CIBO_PET, NO_PIETRABILE e NO_TRASF_STOLA",
                                     266805404: "NO_MFIPG, NO_GNSUL e NO_PROIEZIONE, NO_AGG_BONUS, NO_GIRA_BONUS, NO_FRAM_ENERGIA, NO_CIBO_PET, NO_PIETRABILE e NO_TRASF_STOLA",
                                     266805408: "NO_MFIPG, NO_SL e NO_PROIEZIONE, NO_AGG_BONUS, NO_GIRA_BONUS, NO_FRAM_ENERGIA, NO_CIBO_PET, NO_PIETRABILE e NO_TRASF_STOLA",
                                     266805428: "NO_MFIPG, NO_GSUSL e NO_PROIEZIONE, NO_AGG_BONUS, NO_GIRA_BONUS, NO_FRAM_ENERGIA, NO_CIBO_PET, NO_PIETRABILE e NO_TRASF_STOLA",
                                     266805432: "NO_MFIPG, NO_NSUSL e NO_PROIEZIONE, NO_AGG_BONUS, NO_GIRA_BONUS, NO_FRAM_ENERGIA, NO_CIBO_PET, NO_PIETRABILE e NO_TRASF_STOLA",
                                     268435456: "NO_IE", #È solo NO_POSTA
                                     268468224: "NO_IE",
                                     268525696: "NO_FIPG e NO_DROP_KARMA_NEGATIVO",
                                     269705344: "NO_MFPG e NO_DROP_KARMA_NEGATIVO, NO_QUICK_SLOT",
                                     269738112: "NO_MFIPG e NO_DROP_KARMA_NEGATIVO, NO_QUICK_SLOT",
                                     403136928: "NESSUNA, NO_SL e NO_DROP_KARMA_NEGATIVO e NO_TRASF_STOLA",
                                     403136948: "NESSUNA, NO_GSUSL e NO_DROP_KARMA_NEGATIVO e NO_TRASF_STOLA",
                                     403136952: "NESSUNA, NO_NSUSL e NO_DROP_KARMA_NEGATIVO e NO_TRASF_STOLA",
                                     404185504: "NESSUNA, NO_SL e NO_DROP_KARMA_NEGATIVO, NO_QUICK_SLOT e NO_TRASF_STOLA",
                                     536076416: "NESSUNA, NO_DROP_KARMA_NEGATIVO, NO_QUICK_SLOT, NO_PROIEZIONE, NO_AGG_BONUS, NO_GIRA_BONUS, NO_FRAM_ENERGIA, NO_CIBO_PET, NO_PIETRABILE e NO_TRASF_STOLA",
                                     }  

#Mob Type
MOB_TYPE = {
             0: ("MONSTER",         "Mostro"),
             1: ("NPC",             "Npc"),
             2: ("STONE",           "Metin"),
             3: ("WARP",            "Portale"),
             4: ("DOOR",            "Porta"),
             5: ("BUILDING",        "Edificio"),
             6: ("PC",              "PG"),
             7: ("POLYMORPH_PC",    "PG Trasformato"),
             8: ("HORSE",           "Cavallo"),
             9: ("GOTO",            "Cambio Zona"),
             10:("PET",             "Pet"),
             11:("PET_PAY",         "Pet Vecchio"),
             255:("MOUNT",          "Cavalcatura"),
           } 

#Grado Mob
MOB_GRADE = {
              0: ("PAWN",       "1"),
              1: ("S_PAWN",     "2"),
              2: ("KNIGHT",     "3"),
              3: ("S_KNIGHT",   "4"),
              4: ("BOSS",       "Boss"),
              5: ("KING",       "5"),
              }

#Battle Type Mob
MOB_BATTLE_TYPE = {
                    0: ("MELEE",        "Mischia"),
                    1: ("RANGE",        "Distanza"),
                    2: ("MAGIC",        "Magico"),
                    3: ("SPECIAL",      "Non Attacca"),
                    4: ("POWER",        "POWER"),
                    5: ("TANKER",       "TANKER"),
                    6: ("SUPER_POWER",  "SUPER_POWER"),
                    7: ("SUPER_TANKER", "SUPER_TANKER"),
                    }
#Mob Size
MOB_SIZE = {
             0: ("SMALL",   "Piccola"),
             1: ("MEDIUM",  "Media"),
             2: ("BIG",     "Grande"),
            }

#Mob AI Flag
MOB_AI_FLAG = {
		0: ("AGGR",             "Aggressivo"),
		1: ("NOMOVE",           "Non si Muove"),
		2: ("COWARD",           "Scappa"),
		3: ("NOATTSHINSU",      "Non Attacca Shinsoo"),
		4: ("NOATTCHUNJO",      "Non Attacca Chunjo"),
		5: ("NOATTJINNO",       "Non Attacca Jinno"),
		6: ("ATTMOB",           "Attacca Mob"),
		7: ("BERSERK",          "BERSERK"),
        8: ("STONESKIN",        "STONESKIN"),
		9: ("GODSPEED",         "GODSPEED"),
		10:("DEATHBLOW",        "DEATHBLOW"),
		11:("REVIVE",           "REVIVE"),
        12:("HEALER",           "Guaritore"),
        13:("COUNT",            "Contatore Colpi"),
        14:("NORECOVERY",       "No Regen HP"),
        15:("REFLECT",          "Ti trasforma in Mob"),
        16:("FALL",             "Disarciona"),
        17:("VIT",              "Dimezza l'attacco per 10 minuti"),
        18:("RATTSPEED",        "Riduce la velocità d'attacco"),
        19:("RCASTSPEED",       "Riduce la velocità della magia"),
        20:("RHP_REGEN",        "Riduce la rigenerazione HP"),
        21:("TIMEVIT",          "Dimezza l'attacco per x secondi"),
        22:("PAUSE_SPECIAL",    "Si muove solo se attaccato"),
        23:("AI_FLAG23",            "AI_FLAG23"),
    }


#Mob Race Flag
MOB_RACE_FLAG = {
		  0: ("ANIMAL",         "Animale"),
		  1: ("UNDEAD",         "Zombie"),
		  2: ("DEVIL",          "Diavolo"),
		  3: ("HUMAN",          "Mezzuomo"),
		  4: ("ORC",            "Orco"),
		  5: ("MILGYO",         "Esoterico"),
		  6: ("INSECT",         "Insetto"),
		  7: ("DESERT",         "Deserto"),
		  8:("TREE",           "Albero"),
		  9:("DECO",           "Decorazione"),
          10:("HIDEABLE",       "Nascondibile"),
          11:("ZODIAC",         "Zodiaco"),
          12:("AWEAKEN",        "Ultraboss"),
          13:("SUNGMAHEE",      "Inferna Sung Ma"),
          14:("OUTPOST",        "Avamposto"),
		}

#Mob Immune Flag
MOB_IMMUNE_FLAG = {
            0: ("STUN",         "Stun"),
		    1: ("SLOW",         "Rallentamento"), 
		    2: ("FALL",         "Cadere"),
		    3: ("CURSE",        "Maledizione"),
            4: ("POISON",       "Veleno"),
		    5: ("TERROR",       "Paura"),
            6: ("REFLECT",      "Riflessione"),
            7: ("IMMUNE_FLAG7", "IMMUNE_FLAG7"),
            8: ("IMMUNE_FLAG8", "IMMUNE_FLAG8"),
                    9: ("IMMUNE_FLAG9", "IMMUNE_FLAG9"),
                    10:("IMMUNE_FLAG10","IMMUNE_FLAG10"),
                    11:("IMMUNE_FLAG11","IMMUNE_FLAG11"),#c'è li ha il Baashido
                    12:("IMMUNE_FLAG12","IMMUNE_FLAG12"),#c'è li ha il Baashido
                    13:("IMMUNE_FLAG13","IMMUNE_FLAG13"),#c'è li ha il Baashido
                    14:("IMMUNE_FLAG14","IMMUNE_FLAG14"),#c'è li ha il U: Bajganamu
                    15:("IMMUNE_FLAG15","IMMUNE_FLAG15"),#c'è li ha il U: Bajganamu
                    }

#Regno
REGNO = {
          0: ("NONE",       "Nessuno"),
          1: ("SHINSOO",    "Shinsoo"),
          2: ("CHUNJO",     "Chunjo"),
          3: ("JINNO",      "Jinno"),
          }


#Flag Template Interazioni Mob Wiki (Flag Immunita')
MOB_WIKI_FLAG = {
                0: "NESSUNA",
                1: "S",
                2: "R",
                3: "SR",
                8: "NESSUNA",   #Maledizione ignorata
                10: "R",        #Maledizione ignorata
                11: "SR",       #Maledizione ignorata
                16: "V",
                32: "P",
                34: "RP",
                35: "SRP",
                40: "P",        #Maledizione ignorata
                42: "RP",
                43: "SRP",      #Maledizione ignorata
                51: "SRVP",
                #??: "TUTTE",
                }

#Flag Template Interazioni Mob Wiki (Proc Status)
MOB_WIKI_FLAG_PROC = {
                     #mettere i proc dei mob non nell'item proto
                    }

#Flag Template Interazioni Mob Wiki (Flag) non presenti nel mob_proto
MOB_WIKI_FLAG_NEW = {
                    }

#Tipo di comportamento sul click dei mostri
MOB_ON_CLICK_TYPE = {
                    0:  ("ON_CLICK_EVENT_NONE", "Nessuno"),
                    #forse 1 è ON_CLICK_EVENT_BATTLE
                    1:  ("ON_CLICK_EVENT_SHOP", "Negozio"),
                    2:  ("ON_CLICK_EVENT_TALK", "Dialogo"),
                    #mentre ON_CLICK_EVENT_VEHICLE = 4
                    }


#Item per Set Up
SET_UP = {
           1   : [(0, 0), (0, 0), (0, 0), "600"],
           2   : [(0, 0), (0, 0), (0, 0), "1.200"],
           3   : [(0, 0), (0, 0), (0, 0), "2.500"],
           4   : [(0, 0), (0, 0), (0, 0), "5.000"],
           5   : [(0, 0), (0, 0), (0, 0), "10.000"],
           6   : [(0, 0), (0, 0), (0, 0), "20.000"],
           7   : [(30053, 1), (0, 0), (0, 0), "30.000"],
           8   : [(30073, 2), (0, 0), (0, 0), "45.000"],
           9   : [(30033, 2), (0, 0), (0, 0), "75.000"],
           10  : [(0, 0), (0, 0), (0, 0), "1.000"],
           11  : [(0, 0), (0, 0), (0, 0), "2.000"],
           12  : [(0, 0), (0, 0), (0, 0), "4.000"],
           13  : [(0, 0), (0, 0), (0, 0), "8.000"],
           14  : [(30030, 2), (0, 0), (0, 0), "13.000"],
           15  : [(30075, 2), (0, 0), (0, 0), "20.000"],
           16  : [(30056, 2), (27799, 1), (0, 0), "40.000"],
           17  : [(30022, 2), (27987, 1), (0, 0), "70.000"],
           18  : [(30067, 2), (27987, 1), (0, 0), "120.000"],
           19  : [(0, 0), (0, 0), (0, 0), "1.200"],
           20  : [(0, 0), (0, 0), (0, 0), "2.500"],
           21  : [(0, 0), (0, 0), (0, 0), "5.000"],
           22  : [(0, 0), (0, 0), (0, 0), "10.000"],
           23  : [(30079, 1), (0, 0), (0, 0), "20.000"],
           24  : [(30015, 1), (0, 0), (0, 0), "30.000"],
           25  : [(30016, 2), (27992, 1), (0, 0), "45.000"],
           26  : [(30089, 2), (27993, 1), (0, 0), "90.000"],
           27  : [(30091, 2), (27994, 1), (0, 0), "150.000"],
           28  : [(0, 0), (0, 0), (0, 0), "600"],
           29  : [(0, 0), (0, 0), (0, 0), "1.200"],
           30  : [(0, 0), (0, 0), (0, 0), "2.500"],
           31  : [(0, 0), (0, 0), (0, 0), "5.000"],
           32  : [(0, 0), (0, 0), (0, 0), "10.000"],
           33  : [(0, 0), (0, 0), (0, 0), "20.000"],
           34  : [(2, 30034), (0, 0), (0, 0), "30.000"],
           35  : [(2, 30011), (0, 0), (0, 0), "45.000"],
           36  : [(2, 30035), (0, 0), (0, 0), "75.000"],
           37  : [(0, 0), (0, 0), (0, 0), "1.000"],
           38  : [(0, 0), (0, 0), (0, 0), "2.000"],
           39  : [(0, 0), (0, 0), (0, 0), "4.000"],
           40  : [(0, 0), (0, 0), (0, 0), "8.000"],
           41  : [(2, 30052), (0, 0), (0, 0), "13.000"],
           42  : [(2, 30046), (0, 0), (0, 0), "20.000"],
           43  : [(2, 30045), (1, 27799), (0, 0), "40.000"],
           44  : [(2, 30025), (1, 27987), (0, 0), "70.000"],
           45  : [(2, 30058), (1, 27987), (0, 0), "120.000"],
           46  : [(0, 0), (0, 0), (0, 0), "1.200"],
           47  : [(0, 0), (0, 0), (0, 0), "2.500"],
           48  : [(0, 0), (0, 0), (0, 0), "5.000"],
           49  : [(0, 0), (0, 0), (0, 0), "10.000"],
           50  : [(30083, 1), (0, 0), (0, 0), "20.000"],
           51  : [(30060, 1), (0, 0), (0, 0), "30.000"],
           52  : [(30061, 2), (27992, 1), (0, 0), "45.000"],
           53  : [(30088, 2), (27993, 1), (0, 0), "90.000"],
           54  : [(30019, 2), (27994, 1), (0, 0), "150.000"],

           352  : [(0, 0), (0, 0), (0, 0), "3.000"],
           353  : [(0, 0), (0, 0), (0, 0), "6.000"],
           354  : [(0, 0), (0, 0), (0, 0), "12.000"],
           355  : [(0, 0), (0, 0), (0, 0), "25.000"],
           356  : [(0, 0), (0, 0), (0, 0), "40.000"],
           357  : [(0, 0), (0, 0), (0, 0), "60.000"],
           358  : [(0, 0), (0, 0), (0, 0), "90.000"],
           359  : [(0, 0), (0, 0), (0, 0), "120.000"],
           360  : [(0, 0), (0, 0), (0, 0), "150.000"],           
           361 : [(33030, 1), (0, 0), (0, 0), "10.000"],
           362 : [(33030, 2), (30611, 1), (0, 0), "20.000"],
           363 : [(33030, 4), (30611, 1), (0, 0), "40.000"],
           364 : [(33030, 8), (30611, 2), (0, 0), "80.000"],
           365 : [(33030, 16), (30611, 2), (0, 0), "160.000"],
           366 : [(33030, 32), (30611, 3), (0, 0), "320.000"],
           367 : [(33030, 64), (30616, 2), (0, 0), "640.000"],
           368 : [(33030, 128), (30617, 1), (0, 0), "1.280.000"],
           369 : [(33030, 200), (30618, 1), (0, 0), "2.560.000"],

           390 : [(33029, 1), (0, 0), (0, 0), "10.000"],
           391 : [(33029, 2), (30611, 1), (0, 0), "20.000"],
           392 : [(33029, 4), (30611, 1), (0, 0), "40.000"],
           393 : [(33029, 8), (30611, 2), (0, 0), "80.000"],
           394 : [(33029, 16), (30611, 2), (0, 0), "160.000"],
           395 : [(33029, 32), (30611, 3), (0, 0), "320.000"],
           396 : [(33029, 64), (30616, 2), (0, 0), "640.000"],
           397 : [(33029, 128), (30617, 1), (0, 0), "1.280.000"],
           398 : [(33029, 200), (30618, 1), (0, 0), "2.560.000"],

           409 : [("stola dello stesso up", 1), (0, 0), (0, 0), "100.000"],
           
           440 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           441 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           442 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           443 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           444 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           445 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           446 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           447 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           448 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           449 : [(33031, 10), (9600, 1), (30031, 1), "50.000"],
           450 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           451 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           452 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           453 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           454 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           455 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           456 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           457 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           458 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           459 : [(33031, 10), (10750, 1), (30031, 1), "50.000"],
           460 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           461 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           462 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           463 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           464 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           465 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           466 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           467 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           468 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           469 : [(33031, 10), (9830, 1), (30031, 1), "50.000"],
           470 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           471 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           472 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           473 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           474 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           475 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           476 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           477 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           478 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           479 : [(33031, 10), (10520, 1), (30031, 1), "50.000"],
           480 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           481 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           482 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           483 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           484 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           485 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           486 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           487 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           488 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           489 : [(33031, 10), (10060, 1), (30031, 1), "50.000"],
           490 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           491 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           492 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           493 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           494 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           495 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           496 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           497 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           498 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],
           499 : [(33031, 10), (10290, 1), (30031, 1), "50.000"],

           501 : [(25040, 2), (70031, 1), (0, 0), "100.000"],
           502 : [(0, 0), (0, 0), (0, 0), "120.000"],
           503 : [(0, 0), (0, 0), (0, 0), "140.000"],
           504 : [(0, 0), (0, 0), (0, 0), "170.000"],
           505 : [(0, 0), (0, 0), (0, 0), "200.000"],
           506 : [(0, 0), (0, 0), (0, 0), "240.000"],
           507 : [(30050, 2), (0, 0), (0, 0), "290.000"],
           508 : [(30083, 2), (27992, 1), (0, 0), "340.000"],
           509 : [(30040, 2), (27993, 1), (0, 0), "410.000"],
           510 : [(30089, 2), (27994, 1), (0, 0), "500.000"],

           530 : [(71123, 3), (71129, 4), (0, 0), "200.000"],

           601 : [(51101, 10), (0, 0), (0, 0), "100.000"],
           602 : [(51101, 15), (0, 0), (0, 0), "125.000"],
           603 : [(51101, 20), (0, 0), (0, 0), "150.000"],
           604 : [(51101, 30), (0, 0), (0, 0), "180.000"],
           605 : [(51101, 45), (0, 0), (0, 0), "225.000"],
           606 : [(51101, 65), (0, 0), (0, 0), "270.000"],
           607 : [(51101, 95), (0, 0), (0, 0), "320.000"],
           608 : [(51101, 140), (0, 0), (0, 0), "400.000"],
           609 : [(51101, 200), (0, 0), (0, 0), "500.000"],
           610 : [(70031, 3), (51101, 100), (25040, 2), "5.000.000"],
           
           620 : [(30623, 3), (25050, 2), (30624, 2), "2.000.000"],
           621 : [(30626, 1), (30629, 1), (0, 0), "330.000"],
           622 : [(30626, 1), (30629, 1), (0, 0), "425.000"],
           623 : [(30626, 2), (30629, 2), (0, 0), "540.000"],
           624 : [(30626, 2), (30629, 2), (0, 0), "720.000"],
           625 : [(30626, 3), (30629, 3), (0, 0), "800.000"],
           626 : [(30627, 2), (30629, 3), (0, 0), "900.000"],
           627 : [(30627, 2), (27992, 1), (0, 0), "950.000"],
           628 : [(30627, 3), (27993, 1), (0, 0), "1.300.000"],
           629 : [(30624, 2), (27994, 1), (0, 0), "1.500.000"],
           630 : [(30623, 3), (25050, 2), (30624, 2), "2.000.000"], 
           631 : [(30625, 1), (30629, 1), (0, 0), "330.000"],
           632 : [(30625, 1), (30629, 1), (0, 0), "425.000"],
           633 : [(30625, 2), (30629, 2), (0, 0), "540.000"],
           634 : [(30625, 2), (30629, 2), (0, 0), "720.000"],
           635 : [(30625, 3), (30629, 3), (0, 0), "800.000"],
           636 : [(30628, 2), (30629, 1), (0, 0), "900.000"],
           637 : [(30628, 2), (30616, 2), (0, 0), "950.000"],
           638 : [(30628, 3), (30617, 2), (0, 0), "1.300.000"],
           639 : [(30624, 2), (30618, 2), (0, 0), "1.500.000"],

         }


