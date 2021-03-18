import generateXMLLinebyLine

fileName = r"H:\Research\IndStudyDrRahimi\TE\XMLHolders\ASTFieldDeclarationTest\\1.xml"

generateXMLLinebyLine.processXML(fileName)
print(generateXMLLinebyLine.lineCount("t3.xml"))