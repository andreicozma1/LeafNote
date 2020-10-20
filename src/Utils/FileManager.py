"""
File Manager module defines the methods used to
open, save, close, create and modify files.
Both Plain-Text and Proprietary Format LEF files.
"""
import logging
import os

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox

from Utils.DialogBuilder import DialogBuilder


class FileManager:
    """
    FileManger handles everything associated with communicating with files.
    It handles all of the opening, closing,
    and saving needed for the project.
    """

    def __init__(self, app):
        """
        Initializes the 'FileManager' object. It sets up all of the class variables.
        """
        logging.debug("Creating File Manager")
        self.app = app
        self.open_documents = {}
        # open_documents - dict that holds the key value pairs of (absolute path : QFileInfo)
        self.current_document = None
        # current_document - the current document that is displayed to the user

        self.encryptor = None

    def saveDocument(self, document):
        """
        :param document: Reference to the document
        :return: Returns whether or not a tab needs to be opened
        """

        # get the current text from the document shown to the user
        if self.app.btn_mode_switch.isChecked():
            data = document.toHtml()
            file_filter = "LeafNote (*.lef)"
        else:
            data = document.toPlainText()
            file_filter = ""

        # if a file has already been opened write to the file
        if self.current_document is None:
            # if a file has not been opened yet prompt the user for a file name then write to
            # that file. Get the entered data
            file_name = QFileDialog.getSaveFileName(self.app, 'Save file',
                                                    self.app.left_menu.model.rootPath(),
                                                    file_filter)

            if file_name[0] == '':
                logging.warning("No File Path Given")
                return False

            path = file_name[0]

            # write the text in the document shown to the user to the given file path
            self.writeFileData(path, data)

            # append the newly created file to the dict of open docs and set it to the curr document
            self.open_documents[path] = QFileInfo(path)
            self.current_document = self.open_documents[path]

            logging.info("Saved File - " + path)
            state = True
        else:
            self.writeFileData(self.current_document.absoluteFilePath(), data)
            logging.info("Saved File -" + self.current_document.absoluteFilePath())
            state = False

        return state

    def saveAsDocument(self, document):
        """
        prompts the user for a new filename or path and saves the document as that
        :param document: Reference to the document
        :return: Returns if the save as succeeded or not
        """
        new_path = \
            QFileDialog.getSaveFileName(self.app, 'Save File', self.app.left_menu.model.rootPath())[
                0]

        # if the new path is an empty string do nothing
        if new_path == '':
            logging.warning("No New File Path Given")
            return False

        # check if the document is formatted
        if self.app.btn_mode_switch.isChecked():
            f_info = QFileInfo(new_path)
            if f_info.suffix() != "lef":
                new_path = os.path.join(f_info.path(), f_info.baseName()) + '.lef'
            data = document.toHtml()
        else:
            f_info = QFileInfo(new_path)
            if f_info.suffix() == "lef":
                new_path = os.path.join(f_info.path(), f_info.baseName()) + '.txt'
            data = document.toPlainText()

        # now write to the new_path
        self.writeFileData(new_path, data)

        # open the document with its new text
        self.openDocument(document, new_path)

        logging.info("Saved File As -" + new_path)
        return True

    def closeDocument(self, document, path: str):
        """
        Closes the document with the given path.
        :param document: reference to the document
        :param path: path to the document that needs to be closed
        :return: Returns whether or not the document is formatted
        """
        # if the path exists in the open docs list remove it
        if path in self.open_documents:
            self.open_documents.pop(path)
            logging.info("Closed File - " + path)

            # if the open documents is NOT empty change the current document to another open file
            if bool(self.open_documents):
                self.current_document = self.open_documents[next(iter(self.open_documents))]
                # get File data will never return None here because the document
                # had to already be opened to get to this point
                # update the formatting enabled accordingly
                text = self.getFileData(self.current_document.absoluteFilePath())
                document.setFormatText(text, self.current_document.suffix() == 'lef')

                state = (self.current_document.suffix() == 'lef')
            # if the open documents IS empty set the current document
            # to none/empty document with no path
            else:
                self.current_document = None
                document.setPlainText("")
                state = False

            self.app.right_menu.updateDetails(self.current_document)
        # if it does not exist print error messages
        else:
            if path == '':
                logging.info("No File Path Given")
            else:
                logging.info("File Is Not Open - " + path)
            state = False

        self.app.updateFormatBtnsState(state)

    def closeAll(self, document):
        """
        Clears the list of all open documents.
        NOTE - This does not save the documents.
        :return: Returns nothing
        """
        logging.info("closeAll")
        self.current_document = None
        self.open_documents.clear()
        document.setPlainText("")
        self.app.updateFormatBtnsState(False)

    def openDocument(self, document, path: str):
        """
        This will open the file with the given path and display it on the document
        :param document:
        :param path:
        :return: returns whether or not the open succeeded
        """
        # if there is already a file open save before the Document's text is overwritten
        if self.current_document is not None:
            self.saveDocument(document)

        # if the document is not already open
        if path not in self.open_documents:

            # if the user clicks out of the open file prompt do nothing
            if path == '':
                logging.info("No File Path Given")
                return False

            # retrieve the text from the file you are attempting to open
            data = self.getFileData(path)
            if data is None:
                return False

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
            if data is None:
                return False

            self.current_document = self.open_documents[path]
            self.app.bar_open_tabs.active = self.app.bar_open_tabs.open_tabs[path]
            logging.info("Document Already Open - " + path)

        # check for the proprietary file extension .lef and update the top bar accordingly
        document.setFormatText(data, self.current_document.suffix() == 'lef')

        # Update the formatting buttons based on the state
        self.app.updateFormatBtnsState(self.current_document.suffix() == 'lef')
        # update the document shown to the user
        self.app.right_menu.updateDetails(path)
        self.app.left_menu.selectPath(path)
        return True

    def getFileData(self, path: str):
        """
        This retrieves the data from the file at the specified path.
        :param path: The path to read data from
        :return: Returns a string of the read in data
        """
        # open the file with read only privileges
        logging.debug(path)
        file = open(path, 'r')
        # check if the file was opened
        if file.closed:
            logging.info("Could Not Open File - " + path)
            return None

        # read all data then close file
        with file:
            try:
                data = file.read()
            except OSError as e:
                corrupted_file = DialogBuilder(self.app,
                                               "File Corrupted",
                                               "Could not open the selected file.",
                                               "")
                button_box = QDialogButtonBox(QDialogButtonBox.Ok)
                corrupted_file.addButtonBox(button_box)
                corrupted_file.exec()
                logging.exception(e)
                logging.error("File could not be opened!")
                return None
        file.close()

        try:
            if self.encryptor is not None:
                data = self.encryptor.decrypt(data.encode()).decode()
                logging.debug("File was encrypted. Decrypting")
        except OSError:
            logging.info("File wasn't encrypted. Proceeding as normal")

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
        logging.debug(path)
        if self.encryptor is not None:
            logging.debug("Writing Encrypted")
            file = open(path, 'wb')
            data = self.encryptor.encrypt(data.encode())
        else:
            logging.debug("Writing Plain Text")
            file = open(path, 'w')

        # check if the file was opened
        if file.closed:
            logging.warning("Could Not Open File - " + path)
            return
        # write data to the file then close the file
        file.write(data)
        file.close()

    def lefToExt(self, document, extension: str = '.txt'):
        """
        Converts a .lef formatted file to a .txt file
        :return: return nothing
        """

        # get the formatted file and the old file path
        unformatted_file = self.app.document.toPlainText()

        # if the current file is none make the user save the file
        if self.current_document is None:
            self.saveDocument(document)

        old_path = self.current_document.absoluteFilePath()

        # grab the index of the last period or if no period get the length of the string
        try:
            period_index = self.current_document.filePath().rindex('.')
        except ValueError:
            period_index = len(self.current_document.filePath())

        # close the .lef file
        self.app.bar_open_tabs.closeTab(old_path, save=False)

        # delete the .txt file
        os.remove(old_path)
        logging.info("Deleted - " + old_path)

        # create the file with the given extension holding the formatted data
        new_path = old_path[:period_index] + extension
        self.writeFileData(new_path, unformatted_file)

        # open the .txt document and add it to the dict of the open files
        # this will also set the current document
        self.openDocument(document, new_path)

    def toLef(self, document):
        """
        Converts an unformatted .txt file to a formatted .lef file
        :return: return nothing
        """
        # get the formatted file
        formatted_file = self.app.document.toHtml()

        # if the current file is none make the user save the file
        is_new_file = False
        if self.current_document is None:
            is_new_file = True
            self.saveDocument(document)

        # get the old file path
        old_path = self.current_document.filePath()

        # if it is a new file open the tab
        if is_new_file:
            self.app.bar_open_tabs.addTab(old_path)

        # grab the index of the last period or if no period get the length of the string
        try:
            period_index = self.current_document.filePath().rindex('.')
        except ValueError:
            period_index = len(self.current_document.filePath())

        # close the .txt file
        self.app.bar_open_tabs.closeTab(old_path, save=False)

        # delete the .txt file
        os.remove(old_path)
        logging.info("Deleted - " + old_path)

        # create the file with the .lef extension holding the formatted data
        new_path = old_path[:period_index] + ".lef"
        self.writeFileData(new_path, formatted_file)

        # open the .lef document and add it to the dict of the open files
        self.openDocument(document, new_path)

    def newFile(self, document):
        """
        This will create a new unformatted file.
        :return: Returns nothing
        """
        # Get path name from user
        file_name = QFileDialog.getSaveFileName(self.app, 'New file',
                                                self.app.left_menu.model.rootPath())
        if file_name[0] == '':
            logging.warning('No File Path Given')
            return

        path = file_name[0]
        logging.info('Creating NewFile - ' + path)
        # create the file and open it
        self.writeFileData(path, "")
        self.openDocument(document, path)

    def printAll(self):
        """
        For debugging. Prints out all of the documents stored in open_documents dictionary.
        :return:
        """
        logging.info("========================================")
        logging.info("Open Documents:")
        for key, path in self.open_documents.items():
            logging.info("----------------------------------------")
            logging.info("path: " + key)
            logging.info("QFileInfo: " + path.absoluteFilePath())
        logging.info("========================================")

    def fixBrokenFilePaths(self):
        """
        this will check all of the current open files to make sure they still exist
        if a file doesnt exist close the file.
        :return:
        """
        for val in self.open_documents.values():
            if not val.exists():
                logging.info("File Does Not Exist - {}".format(val.absoluteFilePath()))
