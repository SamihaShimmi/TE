import os
import filecmp
from datetime import time

import generateXMLLinebyLine
from xml.etree import ElementTree

parentRootMain = r"H:\Research\TestEvolution\TE\XMLHolders\P3"
parentRootV2 = r"H:\Research\TestEvolution\TE\XMLHolders\P3\\v2"
sourceCodePathv2 = r"H:\Research\TestEvolution\DataAnalysis\pmd-pmd_releases-6.21.0\pmd-pmd_releases-6.21.0\pmd-java\src\main\java\net\sourceforge\pmd"
# sourceCodePathv2="H:\Research\TestEvolution\DataAnalysis\joda-time-2.10.9\src\main\java\org\joda\time"
parentRootV1 = r"H:\Research\TestEvolution\TE\XMLHolders\P3\\v1"
sourceCodePathv1 = "H:\Research\TestEvolution\DataAnalysis\pmd-pmd_releases-6.20.0\pmd-pmd_releases-6.20.0\pmd-java\src\main\java\net\sourceforge\pmd"
testCodePathV1 = r"H:\Research\TestEvolution\DataAnalysis\mug-mug-root-5.0\mug-mug-root-5.0\mug\src\test\java\com\google\mu"
parentRootTestV1 = r"H:\Research\TestEvolution\TE\XMLHolders\P3\\v1Test"
totalNumberOfMethodsFound = 0

# sourceCodePathv1="H:\Research\TestEvolution\DataAnalysis\joda-time-2.8.2\src\main\java\org\joda\time"
deprecatedMethodListV1 = list()
deprecatedMethodListV2 = list()


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
    # print(functionStorePath)
    f = open(ParentRootV+r"\\imports.txt","a")
    f.write(functionStorePath)
    try:
        root = ElementTree.parse(xmlFile).getroot()
    except Exception as e:
        print(e)
    elements = list()
    elementCount = 0
    try:
        for item in root.iter(elementName):
            # print(ElementTree.tostring(item, encoding='unicode', method='xml'))
            file = open(functionStorePath + r"\\" + elementCount.__str__() + ".xml", "wt")
            # file.write("<unit>")
            file.write(ElementTree.tostring(item, encoding='unicode', method='xml'))
            f.write(ElementTree.tostring(item, encoding='unicode', method='text'))
            # file.write("</unit>")
            file.close()

            outPath = functionStorePath + r"\\" + elementCount.__str__() + ".java"
            # XMLToJava(functionStorePath + r"\\" + elementCount.__str__() + ".xml",outPath)

            elementCount += 1
            elements.append(ElementTree.tostring(item, encoding='unicode', method='xml'))

    except Exception as e:
        print("error occured ")
        print(e)
    return elements

def XMLParser(XMLfileNameList, parentRoot, version):
    count = 0
    for item in XMLfileNameList:
        # itemTemp = r"H:\Research\TestEvolution\TE\XMLHolders\P3\v2\xmlTemp\temp.xml"
        itemTemp = parentRoot + r"\xmlTemp\temp.xml"

        with open(item, "rt") as fin:
            with open(itemTemp, "wt") as fout:
                for line in fin:
                    fout.write(line.replace('http://www.srcML.org/srcML/src', ''))
            # print("-----------------------------")
            # print(item)
            functionStorePath = item.rpartition("\\")[0]
            if version == 1:
                elementsFetched = parseImport(itemTemp, "import", functionStorePath,parentRootV1)
            elif version == 2:
                elementsFetched = parseImport(itemTemp, "import", functionStorePath,parentRootV2)

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


def do():
    fileNameListV2 = fileNames(sourceCodePathv2, ".java")
    javaToXMLPreprocessing(fileNameListV2, parentRootV2, sourceCodePathv2)
    XMLfileNameListV2 = fileNames(parentRootV2, ".xml")
    print(XMLfileNameListV2)
    XMLParser(XMLfileNameListV2, parentRootV2, 2)

    fileNameListV1 = fileNames(sourceCodePathv1, ".java")
    javaToXMLPreprocessing(fileNameListV1, parentRootV1, sourceCodePathv1)
    XMLfileNameListV1 = fileNames(parentRootV1, ".xml")
    print(XMLfileNameListV1)
    XMLParser(XMLfileNameListV1, parentRootV1, 1)

    '''
    

    fileNameListV1 = fileNames(sourceCodePathv1, ".java")
    javaToXMLPreprocessing(fileNameListV1, parentRootV1, sourceCodePathv1)
    XMLfileNameListV1 = fileNames(parentRootV1, ".xml")
    XMLParser(XMLfileNameListV1, parentRootV1, 1)

    testfileNameListV1 = fileNames(testCodePathV1, ".java")

    javaToXMLPreprocessing(testfileNameListV1, parentRootTestV1, testCodePathV1)
    XMLfileNameListTestV1 = fileNames(parentRootTestV1, ".xml")
    XMLParserTestCode(XMLfileNameListTestV1, parentRootTestV1)

    functionsTestAll = fileNames(parentRootTestV1, ".java")
    print(functionsTestAll)
   '''


do()
