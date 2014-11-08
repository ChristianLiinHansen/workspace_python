# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 14:24:42 2014

@author: christian
"""

#Imports
import os

#Introduction note
print("This program renames the files")

def rename_files():
    #Get the file names    
    file_list = os.listdir("/home/christian/Dropbox/E14/MasterThesis/PythonTutorials/prank")
    
    #Be sure that the computer looks in the right folder
    saved_path = os.getcwd();       
    print(saved_path)
    
    #Well it did not.. So we change the directory. 
    os.chdir("/home/christian/Dropbox/E14/MasterThesis/PythonTutorials/prank")

    #Check again...
    saved_path = os.getcwd()
    print(saved_path)
    
    #Print this
    print(file_list)
    
    for file_name in file_list:
        os.rename(file_name, file_name.translate(None,"0123456789"))
        
rename_files()  