import boto3
from dateutil.parser import parse
import datetime
import csv
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

def older_than_march(date):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    return date_obj < datetime.datetime(2022, 3, 1)

ec2 = boto3.client('ec2', region_name='us-west-1')
ims = ec2.describe_images(Owners=['self'])
snapshots = ec2.describe_snapshots()['Snapshots']

ami_data = []
for im in ims['Images']:
    create_date = im['CreationDate']
    day_old = older_than_march(create_date)
    ami_id = im['ImageId']
    ami_name = im['Name']
    name = ""
    try:
        for tag in im['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
    except:
        name = ""
    
    if day_old and 'awsbackup' not in ami_name.lower():
        
        snap_size = 0
        snap_count = 0
        for snapshot in snapshots:
            if snapshot['Description'].find(ami_id) > 0:
                snap_size += snapshot['VolumeSize']
                snap_count += 1
        
        ami_data.append({'AMI Name':ami_name, 'AMI Id':ami_id,
                                     'SNAPSHOT Count':snap_count, 'SNAPSHOT Size (in GB)':snap_size, 'Creation Date':create_date})
        print(name, ami_name, create_date)
 

file_name = 'Ami data.csv'
fields = ['AMI Name', 'AMI Id', 'Creation Date', 'SNAPSHOT Count', 'SNAPSHOT Size (in GB)']
# writing to csv file 
with open(file_name, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names) 
    writer.writeheader() 
        
    # writing data rows 
    writer.writerows(ami_data) 
print('DataFrame is written to Excel File successfully.\n')
           
print("--- %s seconds ---" % (time.time() - start_time))