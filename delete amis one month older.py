import boto3
import pandas as pd
from dateutil.parser import parse
import datetime
import time
start_time = time.time()

def days_old(date):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days

age = -1
ami_ids = []
ami_names = []
snap_sizes = []
snap_counts = []

for region in ["us-east-1", "us-west-1"]:
    ec2 = boto3.client('ec2', region_name = region)
    ims = ec2.describe_images(Owners=['self'])
    snapshots = ec2.describe_snapshots()['Snapshots']
    
    for im in ims['Images']:
        create_date = im['CreationDate']
        day_old = days_old(create_date)
        ami_id = im['ImageId']
        ami_name = im['Name']
        
        name = ""
        for tag in im['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
        
        if day_old and 'awsbackup' not in ami_name.lower() and "golden" not in ami_name.lower() and not ('do' in ami_name.lower() and 'not' in ami_name.lower() and 'delete' in ami_name.lower()) \
           and "golden" not in name.lower() and not ('do' in name.lower() and 'not' in name.lower() and 'delete' in name.lower()):
    
            print("deleting -> " + ami_id + " - create_date = " + create_date)
            ec2.deregister_image(ImageId=ami_id)
            
            snap_size = 0
            snap_count = 0
            for snapshot in snapshots:
                if snapshot['Description'].find(ami_id) > 0:
                    ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    print("Deleting snapshot {snapshot} \n".format(snapshot=snapshot['SnapshotId']))
                    snap_size += snapshot['VolumeSize']
                    snap_count += 1
            
            ami_ids.append(ami_id)
            ami_names.append(ami_name)
            snap_sizes.append(snap_size)
            snap_counts.append(snap_count)
 
deleted_amis = pd.DataFrame({'AMI Name':ami_names, 'AMI Id':ami_ids,
                             'SNAPSHOT Count':snap_counts, 'SNAPSHOT Size':snap_sizes})

file_name = '/home/AVJ1007/Deleted Ami.csv'
deleted_amis.to_csv(file_name, index=False)  
print('DataFrame is written to Excel File successfully.\n')    
           
print("--- %s seconds ---" % (time.time() - start_time))