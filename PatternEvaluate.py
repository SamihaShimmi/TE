import os
import filecmp
from datetime import time

import generateXMLLinebyLine
from xml.etree import ElementTree

parentRootV2 = r"H:\Research\TestEvolution\TE\XMLHolders\P2\\v2"
sourceCodePathv2= "H:\Research\TestEvolution\DataAnalysis\mug-mug-root-5.2\mug-mug-root-5.2\mug\src\main"
parentRootV1 = r"H:\Research\TestEvolution\TE\XMLHolders\P2\\v1"
sourceCodePathv1= "H:\Research\TestEvolution\DataAnalysis\mug-mug-root-5.0\mug-mug-root-5.0\mug\src\main"
deprecatedMethodListV1 = list()
deprecatedMethodListV2 = list()


loopC = 0

def parseFunctionName(xmlFileName):

    root = ElementTree.parse(xmlFileName).getroot()
    name = root.find("name").text
    return name

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

def javaToXMLPreprocessing(fileNameListV2,parentRoot):
    for name in fileNameListV2:
        nameParsed = name.rpartition(".java")
        parseName = nameParsed[0].rpartition("\\")
        tuk = name.rpartition(sourceCodePathv2)
        outFolder = (tuk[2].rpartition(".java"))
        if not os.path.exists(parentRoot + outFolder[0]):
            os.makedirs(parentRoot + outFolder[0], 0o777)
        javaToXML(parseName[2] + ".xml", name, parentRoot + outFolder[0] + r"\\")

def removeExtraBracket(xmlFile):

    with open(xmlFile, 'rb+') as f:
        f.seek(f.tell() - 1, 2)  # f.seek(0,2) is legal for last char in both python 2 and 3 though
        chu = f.read()
        my_str_as_bytes1 = str.encode("}")
        my_str_as_bytes2 = str.encode(")")
        if my_str_as_bytes1 == chu or my_str_as_bytes2 == chu:
            f.seek(-1, os.SEEK_END)
            f.truncate()

def parseNode(xmlFile):
    temp = list()
    with open(xmlFile,"rt") as f:
        methodName = str()
        temp.append(xmlFile)
        for line in f:
            if "<annotation>@<name>Deprecated" in line:
                print("deprecated found")
                methodName = parseFunctionName(xmlFile)
                #print(methodName)
                temp.append(methodName)
                deprecatedMethodListV2.append(temp)
                break



def parseFunction(xmlFile,elementName,functionStorePath):
    print("location")
    print(functionStorePath)
    try:
        root = ElementTree.parse(xmlFile).getroot()
    except Exception as e:
        print(e)
    elements = list()
    elementCount = 0
    for item in root.iter(elementName):
        #print(ElementTree.tostring(item, encoding='unicode', method='xml'))
        file = open(functionStorePath+r"\\"+elementCount.__str__()+".xml","wt")
        file.write(ElementTree.tostring(item, encoding='unicode', method='xml'))
        elementCount += 1
        elements.append(ElementTree.tostring(item, encoding='unicode', method='xml'))
    return elements

def XMLParser(XMLfileNameList,parentRoot):
    count = 0
    for item in XMLfileNameList:
        #itemTemp = r"H:\Research\TestEvolution\TE\XMLHolders\P2\v2\xmlTemp\temp.xml"
        itemTemp = parentRoot + r"\xmlTemp\temp.xml"

        with open(item,"rt") as fin:
            with open(itemTemp,"wt") as fout:
                for line in fin:
                    fout.write(line.replace('http://www.srcML.org/srcML/src', ''))
            print("-----------------------------")
            print(item)
            functionStorePath = item.rpartition("\\")[0]
            elementsFetched = parseFunction(itemTemp,"function",functionStorePath)
            for element in elementsFetched:
                if "Deprecated" in element:
                    count += 1
            findDeprecated(functionStorePath)
    print("total deprecated found ")
    print(count)

def findDeprecated(functionStorePath):
    print("printing the xml created")
    listOfFiles = fileNames(functionStorePath,".xml")

    for item in listOfFiles:
        if (item.rpartition("\\")[2].rpartition(".xml")[0].isnumeric()) == False:
            listOfFiles.remove(item)
    print(listOfFiles)

    for item in listOfFiles:
        removeExtraBracket(item)
        parseNode(item)


def do():
    fileNameListV2 = fileNames(sourceCodePathv2, ".java")
    javaToXMLPreprocessing(fileNameListV2,parentRootV2)
    XMLfileNameListV2 = fileNames(parentRootV2, ".xml")
    XMLParser(XMLfileNameListV2,parentRootV2)
    '''
    fileNameListV1 = fileNames(sourceCodePathv1, ".java")
    javaToXMLPreprocessing(fileNameListV2, parentRootV2)
    XMLfileNameListV2 = fileNames(parentRootV2, ".xml")
    XMLParser(XMLfileNameListV2, parentRootV2)
    '''

    print(deprecatedMethodListV2)


do()
