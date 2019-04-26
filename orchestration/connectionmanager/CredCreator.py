#!/usr/bin/env python

import configparser
from cryptography.fernet import Fernet
import sys


class CredCreator():
    def createCredIni(self, tech, server, user, passwd):
        Config = configparser.ConfigParser()
        with open("/var/.osdscreds.ini", 'w') as credFile:
            Config.add_section('CREDS')
            Config.set('CREDS', 'tech', tech)
            Config.set('CREDS', 'server', server)
            Config.set('CREDS', 'user', user)
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            passwd = passwd.encode()
            cipher_text = cipher_suite.encrypt(passwd)
            Config.set('CREDS', 'pass', cipher_text)
            Config.set('CREDS', 'phrase', key)
            Config.write(credFile)
            credFile.close()

    def getCreds(self):
        tech = ''
        server = ''
        user = ''
        passwd = ''
        try:
            Config = configparser.ConfigParser()
            Config.read('/var/.osdscreds.ini')
            server = Config.get('CREDS', 'server')
            user = Config.get('CREDS', 'user')
            phrase = Config.get('CREDS', 'phrase')
            passwd = Config.get('CREDS', 'pass')
            tech = Config.get('CREDS', 'tech')
            ciphered_suite = Fernet(phrase.encode())
            passwd = (ciphered_suite.decrypt(passwd.encode()))
        except Exception as ex:
            print(passwd)
            print(ex)
            raise ex
        finally:
            return tech, server, user, passwd


def usage():
    str = """
            This utility takes technology, servername,
            username and password and stores in file
            To store use 'set <technology> <servername>
                                <username> <password>
            And to retrieve, use 'get'
            Usage:
            ./credCreator set <servername> <username> <password>
            ./credCreator get
            """
    print(str)


if __name__ == '__main__':
    count = len(sys.argv)
    if count < 2:
        usage()
        sys.exit(1)
    if sys.argv[1] == 'set':
        if count != 6:
            usage()
            sys.exit(1)
        else:
            tech = sys.argv[2]
            server = sys.argv[3]
            user = sys.argv[4]
            passwd = sys.argv[5]
            CredCreator().createCredIni(tech, server, user, passwd)
    elif sys.argv[1] == 'get':
        print(CredCreator().getCreds())
