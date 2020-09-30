import os

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog


# this class manages all of the open documents and stores their paths into a dict (absolute path: QFileInfo)
from tr import tr


class FileManager:
    def __init__(self, app):
        print('FileManager - init')
        self.app = app  # app - QMainWindow instance
        self.open_documents = {}  # open_documents - dict that holds the key value pairs of (absolute path : QFileInfo)
        self.current_document = None  # current_document - the current document that is displayed to the user

    # saves text to the current file
    def saveDocument(self):
        # get the current text from the document shown to the user

        if self.app.top_bar.button_mode_switch.isChecked():
            data = self.app.document.toHtml()
            filter = "LeafNote (*.lef)"
        else:
            data = self.app.document.toPlainText()
            filter = ""

        # if a file has already been opened write to the file
        if self.current_document is not None:
            self.writeFileData(self.current_document.absoluteFilePath(), data)
            print('FileManager - saveDocument - Saved File - ', self.current_document.absoluteFilePath())

        # if a file has not been opened yet prompt the user for a file name then write to that file
        else:
            # get the entered data
            file_name = QFileDialog.getSaveFileName(self.app, 'Save file', self.app.app_props.mainPath, filter)

            if file_name[0] == '':
                print('FileManager - saveDocument - No File Path Given')
                return

            path = file_name[0]

            # write the text in the document shown to the user to the given file path
            self.writeFileData(path, data)

            # append the newly created file to the dict of open docs and set it to the curr document
            self.open_documents[path] = QFileInfo(path)
            self.current_document = self.open_documents[path]


            # open a new tab associated with the new file
            self.app.bar_open_tabs.addTab(path)

            print('FileManager - saveDocument - Saved File - ', path)

    # saves the file at the current path to the new path
    def saveAsDocument(self, new_path):
        if new_path == '':
            print('FileManager - saveAsDocument - No New File Path Given')
            return

        # check if the document is formatted
        if self.app.top_bar.button_mode_switch.isChecked():
            data = self.app.document.toHtml()
        else:
            data = self.app.document.toPlainText()

        # if the user is working on a document then delete that document
        if self.current_document is not None:
            old_path = self.current_document.absoluteFilePath()
            if self.current_document.exists():
                os.remove(old_path)
                print('FileManager - saveAsDocument - Deleted - ',old_path)
            # close the tab associated with the old file path
            self.app.bar_open_tabs.closeTab(old_path)

        # open a new tab associated with the new file
        self.app.bar_open_tabs.addTab(new_path)

        # now write to the new_path
        self.writeFileData(new_path, data)

        # open the document with its new text
        self.openDocument(new_path)

        print('FileManager - saveAsDocument - Saved File As - ', new_path)

    # this closes the document with the given path
    # !note! this does not save the document
    def closeDocument(self, path):  # TODO - change to work with dict
        # if the path exists in the open docs list remove it
        if path in self.open_documents:
            self.open_documents.pop(path)
            print('FileManager - closeDocument - Closed File - ', path)

            # if the open documents is NOT empty change the current document to another open file
            if bool(self.open_documents):
                self.current_document = self.open_documents[next(iter(self.open_documents))]
                self.app.document.updateTextBox(self.getFileData(self.current_document.absoluteFilePath()))
            # if the open documents IS empty set the current document to none/empty document with no path
            else:
                self.current_document = None
                self.app.document.updateTextBox("")
                self.app.top_bar.setFormattingEnabled(False)
                self.app.top_bar.button_mode_switch.setChecked(False)

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
        self.app.document.updateTextBox("")

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

            if path not in self.app.bar_open_tabs.open_tabs:
                self.app.bar_open_tabs.addTab(path)

            print('FileManager - openDocument - Opened Document - ', path)

        # if the document has already been opened in this session
        else:
            # get the data from the file and set the current document
            data = self.getFileData(path)
            self.current_document = self.open_documents[path]
            print('FileManager - openDocument - Document Already Open - ', path)

        # check for the proprietary file extension .lef and update the top bar accordingly
        print(self.current_document.suffix() == 'lef')
        self.app.top_bar.setFormattingEnabled(self.current_document.suffix() == 'lef')
        self.app.top_bar.button_mode_switch.setChecked(self.current_document.suffix() == 'lef')

        # update the document shown to the user
        self.app.document.updateTextBox(data)
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

    def lefToExt(self, extension: str = '.txt'):
        """
        Converts a .lef formatted file to a .txt file
        :return: return nothing
        """
        # get the formatted file and the old file path
        unformatted_file = self.app.document.toPlainText()
        print(unformatted_file)

        # if the current file is none make the user save the file
        if self.current_document is None:
            self.saveDocument()

        old_path = self.current_document.absoluteFilePath()

        # grab the index of the last period or if no period get the length of the string
        try:
            period_index = self.current_document.filePath().rindex('.')
        except ValueError:
            period_index = len(self.current_document.filePath())

        # create the file with the .lef extension holding the formatted data
        new_path = self.current_document.filePath()[:period_index]+extension
        self.writeFileData(new_path, unformatted_file)

        # open the .lef document and add it to the dict of the open files
        self.openDocument(new_path)

        # close the .txt document from the dict of open files
        self.closeDocument(self.current_document.absolutePath())

        # close the .txt file tab
        self.app.bar_open_tabs.closeTab(old_path)

        # delete the .txt file
        if True:  # TODO - figure out if we do want to delete the file
            if self.current_document.exists():
                os.remove(old_path)
                print('FileManager - lefToExt - Deleted - ', old_path)

    def toLef(self):
        """
        Converts an unformatted .txt file to a formatted .lef file
        :return: return nothing
        """
        # get the formatted file and the old file path
        formatted_file = self.app.document.toHtml()

        # if the current file is none make the user save the file
        if self.current_document is None:
            self.saveDocument()

        old_path = self.current_document.absoluteFilePath()

        # grab the index of the last period or if no period get the length of the string
        try:
            period_index = self.current_document.filePath().rindex('.')
        except ValueError:
            period_index = len(self.current_document.filePath())

        # create the file with the .lef extension holding the formatted data
        new_path = self.current_document.filePath()[:period_index]+".lef"
        self.writeFileData(new_path, formatted_file)

        # open the .lef document and add it to the dict of the open files
        self.openDocument(new_path)

        # close the .txt document from the dict of open files
        self.closeDocument(self.current_document.absolutePath())

        # close the .txt file tab
        self.app.bar_open_tabs.closeTab(old_path)

        # delete the .txt file
        if True:  # TODO - figure out if we do want to delete the file
            if self.current_document.exists():
                os.remove(old_path)
                print('FileManager - txtToLef - Deleted - ', old_path)

    def printAll(self):
        """
        For debugging. Prints out all of the documents stored in open_documents dictionary.
        :return:
        """
        print('========================================')
        print('Open Documents:')
        for key, path in self.open_documents.items():
            print('----------------------------------------')
            print('path: ', key)
            print('QFileInfo:\n', path)
        print('========================================')

    def fixBrokenFilePaths(self):
        """
        this will check all of the current open files to make sure they still exist
        if a file doesnt exist close the file.
        :return:
        """
        for key, val in self.open_documents.items():
            if not val.exists():
                print('FileManager - fixBrokenFilePaths - File Does Not Exist - {}'.format(val.absoluteFilePath()))
