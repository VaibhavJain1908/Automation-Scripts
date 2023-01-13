import paramiko
import getpass
import datetime
import time
from colorama import Fore
from colorama import Style
import warnings
warnings.filterwarnings("ignore")

print(Fore.BLUE + Style.BRIGHT + "\n\n*****************************************************\n***************************************************")
print("******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "**********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*******************")
print("*******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "***********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*****************")
print("********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "****" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "***************")
print("*********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "**" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*******" + Style.RESET_ALL + "##" +  Fore.BLUE + Style.BRIGHT + "****" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*************")
print("**********" + Style.RESET_ALL + "####" + Fore.BLUE + Style.BRIGHT + "*********" + Style.RESET_ALL + "##" +  Fore.BLUE + Style.BRIGHT + "**" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************")
print("***********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************")
print("*************************************\n***********************************\n\n" + Style.RESET_ALL)

paramiko.util.log_to_file("filename.log")
today = datetime.date.today()

def get_ssh(server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username=username, password=password)

    return ssh

def get_file(ssh, filename):
    ftp_client=ssh.open_sftp()
    ftp_client.get(filename, filename)
    ftp_client.close()
    
    del ftp_client

print("\nEnter server names: ")
servers = []
while True:
    server = raw_input()
    if server == "":
        break
    servers.append(server)

username = raw_input("Username: ")
password = getpass.getpass()
filename = raw_input("File Name to get: ")

start_time = time.time()
for server in servers:
    print(server)
    try:
        ssh = get_ssh(server, username, password)
        get_file(ssh, filename)

        ssh.close()
        del ssh
    except Exception as exc:
        print(exc)
        print("Issue logging into " + server)

print("--- %s seconds ---" % (time.time() - start_time))
