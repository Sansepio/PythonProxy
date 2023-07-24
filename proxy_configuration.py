#!/usr/bin/python3

"""
created by :
David Pardo
27/10/20
"""


# run it as sudo


"""
Archivos a modificar
1) /etc/apt/apt.conf
2) /etc/environment
3) /etc/bash.bashrc
"""

# This files takes the location as input and writes the proxy authentication

import getpass  # for taking password input
import shutil  # for copying file
import sys
import os
import os.path  # for checking if file is present or not

apt_ = r'/etc/apt/apt.conf'
apt_backup = r'./.backup_proxy/apt.txt'
bash_ = r'/etc/bash.bashrc'
bash_backup = r'./.backup_proxy/bash.txt'
env_ = r'/etc/environment'
env_backup = r'./.backup_proxy/env.txt'


# This function directly writes to the apt.conf file
def writeToApt(proxy, port, username, password, flag):
    filepointer = open(apt_, "w")
    if not flag:
        filepointer.write(
            'Acquire::http::proxy "http://{0}:{1}@{2}:{3}/";\n'.format(username, password, proxy, port))
        filepointer.write(
            'Acquire::https::proxy  "https://{0}:{1}@{2}:{3}/";\n'.format(username, password, proxy, port))
        filepointer.write(
            'Acquire::ftp::proxy  "ftp://{0}:{1}@{2}:{3}/";\n'.format(username, password, proxy, port))
        filepointer.write(
            'Acquire::socks::proxy  "socks://{0}:{1}@{2}:{3}/";\n'.format(username, password, proxy, port))
    filepointer.close()


# This function writes to the environment file
# Fist deletes the lines containng http:// , https://, ftp://
def writeToEnv(proxy, port, username, password, flag):
    # find and delete line containing http://, https://, ftp://
    with open(env_, "r+") as opened_file:
        lines = opened_file.readlines()
        opened_file.seek(0)  # moves the file pointer to the beginning
        for line in lines:
            if r"http://" not in line and r"https://" not in line and r"ftp://" not in line and r"socks://" not in line:
                opened_file.write(line)
        opened_file.truncate()

    # writing starts
    if not flag:
        filepointer = open(env_, "a")
        filepointer.write(
            'http_proxy="http://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'https_proxy="https://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'ftp_proxy="ftp://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'socks_proxy="socks://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.close()


# This function will write to the
def writeToBashrc(proxy, port, username, password, flag):
    # find and delete http:// , https://, ftp://
    with open(bash_, "r+") as opened_file:
        lines = opened_file.readlines()
        opened_file.seek(0)
        for line in lines:
            if r"http://" not in line and r'"https://' not in line and r"ftp://" not in line and r"socks://" not in line:
                opened_file.write(line)
        opened_file.truncate()

    # writing starts
    if not flag:
        filepointer = open(bash_, "a")
        filepointer.write(
            'export http_proxy="http://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'export https_proxy="https://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'export ftp_proxy="ftp://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'export socks_proxy="socks://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.close()


def set_proxy(flag):
    proxy, port, username, password = "", "", "", ""
    if not flag:
        proxy = input("Introduce el proxy : ")
        port = input("Introduce el port : ")
        username = input("Introduce el username : ")
        password = getpass.getpass("Introduce la contraceña : ")
    writeToApt(proxy, port, username, password, flag)
    writeToEnv(proxy, port, username, password, flag)
    writeToBashrc(proxy, port, username, password, flag)


def view_proxy():
    # finds the size of apt file
    size = os.path.getsize(apt_)
    if size:
        filepointer = open(apt_, "r")
        string = filepointer.readline()
        print('\nHTTP Proxy: ' + string[string.rfind('@')+1 : string.rfind(':')])
        print('Port: ' + string[string.rfind(':')+1 : string.rfind('/')])
        print('Usuario: ' + string.split('://')[1].split(':')[0])
        print('Contraceña: ' + '*' * len(string[string.rfind(':',0,string.rfind('@'))+1 : string.rfind('@')]))
        filepointer.close()
    else:
        print("No proxy is set")

def restore_default():
    # copy from backup to main
    shutil.copy(apt_backup, apt_)
    shutil.copy(env_backup, env_)
    shutil.copy(bash_backup, bash_)


# The main Function Starts


if __name__ == "__main__":

    # create backup	if not present
    if not os.path.isdir("./.backup_proxy"):
        os.makedirs("./.backup_proxy")
        if os.path.isfile(apt_):
            shutil.copyfile(apt_, apt_backup)
        shutil.copyfile(env_, env_backup)
        shutil.copyfile(bash_, bash_backup)

    # choice
    print("Ejecuta el Programa como sudo\n")
    print("1:) Configura el Proxy")
    print("2:) Remover el Proxy")
    print("3:) Mostrar proxy actual")
    print("4:) Default")
    print("5:) Salir")
    choice = int(input("\nEscoje (1/2/3/4/5) : "))

    if(choice == 1):
        set_proxy(flag=0)
    elif(choice == 2):
        set_proxy(flag=1)
    elif(choice == 3):
        view_proxy()
    elif(choice == 4):
        restore_default()
    else:
        sys.exit()

    print("Echo!")