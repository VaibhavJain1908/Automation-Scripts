import boto3
from dateutil.parser import parse
import datetime
import csv
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

def days_old(date):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days

ec2 = boto3.client('ec2', region_name='us-west-1')
ims = ec2.describe_images(Owners=['self'])
snapshots = ec2.describe_snapshots()['Snapshots']

ami_data = []
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
    
    if 'awsbackup' not in ami_name.lower() and "golden" not in ami_name.lower() and not ('not' in ami_name.lower() and 'delete' in ami_name.lower()) \
       and "golden" not in name.lower() and not ('not' in name.lower() and 'delete' in name.lower()) and 'adhoc' not in ami_name.lower() and 'adhoc' not in name.lower():
        
        if (day_old > 6 and "pre" in ami_name.lower()) or (day_old > 29 and "post" in ami_name.lower()):
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