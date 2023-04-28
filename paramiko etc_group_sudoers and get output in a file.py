import paramiko
import getpass
import datetime
import time
from colorama import Fore
from colorama import Style
import warnings
warnings.filterwarnings("ignore")

paramiko.util.log_to_file("filename.log")
today = datetime.date.today()

print(Fore.BLUE + Style.BRIGHT + "\n\n*****************************************************\n***************************************************")
print("******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "**********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*******************")
print("*******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "***********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*****************")
print("********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "****" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "***************")
print("*********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "**" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*******" + Style.RESET_ALL + "##" +  Fore.BLUE + Style.BRIGHT + "****" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*************")
print("**********" + Style.RESET_ALL + "####" + Fore.BLUE + Style.BRIGHT + "*********" + Style.RESET_ALL + "##" +  Fore.BLUE + Style.BRIGHT + "**" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************")
print("***********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************")
print("*************************************\n***********************************\n\n" + Style.RESET_ALL)

def get_ssh(server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username=username, password=password)

    return ssh

def ssh_func(ssh, server, username, password):
    output.append("=========\n")
    print("=========")
    
    commands = ["date", "cat /etc/group", "cat /etc/passwd", "cat /etc/sudoers"]
    
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
            
        stdin, stdout, stderr = ssh.exec_command('sudo su - -c "ls /etc/sudoers.d"', get_pty=True)
        stdin.write(password + '\n')
        stdin.flush()
        i = -1
        for line in stdout.readlines():
            i += 1
            if i==0 or i==1 or "bash: /home/" + username + "/.bashrc: Not a directory" in line or "[sudo] password for " + username + ":" in line:
                continue
            commands.append("cat /etc/sudoers.d/" + line.strip())
                  
        for cmd in commands:
            output.append(hostname + ":~ # " + cmd + "\n")
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            i = -1
            for line in stdout.readlines():
                i += 1
                if i==0 or i==1 or "bash: /home/" + username + "/.bashrc: Not a directory" in line or "[sudo] password for " + username + ":" in line:
                    continue
                output.append(line)
                print(line),
            
    else:
        stdin, stdout, stderr = ssh.exec_command('sudo su - -c "ls /etc/sudoers.d"', get_pty=True)
        stdin.flush()
        for line in stdout.readlines():
            for filename in line.split():
                commands.append("cat /etc/sudoers.d/" + filename)
        
        for cmd in commands:
            output.append(hostname + ":~ # " + cmd + "\n")
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.flush()
            for line in stdout.readlines():
                output.append(line)
                print(line),

    output.append("=========\n")
    print("=========")
    
output = []

print("\nEnter server names: ")
servers = []
while True:
    server = raw_input()
    if server == "":
        break
    servers.append(server)

username = raw_input("Username: ")
password = getpass.getpass()

start_time = time.time()

output.append("=========\n")

print("=========")
for server in servers:
    output.append(server + "\n")
    print(server)
    try:
        ssh = get_ssh(server, username, password)
        ssh_func(ssh, server, username, password)

        ssh.close()
        del ssh
    except Exception as exc:
        output.append(str(exc) + "\n")
        print(exc)
        output.append("Issue logging into " + server + "\n")
        print("Issue logging into " + server)
        
with open("output.txt", "w") as f:
    f.writelines(output)

print("--- %s seconds ---" % (time.time() - start_time))
