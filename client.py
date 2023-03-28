from ast import arg
from asyncore import file_dispatcher
import os
from cryptography.fernet import Fernet
import getpass

class Client:
    def __init__(self, args):
        if "all" in args and args["all"]:
            # Generate a unique master key
            self.master_key = Fernet.generate_key()
            # Save the encrypted master key to a file
            with open('./samples/master_key.key', 'wb') as file:
                file.write(self.master_key)
            self.fernet = Fernet(self.master_key)
            self.encryptAllFiles()

        elif "each" in args and args["each"]:
            # Ask the user for a password to protect the master key
            self.password = bytes(getpass.getpass(prompt='Enter a password to protect the Master Key:'), 'utf-8')
            self.encryptEachFile()

        elif "decrypt" in args and args["decrypt"] != '':
            pwd = getpass.getpass(prompt='Please enter your password:')
            self.decryptFile(args["decrypt"].split("/")[-1], pwd)

        else:
            print("Invalid arguments...")
            return

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
                # Ignore the master key and dek files
                if file == 'master_key.key' or '.key' in file or file.split('.')[0] + '.key' in files:
                    continue

                # Generate a unique master key
                self.master_key = Fernet.generate_key()
                # Save the encrypted master key to a file
                with open('./samples/master_key.key', 'wb') as fileMasterKey:
                    fileMasterKey.write(self.master_key)

                # Load the file data to be encrypted
                with open(os.path.join(root, file), 'rb') as fileToEncrypt:
                    file_data = fileToEncrypt.read()

                # Generate a new DEK for the file
                dek = Fernet.generate_key()

                # Encrypt the file using the DEK and Master Key
                fernet = Fernet(dek)
                encrypted_file = fernet.encrypt(file_data)

                # Encrypt the DEK with MK and password
                fernet2 = Fernet(self.master_key)
                encrypted_key = fernet2.encrypt(dek + bytes("-pwd-", "utf-8") + self.password)

                # Save the encrypted file and encrypted DEK to files
                with open(os.path.join(root, file), 'wb') as fileEncrypted:
                    fileEncrypted.write(encrypted_file)

                with open(os.path.join(root, file.split('.')[0] + '.key'), 'wb') as fileKey:
                    fileKey.write(encrypted_key)

                print(f'File {file} encrypted')
                

    def decryptFile(self, name_file, pwd):
        for root, dirs, files in os.walk('./samples/'):
            with open(os.path.join(root, name_file), 'rb') as fileToDecrypt:
                self.file_data = fileToDecrypt.read()

            with open(os.path.join(root, name_file.split(".")[0] + '.key'), 'rb') as keyToDecrypt:
                self.key_data = keyToDecrypt.read()

        with open('./samples/master_key.key', 'rb') as masterKey:
            self.master_key_data = masterKey.read()

        
        fernet = Fernet(self.master_key_data)
        key_decrypted = fernet.decrypt(self.key_data)
        key_decrypted_string = key_decrypted.decode('utf-8')

        if pwd == key_decrypted_string.split("-pwd-")[-1]:
            fer = Fernet(bytes(key_decrypted_string.split("-pwd-")[0], "utf-8"))
            file_decrypted = fer.decrypt(self.file_data)
            print(file_decrypted)
        else:
            print("Invalid password...")

