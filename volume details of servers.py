import boto3
import time
import csv
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

num = int(input("Enter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
instance_names = [input() for i in range(num)]

data = []

ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters = [{  
    'Name': 'tag:Name',
    'Values': instance_names
    }]
)

for instance in instances:
    data.append({})
    
    for tag in instance.tags:
        if tag["Key"] == "Name":
            data[-1]["Server"] = tag["Value"]
    
    count = 0
    for volume in instance.volumes.all():
        count+=1
        data[-1]["Volume " + str(count)] = "ID = " + volume.id + "\n" + \
                                      "Type = " + volume.volume_type + "\n" + \
                                      "IOPS = " + str(volume.iops)
        for tag in volume.tags:
            data[-1]["Volume " + str(count)] += "\n" + tag["Key"] + " = " + tag["Value"]
        
fields = ['Server']
fields.extend(["Volume " + str(i) for i in range(1, 21)])
file_name = "Volume data.csv"

# writing to csv file
with open(file_name, 'w') as csvfile: 
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names)
    writer.writeheader()
        
    # writing data rows
    writer.writerows(data)
    
    
print('\nDataFrame is written to Excel File successfully.\n')
    
print("--- %s seconds ---" % (time.time() - start_time))