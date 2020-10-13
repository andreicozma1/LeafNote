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
    def onDialogButtonClicked(button):
        encryptionDialogHandler(app, file_manager, button)

    # TODO - add ability to permanently decrypt directory (delete key and write plain text)
    # TODO - upon encryption loop through all files in workspace and write encrypted
    if file_manager.encryptor is None:
        dialog_encryptor = DialogBuilder(app, "Encryptor",
                                         "Would you like to encrypt all files in the workspace?",
                                         "This process is irreversible. Please proceed with caution.\n")
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
        buttons.clicked.connect(onDialogButtonClicked)
        dialog_encryptor.addButtonBox(buttons)
        dialog_encryptor.show()
    else:
        dialog_encryptor = DialogBuilder(app, "Encryptor",
                                         "Workspace already encrypted!")
        dialog_encryptor.show()


def encryptionDialogHandler(app, file_manager, button):
    if button.text() == "&Yes":
        logging.info("User clicked Yes")
        key = Fernet.generate_key()
        save_path = os.path.join(app.left_menu.model.rootPath(), '.leafCryptoKey')
        with open(save_path, 'wb') as f:
            f.write(key)
        logging.debug("Saved key to: " + save_path)
        file_manager.encryptor = Encryptor(key)
    else:
        logging.info("User canceled")
