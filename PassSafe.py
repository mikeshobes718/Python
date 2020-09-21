#!/user/bin/env python3 
"""
PassSafe.py: This program is used for password encryption purposes.
"""

__author__      = "Michael Shobitan"
__copyright__ = "Copyright 2019, BTCS Platform Engineering"
__credits__ = ["Michael Shobitan"]
__license__ = "PFE"
__version__ = "0.1.0"
__maintainer__ = "Michael Shobitan"
__email__ = "michael.shobitan@pfizer.com"
__status__ = "Development"

import getpass
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

try:
	# Generating a Key From A Password
	password_provided = getpass.getpass()  # This is input in the form of a string
	password = password_provided.encode() # Convert to type bytes
	salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
	kdf = PBKDF2HMAC(
	algorithm=hashes.SHA256(),
	length=32,
	salt=salt,
	iterations=100000,
	backend=default_backend()
	)
	key = base64.urlsafe_b64encode(kdf.derive(password))

	# Encrypting
	f = Fernet(key)
	encrypted = f.encrypt(password_provided)

	# Decrypting
	decrypted = f.decrypt(encrypted)
	password_provided == decrypted

	# print password_provided
except Exception as error: 

	try:
		print("")
		print('ERROR: ', error)
	except:
		print("\nERROR: Please enter a valid password!")
finally:
	try:
		print("\nNOTE: Please store your key and encryted password in a safe & secure location!")
		print('\nINFO: Password entered: ' + password_provided)
		print('INFO: Password Key: ' + key)
		print('INFO: Password Encryption Key: ' + encrypted)
	except NameError as error:
		# print("Sorry")
		pass
