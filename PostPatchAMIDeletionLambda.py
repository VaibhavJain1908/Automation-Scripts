import csv
import boto3
from dateutil.parser import parse
import datetime
import time

today = datetime.date.today()
start_time = time.time()

def days_old(date):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days

# Deleted AMI data in Table form
def table(myDict, colList=None):
   
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] if item[col] is not None else '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   output = ""
   for item in myList: output += (formatStr.format(*item)) + "\n"
   return output

age = 29
data = []

def lambda_handler(event, context):
    try:
        total_ami_count = 0
        total_snap_count = 0
        total_snap_size = 0
    
        for region in ["us-east-1"]:
            ec2 = boto3.client('ec2', region_name = region)
            ims = ec2.describe_images(Owners=['self'])
            snapshots = ec2.describe_snapshots()['Snapshots']
            
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
                
                if day_old > age and 'post' in ami_name.lower() and 'patch' in ami_name.lower() and "golden" not in ami_name.lower() and not ('do' in ami_name.lower() and 'not' in ami_name.lower() and 'delete' in ami_name.lower()) \
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
                    
                    total_ami_count += 1
                    total_snap_count += snap_count
                    total_snap_size += snap_size
                    
                    data.append({'AMI Name':ami_name, 'AMI Id':ami_id,
                                                 'SNAPSHOT Count':snap_count, 'SNAPSHOT Size (in GB)':snap_size, 'Creation Date':create_date})
            
        fields = ['AMI Name', 'AMI Id', 'SNAPSHOT Count', 'SNAPSHOT Size (in GB)', 'Creation Date']
        file_name = "Deleted AMI.csv"
        
        # writing to csv file
        with open('/tmp/' + file_name, 'w+') as csvfile: 
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames = fields) 
                
            # writing headers (field names)
            writer.writeheader()
                
            # writing data rows
            writer.writerows(data)
            
        print('\nDataFrame is written to Excel File successfully.\n')
        
        message = "Hi All,\n\nTotal AMIs = " + str(total_ami_count) + "\nTotal Snapshot Count = " + str(total_snap_count) + "\nTotal Snapshot Size = " + str(total_snap_size)

        # Uploading the CSV file to S3
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file('/tmp/' + file_name, 'lw-ami-deletion', 'Dev/PostPatch/' + str(today.year) + '/' + str(today.month).rjust(2, '0') + '/' + str(today.day).rjust(2, '0') + '/' + file_name, ExtraArgs={'ACL': 'bucket-owner-full-control'})
            print('Upload done !!') 

        except Exception as e:
            # Sending SNS notification
            sns_client = boto3.client('sns')
    
            message += "\n\nData could not be uploaded to S3 !!\n\n"
            print("Error : Could not upload file to S3.\n" + str(e))
            
            response = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:891108200673:AMI_Deletion',
                Message=message + table(data),
                Subject="Post Patch AMI Deletion !!",
            )['MessageId']
            
            return response
    
        print("--- %s seconds ---" % (time.time() - start_time))
     
    except Exception as e:
        print(e)
        # Sending SNS notification
        sns_client = boto3.client('sns')
        response = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:891108200673:AMI_Deletion',
                Message='AMIs could not be deleted correctly !!!',
                Subject="Post Patch AMI Deletion !!",
            )['MessageId']
            
        return response
    