import logging
import os

from PyQt5.QtWidgets import QDialogButtonBox
from cryptography.fernet import Fernet

from Utils.DialogBuilder import DialogBuilder


class Encryptor(Fernet):
    def __init__(self, key):
        super(Encryptor, self).__init__(key)
        logging.debug("Creating Encryptor")

    def encryptFile(self, path):
        """
        Given a filename (str) and key (bytes), it encrypts the file and write it
        """
        with open(path, "rb") as file:
            # read all file data
            file_data = file.read()
        # encrypt data
        encrypted_data = self.encrypt(file_data)
        # write the encrypted file
        with open(path, "wb") as file:
            file.write(encrypted_data)

    def decryptFile(self, path):
        """
        Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        with open(path, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
        decrypted_data = self.decrypt(encrypted_data)
        # write the original file
        with open(path, "wb") as file:
            file.write(decrypted_data)


def onEncryptionAction(app, file_manager):
    # Helper Functions
    def onEncryptBtnClicked(button):
        encryptionDialogHandler(app, file_manager, button)

    def onDecryptBtnClicked(button):
        decryptionDialogHandler(app, file_manager, button)

    # Check whether the encryptor already exists
    if file_manager.encryptor is None:
        # To encrypt workspace
        logging.info("Encryptor NOT initialized")
        dialog_encryptor = DialogBuilder(app, "Crypto - Encrypt",
                                         "Would you like to Encrypt all files in the workspace?",
                                         "Please proceed with caution.")
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
        buttons.clicked.connect(onEncryptBtnClicked)
        dialog_encryptor.addButtonBox(buttons)
        dialog_encryptor.show()
    else:
        # To decrypt workspace
        logging.info("Encryptor already initialized")
        dialog_encryptor = DialogBuilder(app, "Crypto - Decrypt",
                                         "Would you like to Decrypt all files in the workspace!",
                                         "Please proceed with caution.")
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
        buttons.clicked.connect(onDecryptBtnClicked)
        dialog_encryptor.addButtonBox(buttons)
        dialog_encryptor.show()


def encryptionDialogHandler(app, file_manager, button):
    """
    Checks user input and encrypts workspace if needed
    :param app: application context
    :file_manager: file_manager context
    :button: button clicked reference
    """
    if button.text() == "&Yes":
        logging.info("User clicked Yes")
        key = Fernet.generate_key()
        path_workspace = app.left_menu.model.rootPath()
        path_key = os.path.join(path_workspace, '.leafCryptoKey')
        try:
            with open(path_key, 'wb') as f:
                f.write(key)
                logging.debug("Saved key to: " + path_key)
        except:
            logging.error("Failed to save CRYPTO KEY")
            return

        file_manager.encryptor = Encryptor(key)
        logging.info("START ENCRYPT FILES IN WORKSPACE: " + path_workspace)
        for dirpath, dirnames, filenames in os.walk(path_workspace):
            for filename in [f for f in filenames if not f.startswith(".")]:
                path = os.path.join(dirpath, filename)
                file_manager.encryptor.encryptFile(path)
                logging.info(" - Encrypted: " + path)
        logging.info("END ENCRYPT FILES IN WORKSPACE: " + path_workspace)

    else:
        logging.info("User canceled")


def decryptionDialogHandler(app, file_manager, button):
    """
    Checks user input and decrypts workspace if needed
    :param app: application context
    :file_manager: file_manager context
    :button: button clicked reference
    """
    if button.text() == "&Yes":
        logging.info("User clicked Yes")

        path_workspace = app.left_menu.model.rootPath()
        logging.info("START DECRYPT WORKSPACE: " + path_workspace)
        for dirpath, dirnames, filenames in os.walk(path_workspace):
            for filename in [f for f in filenames if not f.startswith(".")]:
                path = os.path.join(dirpath, filename)
                file_manager.encryptor.decryptFile(path)
                logging.info(" - Decrypted: " + path)
        logging.info("END DECRYPT WORKSPACE: " + path_workspace)

        path_key = os.path.join(path_workspace, '.leafCryptoKey')
        if os.path.exists(path_key):
            os.remove(path_key)
            logging.debug("Removed CRYPTO KEY: " + path_key)
        else:
            logging.error("Failed to remove CRYPTO KEY")
            return

        file_manager.encryptor = None
        logging.debug("De-initialized Encryptor")

    else:
        logging.info("User canceled")
