from readData import ReadCSV


# global variables


class SearchEngine:
    def __init__(self, database):
        self.searchIndex = {}
        self.database = database
        self.index = False
        self.list = []

    def search(self, queryString):
        # todo implement
        if not self.index:
            errorMsg = "Index the search engine before starting any query"
            raise Exception(errorMsg)
        else:
            # implement the search logic after indexing is done
            return []

    def __prepSchoolList__(self, node):
        if node.type == 'School':
            self.list.append(node.name)
        elif len(node.children) != 0:
            for key in node.children:
                self.__prepSchoolList__(node.children[key])
        return True

    def __prepSearchIndex__(self):
        for sName, index in self.list:
            splitnames = sName.split(" ")
            # splitname = ['abc', 'cfd', 'rred']
            splitnames = [n.lower() for n in splitnames]
            splitnames = splitnames.remove('school')
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

    print(google.searchIndex)
    # queryString = ""
    # results = google.search(queryString)

    # print(results)


if __name__ == "__main__":
    main()
