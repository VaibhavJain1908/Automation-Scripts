import boto3
import csv

ec2 = boto3.client('ec2')
sgs = ec2.describe_security_groups()
data = []
for sg in sgs['SecurityGroups']:
    data.append({})
    data[-1]['Group Name'] = sg['GroupName']
    data[-1]['Port Range'] = ""
    for perm in sg['IpPermissions']:
        try:
            print(perm['FromPort'])
            data[-1]['Port Range'] += str(perm['FromPort']) + " - "
        except:
            print(sg['GroupName'] + "No From Port")
        try:
            print(perm['ToPort'])
            data[-1]['Port Range'] += str(perm['ToPort'])
        except:
            print(sg['GroupName'] + "No To Port")    
        data[-1]['Port Range'] += "\n"
        
file_name = 'Security Group.csv'
fields = ['Group Name', 'Port Range']
# writing to csv file 
with open(file_name, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names) 
    writer.writeheader() 
        
    # writing data rows 
    writer.writerows(data) 
print('DataFrame is written to Excel File successfully.\n')