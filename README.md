# Hack Chrome Password
A python program for getting the stored url, username &amp; password stored in Chrome.


# Requirements
This program only works on `Windows` computer where `Google Chrome` is installed.

Before running the program the `requirements` file need to be run, to get the libaries that is used. This is done throug running the following command:

```python
  pip install -r requirements.txt
```

The the program can be runned with follwing command:

```python
    python hack-chrome-password.py
``` 
or if you're using *python3*:

```python
    python3 hack-chrome-password.py
```


# Information
The program is working in the way that it is looking for two files in the (Windows) system. Then it uses data from these files and decrypting the password and print it out.

1. The first file the program is looking for is a JSON-file that stores the **"encryption key"**. It's located in the path: `C:\Users\<PC Name>\AppData\Local\Google\Chrome\User Data\Local State`
2. The second file is the **"Google Chrome database"**, that is located in the path: `C:\Users\<PC Name>\AppData\Local\Google\Chrome\User Data\Default\Login Data`
3. Then it's getting the login-data from the table `logins` in SQLite3 database and are useing the **"encryption key"** to decrypt the password with `win32crypt`.
4. Print the findings.

_NOTE:_ You'll find the computers `<PC NAME>` from running the command: `echo %USERNAME%`


# Credits
Thanks to:
[ohyicong](https://github.com/ohyicong) for inspiration and knowleage through his article on [Medium](https://ohyicong.medium.com/how-to-hack-chrome-password-with-python-1bedc167be3d)
