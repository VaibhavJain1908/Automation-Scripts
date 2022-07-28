import boto3
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

num = int(input("Enter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
instance_names = [input() for i in range(num)]

client = boto3.client('ec2')
Myec2=client.describe_instances(
    Filters = [{  
    'Name': 'tag:Name',
    'Values': instance_names
    }]
)

for instances in Myec2['Reservations']:
    for instance in instances['Instances']:
        instanceId = instance['InstanceId']
        
        name = ""
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
                break
        
        print("Creating Ami " + name)
        client.create_image(InstanceId=instanceId, Name=name + '_PrePatch', NoReboot=True)
        time.sleep(2)

print("--- %s seconds ---" % (time.time() - start_time))
