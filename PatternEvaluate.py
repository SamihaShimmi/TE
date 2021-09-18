import os
import filecmp
from datetime import time

import generateXMLLinebyLine
from xml.etree import ElementTree

parentRoot = r"H:\Research\TestEvolution\TE\XMLHolders\\"
fileNamesSourceJavaV2 = list()
fileNamesSourceJavaV1 = list()
fileNamesTestJava = list()
fileNameSourceSplitted = list()
fileNameTestSplitted = list()
classCount = 0
testFileNames = list()

loopC = 0

def fileNames(path,extensionSent):
    listOfFilesTemp = list()
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        listOfFilesTemp += [os.path.join(dirpath, file) for file in filenames]

    for item in listOfFilesTemp:
        extension = os.path.splitext(item)[1]
        if extension == extensionSent:
            listOfFiles.append((item))
    return listOfFiles
fileNameList = fileNames("H:\Research\TestEvolution\DataAnalysis\jfreechart-1.5.2\jfreechart-1.5.2\src\main\java\org",".java")
print(fileNameList)
