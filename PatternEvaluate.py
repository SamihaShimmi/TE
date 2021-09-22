import os
import filecmp
from datetime import time

import generateXMLLinebyLine
from xml.etree import ElementTree

parentRoot = r"H:\Research\TestEvolution\TE\XMLHolders\\P2"
sourceCodePathv2= "H:\Research\TestEvolution\DataAnalysis\mug-mug-root-5.2\mug-mug-root-5.2\mug\src"


loopC = 0

def javaToXML(nameWithoutPath,fileNameFull,outPath):

    cmd = "srcml " + fileNameFull + " -o " +outPath+nameWithoutPath
    os.popen(cmd).read()


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

def javaToXMLPreprocessing(fileNameList):
    for name in fileNameList:
        nameParsed = name.rpartition(".java")
        parseName = nameParsed[0].rpartition("\\")
        tuk = name.rpartition(sourceCodePathv2)
        outFolder = (tuk[2].rpartition(".java"))
        tt = outFolder[0].rpartition("\\")
        if not os.path.exists(parentRoot + outFolder[0]):
            os.makedirs(parentRoot + outFolder[0], 0o777)
        javaToXML(parseName[2] + ".xml", name, parentRoot + outFolder[0] + r"\\")


def parseNode(xmlFile):
    print("-----------------------------")
    print(xmlFile)
    try:
        root = ElementTree.parse(xmlFile).getroot()
    except Exception as e:
        print(e)
    for item in root.iter("function"):
        print("*******************************************************************")
        print("function")


def XMLParser(XMLfileNameList):
    for item in XMLfileNameList:
        itemTemp = r"H:\Research\TestEvolution\TE\XMLHolders\P2\xmlTemp\temp.xml"
        with open(item,"rt") as fin:
            with open(itemTemp,"wt") as fout:
                for line in fin:
                    fout.write(line.replace('http://www.srcML.org/srcML/src', ''))
            print(item)
            parseNode(itemTemp)

def do():
    fileNameList = fileNames(sourceCodePathv2, ".java")

    javaToXMLPreprocessing(fileNameList)
    XMLfileNameList = fileNames(parentRoot, ".xml")

    XMLParser(XMLfileNameList)

do()
