import boto3

print("\nEnter instance ids:")
ids = []
while True:
    id = input()
    if id == "":
        break
    ids.append(id)
    
ec2 = boto3.resource('ec2')
for ins in ec2.instances.filter(InstanceIds=ids):
    print(ins.metadata_options['HttpTokens'])