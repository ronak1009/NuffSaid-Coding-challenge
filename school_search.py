from readData import ReadCSV
from functools import reduce
import datetime

# global variables

# global util methods


def formatQueryList(queryString):
    queryString = queryString.lower()
    queryList = queryString.split(" ")
    if queryList[-1] == 'school':
        queryList.pop()
    return queryList


def isBad(str):
    badwords = ("-", "(", ")")
    return (str in badwords)


# search engine class
class SearchEngine:
    def __init__(self, database):
        self.searchIndex = {}
        self.database = database
        self.index = False
        self.list = []
        self.matchCount = 3

    def __findTopMatches__(self, matches):
        lenMap = {}
        for idx in matches:
            word = self.list[idx]
            key = len(word)
            if key in lenMap:
                lenMap[key].append(word)
            else:
                lenMap[key] = [word, ]

        sortList = sorted(lenMap)
        topResults = []
        # filtering the top results
        itr = iter(sortList)
        while(len(topResults) < self.matchCount):
            topResults.extend(lenMap[next(itr)])
        return topResults

    def search(self, queryString):
        # todo implement
        if not self.index:
            errorMsg = "Index the search engine before starting any query"
            raise Exception(errorMsg)
        else:
            # implement the search logic after indexing is done
            matches = []
            queryList = formatQueryList(queryString)
            for query in queryList:
                try:
                    match = set(self.searchIndex[query])
                    if len(matches) > 0:
                        # FIND THE COMMON MATCH
                        matches = matches & match
                    else:
                        matches = set(match)
                except KeyError as err:
                    err.message = "key not found in index"
                    pass
            topMatches = list(self.__findTopMatches__(matches))
            return (topMatches[0:self.matchCount])

    def __prepSchoolList__(self, node):
        if (node.type == 'School') and (not isBad(node.name)):
            self.list.append(node.name)
        elif len(node.children) != 0:
            for key in node.children:
                self.__prepSchoolList__(node.children[key])
        return True

    def __prepSearchIndex__(self):
        for index, sName in enumerate(self.list):
            # splitname = ['abc', 'cfd', 'rred']
            # splitnames = sName.split(" ")
            # splitnames = [n.lower() for n in splitnames]
            # splitnames = splitnames.remove('school')
            splitnames = formatQueryList(sName)
            for ssname in splitnames:
                # ssname=abc
                if ssname in self.searchIndex:
                    # searchIndex = {'abc' : []}
                    vals = self.searchIndex[ssname]
                    vals.append(index)
                else:
                    vals = [index, ]
                    self.searchIndex[ssname] = vals

    def indexing(self):

        # travel to all the leaf school nodes and store their names
        # index data structure
        # schoolList = ['school1', 'school2', ...]
        # index
        #   word1 = [indexInSchoolList]
        self.__prepSchoolList__(self.database)
        # prepare the search index
        self.__prepSearchIndex__()
        # completed indexing
        self.index = True


def main():
    fileReader = ReadCSV("school_data.csv")
    fileReader.read()
    data = fileReader.data['rootNode']
    google = SearchEngine(database=data)
    google.indexing()
    start = datetime.datetime.now()
    matches = google.search("DETENTION CENTER")
    end = datetime.datetime.now()
    print(matches)
    print("Search took total time ", end-start)
    # queryString = ""
    # results = google.search(queryString)

    # print(results)


if __name__ == "__main__":
    main()
