import os
import filecmp
from datetime import time
from os.path import exists


import generateXMLLinebyLine
from xml.etree import ElementTree

parentRootMain = r"H:\Research\TestEvolution\TE\XMLHolders\P4"
parentRootV2 = r"H:\Research\TestEvolution\TE\XMLHolders\P4\\v2"
sourceCodePathv2 = r"H:\Research\TestEvolution\DataAnalysis\jfreechart-1.5.2\jfreechart-1.5.2\src\main\java\org\jfree"
# sourceCodePathv2="H:\Research\TestEvolution\DataAnalysis\joda-time-2.10.9\src\main\java\org\joda\time"
parentRootV1 = r"H:\Research\TestEvolution\TE\XMLHolders\P4\\v1"
sourceCodePathv1 = r"H:\Research\TestEvolution\DataAnalysis\jfreechart-1.5.0\jfreechart-1.5.0\src\main\java\org\jfree"
testCodePathV1 = r"H:\Research\TestEvolution\DataAnalysis\jfreechart-1.5.0\jfreechart-1.5.0\src\test\java\org\jfree"
parentRootTestV1 = r"H:\Research\TestEvolution\TE\XMLHolders\P4\\v1Test"
totalNumberOfMethodsFound = 0
XMLfileNameListTestV1 = list()
# sourceCodePathv1="H:\Research\TestEvolution\DataAnalysis\joda-time-2.8.2\src\main\java\org\joda\time"
deprecatedMethodListV1 = list()
deprecatedMethodListV2 = list()
alreadyExistingGenericList = list()
addedGenericList = list()
totalNumberOfClassesAffectedTestCase = 0

def XMLToJava(fileName, outFileName):
    cmd = "srcml " + fileName + " -o " + outFileName
    # print(cmd)
    os.popen(cmd).read()


def parseFunctionName(xmlFileName):
    try:
        root = ElementTree.parse(xmlFileName).getroot()
        name = root.find("name").text
        return name
    except Exception as e:
        print("error occured here")
        return "none"


def javaToXML(nameWithoutPath, fileNameFull, outPath):
    cmd = "srcml " + fileNameFull + " -o " + outPath + nameWithoutPath
    os.popen(cmd).read()


def fileNames(path, extensionSent):
    listOfFilesTemp = list()
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        listOfFilesTemp += [os.path.join(dirpath, file) for file in filenames]
    for item in listOfFilesTemp:
        extension = os.path.splitext(item)[1]

        if extension == extensionSent:
            listOfFiles.append((item))
    return listOfFiles


def javaToXMLPreprocessing(fileNameList, parentRoot, sourceCodePath):
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


def parseNode(xmlFile, version):
    temp = list()
    with open(xmlFile, "rt") as f:
        methodName = str()
        temp.append(xmlFile)

        if version == 1:
            parsedFilePath = xmlFile.rpartition(parentRootV1)[2].rpartition("\\")[0]
        elif version == 2:
            parsedFilePath = xmlFile.rpartition(parentRootV2)[2].rpartition("\\")[0]

        temp.append(parsedFilePath)
        for line in f:
            if "<annotation>@<name>Deprecated" in line:
                # print("deprecated found")
                methodName = parseFunctionName(xmlFile)
                # print(methodName)
                temp.append(methodName)
                if version == 1:
                    deprecatedMethodListV1.append(temp)
                elif version == 2:
                    deprecatedMethodListV2.append(temp)
                break


def parseImport(xmlFile, elementName, functionStorePath,ParentRootV):
    # print("location")
    #print(functionStorePath)
    #f = open(ParentRootV+r"\\imports.txt","a")
    #f.write(functionStorePath+"\n")
    result = str()
    try:
        root = ElementTree.parse(xmlFile).getroot()
    except Exception as e:
        print(e)
    elements = list()
    elementCount = 0
    try:
        for item in root.iter(elementName):
            '''
            # print(ElementTree.tostring(item, encoding='unicode', method='xml'))
            file = open(functionStorePath + r"\\" + elementCount.__str__() + ".xml", "wt")
            # file.write("<unit>")
            file.write(ElementTree.tostring(item, encoding='unicode', method='xml'))
            f.write(ElementTree.tostring(item, encoding='unicode', method='text'))
            # file.write("</unit>")
            file.close()
            '''
            #print(ElementTree.tostring(item))
            if not item.find("name"):
                return("no g probably")
            print(item.find("name").text)
            result = item.find("name").find("name").text
            #print(item.find("name").find("name").text)
            print(result)
            genericCheck = item.find("name").find("parameter_list").text
            print(genericCheck)
            if(genericCheck == '<'):
                print("generic found")
                return result

            print("found")
            outPath = functionStorePath + r"\\" + elementCount.__str__() + ".java"
            # XMLToJava(functionStorePath + r"\\" + elementCount.__str__() + ".xml",outPath)

            elementCount += 1
            elements.append(ElementTree.tostring(item, encoding='unicode', method='xml'))

    except Exception as e:
        print("error occured ")
        print(e)
    return elements

def existenceOfGeneric(name):
    global addedGenericList
    if name not in alreadyExistingGenericList:
        print("here")
        addedGenericList.append(name)

def XMLParser(XMLfileNameList, parentRoot, version):
    count = 0
    global alreadyExistingGenericList
    for item in XMLfileNameList:
        # itemTemp = r"H:\Research\TestEvolution\TE\XMLHolders\P4\v2\xmlTemp\temp.xml"
        itemTemp = parentRoot + r"\xmlTemp\temp.xml"
        print(item)
        with open(item, "rt") as fin:
            with open(itemTemp, "wt") as fout:
                for line in fin:
                    fout.write(line.replace('http://www.srcML.org/srcML/src', ''))
            # print("-----------------------------")
            # print(item)
            functionStorePath = item.rpartition("\\")[0]
            if version == 1:
                #elementsFetched = parseImport(itemTemp, "class", functionStorePath,parentRootV1)
                v2Path = item.replace("v1", "v2")
                print(v2Path)
                file_exists = exists(v2Path)
                # print(file_exists)
                if file_exists == True:
                    elementsFetched1 = parseImport(itemTemp, "class", functionStorePath, parentRootV1)
                    print(elementsFetched1)
                    if elementsFetched1 != "no g probably" and len(elementsFetched1) != 0:
                        alreadyExistingGenericList.append(elementsFetched1)
            elif version == 2:
                v1Path = item.replace("v2","v1")
                print(v1Path)
                file_exists = exists(v1Path)
                #print(file_exists)
                if file_exists == True:
                    elementsFetched2 = parseImport(itemTemp, "class", functionStorePath, parentRootV2)
                    print("check")
                    print(elementsFetched2)
                    if elementsFetched2 != "no g probably" and len(elementsFetched2) != 0:
                        print("want this")
                        existenceOfGeneric(elementsFetched2)
                    #elementsFetched1 = parseImport(itemTemp, "class", functionStorePath, parentRootV1)
                    #print(elementsFetched1)

def findDeprecatedMethodsInTestCase(functionsTestAll, deprecatedAddedList):
    global totalNumberOfMethodsFound
    for i in range(0, len(deprecatedAddedList)):
        toCheck = deprecatedAddedList[i][1] + "("
        print(toCheck)
        count = 0
        for item in functionsTestAll:
            file = open(item, "rt")
            for line in file:
                if toCheck in line:
                    totalNumberOfMethodsFound += 1
                    count += 1
                    break
        print("deprecated for this method")
        print(count)

    print("total deprecated ")
    print(totalNumberOfMethodsFound)

def onlyDifLineAPI():
    fOut = open(r"H:\Research\TestEvolution\TE\XMLHolders\P4\v1\diff.txt")
    with open(r"H:\Research\TestEvolution\TE\XMLHolders\P4\v1\imports.txt") as f1:
        with open(r"H:\Research\TestEvolution\TE\XMLHolders\P4\v2\imports.txt") as f2:
            for line in f1:
                if line not in f2:
                    fOut.write(line)
    if fOut:
        fOut.close()
    if f1:
        f1.close()
    if f2:
        f2.close()

def parseGenericClassNumber(xmlFile):
    for item in xmlFile:
        try:
            root = ElementTree.parse(item).getroot()
            print(item)
        except Exception as e:
            print(e)
        for element in root.iter("class"):
            print("found")

def getCountGenericTestCase():
    global totalNumberOfClassesAffectedTestCase
    print("test")
    for item in XMLfileNameListTestV1:
        with open(item, "r") as file:
            for line in file:
                breakCheck = 0
                for i in addedGenericList:
                    if i in line:
                        totalNumberOfClassesAffectedTestCase += 1
                        breakCheck =1
                        break
                if breakCheck == 1:
                    break


def do():
    global XMLfileNameListTestV1
    fileNameListV2 = fileNames(sourceCodePathv2, ".java")
    javaToXMLPreprocessing(fileNameListV2, parentRootV2, sourceCodePathv2)
    XMLfileNameListV2 = fileNames(parentRootV2, ".xml")

    #print(len(XMLfileNameListV2))
    #XMLParser(XMLfileNameListV2, parentRootV2, 2)

    fileNameListV1 = fileNames(sourceCodePathv1, ".java")
    javaToXMLPreprocessing(fileNameListV1, parentRootV1, sourceCodePathv1)
    XMLfileNameListV1 = fileNames(parentRootV1, ".xml")
    print(XMLfileNameListV1)

    print(len(XMLfileNameListV1))

    fileNameListTestV1 = fileNames(testCodePathV1, ".java")
    javaToXMLPreprocessing(fileNameListTestV1, parentRootTestV1, testCodePathV1)
    XMLfileNameListTestV1 = fileNames(parentRootTestV1, ".xml")
    print(XMLfileNameListTestV1)
    print("total test class")
    print(len(XMLfileNameListTestV1))
    #parseGenericClassNumber(XMLfileNameListV2)

    XMLParser(XMLfileNameListV1, parentRootV1, 1)
    XMLParser(XMLfileNameListV2, parentRootV2, 2)
    #onlyDifLineAPI()
    print(alreadyExistingGenericList)
    print(addedGenericList)
    print(len(addedGenericList))
    getCountGenericTestCase()
    print("totalNumberOfClassesAffectedTestCase")
    print(totalNumberOfClassesAffectedTestCase)
do()
