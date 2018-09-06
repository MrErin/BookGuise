import xml.etree.ElementTree as ET

# documentation: https://docs.python.org/3.7/library/xml.etree.elementtree.html


# tree = ET.parse(
#     'C:/Users/Erin of the Lake/workspace/Repos/backEndCapstone/dataExperiments/home/sample.xml')
# check where you're running this from because the relative paths can get wonky
tree = ET.parse('Data/Python_Only/Tutorials/XMLTutorial/sample.xml')
root = tree.getroot()

# alternative setup:
# root = ET.fromstring(sample_as_string)

# root.findall("./country/neighbor")
# for country in root.findall('country'):
#   rank = country.find('rank').text
#   name = country.get('name')
#   print(name, rank)


def test():
    for child in root:
        print(child.tag, child.attrib)
        for popularshelves in child:
            for shelf in popularshelves:
                print(shelf.attrib["name"], shelf.attrib["count"])
        for neighbor in child.iter('neighbor'):
                print(neighbor.attrib)
    print(root.tag)
    print(root[0][1].text)


test()
