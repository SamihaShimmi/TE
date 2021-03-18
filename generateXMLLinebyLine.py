'''
XML generated from SrcMl is not line by line
To parse the XML line by line, XML file is rewritten line by line
'''

import os

import xml.etree.ElementTree as ET
ET.register_namespace("","http://www.srcML.org/srcML/src")

Matrix = list()
loopC1 = 0

def parseValue(toParse1,toParse2):
    listTemp = list()
    str=toParse1.split(">",1)[1]
    global loopC1
    result=str.rpartition("<")
    listTemp.append(result[0])
    str = toParse2.split(">", 1)[1]

    result = str.rpartition("<")
    listTemp.append(result[0])
    loopC1 += 1
    Matrix.append(listTemp)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def processXML(fileName):
    #file1 = open(r"H:\Research\IndStudyDrRahimi\TE\XMLHolders\ASTFieldDeclarationTest\3.xml")

    file1 = open(fileName,"r")
    t = str()

    c = int()

    for line in file1:
        t +=line
        c += 1


    root = ET.fromstring(t)
    tree = ET.ElementTree(root)
    indent(root)
    # writing xml

    if file1:
        file1.close()
    nameLinebyLine = fileName.rpartition('.xml')[0].rpartition(r"\\")[2]+"_"+".xml"
    tree.write(fileName.rpartition('.xml')[0].rpartition(r"\\")[0]+"\\"+fileName.rpartition('.xml')[0].rpartition(r"\\")[1]+nameLinebyLine, encoding="utf-8", xml_declaration=True)
    #getLineCount = lineCount(nameLinebyLine)
    #os.rename(nameLinebyLine,fileName.rpartition('.xml')[0].rpartition(r"\\")[2]+"_"+getLineCount.__str__()+".xml" )


#processXML(r"H:\Research\IndStudyDrRahimi\TE\XMLHolders\ASTFieldDeclarationTest\3.xml")

def lineCount(fileName):
    fileLineCount = open(fileName,"r")
    num_lines = sum(1 for line in fileLineCount)
    if fileLineCount:
        fileLineCount.close()
    return  num_lines
