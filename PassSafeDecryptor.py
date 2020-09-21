#!/user/bin/env python3 
"""
PassSafeDecryptor.py: This program is used for password decryption purposes.
"""

__author__      = "Michael Shobitan"
__copyright__ = "Copyright 2020, UNITED Platform Engineering"
__credits__ = ["Michael Shobitan"]
__license__ = "UG"
__version__ = "0.1.0"
__maintainer__ = "Michael Shobitan"
__email__ = "michael.shobitan@yahoo.com"
__status__ = "Development"

import sys
from cryptography.fernet import Fernet

key = raw_input("What's your password key? ")
decryption_token = raw_input("What's your encryption token? ")
encrypted = b"{}".format(decryption_token)

try:
    f = Fernet(key)
except(TypeError, ValueError):
    print("\nERROR: Please re-run program and enter the correct password key!")
    sys.exit()
# except ValueError:
#     print("\nERROR: Please re-run program and enter the correct keys!")
#     sys.exit()

try:
    decrypted = f.decrypt(encrypted)
except:
    print("\nERROR: Please re-run program and enter the correct encrypted key!")
    sys.exit()

print("\nINFO: Actual Password \"" + decrypted + "\"")
