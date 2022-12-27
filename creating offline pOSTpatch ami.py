import boto3
import time
import datetime
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

today = datetime.date.today()

num = int(input("Enter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
instance_names = [input() for i in range(num)]

client = boto3.client('ec2')
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters = [{  
    'Name': 'tag:Name',
    'Values': instance_names
    }]
)

print("=========Stopping Instances=========")
instances.stop() 

for instance in instances:
    instanceName = ""
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            instanceName = tag['Value']
            break
    
    instance.wait_until_stopped()
    print("Creating Post Patch AMI for " + instanceName)
    client.create_image(InstanceId=instance.id, Name=instanceName + '_PostPatchWithReboot_' + str(today.day).rjust(2, '0') + str(today.month).rjust(2, '0') + str(today.year))
    time.sleep(2)

print("=========Starting Instances=========")        
instances.start()

print("--- %s seconds ---" % (time.time() - start_time))