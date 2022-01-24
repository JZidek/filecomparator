import os
import datetime


class CheckDir():
    def __init__(self):
        self.infoMissing = []
        self.info = []
    
    def del_info(self):
        self.infoMissing.clear()
        self.info.clear()

    def path_area_compare(self,path1, path2):
        # obsah cest
        dir1 = os.listdir(path1)
        dir2 = os.listdir(path2)
        # rozdil mezi cestami
        dirdif1 = [f for f in dir1+dir2 if f not in dir1]
        dirdif2 = [f for f in dir1+dir2 if f not in dir2]
        # shoda mezi cestami
        direqual = [f for f in dir1 if f in dir2]
        # all files
        files = [f for f in direqual if os.path.isfile(path1 + "/" + f)]
        # all directories
        directories = [f for f in direqual if os.path.isdir(path1 + "/" + f)]
        # zapis chybejicich souboru/adresaru
        for i in dirdif1:
            self.infoMissing.append(["adresář/soubor   '{}'   nenalezen v umisteni 1.".format(i), path2+"/"+i, path1+"/"+i])
        for i in dirdif2:
            self.infoMissing.append(["adresář/soubor   '{}'   nenalezen v umisteni 2.".format(i), path1+"/"+i, path2+"/"+i])
        for i in files:
            self.file_timestamp_compare(path1, path2, i)    
        
        for i in directories:
            self.path_area_compare(path1+"/"+i, path2+"/"+i)

    # compare files time stamp
    def file_timestamp_compare(self,path1, path2, file1):

        if (os.path.getmtime(path1+"/"+file1) - os.path.getmtime(path2+"/"+file1)) < 0:
            print("detekovan novejsi soubor v {}".format(path2+"/"+file1))
            self.info.append(["detekovan novejsi soubor v {}".format(path2+"/"+file1), path2+"/"+file1, path1+"/"+file1])
            return False
        elif (os.path.getmtime(path1+"/"+file1) - os.path.getmtime(path2+"/"+file1)) > 0:
            print("detekovan novejsi soubor v {}".format(path1+"/"+file1))
            self.info.append(["detekovan novejsi soubor v {}".format(path1+"/"+file1), path1+"/"+file1, path2+"/"+file1])
            return False
        else:
            return False

    def save_directory(self, d1, d2):
        with open('adr.txt', "w", encoding='utf-8') as f:
            f.write(d1 + "\n" + d2)

    def load_directory(self):
        paths = []
        with open('adr.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                paths.append(line)
        return paths
        