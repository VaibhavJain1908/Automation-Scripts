import boto3
import time
import datetime
import warnings
from termcolor import colored

print(colored("\n\n*****************************************************\n***************************************************","blue",attrs=["bold"]))
print(colored("******","blue",attrs=["bold"]) + "##" + colored("********","blue",attrs=["bold"]) + "##" + colored("**********","blue",attrs=["bold"]) + "##" + colored("*******************","blue",attrs=["bold"]))
print(colored("*******","blue",attrs=["bold"]) + "##" + colored("******","blue",attrs=["bold"]) + "##" + colored("***********","blue",attrs=["bold"]) + "##" + colored("*****************","blue",attrs=["bold"]))
print(colored("********","blue",attrs=["bold"]) + "##" + colored("****","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]) + "##"  + colored("***************","blue",attrs=["bold"]))
print(colored("*********","blue",attrs=["bold"]) + "##" + colored("**","blue",attrs=["bold"]) + "##" + colored("*******","blue",attrs=["bold"]) + "##" + colored("****","blue",attrs=["bold"]) + "##" + colored("*************","blue",attrs=["bold"]))
print(colored("**********","blue",attrs=["bold"]) + "####" + colored("*********","blue",attrs=["bold"]) + "##" + colored("**","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]))
print(colored("***********","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]))
print(colored("*************************************\n***********************************\n\n","blue",attrs=["bold"]))

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

print("=========Restarting Instances=========")
instances.reboot()

print("--- %s seconds ---" % (time.time() - start_time))