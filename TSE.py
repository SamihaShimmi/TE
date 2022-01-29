import os
import filecmp
import generateXMLLinebyLine
from xml.etree import ElementTree

parentRoot = r"H:\Research\TestEvolution\TE\XMLHolders\\"
parentRootV1 = r"H:\Research\TestEvolution\TE\XMLHolders\\Version1"
fileNamesSourceJavaV2 = list()
fileNamesSourceJavaV1 = list()
fileNamesTestJava = list()
fileNameSourceSplitted = list()
fileNameTestSplitted = list()
classCount = 0
testFileNames = list()

loopC = 0


def XMLToJava(fileName):
    cmd = "srcml " + fileName + " -o " + parentRoot+"Output\\javaTmp.java"
    os.popen(cmd).read()


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

    cmd = "srcml " + fileNameFull + " -o " +outPath+nameWithoutPath
    os.popen(cmd).read()


'''
Given xml filename, this method generates XML for each method in that xml file.
'''

def methodParserXML(filename,filePath,version):
    if version == 2:
        print(filePath)
    count = 0
    fileNameInt = 0
    fileNameOut = "1"
    methodNameList = list()
    fileOut = open("dummy.txt", "w")

    filename = filePath+filename
    with open(filename, "rt") as fin:
        with open(filename.rpartition(".xml")[0] + "_.xml", "wt") as fout:
            for line in fin:
                fout.write(line.replace('http://www.srcML.org/srcML/src', ''))

    root = ElementTree.parse(filename.rpartition(".xml")[0] + "_.xml").getroot()
    for method in root.iter("function"):
        methodStringTemp = ElementTree.tostring(method, encoding='unicode', method='xml')
        methodString =  methodStringTemp[0:len(methodStringTemp)-1]
        fileNamePrefix = filePath + fileNameOut
        fileOut = open(fileNamePrefix + ".xml", "w")
        fileNameInt = int(fileNameOut)
        fileNameInt = fileNameInt + 1
        fileNameOut = fileNameInt.__str__()
        fileOut.write(methodString)

    if fileOut:
        fileOut.close()

    files = fileNames(filePath, ".xml")

    # Parsing the xml so that I can count lines
    for items in files:
        parsed = items.rpartition("\\")[2].rpartition(".xml")[0]
        if parsed.isdigit() == True:
            tmp = list()
            mName = parseFunctionName(items)
            mFileName = parsed+".xml"
            tmp.append(mFileName)
            tmp.append(mName)
            methodNameList.append(tmp)
            generateXMLLinebyLine.processXML(items)

    # Removing the old xmls
    files2 = fileNames(filePath, ".xml")
    for items in files2:
        if ("_" not in items and (items.rpartition("\\")[2].rpartition(".xml")[0]).isdigit() == True):
            os.remove(items)

    files4 = fileNames(filePath, ".xml")
    for items in files4:
        if (items.rpartition("\\")[2].rpartition("_.xml")[0]).isdigit() == True:
            XMLtoXSD(filePath + items.rpartition("\\")[2].rpartition(".xml")[0] + ".xml",
                     filePath + items.rpartition("\\")[2].rpartition("_.xml")[0] + ".xsd")

    if version == 2:
        compareXSD(filePath,methodNameList)


'''
This method generates xsd from each function
'''
def XMLtoXSD(fileName,fileNameOut):

    commandString = r"java -jar trang.jar " + fileName + " " + fileNameOut
    os.popen(commandString).read()


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


def TestCaseGeneratorSSM(filePath,SSM,trackerTestCase,version1Path,version):
    #print("SSM ")
    #print(SSM)
    #print("trackerTestCase")
    #for t in range(0,len(trackerTestCase)):
        #if trackerTestCase[t]!= 0:
            #print("test case for trackertestcase")
        #else:
            #print(trackerTestCase[t])

    fileTemp = open(parentRoot+r"\\Output\\tmp.txt","a")

    difference = list()
    loop = 0
    if version == 2:

        # detecting existing SSM
        for i in trackerTestCase:
            if i != 0:
                break
            loop += 1

        existingSSM = open(filePath+"\\"+SSM[loop].__str__()+"_.xml")
        toGenSSM = open("dummy.txt","r")
        loopCounter =0
        for i in range(0,len(SSM)):

            # added
            fileTemp = open(parentRoot + r"\\Output\\tmp.txt", "a")
            toGenSSM = open("dummy.txt", "r")
            # added end

            #print("checkpoint 1")
            #print("loop")
            #print(loop)
            #print("loopcounter")
            #print(loopCounter)
            fileTemp.write(filePath + "\n")
            fileTemp.write("\n")
            #print("checkpoint 1.2")
            if loopCounter == loop:
                loopCounter += 1
                continue
            #print("checkpoint 1.5")
            #print("loop")
            #print(loop)
            #print("loopcounter")
            #print(loopCounter)

            # it will be required to generate cases for existing
            if trackerTestCase[loopCounter] != 0:
                print("checkpoint 2")
                loopCounter += 1
                continue
            #print("checkpoint 3")
            try:
                toGenSSM = open(filePath+"\\"+SSM[loopCounter].__str__()+"_.xml")
            except Exception as e:
                print(e)

            existingSSM = open(filePath + "\\" + SSM[loop].__str__() + "_.xml")
            print("existing ssm name " + existingSSM.name)
            print("to gen ssm name "+ toGenSSM.name)
            methodName = parseFunctionName(filePath+"\\"+SSM[loopCounter].__str__()+"_.xml")
            print("methodName " + methodName)
            print("method name 2 = ", parseFunctionName(filePath+"\\"+SSM[loop].__str__()+"_.xml"))
            fileTemp.write(SSM[loop].__str__()+" "+ SSM[loopCounter].__str__())
            for lineF1 in toGenSSM:
                for lineF2 in existingSSM:
                    if lineF1 != lineF2:

                        temp = parseValue(lineF2, lineF1)
                        if temp not in difference:
                            difference.append(temp)
                    break
            #fileTemp.write(trackerTestCase[loop].__str__() + "\n")
            fileTemp.write(difference.__str__()+"\n")
            fileTemp.write("\n")
            print(difference)
            #print("checkpoint 4")
            # generating the test cases

            testMethodPath = parentRoot +"\\Output\\" +"Test.xml"

            try:
                fileTestCodeXML = open(testMethodPath, "w")
                fileTestCodeXML.write(trackerTestCase[loop].__str__())

                if fileTestCodeXML:
                    fileTestCodeXML.close()

                tempOutputPath = "H:\Research\TestEvolution\TE\XMLHolders\Output\\Output.xml"
                fileTemp.write("Test case" + "\n")

                with open(testMethodPath, "rt") as fin:
                    with open(tempOutputPath, "wt") as fout:
                        fout.write("<unit>")
                        for line in fin:
                            replacedLineTmp = line
                            replacedLine = line
                            for row in difference:
                                if row[0] in replacedLineTmp:
                                    replacedLine = replacedLineTmp.replace(row[0], row[1])
                                    replacedLineTmp = replacedLine

                            fout.write(replacedLine)
                            #fileTemp.write(replacedLine)
                        fout.write("</unit>")

                fileTemp.write("Test case written" + "\n")
                methodNameTest = parseFunctionName(testMethodPath)

                # generating java method from XML file
                XMLToJava(tempOutputPath)
                with open(parentRoot+ "Output\\javaTmp.java","rt") as fWrite:
                    with open(parentRoot+ "Output\\java.java","wt") as fWrite2:
                        for eachLine in fWrite:
                            lineTemp = eachLine
                            if methodNameTest in eachLine:
                                lineTemp = eachLine.replace(methodNameTest,methodName+"Test")
                            fileTemp.write(lineTemp)
                            fWrite2.write(lineTemp)
                fWrite.close()
            except Exception as e:
                print(str(e))

            loopCounter += 1
            difference.clear()
            existingSSM.close()
            if existingSSM:
                existingSSM.close()
            if toGenSSM:
                toGenSSM.close()
            if fileTemp:
                fileTemp.close()
            #print("loop")
            #print(loop)
            #print("loopcounter")
            #print(loopCounter)
            #print("checkpoint 5")
    else:


        for i in trackerTestCase:
            if i != 0:
                break
            loop += 1

        print(filePath + "\\" + SSM[loop].rpartition("v2")[0].__str__() + "_.xml")
        print("without rpartition")
        print(filePath + "\\" + SSM[loop].__str__() + "_.xml")

        existingSSM = open(filePath + "\\" + SSM[loop].__str__() + "_.xml")
        print("still there")
        toGenSSM = open("dummy.txt", "r")
        loopCounter = 0
        for i in range(0, len(SSM)):
            # added
            fileTemp = open(parentRoot + r"\\Output\\tmp.txt", "a")
            toGenSSM = open("dummy.txt", "r")
            # added end

            fileTemp.write(filePath + "\n")
            fileTemp.write("\n")
            if loopCounter == loop:
                loopCounter += 1
                continue

            if trackerTestCase[loopCounter] != 0:
                loopCounter += 1
                continue
            #print("pre tuk tuk tuk")
            print(version1Path + "\\" + SSM[loopCounter].rpartition("v2")[0].__str__() + "_.xml")
            try:
                toGenSSM = open(filePath + "\\" + SSM[loopCounter].rpartition("v2")[0].__str__() + "_.xml")
            except Exception as e:
                print(e)
            #print("tuk tuk tuk")
            existingSSM = open(version1Path + "\\" + SSM[loop].__str__() + "_.xml")
            print("existing ssm name " + existingSSM.name)
            print("to gen ssm name " + toGenSSM.name)

            methodName = parseFunctionName(filePath + "\\" + SSM[loopCounter].rpartition("v2")[0].__str__() + "_.xml")
            print("methodName " + methodName)
            print("method name 2 = ", parseFunctionName(version1Path + "\\" + SSM[loop].__str__() + "_.xml"))

            fileTemp.write(SSM[loop].__str__() + " " + SSM[loopCounter].rpartition("v2")[0].__str__())
            #print("tttttt")

            for lineF1 in toGenSSM:
                for lineF2 in existingSSM:
                    if lineF1 != lineF2:

                        temp = parseValue(lineF2, lineF1)
                        if temp not in difference:
                            difference.append(temp)
                    break
            #fileTemp.write(trackerTestCase[loop].__str__() + "\n")
            fileTemp.write(difference.__str__() + "\n")
            fileTemp.write("\n")
            #fileTemp.write("tttttt")
            print(difference)
            #print("qqqqq")

            # generating the test cases

            testMethodPath = parentRoot + "\\Output\\" + "Test.xml"

            try:
                fileTestCodeXML = open(testMethodPath, "w")
                fileTestCodeXML.write(trackerTestCase[loop].__str__())

                if fileTestCodeXML:
                    fileTestCodeXML.close()

                tempOutputPath = "H:\Research\IndStudyDrRahimi\TE\XMLHolders\Output\\Output.xml"
                fileTemp.write("Test case" + "\n")
                with open(testMethodPath, "rt") as fin:
                    with open(tempOutputPath, "wt") as fout:
                        print("yes")
                        print("<unit>")
                        fout.write("<unit>")
                        for line in fin:
                            replacedLineTmp = line
                            replacedLine = line
                            for row in difference:
                                if row[0] in replacedLineTmp:
                                    replacedLine = replacedLineTmp.replace(row[0], row[1])
                                    replacedLineTmp = replacedLine
                            print("replacedLine")
                            print(replacedLine)
                            fout.write(replacedLine)
                            #fileTemp.write(replacedLine)
                        print("/unit")
                        fout.write("</unit>")
                fileTemp.write("Test case written " + "\n")
                print("Test case written ")
                #methodNameTest = parseFunctionName(testMethodPath)
                methodNameTest ="shimtuk"

                # generating java method from XML file
                XMLToJava(tempOutputPath)
                with open(parentRoot + "Output\\javaTmp.java", "rt") as fWrite:
                    with open(parentRoot + "Output\\java.java", "wt") as fWrite2:
                        for eachLine in fWrite:
                            lineTemp = eachLine
                            if methodNameTest in eachLine:
                                lineTemp = eachLine.replace(methodNameTest, methodName + "Test")
                            fileTemp.write(lineTemp)
                            fWrite2.write(lineTemp)
                fWrite.close()

            except Exception as e:
                print(str(e))

            loopCounter += 1

            difference.clear()
            existingSSM.close()
            if existingSSM:
                existingSSM.close()
            if toGenSSM:
                toGenSSM.close()
            if fileTemp:
                fileTemp.close()






def testCaseMatchForSSM(filePath,similarMethodsList,version1Path, version):

    if version == 1:
        print("testCaseMatchForSSM "+ filePath)
        print("what i get inside in matchingssm")
        print(similarMethodsList)
        for item in similarMethodsList:
            #print("item ")
            #print(item)

            testCaseFound = 0
            index =0
            trackerTestCase = list()

            for j in item:
                print("j")
                print(type(j))

                if "v2" in j:
                    trackerTestCase.insert(index, 0)
                    print("once")
                    index += 1
                    continue

                k = int(j)
                methodName = parseFunctionName(version1Path + r"\\" + j.__str__() + "_.xml")
                testMethod = xmlParser(filePath +"\\"+ "tuk.xml",methodName)
                print("pre test test test")
                if(testMethod):
                    print("v1 method found")
                    trackerTestCase.insert(index,testMethod)
                    testCaseFound += 1
                else:
                    print("v1 method not found")
                    print("method " + methodName + "---->" + " test method not found")
                    trackerTestCase.insert(index, 0)
                print("test test test")
                index += 1

            count = len(item)
            #print("test case found " + testCaseFound.__str__()+" out of "+ count.__str__())
            if (count != testCaseFound and testCaseFound >= 1):
                print("file path, item, trackertestcase")
                print(filePath)
                print(item)
                print(trackerTestCase)
                TestCaseGeneratorSSM(filePath, item, trackerTestCase,version1Path,1)

    if version == 2:
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
            if(count != testCaseFound and testCaseFound >= 1):
                TestCaseGeneratorSSM(filePath,item,trackerTestCase,version1Path,2)


def compareXSD(filePath,methodNameList):

    matchingSSMV1 = list()
    # check if v2 and v1 of source code is different
    version1Path =parentRootV1+ (filePath.rpartition(parentRoot)[2])

    mismatch = list()
    print("______________________________________________________")
    fileNameComp = version1Path.rpartition("\\")[0].rpartition("\\")[0].rpartition("\\")[2]
    #print(filecmp.cmp(filePath+fileNameComp, version1Path+fileNameComp))

    #print(filePath+fileNameComp+".xml")
    #print(version1Path+fileNameComp+".xml")

    File1 = open(filePath+fileNameComp+".xml","r")
    File2 = open(version1Path+fileNameComp+".xml","r")
    lineCount = 1
    match = "True"
    for lineF1 in File1:
        for lineF2 in File2:
            if lineF1 != lineF2:
                match = "False"
            if lineCount == 2 or "* (C) Copyright" in lineF1:
                match = "True"
            lineCount += 1
            break
    print(match)

    if match == "False":
        # getting total file counts in version 1
        v1xsds = fileNames(version1Path, '.xsd')
        methodNameListV1 = list()
        for items in v1xsds:
            parsed = items.rpartition("\\")[2].rpartition(".xsd")[0]
            tmp = list()
            mName = parseFunctionName(version1Path + parsed + "_.xml")
            mFileName = parsed + ".xml"
            tmp.append(mFileName)
            tmp.append(mName)
            methodNameListV1.append(tmp)

        print("method v2")
        print(methodNameList)
        print("method v1")
        print(methodNameListV1)

        for items in methodNameListV1:
            if not any(items[1] in sublist for sublist in methodNameList):
                tmp = list()
                tmp.append(version1Path+ items[0].rpartition(".xml")[0]+".xsd")
                tmp.append(items[1])
                mismatch.append(tmp)

    if File1:
        File1.close()
    if File2:
        File2.close()
    #fileStatisticalData = open("statistics.txt","a")
    countSimilar = 0
    xsds = fileNames(filePath,'.xsd')
    similarMethodsList = list()
    count = 0
    for i in range(1,len(xsds)+1):
        temp = list()
        for j in range(i+1,len(xsds)+1):
            # These two lines are added to check if the line number of the xmls are same, if not, xsds are not compared
            lineCount1 =  generateXMLLinebyLine.lineCount(filePath + i.__str__() + "_.xml")
            lineCount2 = generateXMLLinebyLine.lineCount(filePath + j.__str__() + "_.xml")

            if filecmp.cmp(filePath+i.__str__()+".xsd", filePath+(j).__str__()+".xsd")== True and lineCount1 == lineCount2:
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
        count = i
    noMatch = list()
    for t in range(1,count+1):
        if not any(t in sublist for sublist in similarMethodsList):
            noMatch.append(t)
    print(noMatch)
    print(similarMethodsList)
    print(mismatch)

    print("************")
    if len(mismatch) !=  0:
        for items in noMatch:
            print("nomatch "+items.__str__()+".xsd" +" "+ parseFunctionName(filePath+items.__str__()+"_.xml"))
        for items in mismatch:
            print("mismatch "+items[0].rpartition("\\")[2]+" " + items[1])


    print("************")
    count2 = 0
    countSimilar2 = 0
    for i in noMatch:

        temp = list()
        for j in mismatch:
            print("i ")
            print(i)
            print("j")
            k= j[0].rpartition("\\")[2].rpartition(".xsd")[0]
            print(k)
            # These two lines are added to check if the line number of the xmls are same, if not, xsds are not compared

            lineCount1 =  generateXMLLinebyLine.lineCount(filePath + i.__str__() + "_.xml")
            lineCount2 = generateXMLLinebyLine.lineCount(version1Path + k.__str__() + "_.xml")
            print("linecount")
            print(lineCount1)
            print(lineCount2)
            print("param 1 and 2")
            print(filePath+i.__str__()+".xsd")
            print(version1Path+k.__str__()+".xsd")
            print("compare result")
            print(filecmp.cmp(filePath + i.__str__() + ".xsd", version1Path + k.__str__() + ".xsd"))
            if filecmp.cmp(filePath+i.__str__()+".xsd", version1Path+k.__str__()+".xsd")== True and lineCount1 == lineCount2:
                print("found equal")
                if any(k in subl for subl in matchingSSMV1):
                    continue
                if i.__str__()+"v2" not in temp:
                    temp.append(i.__str__()+"v2")

                temp.append(k)

        if len(temp)!=0:
            matchingSSMV1.append(temp)
        count2 = i

    if len(matchingSSMV1)!=0:
        print(" matchingSSMV1")
        print(matchingSSMV1)
    testCaseMatchForSSM(filePath,similarMethodsList,version1Path,2)
    if len(matchingSSMV1) != 0:
        testCaseMatchForSSM(filePath, matchingSSMV1,version1Path,1)

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

def allClassParser(sourceCodePathV2,testCodePath,sourceCodePathV1):
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
            tuk = name.rpartition(sourceCodePathV2)


        except:
            continue

    testFileNames = fileNameSplitter(testFileNameRelative)

    # source code parse V1

    fileNamesSourceJavaV1 = fileNames(sourceCodePathV1, '.java')

    for name in fileNamesSourceJavaV1:
        try:
            nameParsed = name.rpartition(".java")
            parseName = nameParsed[0].rpartition("\\")
            tuk = name.rpartition(sourceCodePathV1)
            outFolder = (tuk[2].rpartition(".java"))

            tt = outFolder[0].rpartition("\\")
            bool = checkIfTextCaseExist(tt[0] + tt[1], tt[2])

            if bool != "None":
                if not os.path.exists(parentRootV1 + outFolder[0]):
                    os.makedirs(parentRootV1 + outFolder[0], 0o777)
                javaToXML(parseName[2] + ".xml", name, parentRootV1 + outFolder[0] + r"\\")
                methodParserXML(parseName[2] + ".xml", parentRootV1 + outFolder[0] + r"\\", 1)

        except:
            continue

    # source code parse V2
    fileNamesSourceJavaV2 = fileNames(sourceCodePathV2,'.java')

    for name in fileNamesSourceJavaV2:
        try:
            nameParsed = name.rpartition(".java")
            parseName = nameParsed[0].rpartition("\\")
            tuk = name.rpartition(sourceCodePathV2)
            outFolder = (tuk[2].rpartition(".java"))

            tt = outFolder[0].rpartition("\\")
            bool = checkIfTextCaseExist(tt[0] + tt[1], tt[2])
            if bool != "None":
                testCodeLocation = testCodePath+tt[0]+tt[1]+bool+".java"
                if not os.path.exists(parentRoot + outFolder[0]):
                    os.makedirs(parentRoot + outFolder[0], 0o777)
                javaToXML("tuk"+".xml",testCodeLocation, parentRoot+outFolder[0]+r"\\")
                javaToXML(parseName[2] + ".xml", name, parentRoot + outFolder[0] + r"\\")
                methodParserXML(parseName[2]+".xml", parentRoot+outFolder[0]+r"\\",2)
        except:
            continue

sourceCodePathV1 = r"H:\Research\TestEvolution\DataAnalysis\jfreechart-1.5.2\jfreechart-1.5.2\src\main\java\org\jfree\data\category"
sourceCodePathV2 = r"H:\Research\TestEvolution\DataAnalysis\jfreechart-1.5.2\jfreechart-1.5.2\src\main\java\org\jfree\data\category"
testCodePath = r"H:\Research\TestEvolution\DataAnalysis\jfreechart-1.5.2\jfreechart-1.5.2\src\test\java\org\jfree\data\category"

def do():

    allClassParser(sourceCodePathV2,testCodePath,sourceCodePathV1)

do()
