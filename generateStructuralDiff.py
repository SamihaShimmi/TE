
import xml.etree.ElementTree as ET
ET.register_namespace("","http://www.srcML.org/srcML/src")

Matrix = list()
loopC = 0
def parseValue(toParse1,toParse2):
    listTemp = list()
    str=toParse1.split(">",1)[1]
    global loopC
    result=str.rpartition("<")
    #print(result[0])
    #Matrix[1][0] = result[0]
    listTemp.append(result[0])
    str = toParse2.split(">", 1)[1]

    result = str.rpartition("<")
    #Matrix[1][1] = result[0]
    listTemp.append(result[0])
    loopC += 1
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
file1 = open("previous.xml")
file2 = open("next.xml")
t = str()
t2 = str()

for line in file1:
    t +=line
for line in file2:
    t2 +=line

root = ET.fromstring(t)

tree = ET.ElementTree(root)

indent(root)
# writing xml
tree.write("example.xml", encoding="utf-8", xml_declaration=True)

root = ET.fromstring(t2)

tree = ET.ElementTree(root)

indent(root)
# writing xml
tree.write("example2.xml", encoding="utf-8", xml_declaration=True)

file1 = open("example.xml")
file2 = open("example2.xml")
tuk=str()

for lineF1 in file1:
    for lineF2 in file2:
        if lineF1!=lineF2:
            #tuk = "" + lineF2+" "+lineF1
            print(lineF2+" "+lineF1)
            parseValue(lineF2, lineF1)
            #print(tuk)
        break
fileT = open("YearTest.java", "r")
fileTC = open("YearTestV2.java", "w")

for line in fileT:
    st = line
    for row in Matrix:

        if row[0] in line and row[0] != "":
            print("found "+ row[0])
            st = st.replace(row[0], row[1])
    fileTC.write(st)

    #print(line)

#parseValue("<name>MINIMUM_YEAR</name>","<name>MAXIMUM_YEAR</name>")
#print(Matrix)
print(Matrix)
print(loopC)