# this file declares all the necessary classes
# required for the creation of the tree (schoolData):


class Node:
    def __init__(self, type):
        self.type = type
        self.children = {}


class Zone (Node):
    def __init__(self, type):
        Node.__init__(self, type)
        self.schoolCount = None


class State (Zone):
    def __init__(self):
        Zone.__init__(self, 'State')


class Agency (Zone):
    def __init__(self):
        Zone.__init__(self, 'Agency')


class Metrocenter (Zone):
    def __init__(self):
        Zone.__init__(self, 'Metrocenter')


class City (Zone):
    def __init__(self):
        Zone.__init__(self, 'City')


class School (Node):
    def __init__(self, name):
        self.name = name
        self.longitude = None
        self.latitude = None
        Node.__init__(self, 'School')
