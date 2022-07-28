import glob
import re
file_list = glob.glob("/etc/zypp/repos.d/*")

for filename in file_list:
    data = []
    with open(filename, "r") as f:
        for line in f.readlines():
            result = re.match("gpgcheck=\w+", line)
            if result:
                line = "gpgcheck=1\n"
            data.append(line)
    
    with open(filename, "w") as f:
        f.writelines(data)