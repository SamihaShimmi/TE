import os
import filecmp
import generateXMLLinebyLine
from xml.etree import ElementTree

parentRoot = r"H:\Research\IndStudyDrRahimi\TE\XMLHolders\\"
fileNamesSourceJava = list()
fileNamesTestJava = list()
fileNameSourceSplitted = list()
fileNameTestSplitted = list()
classCount = 0
testFileNames = list()

loopC = 0


def XMLToJava(fileName):
    print(fileName)
    cmd = "srcml " + fileName + " -o " + parentRoot+"Output\\javaTmp.java"
    so = os.popen(cmd).read()


def parseOneValue(toParse1):
    listTemp = list()
    str=toParse1.split(">",1)[1]
    result=str.rpartition("<")
    listTemp.append(result[0])
    return listTemp

def parseValue(toParse1,toParse2):
    listTemp = list()
    str=toParse1.split(">",1)[1]
    result=str.rpartition("<")
    listTemp.append(result[0])

    str = toParse2.split(">", 1)[1]
    result = str.rpartition("<")
    listTemp.append(result[0])
    return listTemp


'''
This function parses the function name from the given xml
'''
def parseFunctionName(xmlFileName):

    root = ElementTree.parse(xmlFileName).getroot()
    name = root.find("name").text
    return name


def xmlParser(xmlFileName,methodName):
    with open(xmlFileName, "rt") as fin:
        with open(xmlFileName.rpartition(".xml")[0]+"_.xml", "wt") as fout:
            for line in fin:
                fout.write(line.replace('http://www.srcML.org/srcML/src', ''))

    root = ElementTree.parse(xmlFileName.rpartition(".xml")[0]+"_.xml").getroot()
    for method in root.iter("function"):

        for item in method.findall("name"):

            if item.text.upper() == ("Test"+methodName).upper():
                print("method "+ methodName + "---->" + " test method " + "Test"+methodName)
                return ElementTree.tostring(method, encoding='unicode', method='xml')
            if item.text.upper() == ("Test"+methodName).upper():
                print("method "+ methodName + "---->" + " test method " + "Test"+methodName)
                return ElementTree.tostring(method, encoding='unicode', method='xml')


'''
Given filename, this method generates the XML from java file. So, for each class, we will call this method.
'''
def javaToXML(nameWithoutPath,fileNameFull,outPath):
    fileNameOut = os.path.splitext(fileNameFull)[0] + '.xml'

    cmd = "srcml " + fileNameFull + " -o " +outPath+nameWithoutPath
    so = os.popen(cmd).read()


'''
Given xml filename, this method generates XML for each method in that xml file.
'''
def methodParserXML(filename,filePath):

    print(filePath)
    f = filePath
    file = open(f+filename,"r")

    fileNameOut = "1"
    flag = 0
    fileNameInt = 0

    fileOut = open("dummy.txt","w")
    fileOut2 = open("dummy2.txt", "w")


    for line in file:

        if "<function>" in line:
            if flag == 0:
                flag = 1
                fileNamePrefix = filePath+fileNameOut
                fileOut = open(fileNamePrefix+".xml", "w")
                fileNameInt = int(fileNameOut)
                fileNameInt = fileNameInt + 1
                fileNameOut = fileNameInt.__str__()
            elif flag == 1:
                flag = 2

                fileNamePrefix = filePath+fileNameOut

                fileOut2 = open(fileNamePrefix+".xml", "w")
                fileNameInt = int(fileNameOut)
                fileNameInt = fileNameInt + 1
                fileNameOut = fileNameInt.__str__()

        if flag == 1:
            fileOut.write(line)
        if flag == 2:
            fileOut.write(line)
            fileOut2.write(line)

        if "</function>" in line:
            if flag == 1:
                flag = 0

            elif flag == 2:
                flag = 1

    if fileOut:
        fileOut.close()
    if fileOut2:
        fileOut2.close()
    file.close()


    # In order to generate xsd if line numbers are equal, the following code is added. Redundant code is added
    # But if I do not add multiple loops, the code does not work. I might have to make it efficient later
    files = fileNames(filePath, ".xml")

    # Parsing the xml so that I can count lines
    for items in files:
        if (items.rpartition("\\")[2].rpartition(".xml")[0]).isdigit() == True:
            generateXMLLinebyLine.processXML(items)


    # Removing the old xmls
    files2 = fileNames(filePath, ".xml")
    for items in files2:
        if ("_" not in items  and (items.rpartition("\\")[2].rpartition(".xml")[0]).isdigit() == True) :
            os.remove(items)


    files4 = fileNames(filePath, ".xml")
    for items in files4:
        if (items.rpartition("\\")[2].rpartition("_.xml")[0]).isdigit() == True:
              XMLtoXSD(filePath + items.rpartition("\\")[2].rpartition(".xml")[0] + ".xml", filePath + items.rpartition("\\")[2].rpartition("_.xml")[0] + ".xsd")



    # This code compares all xsds. To check line number, all codes above is added. If I want to remove line number condition
    # I have to uncomment this
    '''
        for i in range(1,fileNameInt):
        XMLtoXSD(filePath+i.__str__()+".xml",filePath+i.__str__()+".xsd" )
    '''

    compareXSD(filePath)


'''
This method generates xsd from each function
'''
def XMLtoXSD(fileName,fileNameOut):

    commandString = r"java -jar trang.jar " + fileName + " " + fileNameOut
    so = os.popen(commandString).read()


'''
This function returns all the  files with some specific extension from a directory
'''
def fileNames(path,extensionSent):
    listOfFilesTemp = list()
    listofFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        listOfFilesTemp += [os.path.join(dirpath, file) for file in filenames]
    for item in listOfFilesTemp:
        extension = os.path.splitext(item)[1]
        if extension == extensionSent:
            listofFiles.append((item))
    return listofFiles


def TestCaseGeneratorSSM(filePath,SSM,trackerTestCase):
    fileTemp = open(parentRoot+r"\\Output\\tmp.txt","a")

    difference = list()
    loop = 0
    for i in trackerTestCase:
        if i != 0:
            break
        loop += 1
    existingSSM = open(filePath+"\\"+SSM[loop].__str__()+"_.xml")
    toGenSSM = open("dummy.txt","r")
    loopCounter =0
    for i in range(0,len(SSM)):
        fileTemp.write(filePath + "\n")
        fileTemp.write("\n")
        if loopCounter == loop:
            continue
        print(SSM[loopCounter])
        toGenSSM = open(filePath+"\\"+SSM[loopCounter].__str__()+"_.xml")
        print(SSM[loop])

        for lineF1 in toGenSSM:
            for lineF2 in existingSSM:
                if lineF1 != lineF2:
                    #print(lineF2 + lineF1)
                    temp = parseValue(lineF2, lineF1)
                    if temp not in difference:
                        difference.append(temp)
                break
        #print(trackerTestCase[loop])
        fileTemp.write(trackerTestCase[loop].__str__() + "\n")
        fileTemp.write(difference.__str__()+"\n")
        fileTemp.write("\n")
        print(difference)

        # generating the test cases

        testMethodPath = parentRoot +"\\Output\\" +"Test.xml"

        try:
            fileTestCodeXML = open(testMethodPath, "w")
            fileTestCodeXML.write(trackerTestCase[loop].__str__())

            if fileTestCodeXML:
                fileTestCodeXML.close()
            generateXMLLinebyLine.processXML(testMethodPath)
            testMethodPath2 = parentRoot + "\\Output\\" + "Test_.xml"
            testMethodPath3 = parentRoot + "\\Output\\" + "generated_.xml"
            fileTestCaseGeneratedTemp = open(testMethodPath2,"r")
            fileTestCaseGenerated = open(testMethodPath3, "w")
            fileTestCaseGenerated.write("<unit>")
            fileTemp.write("\nTest case\n")
            lineCount =0
            for line in fileTestCaseGeneratedTemp:
                if lineCount == 0:
                    lineCount = 1
                    continue
                flag = 0
                #fileTemp.write(line)
                t = parseOneValue(line)
                for row in difference:
                    if row[0] == t[0]:
                        print("found "+row[0]+" "+ t[0])
                        replacedLine = line.replace(row[0],row[1])
                        print(replacedLine)

                        flag = 1
                        break
                if flag ==0:
                    fileTemp.write(line)
                    fileTestCaseGenerated.write(line)
                else:
                    fileTemp.write(replacedLine)
                    fileTestCaseGenerated.write(replacedLine)
            fileTestCaseGenerated.write("</unit>")
            fileTestCaseGeneratedTemp.close()
            if fileTestCaseGenerated:
                fileTestCaseGenerated.close()
            XMLToJava(testMethodPath3)
            fileTemp.write("Test case written"+"\n")

        except Exception as e:
            print(str(e))

        loopCounter += 1

    if existingSSM:
        existingSSM.close()
    if toGenSSM:
        toGenSSM.close()
    if fileTemp:
        fileTemp.close()
    if fileTestCaseGenerated:
        fileTestCaseGenerated.close()


def testCaseMatchForSSM(filePath,similarMethodsList):
    #fileTestCodeXML = open("d.xml", "r")
    for item in similarMethodsList:
        testCaseFound = 0
        index =0
        trackerTestCase = list()
        for j in item:
            methodName = parseFunctionName(filePath + r"\\" + j.__str__() + "_.xml")
            testMethod = xmlParser(filePath +"\\"+ "tuk.xml",methodName)
            if(testMethod):
                trackerTestCase.insert(index,testMethod)
                testCaseFound += 1
            else:
                print("method " + methodName + "---->" + " test method not found")
                trackerTestCase.insert(index, 0)
            index += 1
        count = len(item)
        print("test case found " + testCaseFound.__str__()+" out of "+ count.__str__())
        if(count != testCaseFound and testCaseFound == 1):
            TestCaseGeneratorSSM(filePath,item,trackerTestCase)


def compareXSD(filePath):
    #fileStatisticalData = open("statistics.txt","a")
    countSimilar = 0
    xsds = fileNames(filePath,'.xsd')
    similarMethodsList = list()
    for i in range(1,len(xsds)+1):
        temp = list()
        for j in range(i+1,len(xsds)+1):
            # These two lines are added to check if the line number of the xmls are same, if not, xsds are not compared
            lineCount1 =  generateXMLLinebyLine.lineCount(filePath + i.__str__() + "_.xml")
            lineCount2 = generateXMLLinebyLine.lineCount(filePath + j.__str__() + "_.xml")

            if filecmp.cmp(filePath+i.__str__()+".xsd", filePath+(j).__str__()+".xsd")== True and lineCount1 == lineCount2:
            #if filecmp.cmp(filePath + i.__str__() + ".xsd",filePath + (j).__str__() + ".xsd") == True:

                if any(i in subl for subl in similarMethodsList):
                    continue
                if i not in temp:
                    temp.append(i)
                    countSimilar += 1

                if any(j in subl for subl in similarMethodsList):
                    continue
                temp.append(j)
                countSimilar += 1

        if len(temp)!=0:
            similarMethodsList.append(temp)

    print(similarMethodsList)
    testCaseMatchForSSM(filePath,similarMethodsList)

    # statistical data code
    '''
    totalMethod = len(xsds)
    percentage = (countSimilar/totalMethod)*100
    fileStatisticalData.write(filePath+"    "+totalMethod.__str__() + "     "+countSimilar.__str__()+"      "+percentage.__str__() +"\n")
    '''

def checkIfTextCaseExist(param1,param2):

    global testFileNames
    for row in testFileNames:
        if (param2+'test').upper() == row[1].upper():
            if param1  in row[0]:
                return param2+'test'
        elif  ('Test'+param2).upper() == row[1].upper():
            if param1 in row[0]:
                return 'Test'+param2
        elif ('Tests' + param2).upper() == row[1].upper():
            if param1 in row[0]:
                return 'Tests' + param2
        elif (param2+'Tests').upper() == row[1].upper():
            if param1 in row[0]:
                return param2 + 'Tests'

    return "None"


def fileNameSplitter(fileNameList):
    fileNameSplitted = list()

    for name in fileNameList:
        temp = list()
        t = name.rpartition('\\')
        temp.append(t[0]+t[1])
        temp.append((t[2]))
        fileNameSplitted.append(temp)
    return fileNameSplitted

def allClassParser(sourceCodePath,testCodePath ):
    """
    :type parentRoot: object
    """

    global testFileNames
    fileNamesTestJava = fileNames(testCodePath, '.java')

    testFileNameRelative = list()
    for name in fileNamesTestJava:
        try:

            tuk = name.rpartition(testCodePath)
            outFolder = (tuk[2].rpartition(".java"))

            testFileNameRelative.append(outFolder[0])
            tuk = name.rpartition(sourceCodePath)


        except:
            continue

    testFileNames = fileNameSplitter(testFileNameRelative)


    # source code parse
    fileNamesSourceJava = fileNames(sourceCodePath,'.java')

    sourceFileNameRelative = list()
    for name in fileNamesSourceJava:
        try:
            nameParsed = name.rpartition(".java")
            parseName = nameParsed[0].rpartition("\\")
            tuk = name.rpartition(sourceCodePath)
            outFolder = (tuk[2].rpartition(".java"))

            tt = outFolder[0].rpartition("\\")
            bool = checkIfTextCaseExist(tt[0] + tt[1], tt[2])
            if bool != "None":
                testCodeLocation = testCodePath+tt[0]+tt[1]+bool+".java"
                if not os.path.exists(parentRoot + outFolder[0]):
                    os.makedirs(parentRoot + outFolder[0], 0o777)
                javaToXML("tuk"+".xml",testCodeLocation, parentRoot+outFolder[0]+r"\\")
                javaToXML(parseName[2] + ".xml", name, parentRoot + outFolder[0] + r"\\")
                methodParserXML(parseName[2]+".xml", parentRoot+outFolder[0]+r"\\")
        except:
            continue
    sourceFileNameRelativeParsed = fileNameSplitter(sourceFileNameRelative)


sourceCodePath = r"H:\Research\IndStudyDrRahimi\DataAnalysis\jfreechart-master\jfreechart-master\src\main\java\org\jfree\data\time"
testCodePath = r"H:\Research\IndStudyDrRahimi\DataAnalysis\jfreechart-1.5.2\jfreechart-1.5.2\src\test\java\org\jfree\data\time"


def do():

    allClassParser(sourceCodePath,testCodePath)
    '''
    f= open("H:\\Research\\IndStudyDrRahimi\\TE\XMLHolders\\Output\\generated_.xml","r")
    for line in f:
        print(parseOneValue(line))
    '''

do()
