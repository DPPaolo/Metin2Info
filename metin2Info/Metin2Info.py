#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, QtWidgets # importiamo i moduli necessari
import os
import proto
import QtMetin2
import metin2Class
import subprocess
import sys
import time

#Variabili da Inizializzare
proto.cur_dir = os.path.dirname(os.path.realpath(__file__))

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() # da porre sempre all'inizio

        proto.gestore_opzioni = metin2Class.gestore_opzioni()

        if (proto.gestore_opzioni.get_option("FirstInit") == 0):
            proto.gestore_opzioni.create_config()
            proto.gestore_opzioni.set_option("FirstInit", 1)

        if (proto.gestore_opzioni.get_option("Update/AutoUpdate") == 1):
            ver = self.get_actual_version()
            ver2 = self.retrieve_version()
            if (float(ver) < float(ver2)):
                return

        if (QtMetin2.check_file("PostUpdate.txt")):
            fp = open(proto.cur_dir + "/PostUpdate.txt", "r")
            line = fp.readlines()
            pid = str(line[0]).replace("\n", "")
            ver = str(line[1]).replace("\n", "")
            fp.close()
            name = r'Metin2 Info ' + ver + ".exe"
            try:
                #subprocess.call("taskkill /PID " + pid)
                #time.sleep(2)
                os.remove(proto.cur_dir + "/" + name)
            except Exception as er:
                proto.stampa_errore("Impossibile cancellare/chiudere la vecchia versione del programma\n" + str(er))
            os.remove(proto.cur_dir + "/PostUpdate.txt")

        self.setWindowTitle('Metin2 Info')
        QtCore.QCoreApplication.setOrganizationName("Akihiko")
        QtCore.QCoreApplication.setApplicationName("Metin2 Info")
        self.setWindowIcon(QtGui.QIcon("assets/icon/metin2.ico"))


        self.MainWidget = QtWidgets.QWidget(self) #Widget Principale
        self.resize(600, 450) #Ridimensiona la finestra

        #Setta il Widget Principale come Centrale
        self.setCentralWidget(self.MainWidget)

        proto.item_data = metin2Class.item_data(proto.cur_dir + "/file/item_proto_dump.xml", proto.cur_dir + "/file/item_proto_dump_en.xml")

        proto.mob_data = metin2Class.mob_data(proto.cur_dir + "/file/mob_proto_dump.xml", proto.cur_dir + "/file/mob_proto_dump_en.xml")
    
        self.ItemWidget = QtMetin2.widget_item(self)
        self.MobWidget = QtMetin2.widget_mob(self)
        self.ItemXMLWidget = QtMetin2.widget_XML_item(self)
        self.MobXMLWidget = QtMetin2.widget_XML_mob(self)

        self.tabber = QtWidgets.QTabWidget(self.MainWidget)

        self.tabber.insertTab(0, self.ItemWidget, "Info Item")
        self.tabber.insertTab(1, self.ItemXMLWidget, "Ricerche Dati Item")
        self.tabber.insertTab(2, self.MobWidget, "Info Mob")
        self.tabber.insertTab(3, self.MobXMLWidget, "Ricerche Dati Mob")

        grid = QtWidgets.QGridLayout(self.MainWidget)
        grid.addWidget(self.tabber, 0, 0, 1, 1)

        self.create_menu()
        self.set_download_file()

    def create_menu(self):

        self.change_file = QtWidgets.QAction("Dati Test Server", self, checkable=True)
        self.change_file.setStatusTip("Cambia i dati attuali con quelli del Server di Test. Clicca per cambiare.")
        self.change_file.triggered.connect(lambda: proto.gestore_opzioni.change_option("Platform", self.change_file.isChecked()))

        self.change_trad = QtWidgets.QAction("Traduci Nomi Mob", self, checkable=True)
        self.change_trad.setStatusTip("Cambia il modo in cui vengono mostriti i nomi dei mostri. Più veloce se disattivato.Clicca per cambiare.")
        self.change_trad.triggered.connect(lambda: proto.gestore_opzioni.change_option("TradMob", self.change_trad.isChecked()))

        update = QtWidgets.QAction("Aggiorna", self)
        update.setShortcut("Ctrl+A")
        update.setStatusTip("Verifica se sono presenti aggiornamenti del programma")
        update.triggered.connect(self.open_update)
   
        esci = QtWidgets.QAction("Esci", self)
        esci.setShortcut("Ctrl+Q")
        esci.setStatusTip("Esci dall'Applicazione")
        esci.triggered.connect(QtCore.QCoreApplication.quit)

        download_icon = QtWidgets.QAction("Scarica Icone", self)
        download_icon.setStatusTip("Scarica tutte le icone per migliorare leggermente le performance")
        download_icon.triggered.connect(QtMetin2.download_all_icon)

        check_all_set_up = QtWidgets.QAction("Controlla Set Up", self)
        check_all_set_up.setStatusTip("Controlla tutti i set up e verifica se sono presentinel database")
        check_all_set_up.triggered.connect(QtMetin2.check_set_up)

        check_all_item_type = QtWidgets.QAction("Controlla Dati Item", self)
        check_all_item_type.setStatusTip("Controlla tutti gli item type degli oggetti, alla ricerca di nuovi")
        check_all_item_type.triggered.connect(QtMetin2.check_all_item_type)

        check_all_mob_type = QtWidgets.QAction("Controlla Dati Mob", self)
        check_all_mob_type.setStatusTip("Controlla tutti i type dei mostri, alla ricerca di nuovi")
        check_all_mob_type.triggered.connect(QtMetin2.check_all_mob_type)

        stamp_diff_item_proto = QtWidgets.QAction("Stampa Differenze Item Proto", self)
        stamp_diff_item_proto.setStatusTip("Confronta l'attuale item proto con uno inserito dall'utente, poi stampa i risultati")
        stamp_diff_item_proto.triggered.connect(QtMetin2.diff_item_proto)

        stamp_diff_mob_proto = QtWidgets.QAction("Stampa Differenze Mob Proto", self)
        stamp_diff_mob_proto.setStatusTip("Confronta l'attuale item proto con uno inserito dall'utente, poi stampa i risultati")
        stamp_diff_mob_proto.triggered.connect(QtMetin2.diff_mob_proto)

        stamp_diff_mob_proto = QtWidgets.QAction("Download Interwiki", self)
        stamp_diff_mob_proto.setStatusTip("[TEST] Crea u file id interwiki per tutti gli oggetti")
        stamp_diff_mob_proto.triggered.connect(QtMetin2.download_interwiki)

        info_aiuto = QtWidgets.QAction("Info sui Dati", self)
        info_aiuto.setStatusTip("Visualizza una guida esplicativa sui vari dati presenti.")
        info_aiuto.triggered.connect(lambda: QtMetin2.open_info_aiuto(self))

        info = QtWidgets.QAction("Informazioni", self)
        info.setStatusTip("Visualizza varie informazioni sul programma")
        info.triggered.connect(QtMetin2.open_info)
        
        menu = self.menuBar()
        self.statusBar()
        
        file = menu.addMenu('&File')
        file.addAction(self.change_file)
        file.addAction(self.change_trad)
        file.addAction(update)
        file.addAction(esci)

        if (proto.gestore_opzioni.get_option("Debug") == 1):
            debug = menu.addMenu('&Debug')
            debug.addAction(download_icon)
            debug.addAction(check_all_set_up)
            debug.addAction(check_all_item_type)
            debug.addAction(check_all_mob_type)

        tool = menu.addMenu('&Tool')
        tool.addAction(stamp_diff_item_proto)
        tool.addAction(stamp_diff_mob_proto)

        aiuto = menu.addMenu('&Aiuto')
        aiuto.addAction(info_aiuto)
        aiuto.addAction(info)

    def set_download_file(self):
        value = proto.gestore_opzioni.get_option("Platform")
        proto.gestore_opzioni.change_option("Platform", value)
        if (int(value) == 1):
            self.change_file.setChecked(True)
        else:
            self.change_file.setChecked(False)

    def open_update(self):
        self.AutoUpdate = self.widget_update()
        self.AutoUpdate.setWindowTitle('Aggiornamento Programma')
        self.AutoUpdate.show()

    def get_actual_version(self):
        opt1 = proto.gestore_opzioni.get_option("Version")
        opt2 = proto.gestore_opzioni.get_option("SubVersion")
        return str(opt1) + "." + str(opt2)

    def retrieve_version(self):
        try:
            QtMetin2.download(proto.UPDATE_SITE + "version.txt", proto.cur_dir + "/version.txt")
            fp = open(proto.cur_dir + "/version.txt", "r")
            for line in fp.readlines():
                ver = line.replace("\n", "")
            fp.close()
            os.remove(proto.cur_dir + '/version.txt')
        except Exception as er:
            proto.err("Impossibile verificare la versione del programma" + str(er))
            proto.stampa_errore("Impossibile verificare la versione del programma" + str(er))
            return 0.0
        return ver

    def check_download_program(self):
        ver = self.retrieve_version()
        ver_at = self.get_actual_version()
        if (ver == ver_at):
            QtMetin2.info("Hai già l'ultima versione")
        else:
            self.download_program()

    def download_program(self):
        self.UpdatePer.show()
        ver = self.retrieve_version()
        ver_at = self.get_actual_version()
        name = r"Metin2 Info " + str(ver) + ".exe"
        try:
            QtMetin2.download_bar(self, proto.UPDATE_SITE + "Metin2_Info.exe", proto.cur_dir + "/" + name)
        except Exception as er:
            QtMetin2.errore("Impossibile scaricare la nuova versione del programma\n" + str(er))
            proto.stampa_errore("Impossibile scaricare versione nuova del programma\n" + str(er))
            proto.err(str(er))
            return
        proto.gestore_opzioni.set_option("Version", int(ver.split(".")[0]))
        proto.gestore_opzioni.set_option("SubVersion", int(ver.split(".")[1]))
        self.UpdatePer.hide()
        pid = os.getpid()
        fp = open(proto.cur_dir + "/PostUpdate.txt", "w")
        fp.write(str(pid) + "\n")
        fp.write(ver_at)
        fp.flush()
        fp.close()
        os.startfile(proto.cur_dir + "/" + name, "open")

    def widget_update(self):
        UpdateWidget = QtWidgets.QWidget() #Widget dell'Aggiornamento
        self.UpdateTitleLabel = QtWidgets.QLabel('Changelog:')
        self.textEditUpdate = QtWidgets.QTextEdit(UpdateWidget)
        self.AutoUpdateConf = QtWidgets.QCheckBox("Abilita Auto Aggiornamento")
        self.UpdatePButton = QtWidgets.QPushButton("Aggiorna Programma")
        self.UpdatePer = QtWidgets.QProgressBar()
        self.UpdatePer.hide()
        try:
            QtMetin2.download(proto.UPDATE_SITE + "changelog.txt", proto.cur_dir + "/changelog_temp.txt")
        except Exception as er:
            proto.err("Impossibile scaricare il changelog: " + str(er))
            proto.stampa_errore("Impossibile scaricare il changelog: " + str(er))
        fp2 = open(proto.cur_dir + "/changelog_temp.txt", "r")
        out = open(proto.cur_dir + "/changelog.txt", "w")
        for line in fp2.readlines():
            out.write(line)
        out.flush()
        out.close()
        fp2.close()
        os.remove(proto.cur_dir + "/changelog_temp.txt")
        try:
            fp = open(proto.cur_dir + "/changelog.txt", "r")
            for line in fp.readlines():
                line = line.replace("\n", "")
                self.textEditUpdate.append(line)
            fp.close()
        except Exception as er:
            self.textEditUpdate.setText("Nessun Changelog Disponibile")
            proto.err("Nessun Changelog Disponibile: " + str(er))
            proto.stampa_errore("impossible aprire Changelog: " + str(er))
        self.textEditUpdate.setReadOnly(True)
        self.textEditUpdate.moveCursor(QtGui.QTextCursor.Start)
        self.textEditUpdate.ensureCursorVisible()
        gridAupdate = QtWidgets.QGridLayout(UpdateWidget)

        gridAupdate.addWidget(self.UpdateTitleLabel, 0, 1)
        gridAupdate.addWidget(self.textEditUpdate, 1, 0, 1, 3)
        gridAupdate.addWidget(self.AutoUpdateConf, 2, 0, 1, 2)
        gridAupdate.addWidget(self.UpdatePButton, 2, 2)
        gridAupdate.addWidget(self.UpdatePer, 3, 0, 1, 3)

        self.AutoUpdateConf.setChecked(proto.inttobool(proto.gestore_opzioni.get_option("Update/AutoUpdate")))
        self.UpdatePButton.clicked.connect(self.check_download_program)
        self.AutoUpdateConf.clicked.connect(self.update_conf_agg)
        return UpdateWidget

    def update_conf_agg(self):
        proto.gestore_opzioni.set_option("Update/AutoUpdate", proto.booltoint(self.AutoUpdateConf.isChecked()))

app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
ver = main.get_actual_version()
ver2 = main.retrieve_version()
if (float(ver) < float(ver2)):
    main.open_update()
else:
    main.show()
sys.exit(app.exec_())
