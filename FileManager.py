from PyQt5.QtWidgets import QApplication

from Document import Document


# TODO - this class should manage all of the open files and store them into a dict keyed by its path
class FileManager:
    def __init__(self, app):
        self.app = app
        self.open_documents = {}

    # def update_all(self):
    #     for key in self.open_documents:
    #         self.open_documents[key].update()
    def printAll(self):
        print('========================================')
        print('Open Documents:')
        for path in self.open_documents:
            print('----------------------------------------')
            print('path: ', path)
            print('text:\n', self.open_documents[path].toPlainText())
        print('========================================')

    # saves text to the file of the given path
    def saveDocument(self, path):
        if path in self.open_documents.keys():
            file = open(path, 'w')

            # get the text of the document with the given path
            data = self.open_documents[path].updateTextBox().toPlainText()

            # TODO - Delete this line once the multiple textbox display is implemented
            # data = self.app.layout.document.toPlainText()

            file.write(data)
            file.close()
            print('Saved File - ', path)
        else:
            if path == "":
                print("No File Path Given")
            else:
                print("Could Not Write To File - ", path)

    # TODO - save the file at the current path to the new path
    def saveAsDocument(self, curr_path, new_path):
        data = None
        curr_path = str(curr_path)

    # saves every file contained in the dictionary
    def saveAll(self):
        for path in self.open_documents:
            self.saveDocument(path)

    # this closes the document with the given path and does not save
    def closeDocument(self, path):
        if path in self.open_documents.keys():
            print("Closed File - ", path)
            self.open_documents.pop(path)
        else:
            if path == "":
                print("No File Path Given")
            else:
                print("Could Not Close File - ", path)

    # clears the dictionary of all open documents
    # !note! this does not save the documents
    def closeAll(self):
        for path in self.open_documents:
            self.closeDocument(path)

    # opens the file of the given path and add the Document to the dictionary
    def openDocument(self, path):
        # opens the file with the given path
        if path not in self.open_documents.keys():
            if path == "":
                print("No File Path Given")
                return ""
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

            file.close()
            print("Opened File - ", path)
        else:
            print("Document Already Open - ", path)
            data = self.open_documents[path].toPlainText()

        # TODO - add the newly created document as a tab in the workspace
        self.app.layout.document = self.open_documents[path]
        self.app.layout.document.updateTextBox(data)

        return data
