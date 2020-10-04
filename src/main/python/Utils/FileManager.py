import logging
import os

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog


class FileManager:
    """
    FileManger handles everything associated with communicating with files. It handles all of the opening, closing,
    and saving needed for the project.
    """

    def __init__(self, app):
        """
        Initializes the 'FileManager' object. It sets up all of the class variables.
        :param app: QMainWindow instance
        """
        logging.info("")
        self.app = app
        self.open_documents = {}  # open_documents - dict that holds the key value pairs of (absolute path : QFileInfo)
        self.current_document = None  # current_document - the current document that is displayed to the user

    def saveDocument(self):
        """
        This saves formatted or unformatted text in the current document to its respective file.
        :return: Returns nothing
        """
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
            logging.info("Saved File -" + self.current_document.absoluteFilePath())

        # if a file has not been opened yet prompt the user for a file name then write to that file
        else:
            # get the entered data
            file_name = QFileDialog.getSaveFileName(self.app, 'Save file', self.app.app_props.mainPath, filter)

            if file_name[0] == '':
                logging.info("No File Path Given")
                return

            path = file_name[0]

            # write the text in the document shown to the user to the given file path
            self.writeFileData(path, data)

            # append the newly created file to the dict of open docs and set it to the curr document
            self.open_documents[path] = QFileInfo(path)
            self.current_document = self.open_documents[path]

            # open a new tab associated with the new file
            self.app.bar_open_tabs.addTab(path)

            logging.info("Saved File - " + path)

    def saveAsDocument(self, new_path: str):
        """
        This saves the current open document to the new given path.
        :param new_path: The new path of the current document
        :return: Returns nothing
        """

        # if the new path is an empty string do nothing
        if new_path == '':
            logging.info("No New File Path Given")
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
                logging.info("Deleted -" + old_path)
            # close the tab associated with the old file path
            self.app.bar_open_tabs.closeTab(old_path)

        # open a new tab associated with the new file
        self.app.bar_open_tabs.addTab(new_path)

        # now write to the new_path
        self.writeFileData(new_path, data)

        # open the document with its new text
        self.openDocument(new_path)

        logging.info("Saved File As -" + new_path)

    def closeDocument(self, path: str):
        """
        This closes the document with the given path.
        NOTE - This does not save the document.
        :param path: The path of an open document to close
        :return: Returns nothing
        """
        # if the path exists in the open docs list remove it
        if path in self.open_documents:
            self.open_documents.pop(path)
            logging.info("Closed File - " + path)

            # if the open documents is NOT empty change the current document to another open file
            if bool(self.open_documents):
                self.current_document = self.open_documents[next(iter(self.open_documents))]
                self.app.document.updateTextBox(self.getFileData(self.current_document.absoluteFilePath()))

                # update the formatting enabled accordingly
                if self.current_document.suffix() != 'lef':
                    self.app.document.resetFormatting()
                self.app.top_bar.setFormattingButtonsEnabled(self.current_document.suffix() == 'lef')
                self.app.top_bar.button_mode_switch.setChecked(self.current_document.suffix() == 'lef')

            # if the open documents IS empty set the current document to none/empty document with no path
            else:
                self.current_document = None
                self.app.document.updateTextBox("")
                self.app.top_bar.setFormattingButtonsEnabled(False)
                self.app.top_bar.button_mode_switch.setChecked(False)

        # if it does not exist print error messages
        else:
            if path == '':
                logging.info("No File Path Given")
            else:
                logging.info("File Is Not Open - " + path)

    def closeAll(self):
        """
        Clears the list of all open documents.
        NOTE - This does not save the documents.
        :return: Returns nothing
        """
        logging.info("closeAll")
        self.current_document = None
        self.open_documents.clear()
        self.app.document.updateTextBox("")
        self.app.top_bar.setFormattingButtonsEnabled(False)
        self.app.top_bar.button_mode_switch.setChecked(False)

    def openDocument(self, path: str):
        """
        Opens the file of the given path and add the Document to the dictionary.
        :param path: The path to the file to open
        :return: Returns nothing
        """
        # if there is already a file open save before the Document's text is overwritten
        if self.current_document is not None:
            self.saveDocument()

        # if the document is not already open
        if path not in self.open_documents:

            # if the user clicks out of the open file prompt do nothing
            if path == '':
                logging.info("No File Path Given")
                return ''

            # retrieve the text from the file you are attempting to open
            data = self.getFileData(path)

            # appends the path to the list of open documents and sets it to the current document
            self.open_documents[path] = QFileInfo(path)
            self.current_document = self.open_documents[path]

            # if the file is not opened in the open tabs bar open it
            if path not in self.app.bar_open_tabs.open_tabs:
                self.app.bar_open_tabs.addTab(path)

            logging.info("Opened Document - " + path)

        # if the document has already been opened in this session
        else:
            # get the data from the file and set the current document
            data = self.getFileData(path)
            self.current_document = self.open_documents[path]
            logging.info("Document Already Open - " + path)

        # check for the proprietary file extension .lef and update the top bar accordingly
        self.app.document.textCursor().clearSelection()
        if self.current_document.suffix() != 'lef':
            self.app.document.resetFormatting()
        self.app.updateFormatBtnsState(self.current_document.suffix() == 'lef')
        # self.app.top_bar.setFormattingButtonsEnabled(self.current_document.suffix() == 'lef')
        self.app.top_bar.button_mode_switch.setChecked(self.current_document.suffix() == 'lef')

        # update the document shown to the user
        self.app.document.updateTextBox(data)
        return data

    def getFileData(self, path: str) -> str:
        """
        This retrieves the data from the file at the specified path.
        :param path: The path to read data from
        :return: Returns a string of the read in data
        """
        # open the file with read only privileges
        file = open(path, 'r')

        # check if the file was opened
        if file.closed:
            logging.info("Could Not Open File - " + path)
            return ''

        # read all data then close file
        with file:
            data = file.read()
        file.close()

        return data

    # opens the file at the given path and writes the given data to it
    def writeFileData(self, path: str, data: str):
        """
        Writes the given data to the file at the specified path.
        :param path: The file to write data to
        :param data: The data to write to the file
        :return: Returns nothing
        """
        # open the file with write only privileges
        file = open(path, 'w')

        # check if the file was opened
        if file.closed:
            logging.info("Could Not Open File - " + path)
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

        # if the current file is none make the user save the file
        if self.current_document is None:
            self.saveDocument()

        old_path = self.current_document.absoluteFilePath()

        # grab the index of the last period or if no period get the length of the string
        try:
            period_index = self.current_document.filePath().rindex('.')
        except ValueError:
            period_index = len(self.current_document.filePath())

        # close the .lef file
        self.app.bar_open_tabs.closeTab(old_path, False)

        # delete the .txt file
        os.remove(old_path)
        logging.info("Deleted - " + old_path)

        # create the file with the given extension holding the formatted data
        new_path = old_path[:period_index] + extension
        self.writeFileData(new_path, unformatted_file)

        # open the .txt document and add it to the dict of the open files
        # this will also set the current document
        self.openDocument(new_path)

        # converting back from a formatted file. Reset all formatting and button selections
        self.app.document.resetFormatting()
        self.app.top_bar.setFormattingButtonsEnabled(False)

    def toLef(self):
        """
        Converts an unformatted .txt file to a formatted .lef file
        :return: return nothing
        """
        # get the formatted file
        formatted_file = self.app.document.toHtml()

        # if the current file is none make the user save the file
        if self.current_document is None:
            self.saveDocument()

        # get teh old file path
        old_path = self.current_document.filePath()

        # grab the index of the last period or if no period get the length of the string
        try:
            period_index = self.current_document.filePath().rindex('.')
        except ValueError:
            period_index = len(self.current_document.filePath())

        # close the .txt file
        self.app.bar_open_tabs.closeTab(old_path, False)

        # delete the .txt file
        os.remove(old_path)
        logging.info("Deleted - " + old_path)

        # create the file with the .lef extension holding the formatted data
        new_path = old_path[:period_index] + ".lef"
        self.writeFileData(new_path, formatted_file)

        # open the .lef document and add it to the dict of the open files
        self.openDocument(new_path)

    def newFile(self):
        """
        This will create a new unformatted file.
        :return: Returns nothing
        """
        # Get path name from user
        file_name = QFileDialog.getSaveFileName(self.app, 'New file', self.app.app_props.mainPath, "")
        if file_name[0] == '':
            logging.info('No File Path Given')
            return
        path = file_name[0]

        # create the file and open it
        self.writeFileData(path, "")
        self.openDocument(path)
        logging.info(' Created NewFile - ', path)

    def printAll(self):
        """
        For debugging. Prints out all of the documents stored in open_documents dictionary.
        :return:
        """
        logging.info("==========================================================")
        logging.info("Open Documents:")
        for key, path in self.open_documents.items():
            logging.info("======================================================")
            logging.info("path: ", key)
            logging.info("QFileInfo:\n", path)
        logging.info("==========================================================")

    def fixBrokenFilePaths(self):
        """
        this will check all of the current open files to make sure they still exist
        if a file doesnt exist close the file.
        :return:
        """
        for key, val in self.open_documents.items():
            if not val.exists():
                logging.info("File Does Not Exist - {}".format(val.absoluteFilePath()))
