from xml.etree import ElementTree

root = ElementTree.parse("fruits.xml").getroot()
def parseFunctionName():


    name = root.find("name")
    ElementTree.dump(name)

#parseFunctionName()

def testCodeParser():
    for name in root.iter("type"):
        print("shim start")
        print(ElementTree.tostring(name, encoding='unicode', method='xml'))
        print("shim end")
        for item in name.findall("name"):
            print(ElementTree.tostring(item, encoding='unicode', method='xml'))

testCodeParser()