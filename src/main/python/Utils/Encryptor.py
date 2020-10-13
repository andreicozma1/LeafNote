import logging
import os

from PyQt5.QtWidgets import QDialogButtonBox, QLineEdit, QFileDialog
from cryptography.fernet import Fernet

from Utils.DialogBuilder import DialogBuilder
from os.path import expanduser


class Encryptor(Fernet):
    def __init__(self, key):
        super(Encryptor, self).__init__(key)
        logging.info("Create Encryptor Class")


def onEncryptionAction(app, file_manager):
    def onEncryptBtnClicked(button):
        encryptionDialogHandler(app, file_manager, button)
    def onDecryptBtnClicked(button):
        decryptionDialogHandler(app, file_manager, button)


    # TODO - add ability to permanently decrypt directory (delete key and write plain text)
    # TODO - upon encryption loop through all files in workspace and write encrypted
    if file_manager.encryptor is None:
        dialog_encryptor = DialogBuilder(app, "Encryptor",
                                         "Would you like to Encrypt all files in the workspace?",
                                         "Please proceed with caution.")
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
        buttons.clicked.connect(onEncryptBtnClicked)
        dialog_encryptor.addButtonBox(buttons)
        dialog_encryptor.show()
    else:
        dialog_encryptor = DialogBuilder(app, "Encryptor",
                                         "Would you like to Decrypt all files in the workspace!",
                                         "Please proceed with caution.")
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
        buttons.clicked.connect(onDecryptBtnClicked)
        dialog_encryptor.addButtonBox(buttons)
        dialog_encryptor.show()


def encryptionDialogHandler(app, file_manager, button):
    if button.text() == "&Yes":
        logging.info("User clicked Yes")
        key = Fernet.generate_key()
        path_workspace = app.left_menu.model.rootPath()
        path_key = os.path.join(path_workspace, '.leafCryptoKey')
        with open(path_key, 'wb') as f:
            f.write(key)
        logging.debug("Saved key to: " + path_key)
        file_manager.encryptor = Encryptor(key)

        logging.info("ENCRYPTING ALL FILES IN WORKSPACE!")
        for dirpath, dirnames, filenames in os.walk(path_workspace):
            for filename in [f for f in filenames if not f.startswith(".")]:
                path = os.path.join(dirpath, filename)
                file_manager.writeFileData(path, file_manager.getFileData(path))

    else:
        logging.info("User canceled")


def decryptionDialogHandler(app, file_manager, button):
    if button.text() == "&Yes":
        logging.info("User clicked Yes")

        path_workspace = app.left_menu.model.rootPath()

        logging.info("DECRYPTING ALL FILES IN WORKSPACE")
        for dirpath, dirnames, filenames in os.walk(path_workspace):
            for filename in [f for f in filenames if not f.startswith(".")]:
                path = os.path.join(dirpath, filename)
                file = open(path, 'w')
                file_data = file_manager.getFileData(path)
                file.write(file_data)
                file.close()

        path_key = os.path.join(path_workspace, '.leafCryptoKey')
        if os.path.exists(path_key):
            os.remove(path_key)
            logging.debug("Removed CRYPTO KEY: " + path_key)
        else:
            logging.error("Failed to remove CRYPTO KEY")

        file_manager.encryptor = None
        logging.debug("De-initialized Encryptor")

    else:
        logging.info("User canceled")
