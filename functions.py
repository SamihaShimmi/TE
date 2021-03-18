import os
import config
import sqlite3
import shutil

# This function returns all the .java files from a directory
def fileNames(path):
    listOfFilesTemp = list()
    listofFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        listOfFilesTemp += [os.path.join(dirpath, file) for file in filenames]
    for item in listOfFilesTemp:
        extension = os.path.splitext(item)[1]
        if extension == '.java':
            listofFiles.append((item))
    return listofFiles


# This function parses the test methods from java files. It can parse jUnit test cases starting with @Test keyword
def parsing(fileName,outFileName):
    flag = 0
    flag2 = 0
    # this is the starting parenthesis for the class. It matches the closing parenthesis in the end.
    stack = list()
    #,encoding='UTF8'
    file = open(fileName, "r",encoding='UTF8')
    fileOut = open(outFileName, "a",encoding='UTF8')
    #shutil.copyfileobj(file, fileOut)
    for line in file:

        if "@Test" in line:
            flag = 1

            config.testCaseCount += 1
            fileOut.write("#############################################\n")
            fileOut.write(fileName + "\n")
            continue
        if flag == 1:

            if "{" in line:
                stack.append("{")
                fileOut.write(line)

            else:

                if "}" not in line:
                    fileOut.write(line)

                elif "}" in line:
                    if len(stack) == 1:

                        fileOut.write(line)
                        stack.pop()

                        flag = 0

                    elif len(stack) > 1:

                        fileOut.write(line)
                        stack.pop()


def writingTestCaseCount(fileName):
    fileOut = open(fileName, "a")
    fileOut.write("Total number of test cases " + str(config.testCaseCount))
    config.testCaseCount = 0

