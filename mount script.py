import subprocess

process = subprocess.Popen(['sh', '-c', '"cat /etc/fstab"'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out1 = process.communicate()[0]

text = []

with open("/etc/fstab", "r") as f:
    
    for line in f.readlines():
        words = line.split()
        
        if "/dev/shm" in words:
            words[3] = "defaults,noexec,nodev,nosuid 0 0"
            words[4] = ""
            words[5] = ""
        
        elif "/tmp" in words:
            words[3] = "defaults,rw,nosuid,nodev,noexec,relatime 0 0"
            words[4] = ""
            words[5] = ""
            
        elif "/var" in words:
            words[3] = "rw,relatime 0 0"
            words[4] = ""
            words[5] = ""
            
        elif "/var/tmp" in words:
            words[3] = "rw,nosuid,nodev,noexec,relatime 0 0"
            words[4] = ""
            words[5] = ""
            
        elif "/var/log/audit" in words:
            words[3] = "rw,relatime 0 0"
            words[4] = ""
            words[5] = ""
            
        elif "/var/log" in words:
            words[3] = "rw,nosuid,nodev,noexec,relatime 0 0"
            words[4] = ""
            words[5] = ""
            
        elif "/home" in words:
            words[3] = "rw,nodev,relatime 0 0"
            words[4] = ""
            words[5] = ""
            
        line = " ".join(words)
        text.append(line+"\n")
        
with open("/etc/fstab", "w") as f:
    f.writelines(text)
    
process = subprocess.Popen(['sh', '-c', 'cat /etc/fstab'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
print(process.communicate()[0])

process = subprocess.Popen(['sh', '-c', 'systemctl restart sssd.service'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
print(process.communicate()[0])