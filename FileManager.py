# TODO - this class should manage all of the open files and store them into a dict keyed by its path
class FileManager:
    def __init__(self):
        self.open_documents = {}

    # TODO - save the file of the given path
    def saveDocument(self, path):
        file = None
        path = str(path)

    # TODO - save the file at the current path to the new path
    def saveAsDocument(self, curr_path, new_path):
        file = None
        curr_path = str(curr_path)

        # update the dict holding the open files
        self.open_documents.pop(curr_path)
        self.open_documents[new_path] = file

    # TODO - save and close the file of the given path and pop it from the dict
    def closeDocument(self, path):
        file = None
        path = str(path)
        self.open_documents.pop(path)
        print(path)

    # TODO - open the file of the given path and add it to the dict
    def openDocument(self, path):
        file = None
        path = str(path)
        self.open_documents[path] = file
        print(path)
