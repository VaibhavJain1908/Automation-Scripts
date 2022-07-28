import boto3

num = int(input("Enter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
instance_names = [input() for i in range(num)]

ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters = [{  
    'Name': 'tag:Name',
    'Values': instance_names
    }]
)

for instance in instances:
    for tag in instance.tags:
        if tag["Key"] == "Name":
            print(tag["Value"] + '\t' + instance.id)
            break