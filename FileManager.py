from Document import Document


# TODO - this class should manage all of the open files and store them into a dict keyed by its path
class FileManager:
    def __init__(self, app):
        self.app = app
        self.open_documents = {}

    def update_all(self):
        for key in self.open_documents:
            self.open_documents[key].update()

    # TODO - save the file of the given path
    def saveDocument(self, path):
        file = None
        path = str(path)

    # TODO - save the file at the current path to the new path
    def saveAsDocument(self, curr_path, new_path):
        data = None
        curr_path = str(curr_path)

        # update the dict holding the open files
        self.open_documents.pop(curr_path)
        # self.open_documents[new_path] = data

    # TODO - save and close the file of the given path and pop it from the dict
    def closeDocument(self, path):
        file = None
        path = str(path)
        self.open_documents.pop(path)
        print(path)

    # opens the file of the given path and add the Document to the dictionary
    def openDocument(self, path):
        # opens the file with the given path
        if path not in self.open_documents.keys():
            file = open(path, 'r')
            if file.closed:
                print("Could Not Open File - ", path)
                return ""
            with file:
                data = file.read()

            # creates a new Document and sets the text to the text of the given file
            # adds the new Document to the dictionary of open documents.
            self.open_documents[path] = Document()
            self.open_documents[path].setText(data)
            print("Opened File - ", path)
        else:
            if path == "":
                print("No File Path Given")
                return ""
            else:
                print("Document Already Open - ", path)
                data = self.open_documents[path].toPlainText()

        # TODO - add the newly created document as a tab in the workspace
        self.app.layout.document.refreshTextBox(data)

        return data
