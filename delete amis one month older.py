# Importing Compulsory Python Libraries
import boto3
import csv
from dateutil.parser import parse
import datetime
import time

# Calculating Age of AMIs
def days_old(date):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days

# Reading Account IDS and IAM Roles from the user
num = int(input("Enter number of account: "))
print("Enter {num} account ids below:".format(num=num))
account_ids = [input() for i in range(num)]

print("\nEnter {num} iam roles below:".format(num=num))
iam_roles = [input() for i in range(num)]

print("\nStarting the process . . .\n")
# Calculating Time to execute the whole program
start_time = time.time()

age = 29
data = []

# Traversing through Accounts
client = boto3.client('sts')
for i in range(len(iam_roles)):
    role_object = client.assume_role(
        RoleArn = 'arn:aws:iam::{account_id}:role/{iam_role}'.format(account_id=account_ids[i], iam_role=iam_roles[i]),
        RoleSessionName = '{iam_role}-session'.format(iam_role=iam_roles[i]))
    
    temp_credentials = role_object['Credentials']
    
    session = boto3.session.Session(
        aws_access_key_id = temp_credentials['AccessKeyId'],
        aws_secret_access_key = temp_credentials['SecretAccessKey'],
        aws_session_token = temp_credentials['SessionToken'], )
    
    # Traversing the regions (If there are only one region in an environment, it will go through only one)
    for region in ["us-east-1", "us-west-1"]:
        ec2 = boto3.client('ec2', region_name = region)
        
        # Getting the required AMIs and Snapshots
        ims = ec2.describe_images(Owners=['self'])
        snapshots = ec2.describe_snapshots()['Snapshots']
        
        # Traversing through the AMIs
        for im in ims['Images']:
            create_date = im['CreationDate']
            day_old = days_old(create_date)
            ami_id = im['ImageId']
            ami_name = im['Name']
            
            name = ""
            try:
                for tag in im['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
            except:
                name = ""
            
            # Checking if the AMI is one month older and is a post patch AMI
            if day_old > age and 'post' in ami_name.lower() and 'patch' in ami_name.lower() and "golden" not in ami_name.lower() and not ('do' in ami_name.lower() and 'not' in ami_name.lower() and 'delete' in ami_name.lower()) \
               and "golden" not in name.lower() and not ('do' in name.lower() and 'not' in name.lower() and 'delete' in name.lower()):
        
                # Deregestring one month older post patch AMI
                print("deleting -> " + ami_id + " - create_date = " + create_date)
                ec2.deregister_image(ImageId=ami_id)
                
                snap_size = 0
                snap_count = 0
                
                # Deleting the associated snapshots
                for snapshot in snapshots:
                    if snapshot['Description'].find(ami_id) > 0:
                        ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                        print("Deleting snapshot {snapshot} \n".format(snapshot=snapshot['SnapshotId']))
                        snap_size += snapshot['VolumeSize']
                        snap_count += 1
                
                data.append({'AMI Name':ami_name, 'AMI Id':ami_id,
                                             'SNAPSHOT Count':snap_count, 'SNAPSHOT Size (in GB)':snap_size, 'Creation Date':create_date})
        
file_name = 'Deleted data.csv'
fields = ['AMI Name', 'AMI Id', 'Creation Date', 'SNAPSHOT Count', 'SNAPSHOT Size (in GB)']

# writing to csv file 
with open(file_name, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names) 
    writer.writeheader() 
        
    # writing data rows 
    writer.writerows(data) 
print('DataFrame is written to Excel File successfully.\n')    
           
print("--- %s seconds ---" % (time.time() - start_time))