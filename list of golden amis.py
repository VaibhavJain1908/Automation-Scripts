import boto3
import csv
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

ec2 = boto3.client('ec2')
ims = ec2.describe_images(Owners=['self'])
snapshots = ec2.describe_snapshots()['Snapshots']

total_snaps = 0
total_snap_size = 0

ami_data = []
for im in ims['Images']:
    create_date = im['CreationDate']
    ami_id = im['ImageId']
    ami_name = im['Name']
    name = ""
    try:
        for tag in im['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
    except:
        name = ""
    
    if 'awsbackup' not in ami_name.lower() and ("golden" in ami_name.lower() or ('not' in ami_name.lower() and 'delete' in ami_name.lower()) \
       or "golden" in name.lower() or ('not' in name.lower() and 'delete' in name.lower()) or 'adhoc' in ami_name.lower() or 'adhoc' in name.lower()):
        
        snap_size = 0
        snap_count = 0
        for snapshot in snapshots:
            if snapshot['Description'].find(ami_id) > 0:
                snap_size += snapshot['VolumeSize']
                snap_count += 1
        
        ami_data.append({'AMI Name':ami_name, 'AMI Id':ami_id,
                                     'SNAPSHOT Count':snap_count, 'SNAPSHOT Size (in GB)':snap_size, 'Creation Date':create_date})
        
        total_snaps += snap_count
        total_snap_size += snap_size
        print(name, ami_name, create_date)
 
ami_data.append({'AMI Name':'Totals', 'SNAPSHOT Count':total_snaps, 'SNAPSHOT Size (in GB)':total_snap_size})

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