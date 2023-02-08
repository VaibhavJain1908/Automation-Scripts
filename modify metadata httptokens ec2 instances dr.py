import subprocess
import boto3
import time
import csv
from termcolor import colored
import warnings
warnings.filterwarnings("ignore")

print(colored("\n\n*****************************************************\n***************************************************","blue",attrs=["bold"]))
print(colored("******","blue",attrs=["bold"]) + "##" + colored("********","blue",attrs=["bold"]) + "##" + colored("**********","blue",attrs=["bold"]) + "##" + colored("*******************","blue",attrs=["bold"]))
print(colored("*******","blue",attrs=["bold"]) + "##" + colored("******","blue",attrs=["bold"]) + "##" + colored("***********","blue",attrs=["bold"]) + "##" + colored("*****************","blue",attrs=["bold"]))
print(colored("********","blue",attrs=["bold"]) + "##" + colored("****","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]) + "##"  + colored("***************","blue",attrs=["bold"]))
print(colored("*********","blue",attrs=["bold"]) + "##" + colored("**","blue",attrs=["bold"]) + "##" + colored("*******","blue",attrs=["bold"]) + "##" + colored("****","blue",attrs=["bold"]) + "##" + colored("*************","blue",attrs=["bold"]))
print(colored("**********","blue",attrs=["bold"]) + "####" + colored("*********","blue",attrs=["bold"]) + "##" + colored("**","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]))
print(colored("***********","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]))
print(colored("*************************************\n***********************************\n\n","blue",attrs=["bold"]))

chnge_num = input("Enter Change Num: ")

print("\nEnter instance ids:")
ids = []
while True:
    id = input()
    if id == "":
        break
    ids.append(id)

data = []

start_time = time.time()

ec2 = boto3.resource('ec2', region_name="us-west-1")
for ins in ec2.instances.filter(InstanceIds=ids):
    data.append({})
    data[-1]['Instance ID'] = ins.id
    data[-1]['HttpTokens(before)'] = ins.metadata_options['HttpTokens']
    for tag in ins.tags:
        if tag['Key'] == 'Name':
            data[-1]['Server'] = tag['Value']
            break

for id in ids:
    
    j = 0
    while True:
        if data[j]['Instance ID'] == id:
            break
        j+=1
    
    process = subprocess.Popen(["sh", "-c", "aws ec2 modify-instance-metadata-options --instance-id {0} --region us-west-1 --http-tokens required".format(id)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print(process.communicate()[0].decode())
    
    time.sleep(2)
    for ins in ec2.instances.filter(InstanceIds=[id]):
        data[j]['HttpTokens(after)'] = ins.metadata_options['HttpTokens']
        print(data[j]['Server'], data[j]['Instance ID'], data[j]['HttpTokens(before)'], ins.metadata_options['HttpTokens'])
        
file_name = chnge_num + "_PIR.csv"
fields = ["Server", "Instance ID", "HttpTokens(before)", "HttpTokens(after)"]

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