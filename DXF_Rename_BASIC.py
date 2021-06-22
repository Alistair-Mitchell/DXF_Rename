import sys
import os
import re

from PyQt5.QtWidgets import *
import PyQt5.QtCore

class GrowingList(list): #Class for doing matlab style lists where you can feed it a value outside the bounds
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)

class App(QDialog):

    def __init__(self):
        super(App,self).__init__() #Standard Qt initilisations
        self.initUI()
    
    def initUI(self):
        
        self.open_fileName_dialog("DXF Files (*.DXF)") #File dialog for .txt and .bdf
        self.populate() #Iterate over all the sets to extract valuesXX
        self.rewrite()
        
        print("OOF")
        sys.exit() 

    def get_download_path(self): #Function to get the download path in windows
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')

    def open_fileName_dialog(self,type): #Function to display file dialog from PyQt
        location = self.get_download_path() #Use earlier download path as start point 
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileNames(self,"IForge GCode uploader", location,type, options=options) #opens a single file dialog box to accept file of specified type
        print(self.fileName)
        return    

    def populate(self,file_spec=""):
        textline = GrowingList()
        self.textcontents = GrowingList()
        for index,tempfile in enumerate(self.fileName):
            with open(tempfile,"r",encoding="utf8") as myfile: #Read into memory the specified file (.bdf/.txt)
                for num, line in enumerate(myfile, 1): #View the file line by line
                    if "ply_name" in line:
                        textline[index]=num+10           
                    if "EOF" in line:
                        try:
                            if textline[index]:
                                break
                        except:
                            textline[index]=0
                    try:
                        if num == textline[index]:
                            print("CURRENT TEXT IS: "+line.rstrip("\n"))
                            self.textcontents[index] = line.rstrip("\n")
                    except:
                        self.textcontents[index] = 0
        # print(self.textcontents)

    def query(self):
        self.replacement =str(input("What characters should i be looking for to replace?: "))
    def rewrite(self):
        self.prefix =str(input("What is the Prefix? (eg '52.' if you wanted 52.01, 52.02 etc): "))
        self.suffix =str(input("What is the Suffix? (eg '-45deg' if you wanted that on the end of everything): "))
        self.start =int(input("Start number?: "))
        self.stop =int(input("Stop number?: "))+1
        
        self.replacement = self.textcontents[0]    
        for index in range(self.start,self.stop):
            number = str(index).zfill(2)
            newtext= self.prefix+number+self.suffix
            name = newtext+".dxf"
            with open(self.fileName[0], 'r') as file :
                filedata = file.read()
            filedata = re.sub(self.replacement, str(newtext), filedata)
            with open(name, 'w') as file:
                file.write(filedata)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())