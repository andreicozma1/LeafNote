"""
File Manager module defines the methods used to
open, save, close, create and modify files.
Both Plain-Text and Proprietary Format LEF files.
"""
import logging
import os

from PyQt5.QtCore import QFileInfo
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox, QDialog

from Utils import DialogBuilder


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

        # open_documents - dict that holds the key value pairs of (absolute path : QFileInfo)
        self.open_documents = {}
        # current_document - the current document that is displayed to the user
        self.current_document = None
        # last_access - the time when the file was opened
        self.file_opened_time = None

        self.encryptor = None

    def saveDocument(self, document):
        """
        This will save the current document to a file on disk
        :param document: Reference to the document
        :return: Returns whether or not the save succeeded
        """
        file_missing = False

        # get the current text from the document shown to the user
        if self.app.btn_mode_switch.isChecked():
            data = document.toHtml()
            file_filter = "LeafNote (*.lef)"
        else:
            data = document.toPlainText()
            file_filter = ""

        # if the file has not been changed do nothing
        if self.current_document is not None and data == self.getFileData(
                self.current_document.absoluteFilePath()):
            return False

        # if a file has already been opened write to the file
        if self.current_document is not None:
            # check if the file that was being worked on has been moved externally
            file_exists, file_missing = self.checkCurrentFileExists()

            if not file_exists:
                # if the user selected not to save the file
                return False

            if not file_missing:
                # if the file is not missing check its time
                if self.checkCurrentFileTime(document):
                    # if the user is up to date or wants to save the current document
                    self.writeFileData(self.current_document.absoluteFilePath(), data)
                    self.file_opened_time = os.path.getatime(
                        self.current_document.absoluteFilePath()
                    )
                    logging.info("Saved File - %s", self.current_document.absoluteFilePath())
                return True

        # get the entered data
        file_name = QFileDialog.getSaveFileName(self.app, 'Save file',
                                                self.app.left_menu.model.rootPath(),
                                                file_filter)

        if file_name is None or file_name[0] == '':
            logging.info("No File Path Given")
            return False

        path = file_name[0]

        # write the text in the document shown to the user to the given file path
        self.writeFileData(path, data)

        # append the newly created file to the dict of open docs and set it to the curr document
        self.open_documents[path] = QFileInfo(path)
        self.current_document = self.open_documents[path]
        self.file_opened_time = os.path.getatime(self.current_document.absoluteFilePath())

        # if the file had been moved or deleted while editing and the user chose to save
        if file_missing:
            document.setText(data)
            self.app.bar_open_tabs.addTab(path)

        logging.info("Saved File - %s", path)
        return True

    def checkCurrentFileExists(self):
        """
        this checks if the current file the user is working on exists.
        this returns a tuple of boolean values where the first value is if the file exists or if
        the user wants to keep the file. The second value in the tuple is if the file itself is
        missing.
        """
        # check if the file exists
        if os.path.exists(self.current_document.absoluteFilePath()):
            # returns true that the file exists and false saying the file is not missing
            return True, False

        # if the file doesnt exist prompt the user to ask if they want to save it
        logging.warning("File not found")
        file_not_found_dialog = DialogBuilder.DialogBuilder(self.app,
                                                            "File not found",
                                                            "File not found",
                                                            "The original file has been "
                                                            "moved/deleted "
                                                            "externally. Would you like "
                                                            "to save a current "
                                                            "copy of the file?")
        button_box = QDialogButtonBox(QDialogButtonBox.No | QDialogButtonBox.Yes)
        file_not_found_dialog.addButtonBox(button_box)

        # close the tab with the current name because we will create newtab if the user
        # wants to save the file and we dont want to keep it if the user does not want to save
        self.app.bar_open_tabs.closeTab(self.current_document.absoluteFilePath(), False)

        if file_not_found_dialog.exec():
            # if the user chose to save the document return true that the file will exist and
            # true that the file is in fact missing
            logging.info("User chose save the current document.")
            return True, True

        # if the user chose not to save the file return false that the file doesnt exist
        # and false that the file is missing
        logging.info("User chose NOT to save the file.")
        return False, False

    def checkCurrentFileTime(self, document):
        """
        this will check the times of the current file to see if its outdated. If it is up to date
        save it. If it is not up to date prompt the user if they want to update to the most
        recent changes or keep their current changes.
        :param document: reference to the document
        :return: returns true if the user wants to keep their changes, false otherwise
        """
        if self.file_opened_time is not None and self.file_opened_time < os.path.getmtime(
                self.current_document.absoluteFilePath()):
            # if the file has been modified since the document was opened
            logging.warning("opened: %s, modified: %s", str(self.file_opened_time),
                            str(os.path.getmtime(self.current_document.absoluteFilePath())))

            # prompt the user if they want to keep their changes
            file_not_up_to_date_dialog = DialogBuilder.DialogBuilder(self.app,
                                                                     "File not up to date",
                                                                     "File not up to date",
                                                                     "The file has been "
                                                                     "externally "
                                                                     "modified. Would you "
                                                                     "like to keep your "
                                                                     "changes?")
            button_box = QDialogButtonBox(QDialogButtonBox.No | QDialogButtonBox.Yes)
            file_not_up_to_date_dialog.addButtonBox(button_box)

            if file_not_up_to_date_dialog.exec():
                # if they want to keep their changes return true
                logging.debug("User chose to keep their changes")
                return True

            # if they want to update to the most recent changes on disk return false
            logging.debug("User chose to update to file saved on disk")
            data = self.getFileData(self.current_document.absoluteFilePath())
            self.writeFileData(self.current_document.absoluteFilePath(), data)
            self.openDocument(document, self.current_document.absoluteFilePath(), False)
            self.file_opened_time = os.path.getatime(self.current_document.absoluteFilePath())
            return False

        # return true if the file is up to date
        return True

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

        # add the document to the dict of documents
        self.open_documents[new_path] = QFileInfo(new_path)
        self.current_document = self.open_documents[new_path]
        self.file_opened_time = os.path.getatime(self.current_document.absoluteFilePath())

        # open the document with its new text
        self.openDocument(document, new_path)

        logging.info("Saved File As - %s", new_path)
        return True

    def closeDocument(self, document, path: str):
        """
        Closes the document with the given path.
        :param document: reference to the document
        :param path: path to the document that needs to be closed
        """
        # if the path exists in the open docs list remove it
        if path in self.open_documents:
            self.open_documents.pop(path)
            logging.info("Closed File - %s", path)

            # if the open documents is NOT empty change the current document to another open file
            if bool(self.open_documents):
                self.current_document = self.open_documents[next(iter(self.open_documents))]

                # get File data will never return None here because the document
                # had to already be opened to get to this point
                # update the formatting enabled accordingly
                text = self.getFileData(self.current_document.absoluteFilePath())
                document.setFormatText(text, self.current_document.suffix() == 'lef')
                self.file_opened_time = os.path.getatime(self.current_document.absoluteFilePath())

                state = (self.current_document.suffix() == 'lef')

            # if the open documents IS empty set the current document
            # to none/empty document with no path
            else:
                self.current_document = None
                self.file_opened_time = None

                document.setPlainText("")
                state = False

            self.app.right_menu.updateDetails(self.current_document)
            self.app.updateFormatBtnsState(state)

        # if it does not exist print error messages
        else:
            if path == '':
                logging.info("No File Path Given")
            else:
                logging.info("File Is Not Open - %s", path)

    def closeAll(self, document):
        """
        Clears the list of all open documents.
        NOTE - This does not save the documents.
        :return: Returns nothing
        """
        logging.info("closeAll")
        self.current_document = None
        self.file_opened_time = None

        self.open_documents.clear()
        document.setPlainText("")
        self.app.updateFormatBtnsState(False)

    def openDocument(self, document, path: str, save: bool = True):
        """
        This will open the file with the given path and display it on the document
        :param document:
        :param path:
        :return: returns whether or not the open succeeded
        """
        # if there is already a file open save before the Document's text is overwritten
        if save and self.current_document is not None:
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
            self.file_opened_time = os.path.getatime(self.current_document.absoluteFilePath())

            # if the file is not opened in the open tabs bar open it
            if path not in self.app.bar_open_tabs.open_tabs:
                self.app.bar_open_tabs.addTab(path)

            logging.info("Opened Document - %s", path)

        # if the document has already been opened in this session
        else:
            # get the data from the file and set the current document
            data = self.getFileData(path)
            if data is None:
                return False

            self.current_document = self.open_documents[path]
            self.file_opened_time = os.path.getatime(self.current_document.absoluteFilePath())

            self.app.bar_open_tabs.active = self.app.bar_open_tabs.open_tabs[path]
            logging.info("Document Already Open - %s", path)

        # check for the proprietary file extension .lef and update the top bar accordingly
        document.setFormatText(data, self.current_document.suffix() == 'lef')

        # Update the formatting buttons based on the state
        self.app.updateFormatBtnsState(self.current_document.suffix() == 'lef')
        # update the document shown to the user
        self.app.right_menu.updateDetails(path)
        self.app.left_menu.selectItemFromPath(path)
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
            logging.info("Could Not Open File - %s", path)
            return None

        # read all data then close file
        with file:
            try:
                data = file.read()

            except OSError as e:
                corrupted_file = DialogBuilder.DialogBuilder(self.app,
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
            logging.warning("Could Not Open File - %s", path)
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
        logging.info("Deleted - %s", old_path)

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
        logging.info("Deleted - %s", old_path)

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
        logging.info('Creating NewFile - %s', path)
        # create the file and open it
        self.writeFileData(path, "")
        self.openDocument(document, path)

    def exportToPDF(self, document):
        """
        this will download the formatted document to the file of the users choice
        :param document: reference to the document
        :param to_print: if the caller intends to print the document
        :return: returns the qprinter object that is created
        """
        logging.debug("")
        # get the file name if exporting
        file_name = QFileDialog.getSaveFileName(self.app, 'Save To PDF')

        if file_name is not None:
            file_name = file_name[0]

        # if the file name is not given return none
        if file_name == '':
            return None

        # if there is no pdf extension then add it
        file_info = QFileInfo(file_name)
        if file_info.suffix() != "pdf":
            if file_name.find('.') != -1:
                file_name = file_name[:file_name.rindex('.')] + ".pdf"
            else:
                file_name = file_name + ".pdf"

        # create the qprinter object
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setColorMode(QPrinter.Color)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_name)
        document.print_(printer)
        return printer

    def printDocument(self, document):
        """
        this will print the document to the selected printer
        :param document: reference to the document
        :return: return true on print, false otherwise
        """
        # create the qprinter object
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setColorMode(QPrinter.Color)
        printer.setOutputFormat(QPrinter.NativeFormat)

        # create and run the print dialog
        print_dialog = QPrintDialog(printer)
        state = print_dialog.exec_()
        print(state)
        print(QDialog.Accepted)
        if state == QDialog.Accepted:
            # print if the user selected print
            logging.debug("User chose to print")
            document.print_(printer)
            return True

        # if the user selected not to print
        logging.warning("User chose NOT to print")
        return False

    def printAll(self):
        """
        For debugging. Prints out all of the documents stored in open_documents dictionary.
        :return: returns nothing
        """
        logging.info("========================================")
        logging.info("Open Documents:")
        for key, path in self.open_documents.items():
            logging.info("----------------------------------------")
            logging.info("path: %s", key)
            logging.info("QFileInfo: %s", path.absoluteFilePath())
        logging.info("========================================")
