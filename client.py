from ast import arg
import os
from cryptography.fernet import Fernet
import getpass

class Client:
    def __init__(self, args):
        # Generate a unique master key
        self.master_key = Fernet.generate_key()

        if "all" in args and args["all"]:
            print(self.master_key)
            self.fernet = Fernet(self.master_key)
            self.encryptAllFiles()

        elif "each" in args and args["each"]:
            # Ask the user for a password to protect the master key
            self.password = bytes(getpass.getpass(prompt='Enter a password to protect the Master Key:'), 'utf-8')
            print(self.password)
            # Encrypt the master key using the user's password
            self.fernet = Fernet(self.master_key)
            self.master_key = self.fernet.encrypt(self.password)
            print("hola")
            # self.encryptEachFile()

        else:
            print("Invalid arguments...")
            return

        # Save the encrypted master key to a file
        with open('master_key.key', 'wb') as file:
            file.write(self.master_key)

    def encryptAllFiles(self):
        # Encrypt all files in the current directory and its subdirectories
        for root, dirs, files in os.walk('./samples/'):
            for file in files:
                # Ignore the master key file
                if file == 'master_key.key':
                    continue

                # Read the contents of the file
                with open(os.path.join(root, file), 'rb') as f:
                    content = f.read()

                # Encrypt the content and write the result to the same file
                encrypted_content = self.fernet.encrypt(content)
                with open(os.path.join(root, file), 'wb') as f:
                    f.write(encrypted_content)

    def encryptEachFile(self):
        # Encrypt all files in the current directory and its subdirectories
        for root, dirs, files in os.walk('./samples/'):
            for file in files:
                # Ignore the master key file
                if file == 'master_key.key':
                    continue

                # Load the file data to be encrypted
                with open(os.path.join(root, file), 'rb') as fileToEncrypt:
                    file_data = fileToEncrypt.read()

                # Generate a new DEK for the file
                dek = Fernet.generate_key()

                # Encrypt the file using the DEK and Master Key
                fernet = Fernet(self.master_key)
                encrypted_file = fernet.encrypt(dek + file_data)

                # Save the encrypted file and encrypted DEK to files
                with open('file.bin', 'wb') as fileEncrypted:
                    fileEncrypted.write(encrypted_file)

                with open('file.key', 'wb') as fileKey:
                    fileKey.write(dek)
