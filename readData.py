import csv
import os
from SchoolDataTree import *

# data structure

# schoolData
#     states
#         cities
#             agency
#                 metrocentric
#                     school


class ReadCSV:

    def __init__(self, filename):
        self.data = None
        self.fileName = None
        self.options = {}
        # only set the filename if the filename exists
        if os.path.exists(filename):
            self.fileName = filename

    def configureOptions(self, options):
        opt = self.options
        opt['headers'] = options['headers']

    def read(self):
        if self.fileName == None:
            return False
        with open(self.fileName, 'r') as csvFile:
            reader = csv.DictReader(csvFile)
            self.prepData(reader)

    def updateSchoolCount(self, Node):
        count = 0
        for child in Node.children:
            count += Node.children[child].schoolCount
        Node.schoolCount = count

    def prepData(self, file):
        self.data = {}
        self.data['rootNode'] = Node('root')
        rootNode = self.data['rootNode']

        rootNode.schoolCount = 0
        rootNode.children = {}

        #headers = self.options['headers']
        for row in file:
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
            if state in rootNode.children:
                stateNode = rootNode.children[state]
            else:
                stateNode = State()
                rootNode.children[state] = stateNode

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

            self.updateSchoolCount(agencyNode)
            self.updateSchoolCount(cityNode)
            self.updateSchoolCount(stateNode)
            self.updateSchoolCount(rootNode)

        # returning the status code after completing the parsing
        if len(self.data) == 0 or self.data == None:
            return False
        else:
            return True
