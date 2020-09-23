# this class manages all of the open documents and stores their paths into a list
import os

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog



# this class manages all of the open documents and stores their paths into a dict (absolute path: QFileInfo)
class FileManager:
    def __init__(self, app):
        print('FileManager - init')
        self.app = app  # app - QMainWindow instance
        self.open_documents = {}  # open_documents - dict that holds the key value pairs of (absolute path : QFileInfo)
        self.current_document = None  # current_document - the current document that is displayed to the user

    # saves text to the file of the given path
    def saveDocument(self):

        # get the current text from the document shown to the user
        data = self.app.layout.document.toPlainText()

        # if a file has already been opened write to the file
        if self.current_document is not None:
            self.writeFileData(self.current_document.absoluteFilePath(), data)
            print('FileManager - saveDocument - Saved File - ', self.current_document.absoluteFilePath())

        # if a file has not been opened yet prompt the user for a file name then write to that file
        else:
            # get the entered data
            file_name = QFileDialog.getSaveFileName(self.app, 'Save file')

            if file_name[0] == '':
                print('FileManager - saveDocument - No File Path Given')
                return

            path = file_name[0]

            # write the text in the document shown to the user to the given file path
            self.writeFileData(path, data)

            # append the newly created file to the dict of open docs and set it to the curr document
            self.open_documents[path] = QFileInfo(path)
            self.current_document = self.open_documents[path]

            print('FileManager - saveDocument - Saved File - ', path)

    # saves the file at the current path to the new path
    def saveAsDocument(self, new_path):
        if new_path == '':
            print('FileManager - saveAsDocument - No New File Path Given')
            return

        data = self.app.layout.document.toPlainText()

        # if the user is working on a document then delete that document
        if self.current_document is not None:
            old_path = self.current_document.absoluteFilePath()
            if self.current_document.exists():
                os.remove(old_path)
                print('FileManager - saveAsDocument - Deleted d')

        # now write to the new_path
        self.writeFileData(new_path, data)
        print('FileManager - saveAsDocument - Saved File As - ', new_path)

    # this closes the document with the given path
    # !note! this does not save the document
    def closeDocument(self, path):  # TODO - change to work with dict
        # if the path exists in the open docs list remove it
        if path in self.open_documents:
            self.open_documents.pop(path)
            print('FileManager - closeDocument - Closed File - ', path)
            if not bool(self.open_documents):
                self.current_document = None
                self.app.layout.document.updateTextBox("")

        # if it does not exist print error messages
        else:
            if path == '':
                print('FileManager - closeDocument - No File Path Given')
            else:
                print('FileManager - closeDocument - File Is Not Open - ', path)

    # clears the list of all open documents
    # !note! this does not save the documents
    def closeAll(self):
        print('FileManager - closeAll')
        self.current_document = None
        self.open_documents.clear()
        self.app.layout.document.updateTextBox("")

    # opens the file of the given path and add the Document to the dictionary
    def openDocument(self, path):
        # if there is already a file open save before the Document's text is overwritten
        if self.current_document is not None:
            self.saveDocument()

        # if the document is not already open
        if path not in self.open_documents:

            # if the user clicks out of the open file prompt do nothing
            if path == '':
                print('No File Path Given')
                return ''

            # retrieve the text from the file you are attempting to open
            data = self.getFileData(path)

            # appends the path to the list of open documents and sets it to the current document
            self.open_documents[path] = QFileInfo(path)
            self.current_document = self.open_documents[path]
            self.app.layout.bar_open_tabs.addTab(path)

            print('FileManager - openDocument - Opened Document - ', path)

        # if the document has already been opened in this session
        else:
            # get the data from the file and set the current document
            data = self.getFileData(path)
            self.current_document = self.open_documents[path]
            print('FileManager - openDocument - Document Already Open - ', path)

        # update the document shown to the user
        self.app.layout.document.updateTextBox(data)
        return data

    # returns the text inside of the file at the given path
    def getFileData(self, path):
        # open the file with read only privileges
        file = open(path, 'r')

        # check if the file was opened
        if file.closed:
            print('FileManager - getFileData - Could Not Open File - ', path)
            return ''

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
            print('FileManager - writeFileData - Could Not Open File - ', path)
            return ''

        # write data to the file then close the file
        file.write(data)
        file.close()

    # For debugging prints out all of the documents stored in open_documents dictionary
    def printAll(self):
        print('========================================')
        print('Open Documents:')
        for key, path in self.open_documents.items():
            print('----------------------------------------')
            print('path: ', key)
            print('QFileInfo:\n', path)
        print('========================================')

    # this will check all of the current open files to make sure they still exist
    # if a file doesnt exist close the file
    # TODO - determine how to handle this problem
    def fixBrokenFilePaths(self):
        for key, val in self.open_documents.items():
            if not val.exists():
                print('FileManager - fixBrokenFilePaths - File Does Not Exist - {}'.format(val.absoluteFilePath()))
