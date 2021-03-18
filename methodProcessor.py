import os
import filecmp
import generateXMLLinebyLine




parentRoot = r"H:\Research\IndStudyDrRahimi\TE\XMLHolders\\"
fileNamesSourceJava = list()
fileNamesTestJava = list()
fileNameSourceSplitted = list()
fileNameTestSplitted = list()
classCount = 0
testFileNames = list()





'''
Given filename, this method generates the XML from java file. So, for each class, we will call this method.
'''
def javaToXML(nameWithoutPath,fileNameFull,outPath):
    fileNameOut = os.path.splitext(fileNameFull)[0] + '.xml'

    cmd = "srcml " + fileNameFull + " -o " +outPath+nameWithoutPath
    so = os.popen(cmd).read()
    methodParserXML(nameWithoutPath,outPath)


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

    # This was the initial code. It was unable to parse 2-level hierachical function
    '''
    for line in file:

        if "<function>" in line:
            flag = 1
            fileNamePrefix = filePath+fileNameOut
            fileOut = open(fileNamePrefix+".xml", "w")

        if flag == 1:
            fileOut.write(line)

        if "</function>" in line:
            flag = 0
            fileNameInt = int(fileNameOut)
            fileNameInt = fileNameInt + 1
            fileNameOut = fileNameInt.__str__()

    '''

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

        generateXMLLinebyLine.processXML(items)


    # Removing the old xmls
    files2 = fileNames(filePath, ".xml")
    for items in files2:
        if "_" not in items:
            os.remove(items)

    # Removing the main xml for the whole class, otherwise I cannot just discard it programatically while generating xsds
    # Normally adding code does not work. So, I removed this
    files3 = fileNames(filePath, ".xml")
    for items in files3:
        if (items.rpartition("\\")[2].rpartition("_.xml")[0]).isdigit() == False:
            os.remove(items)


    files4 = fileNames(filePath, ".xml")
    for items in files4:
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


def compareXSD(filePath):
    fileStatisticalData = open("statistics.txt","a")
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

    # statistical data code
    '''
    totalMethod = len(xsds)
    percentage = (countSimilar/totalMethod)*100
    fileStatisticalData.write(filePath+"    "+totalMethod.__str__() + "     "+countSimilar.__str__()+"      "+percentage.__str__() +"\n")
    '''

def checkIfTextCaseExist(param1,param2):

    global  testFileNames
    for row in testFileNames:
        #print("tuk tuk " + param2 + " " + row[1])
        if (param2+'test').upper() == row[1].upper() or ('Test'+param2).upper() == row[1].upper():
            if param1  in row[0]:
                return True

    return False


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
    #print("test file name splitted")
    #print(testFileNames)


    # source code parse
    fileNamesSourceJava = fileNames(sourceCodePath,'.java')

    sourceFileNameRelative = list()
    for name in fileNamesSourceJava:
        try:
            nameParsed = name.rpartition(".java")
            parseName = nameParsed[0].rpartition("\\")
            tuk = name.rpartition(sourceCodePath)
            outFolder = (tuk[2].rpartition(".java"))
            directory = parentRoot+ parseName[2]

            # print testing
            #print("print")
            tt = outFolder[0].rpartition("\\")
            #print(tt[0] + tt[1])
            #print(tt[2])
            #print("print end")
            # print testing end
            bool = checkIfTextCaseExist(tt[0] + tt[1], tt[2])
            #print(tt[0] + tt[1] +" "+tt[2] + " "+ bool.__str__())
            if bool == True:
                if not os.path.exists(parentRoot + outFolder[0]):
                    os.makedirs(parentRoot + outFolder[0], 0o777)
                javaToXML(parseName[2]+".xml",name, parentRoot+outFolder[0]+r"\\")
        except:
            continue
    sourceFileNameRelativeParsed = fileNameSplitter(sourceFileNameRelative)


sourceCodePath = r"H:\Research\IndStudyDrRahimi\DataAnalysis\jfreechart-master\jfreechart-master\src\main\java\org\jfree\data\time"
testCodePath = r"H:\Research\IndStudyDrRahimi\DataAnalysis\jfreechart-1.5.2\jfreechart-1.5.2\src\test\java\org\jfree\data\time"


def do():

    allClassParser(sourceCodePath,testCodePath)

do()
