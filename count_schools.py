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

class State (Node):
    def __init__(self):
        Node.__init__(self, 'State')
        self.cities = {}
        self.schoolCount = None

class Agency (Node):
    def __init__(self):
        Node.__init__(self, 'Agency')
        self.metrocenters = {}
        self.schoolCount = None

class Metrocenter (Node):
    def __init__(self):
        Node.__init__(self, 'Metrocenter')
        self.schools = {}
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
        self.agencies = {}
    

def readData(filename):
    if os.path.exists(filename):
        with open(filename, newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            prepData(reader)
    else:
        return None

def prepData(data):
    global schoolData 
    
    schoolData =  Node('root')
    schoolData.states = {}
    
    headers = data.fieldnames
    for row in data:
        #state LSTATE05 , city LCITY05, metrocentric MLOCALE, 
        #agency LEANM05, schoolName SCHNAM05, 

        state = row['LSTATE05']
        city = row['LCITY05']
        agency = row['LEANM05']
        locale = row['MLOCALE']
        schoolName = row['SCHNAM05']
    
        ##arranging the data in the schoolData tree
        if state in schoolData.states:
            stateNode = schoolData.states[state]
        else:
            stateNode = State()
            schoolData.states[state] = stateNode
        
        if city in stateNode.cities:
            cityNode = stateNode.cities[city]
        else:
            cityNode = City()
            stateNode.cities[city] = cityNode
        
        if agency in cityNode.agencies:
            agencyNode = cityNode.agencies[agency]
        else:
            agencyNode = Agency()
            cityNode.agencies[agency] = agencyNode
        
        if locale in agencyNode.metrocenters:
            metroNode = agencyNode.metrocenters[locale]
        else:
            metroNode = Metrocenter()
            agencyNode.metrocenters[locale] = metroNode
        
        #fill the school details
        if not schoolName in metroNode.schools:
            schoolNode = School(schoolName)
            metroNode.schools[schoolName] = schoolNode

        

if __name__ == "__main__":
    #global schoolData
    readData("school_data.csv")
        
    