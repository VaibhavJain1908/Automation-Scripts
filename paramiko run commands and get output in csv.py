import paramiko
import getpass
import datetime
import csv
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
data = []

def get_ssh(server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username=username, password=password)

    return ssh

def ssh_func(ssh, server, username, password, commands):
    print("=========")
    
    data.append({'IP Address':server})
    stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"')
    stdin.flush()
    hostname = ""
    for line in stdout.readlines():
        hostname += line.replace("\n", "")

    if hostname == "":  
        stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"', get_pty=True)
        stdin.write(password + '\n')
        stdin.flush()
        i = -1
        for line in stdout.readlines():
            i += 1
            if i==0 or i==1 or "bash: /home/" + username + "/.bashrc: Not a directory" in line or "[sudo] password for " + username + ":" in line:
                continue
            hostname += line.strip()
                  
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            i = -1
            
            data[-1][cmd] = ""
            for line in stdout.readlines():
                i += 1
                if i==0 or i==1 or "bash: /home/" + username + "/.bashrc: Not a directory" in line or "[sudo] password for " + username + ":" in line:
                    continue
                print(line),
                data[-1][cmd] += line.strip().encode('UTF-8')
            
    else:
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.flush()
            
            data[-1][cmd] = ""
            for line in stdout.readlines():
                print(line),
                data[-1][cmd] += line.strip().encode('UTF-8')
                
    data[-1]["Server"] = hostname
    print("=========")

print("\nEnter IP Addresses: ")
servers = []
while True:
    server = raw_input()
    if server == "":
        break
    servers.append(server)

username = raw_input("Username: ")
password = getpass.getpass()

print("\nEnter commands:")
commands = []
while True:
    command = raw_input()
    if command == "":
        break
    commands.append(command)

start_time = time.time()

print("=========")
for server in servers:
    print(server)
    try:
        ssh = get_ssh(server, username, password)
        ssh_func(ssh, server, username, password, commands)

        ssh.close()
        del ssh
    except Exception as exc:
        print(exc)
        print("Issue logging into " + server)
 
file_name = "Output.csv"
fields = ["Server", "IP Address"]
fields.extend(commands)

# writing to csv file 
with open(file_name, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields)
        
    # writing headers (field names)
    writer.writeheader()
        
    # writing data rows 
    writer.writerows(data)
print('\nOutput is written to Excel File successfully.\n')

print("--- %s seconds ---" % (time.time() - start_time))
