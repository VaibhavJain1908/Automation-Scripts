import paramiko
import getpass
import datetime
import time
import warnings
warnings.filterwarnings("ignore")

paramiko.util.log_to_file("filename.log")
today = datetime.date.today()

def get_ssh(server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username=username, password=password)

    return ssh

def ssh_func(ssh, server, username, password, commands):
    print("=========")

    stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"')
    stdin.flush()
    hostname = ""
    for line in stdout.readlines():
        hostname += line.replace("\n", "")

    for cmd in commands:
        print(hostname + ":~ # " + cmd)
        stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
        stdin.flush()

        for line in stdout.readlines():
            print(line),

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

print("--- %s seconds ---" % (time.time() - start_time))

