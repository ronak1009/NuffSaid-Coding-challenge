import csv
import os
solution1 = None

# schoolData
#     states
#         cities
#             agency
#                 metrocentric
#                     school


schoolData = None


class Node:
    def __init__(self, type):
        self.type = type
        self.children = {}


class State (Node):
    def __init__(self):
        Node.__init__(self, 'State')
        self.schoolCount = None


class Agency (Node):
    def __init__(self):
        Node.__init__(self, 'Agency')
        self.schoolCount = None


class Metrocenter (Node):
    def __init__(self):
        Node.__init__(self, 'Metrocenter')
        self.schoolCount = None


class School (Node):
    def __init__(self, name):
        self.name = name
        self.longitude = None
        self.latitude = None


class City (Node):
    def __init__(self):
        Node.__init__(self, 'City')
        self.schoolCount = None

# the node is passed for which the school count is to be updated


def updateSchoolCount(Node):
    count = 0
    for child in Node.children:
        count += Node.children[child].schoolCount
    Node.schoolCount = count


def readData(filename):
    if os.path.exists(filename):
        with open(filename, newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            prepData(reader)
    else:
        return None


def prepData(data):
    global schoolData

    schoolData = Node('root')
    schoolData.schoolCount = 0
    schoolData.children = {}

    headers = data.fieldnames
    for row in data:
        # state LSTATE05 , city LCITY05, metrocentric MLOCALE,
        # agency LEANM05, schoolName SCHNAM05,

        state = row['LSTATE05']
        city = row['LCITY05']
        agency = row['LEANM05']
        locale = row['MLOCALE']
        schoolName = row['SCHNAM05']

        # locale value is an int for which the data is available
        # for no value, it is a string represented as 'N'
        try:
            locale = int(locale)
        except ValueError:
            pass

        # arranging the data in the schoolData tree
        if state in schoolData.children:
            stateNode = schoolData.children[state]
        else:
            stateNode = State()
            schoolData.children[state] = stateNode

        if city in stateNode.children:
            cityNode = stateNode.children[city]
        else:
            cityNode = City()
            stateNode.children[city] = cityNode

        if agency in cityNode.children:
            agencyNode = cityNode.children[agency]
        else:
            agencyNode = Agency()
            cityNode.children[agency] = agencyNode

        if locale in agencyNode.children:
            metroNode = agencyNode.children[locale]
        else:
            metroNode = Metrocenter()
            agencyNode.children[locale] = metroNode

        # fill the school details
        if not schoolName in metroNode.children:
            schoolNode = School(schoolName)
            metroNode.children[schoolName] = schoolNode
            metroNode.schoolCount = len(metroNode.children)

        updateSchoolCount(agencyNode)
        updateSchoolCount(cityNode)
        updateSchoolCount(stateNode)
        updateSchoolCount(schoolData)


def getInstanceMap(NodeType, result):
    instanceMap = None
    if NodeType in result:
        instanceMap = result[NodeType]
    else:
        instanceMap = {}
        result[NodeType] = instanceMap
    return instanceMap


def UpdateResult(key, value, instanceMap):

    if key in instanceMap:
        instanceMap[key] += value
    else:
        instanceMap[key] = value


def query(node, result):
    for child in node.children:
        instance = node.children[child]
        instanceMap = getInstanceMap(instance.type, result)
        if (instance.type != 'Metrocenter'):
            UpdateResult(child, instance.schoolCount, instanceMap)
        elif(instance.type == 'Metrocenter' and isinstance(child, (int))):
            UpdateResult(child, instance.schoolCount, instanceMap)

        # call recurrsive to update the data from the children
        if instance.type in ['State', 'City', 'Agency']:
            query(instance, result)
    return


def writeDict(fileHandle, data):
    for index in data:
        line = str(index) + ": " + str(data[index]) + "\n"
        fileHandle.write(line)


def createOutputFolder(filename):
    if not os.path.exists('output'):
        os.mkdir('output')
    absfilepath = os.path.join('output', filename)

    return absfilepath


def print_counts():
    # prints the data for different queries
    result = {}
    query(schoolData, result)
    filename = createOutputFolder('query1.txt')
    with open(filename, 'w') as outputFile:
        text = "Total Schools: " + str(schoolData.schoolCount) + "\n"
        outputFile.write(text)

        text = "Schools by state: " + "\n"
        outputFile.write(text)
        writeDict(outputFile, result['State'])

        text = "School by Metrocenter: " + "\n"
        outputFile.write(text)
        writeDict(outputFile, result['Metrocenter'])


#   main function
if __name__ == "__main__":
    # global schoolData
    readData("school_data.csv")

    print_counts()
