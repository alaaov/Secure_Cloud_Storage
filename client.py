import os
from cryptography.fernet import Fernet

# Generate a unique master key and store it in a local file
master_key = Fernet.generate_key()
with open('master.key', 'wb') as f:
    f.write(master_key)

# Load the master key from the file
with open('master.key', 'rb') as f:
    master_key = f.read()

# Create a Fernet object using the master key
fernet = Fernet(master_key)

# Encrypt all files in the current directory and its subdirectories
for root, dirs, files in os.walk('./samples/'):
    for file in files:
        # Ignore the master key file
        if file == 'master.key':
            continue

        # Read the contents of the file
        with open(os.path.join(root, file), 'rb') as f:
            content = f.read()

        # Encrypt the content and write the result to the same file
        encrypted_content = fernet.encrypt(content)
        with open(os.path.join(root, file), 'wb') as f:
            f.write(encrypted_content)
