import boto3
import time
import csv
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

num = int(input("Enter number of images: "))
print("Enter {num} image ids below:".format(num=num))
images = [input() for i in range(num)]

ec2 = boto3.client('ec2')
snapshots = ec2.describe_snapshots()['Snapshots']

data = []
for image in images:
    try:
        ec2.deregister_image(ImageId=image)
        print("====================\nDeregistering {image}\n====================".format(image=image))
    except:
        print("Ami " + image + " not found!!")
    snap_size = 0
    snap_count = 0
    for snapshot in snapshots:
        if snapshot['Description'].find(image) > 0:
            ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            print("Deleting snapshot {snapshot} \n".format(snapshot=snapshot['SnapshotId']))
            snap_size += snapshot['VolumeSize']
            snap_count += 1
            
    data.append({'AMI Id':image,'SNAPSHOT Count':snap_count, 'SNAPSHOT Size (in GB)':snap_size})

file_name = 'Deleted data.csv'
fields = ['AMI Id','SNAPSHOT Count', 'SNAPSHOT Size (in GB)']
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