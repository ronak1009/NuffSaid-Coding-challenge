import csv
import os
from SchoolDataTree import *
from readData import ReadCSV
solution1 = None


# global variables
schoolData = None


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


def findCity(queryContainer):
    result = {
        'name': "",
        'count': 0
    }
    name = ""
    count = 0

    for city in queryContainer:
        cityCount = queryContainer[city]
        if count < cityCount:
            name = city
            count = cityCount
    result['name'] = name
    result['count'] = count
    return result


def findUniqueCity(container):
    cityCount = 0
    for city in container:
        if container[city] > 0:
            cityCount += 1
    return cityCount


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

        maxCity = findCity(result['City'])
        text = "City with most schools: " + maxCity['name'] + \
            "( " + str(maxCity['count']) + " schools ) \n"
        outputFile.write(text)

        uniqueCities = findUniqueCity(result['City'])
        text = 'Unique cities with at least one school: ' + \
            str(uniqueCities) + "\n"
        outputFile.write(text)


def main():
    global schoolData
    fileReader = ReadCSV("school_data.csv")
    fileReader.read()
    schoolData = fileReader.data['rootNode']
    print_counts()


    #   main function
if __name__ == "__main__":
    main()
