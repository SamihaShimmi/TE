'''
################################################
Developed by Samiha
Start date 01/21/2021
This is a simple parser to extract Junit test cases from JfreeChart application
################################################
'''

import sys
import os
import functions
import config

if os.path.exists("version1.txt"):
    os.remove(r"version1.txt")

if os.path.exists("version2.txt"):
    os.remove(r"version2.txt")

if os.path.exists("version3.txt"):
    os.remove(r"version3.txt")

fileNameListV1 = functions.fileNames(r"H:\Research\IndStudyDrRahimi\DataAnalysis\accumulo-rel-2.0.1\core\src\test")
fileNameListV2 = functions.fileNames(r"H:\Research\IndStudyDrRahimi\DataAnalysis\accumulo-main\core\src\test")

for item in fileNameListV1:
    functions.parsing(item, "version1.txt")

functions.writingTestCaseCount("version1.txt")


for item in fileNameListV2:
    functions.parsing(item, "version2.txt")

functions.writingTestCaseCount("version2.txt")

'''
for item in fileNameListV3:
    functions.parsing(item, "version3.txt")

functions.writingTestCaseCount("version3.txt")
'''

