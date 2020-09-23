# this class manages all of the open documents and stores their paths into a list
from PyQt5.QtWidgets import QInputDialog, QLineEdit


class FileManager():
    def __init__(self, app):
        print("FileManager - init")

        self.app = app  # app - QMainWindow instance
        self.open_documents = []  # open_documents - holds the paths of all of the open documents
        self.current_document = None  # current_document - the current document that is displayed to the user

    # saves text to the file of the given path
    def saveDocument(self):
        print("FileManager - saveDocument")

        # get the current text from the document shown to the user
        data = self.app.layout.document.toPlainText()

        # if a file has already been opened write to the file
        if self.current_document is not None:
            self.writeFileData(self.open_documents[self.current_document], data)
            print('Saved File - ', self.open_documents[self.current_document])

        # if a file has not been opened yet prompt the user for a file name then write to that file
        else:
            # get the entered data
            file_name = QInputDialog.getText(self.app, "Get text", "File Name:", QLineEdit.Normal, "")

            if file_name[0] == '':
                print("No File Path Given")
                return

            path = self.app.app_props.mainPath + "/" + file_name[0]

            # write the text in the document shown to the user to the given file path
            self.writeFileData(path, data)

            # append the newly created file to the list of open docs and set it to the curr document
            self.open_documents.append(path)
            self.current_document = len(self.open_documents) - 1

            print('Saved File - ', path)

    # TODO - save the file at the current path to the new path
    def saveAsDocument(self, new_path):
        print("FileManager - saveAsDocument - ", new_path)
        data = self.app.layout.document.toPlainText()

    # this closes the document with the given path
    # !note! this does not save the document
    def closeDocument(self, path):
        print("FileManager - closeDocument - ", path)

        # if the path exists in the open docs list remove it
        if path in self.open_documents:
            self.open_documents.remove(path)
            print("Closed File - ", path)

        # if it does not exist print error messages
        else:
            if path == "":
                print("No File Path Given")
            else:
                print("File Is Not Open - ", path)

    # clears the list of all open documents
    # !note! this does not save the documents
    def closeAll(self):
        print("FileManager - closeAll")
        self.open_documents.clear()

    # opens the file of the given path and add the Document to the dictionary
    def openDocument(self, path):
        print("FileManager - openDocument - ", path)
        # if there is already a file open save before the Document's text is overwritten
        if self.current_document is not None:
            self.saveDocument()

        # if the document is not already open
        if path not in self.open_documents:

            # if the user clicks out of the open file prompt do nothing
            if path == "":
                print("No File Path Given")
                return ""

            # retrieve the text from the file you are attempting to open
            data = self.getFileData(path)

            # appends the path to the list of open documents and sets it to the current document
            self.open_documents.append(path)
            self.current_document = len(self.open_documents) - 1

        # if the document has already been opened in this session
        else:
            # get the data from the file and set the current document
            data = self.getFileData(path)
            self.current_document = self.open_documents.index(path)
            print("Document Already Open - ", path)

        # update the document shown to the user
        self.app.layout.document.updateTextBox(data)

        return data

    # For debugging prints out all of the documents stored in open_documents dictionary
    def printAll(self):
        print('========================================')
        print('Open Documents:')
        for path in self.open_documents:
            print('----------------------------------------')
            print('path: ', path)
            print('text:\n', self.getFileData(path))
        print('========================================')

    # returns the text inside of the file at the given path
    def getFileData(self, path):
        # open the file with read only privileges
        file = open(path, 'r')

        # check if the file was opened
        if file.closed:
            print("FileManager - getFileData - Could Not Open File - ", path)
            return ""

        # read all data then close file
        with file:
            data = file.read()
        file.close()

        return data

    # opens the file at the given path and writes the given data to it
    def writeFileData(self, path, data):
        # open the file with write only privileges
        file = open(path, 'w')

        # check if the file was opened
        if file.closed:
            print("FileManager - writeFileData - Could Not Open File - ", path)
            return ""

        # write data to the file then close the file
        file.write(data)
        file.close()
