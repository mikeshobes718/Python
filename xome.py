#!/user/bin/env python3 
"""
PassSafe.py: This program is used for password encryption purposes.
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

# key = raw_input("What's your password key? ")
# decryption_token = raw_input("What's your encryption token? ")
key = "-8so0UHGulJw6DMSHHq9iR3RA6wctC25MvjUDcrnkqc="
decryption_token = "gAAAAABfamvS6EIGEF0MZj5zsMxr_d904yXZZA9DSFjYAzlGb6CnylKyPu6TLHcgBPYJMq0b_h5IdpaQ66ThMdxyoC-2ef2UFA=="
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

from webbot import Browser 
web = Browser()
# web.go_to('google.com') 
web.go_to('https://vendor.xomevaluations.com/Account/Login?ReturnUrl=%2f') 
# web.click('Sign in')
web.type('401154' , into='Email')
web.click('NEXT' , tag='span')
web.type(decrypted , into='Password' , id='passwordFieldId') # specific selection
web.click('NEXT' , tag='span') # you are logged in ^_^
web.click('Login')
