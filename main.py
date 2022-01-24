import os, sys
import datetime
from PyQt5 import QtWidgets
from CheckDir import CheckDir
import shutil



class MainW(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainW, self).__init__(*args, **kwargs)
        # zalozeni hlavniho okna
        mainWid = QtWidgets.QWidget()
        mainWidL = QtWidgets.QVBoxLayout()
        mainWid.setLayout(mainWidL)
        self.setCentralWidget(mainWid)
        self.setWindowTitle("kontrola PLC zaloh")
        self.setMinimumSize(1000,300)
        self.chck = CheckDir()
        try:
            self.paths = self.chck.load_directory()            
        except:
            self.paths = ['-','-']

        
        # vyber adresare c. 1
        self.path1L = QtWidgets.QHBoxLayout()      
        self.path1TextW = QtWidgets.QLabel("Umístění adresář 1: ")
        self.file1W =  QtWidgets.QLabel(self.paths[0][:-1])
        self.file1SelectBut = QtWidgets.QPushButton("Vyber")
        self.path1L.addWidget(self.path1TextW)
        self.path1L.addWidget(self.file1W)
        self.path1L.addWidget(self.file1SelectBut)
        # vyber adresare c. 2
        self.path2L = QtWidgets.QHBoxLayout()      
        self.path2TextW = QtWidgets.QLabel("Umístění adresář 2: ")
        self.file2W =  QtWidgets.QLabel(self.paths[1])
        self.file2SelectBut = QtWidgets.QPushButton("Vyber")
        self.path2L.addWidget(self.path2TextW)
        self.path2L.addWidget(self.file2W)
        self.path2L.addWidget(self.file2SelectBut)
        # start porovnani + vysledky
        self.workInfoLay = QtWidgets.QHBoxLayout()
        self.confButL = QtWidgets.QVBoxLayout()
        self.confButW = QtWidgets.QPushButton("Kontrola")
        self.confButL.addWidget(self.confButW)
        self.actualizeAllBtnW = QtWidgets.QPushButton("Aktualizovat vse")
        self.actualizeAllBtnW.setVisible(False)
        self.confButL.addWidget(self.actualizeAllBtnW)
        self.actualizeBtnW = QtWidgets.QPushButton("Aktualizovat vyber")
        self.actualizeBtnW.setVisible(False)
        self.confButL.addWidget(self.actualizeBtnW)
        self.infoListW = QtWidgets.QListWidget()
        self.infoListW.setSelectionMode(2)
        self.workInfoLay.addLayout(self.confButL)
        self.workInfoLay.addWidget(self.infoListW)
        # pridani do hlavniho layoutu
        mainWidL.addLayout(self.path1L)
        mainWidL.addLayout(self.path2L)
        mainWidL.addStretch()
        mainWidL.addLayout(self.workInfoLay)
        # provoz tlacitek
        self.file1SelectBut.clicked.connect(self.path1Sel)
        self.file2SelectBut.clicked.connect(self.path2Sel)
        self.confButW.clicked.connect(self.checkDirectories)
        self.actualizeAllBtnW.clicked.connect(self.fileAllUpdate)
        self.actualizeBtnW.clicked.connect(self.fileUpdate)

        self.checkDirectories()
        
        self.show()
    # vyber 1. adresare k porovnani
    def path1Sel(self):
        self.file1W.setText(QtWidgets.QFileDialog.getExistingDirectory())
    # vyber 2. adresare k porovnani
    def path2Sel(self):
        self.file2W.setText(QtWidgets.QFileDialog.getExistingDirectory())
    # start porovnani adresaru
    def checkDirectories(self): 
        try:
            self.chck.save_directory(self.file1W.text(), self.file2W.text())
            # vycisteni info panelu
            self.chck.del_info()
            self.infoListW.clear()
            # funkce porovnani
            self.chck.path_area_compare(self.file1W.text(), self.file2W.text())
            # zapis vysledku do infopanelu
            if len(self.chck.infoMissing) + len(self.chck.info) == 0:
                self.infoListW.addItem("Adresare/soubory aktualni  ("+ datetime.datetime.now().strftime("%d.%m.%Y %H:%M")+ ")")
                self.actualizeAllBtnW.setVisible(False)
                self.actualizeBtnW.setVisible(False)
            else:
                for i in self.chck.infoMissing:
                    self.infoListW.addItem(i[0])
                for i in self.chck.info:
                    self.infoListW.addItem(i[0])
                self.actualizeAllBtnW.setVisible(True)
                self.actualizeBtnW.setVisible(True)
            print("done")
        except:
            self.infoListW.addItem("Zkontrolujte prosim aktualnost zadanych cest...")
    # aktualizace souboru
    def fileAllUpdate(self):
        try:
            for i in self.chck.infoMissing:
                # pokud jde o soubor
                if os.path.isfile(i[1]):
                    shutil.copy2(i[1], i[2])
                # pokud jde o adresar
                elif os.path.isdir(i[1]):
                    shutil.copytree(i[1], i[2])
            print('copy missing file done')
            for i in self.chck.info: 
                shutil.copy2(i[1], i[2])    
            print('copy newer file done')
        except:
            self.infoListW.addItem("Neco se pokazilo behem prehravani, zkontrolujte prosim umisteni...")
        self.checkDirectories()

    def fileUpdate(self):
        for i in self.chck.infoMissing:
            for j in self.infoListW.selectedItems():
                if i[0] == j.text():
                    # pokud jde o soubor
                    if os.path.isfile(i[1]):
                        shutil.copy2(i[1], i[2])
                    # pokud jde o adresar
                    elif os.path.isdir(i[1]):
                        shutil.copytree(i[1], i[2])
        for i in self.chck.info:
            for j in self.infoListW.selectedItems():
                if i[0] == j.text():
                    shutil.copy2(i[1], i[2])
        self.checkDirectories()



class App(QtWidgets.QApplication):
    def __init__(self):
        super(App, self).__init__(sys.argv)
    
    def build(self):
        self.mainW = MainW()
        sys.exit(self.exec_())

app = App()
app.build()