import os
import filecmp
from datetime import time

import generateXMLLinebyLine
from xml.etree import ElementTree

parentRootMain = r"H:\Research\TestEvolution\TE\XMLHolders\P2"
parentRootV2 = r"H:\Research\TestEvolution\TE\XMLHolders\P2\\v2"
sourceCodePathv2= "H:\Research\TestEvolution\DataAnalysis\mug-mug-root-5.2\mug-mug-root-5.2\mug\src\main\java\com\google\mu"
#sourceCodePathv2="H:\Research\TestEvolution\DataAnalysis\joda-time-2.10.9\src\main\java\org\joda\time"
parentRootV1 = r"H:\Research\TestEvolution\TE\XMLHolders\P2\\v1"
sourceCodePathv1= "H:\Research\TestEvolution\DataAnalysis\mug-mug-root-5.0\mug-mug-root-5.0\mug\src\main\java\com\google\mu"
testCodePathV1 = r"H:\Research\TestEvolution\DataAnalysis\mug-mug-root-5.0\mug-mug-root-5.0\mug\src\test\java\com\google\mu"
parentRootTestV1 = r"H:\Research\TestEvolution\TE\XMLHolders\P2\\v1Test"
totalNumberOfMethodsFound = 0


#sourceCodePathv1="H:\Research\TestEvolution\DataAnalysis\joda-time-2.8.2\src\main\java\org\joda\time"
deprecatedMethodListV1 = list()
deprecatedMethodListV2 = list()

def XMLToJava(fileName,outFileName):
    cmd = "srcml " + fileName + " -o " + outFileName
    #print(cmd)
    os.popen(cmd).read()


def parseFunctionName(xmlFileName):

    try:
        root = ElementTree.parse(xmlFileName).getroot()
        name = root.find("name").text
        return name
    except Exception as e:
        print("error occured here")
        return "none"

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

def javaToXMLPreprocessing(fileNameList,parentRoot,sourceCodePath):
    for name in fileNameList:
        nameParsed = name.rpartition(".java")
        parseName = nameParsed[0].rpartition("\\")
        tuk = name.rpartition(sourceCodePath)
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

def parseNode(xmlFile,version):
    temp = list()
    with open(xmlFile,"rt") as f:
        methodName = str()
        temp.append(xmlFile)

        if version == 1:
            parsedFilePath = xmlFile.rpartition(parentRootV1)[2].rpartition("\\")[0]
        elif version == 2:
            parsedFilePath = xmlFile.rpartition(parentRootV2)[2].rpartition("\\")[0]

        temp.append(parsedFilePath)
        for line in f:
            if "<annotation>@<name>Deprecated" in line:
                #print("deprecated found")
                methodName = parseFunctionName(xmlFile)
                #print(methodName)
                temp.append(methodName)
                if version == 1:
                    deprecatedMethodListV1.append(temp)
                elif version == 2:
                    deprecatedMethodListV2.append(temp)
                break

def parseFunctionTest(xmlFile,elementName,functionStorePath):
    #print("location")
    #print(functionStorePath)
    try:
        root = ElementTree.parse(xmlFile).getroot()
    except Exception as e:
        print(e)
    elements = list()
    elementCount = 0
    try:
        for item in root.iter(elementName):
            #print(ElementTree.tostring(item, encoding='unicode', method='xml'))
            file = open(functionStorePath+r"\\"+elementCount.__str__()+".xml","wt")
            file.write("<unit>")
            file.write(ElementTree.tostring(item, encoding='unicode', method='xml'))
            file.write("</unit>")
            file.close()

            outPath = functionStorePath + r"\\" + elementCount.__str__() + ".java"
            XMLToJava(functionStorePath + r"\\" + elementCount.__str__() + ".xml",outPath)

            elementCount += 1
            elements.append(ElementTree.tostring(item, encoding='unicode', method='xml'))
    except Exception as e:
        print("error occured ")
        print(e)
    return elements


def parseFunction(xmlFile,elementName,functionStorePath):
    #print("location")
    #print(functionStorePath)
    try:
        root = ElementTree.parse(xmlFile).getroot()
    except Exception as e:
        print(e)
    elements = list()
    elementCount = 0
    try:
        for item in root.iter(elementName):
            #print(ElementTree.tostring(item, encoding='unicode', method='xml'))
            file = open(functionStorePath+r"\\"+elementCount.__str__()+".xml","wt")
            #file.write("<unit>")
            file.write(ElementTree.tostring(item, encoding='unicode', method='xml'))
            #file.write("</unit>")
            file.close()

            outPath = functionStorePath + r"\\" + elementCount.__str__() + ".java"
            #XMLToJava(functionStorePath + r"\\" + elementCount.__str__() + ".xml",outPath)

            elementCount += 1
            elements.append(ElementTree.tostring(item, encoding='unicode', method='xml'))

    except Exception as e:
        print("error occured ")
        print(e)
    return elements

def XMLParserTestCode(XMLfileNameList,parentRoot):
    count = 0
    for item in XMLfileNameList:
        #itemTemp = r"H:\Research\TestEvolution\TE\XMLHolders\P2\v2\xmlTemp\temp.xml"
        itemTemp = parentRoot + r"\xmlTemp\temp.xml"

        with open(item,"rt") as fin:
            with open(itemTemp,"wt") as fout:
                for line in fin:
                    fout.write(line.replace('http://www.srcML.org/srcML/src', ''))
            #print("-----------------------------")
            #print(item)
            functionStorePath = item.rpartition("\\")[0]
            elementsFetched = parseFunctionTest(itemTemp,"function",functionStorePath)
            #print("elements fetched")
            #print(elementsFetched)




def XMLParser(XMLfileNameList,parentRoot,version):
    count = 0
    for item in XMLfileNameList:
        #itemTemp = r"H:\Research\TestEvolution\TE\XMLHolders\P2\v2\xmlTemp\temp.xml"
        itemTemp = parentRoot + r"\xmlTemp\temp.xml"

        with open(item,"rt") as fin:
            with open(itemTemp,"wt") as fout:
                for line in fin:
                    fout.write(line.replace('http://www.srcML.org/srcML/src', ''))
            #print("-----------------------------")
            #print(item)
            functionStorePath = item.rpartition("\\")[0]
            elementsFetched = parseFunction(itemTemp,"function",functionStorePath)
            for element in elementsFetched:
                if "Deprecated" in element:
                    count += 1
            findDeprecated(functionStorePath,version)
    print("total deprecated found ")
    print(count)

def findDeprecated(functionStorePath,version):
    #print("printing the xml created")
    listOfFiles = fileNames(functionStorePath,".xml")

    for item in listOfFiles:
        if (item.rpartition("\\")[2].rpartition(".xml")[0].isnumeric()) == False:
            listOfFiles.remove(item)
    #print(listOfFiles)

    for item in listOfFiles:
        removeExtraBracket(item)
        parseNode(item,version)

def findDeprecatedMethodsInTestCase(functionsTestAll,deprecatedAddedList):
    for i in range(0,len(deprecatedAddedList)):
        toCheck = deprecatedAddedList[i][1]+"("
        print(toCheck)
    for item in functionsTestAll:
        file = open(item,"rt")
        for line in file:
            if "toListAndThen" in line:
                print("found")
                break



def do():


    fileNameListV2 = fileNames(sourceCodePathv2, ".java")
    javaToXMLPreprocessing(fileNameListV2,parentRootV2,sourceCodePathv2)
    XMLfileNameListV2 = fileNames(parentRootV2, ".xml")
    XMLParser(XMLfileNameListV2,parentRootV2,2)

    fileNameListV1 = fileNames(sourceCodePathv1, ".java")
    javaToXMLPreprocessing(fileNameListV1, parentRootV1, sourceCodePathv1)
    XMLfileNameListV1 = fileNames(parentRootV1, ".xml")
    XMLParser(XMLfileNameListV1, parentRootV1, 1)

    '''
    print("v1")
    print(len(deprecatedMethodListV1))
    print(deprecatedMethodListV1)
    print("v2")
    print(len(deprecatedMethodListV2))
    print(deprecatedMethodListV2)
    '''
    for i in range (0,len(deprecatedMethodListV1)):
        for j in range(0,len(deprecatedMethodListV2)):
            if deprecatedMethodListV1[i][1] == deprecatedMethodListV2[j][1] and deprecatedMethodListV1[i][2] == deprecatedMethodListV2[j][2]:
                deprecatedMethodListV2[j][2]="ss"
                break
    '''
    print("v1")

    print(deprecatedMethodListV1)
    print("v2")

    print(deprecatedMethodListV2)
    '''
    print("difference")
    deprecatedAddedList = list()
    for i in deprecatedMethodListV2:
        temp = list()
        if i[2] != "ss":
            temp.append(i[1])
            temp.append(i[2])
            print(i[1])
            print(i[2])
            deprecatedAddedList.append(temp)

    testfileNameListV1 = fileNames(testCodePathV1, ".java")

    
    javaToXMLPreprocessing(testfileNameListV1,parentRootTestV1,testCodePathV1)
    XMLfileNameListTestV1 = fileNames(parentRootTestV1, ".xml")
    XMLParserTestCode(XMLfileNameListTestV1, parentRootTestV1)

    functionsTestAll = fileNames(parentRootTestV1,".java")
    print(functionsTestAll)
    findDeprecatedMethodsInTestCase(functionsTestAll,deprecatedAddedList)

do()
