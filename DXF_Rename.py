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
        textcontents = GrowingList()
        self.replacement =str(input("What characters should i be looking for to replace?: "))
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
                            print(line)
                            if self.replacement in line:                             
                                textcontents[index] = line
                    except:
                        textcontents[index] = 0
        print(textline)
        print(textcontents)

    def query(self):
        self.replacement =str(input("What characters should i be looking for to replace?: "))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())