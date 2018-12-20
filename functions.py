import json
import boto3
from collections import defaultdict
import pprint
import datetime

def main( ):
    
    ans=True
    while ans:
        print("""
        1.Listado de instancias de EC2 segun estado.
        2.Listado de instancias de db (RDS) segun estado.
        3.Listado de balanceadores de carga.
        4.Listado de grupos de auto-escalado creados.
        5.Listado de IPs elasticas (que no esten conectadas a instancias)
        6.Listado de instancias de EC2.
        7.Listado de instancias de db (RDS).
        8.Quit
        """)
        ans=input("Elige una opcion: ")
        if ans=="1":
            state=input("Estado (running,stopped,..): ")
            getInstancesByStateEC2(state)
        elif ans=="2":
            state=input("Estado (running,terminated,..): ")
            getInstancesByStateRDS(state)
        elif ans=="3":
            getElasticLoadBalancing()
        elif ans=="4":
            getAutoScallingGroups()
        elif ans=="5":
            getElasticIP()
        elif ans=="6":
            getAllInstancesEC2()
        elif ans=="7":
            getAllInstancesRDS()
        elif ans=="8":
            ans = None
        else:
            print("\n Opcion incorrecta")


def myconverter(o):
 if isinstance(o, datetime.datetime):
    return o.__str__()

def print_pretty(response):
    pp = pprint.PrettyPrinter()
    pp.pprint(response)

def getInfoInstanceEC2(instance,owner):

    if 'InstanceId' in instance:
        InstanceId=instance['InstanceId']
    else :
        InstanceId=''

    if 'InstanceType' in instance:
        InstanceType=instance['InstanceType']
    else :
        InstanceType=''

    if 'State' in instance:
        State=instance['State']['Name']
    else :
        State=''

    if 'PrivateIpAddress' in instance:
        PrivateIpAddress=instance['PrivateIpAddress']
    else :
        PrivateIpAddress=''
    
    if 'PublicIpAddress' in instance:
        PublicIpAddress=instance['PublicIpAddress']
    else :
        PublicIpAddress=''

    if 'LaunchTime' in instance:
        LaunchTime=json.dumps(instance['LaunchTime'],default = myconverter)
    else :
        LaunchTime=''

    print_instance = { "Id:" : InstanceId, "Type" : InstanceType , "State" : State, "Private IP" : PrivateIpAddress,"Public IP" : PublicIpAddress, "Launch time" : LaunchTime, "Owner": owner }
    return print_instance

def getInfoInstanceRDS(dbinstance):

    if 'DBInstanceIdentifier' in dbinstance:
        DBInstanceIdentifier=dbinstance['DBInstanceIdentifier']
    else :
        DBInstanceIdentifier=''

    if 'DBInstanceClass' in dbinstance:
        DBInstanceClass=dbinstance['DBInstanceClass']
    else :
        DBInstanceClass=''

    if 'DBInstanceStatus' in dbinstance:
        DBInstanceStatus=dbinstance['DBInstanceStatus']
    else :
        DBInstanceStatus=''

    if 'Engine' in dbinstance:
        Engine=dbinstance['Engine']
    else :
        Engine=''
    
    print_instance = { "DBInstanceIdentifierId:" : DBInstanceIdentifier, "DBInstanceClass" : DBInstanceClass , "DBInstanceStatus" : DBInstanceStatus, "Engine" : Engine }
    return print_instance

def getInfoElasticIP(elasticip):

    if 'InstanceId' in elasticip:
        return
    
    if 'PrivateIpAddress' in elasticip:
        PrivateIpAddress=elasticip['PrivateIpAddress']
    else :
        PrivateIpAddress=''
    
    if 'PublicIp' in elasticip:
        PublicIp=elasticip['PublicIp']
    else :
        PublicIp=''

    print_instance = { "PrivateIpAddress" : PrivateIpAddress , "PublicIp" : PublicIp}
    return print_instance

def getInfoAutoScallingGroups(asg):

    if 'AutoScalingGroupName' in asg:
        AutoScalingGroupName=asg['AutoScalingGroupName']

    if 'AvailabilityZones' in asg:
        AvailabilityZones=asg['AvailabilityZones']

    if 'CreatedTime' in asg:
        CreatedTime=json.dumps(asg['CreatedTime'],default = myconverter)

    if 'Instances' in asg:
        Instances=asg['Instances']

    print_asg = { "AutoScalingGroupName" : AutoScalingGroupName , "AvailabilityZones" : AvailabilityZones, "CreatedTime" : CreatedTime, "Instances" : Instances }
    return print_asg

def getAllInstancesEC2():
    returned = []
    
    client = boto3.client('ec2')
    response = client.describe_instances()
    reservations = response['Reservations']
    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            owner = ''
            if ('Tags' in instance):
                for tag in instance['Tags']:
                    if 'owner' in tag['Key']:
                        owner = tag['Value']
                    #print(json.dumps(getInfoInstanceEC2(instance,owner),default = myconverter))
            returned.append(getInfoInstanceEC2(instance,owner))
    return returned     
                
def getBuckets():
    returned=[]
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        returned.append(bucket.name)
    return returned
  

def getInstancesByStateEC2(state):
    returned = []
    client = boto3.client('ec2')
    response = client.describe_instances(
        Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                state
            ]
        }
        ]
    )
    reservations = response['Reservations']
    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            owner = ''
            for tag in instance['Tags']:
                if 'owner' in tag['Key']:
                    owner = tag['Value']
                #print(json.dumps(getInfoInstanceEC2(instance,owner),default = myconverter))
                returned.append(getInfoInstanceEC2(instance,owner))
    
    return returned

def getAllInstancesRDS():
    returned = []
    client = boto3.client('rds')
    response = client.describe_db_instances()
    
    dbinstances = response['DBInstances']
    
    for dbinstance in dbinstances:
        #print(json.dumps(getInfoInstanceRDS(dbinstance),default = myconverter))
        returned.append(getInfoInstanceRDS(dbinstance))
    return returned

def getInstancesByStateRDS(state):
    returned = []
    client = boto3.client('rds')
    response = client.describe_db_instances()
    
    dbinstances = response['DBInstances']
    
    for dbinstance in dbinstances:
        if (dbinstance['DBInstanceStatus'] == state): #print(json.dumps(getInfoInstanceRDS(dbinstance),default = myconverter))
            returned.append(getInfoInstanceRDS(dbinstance))
    return returned

def getElasticLoadBalancing():
    returned = []
    client = boto3.client('elb')
    response = client.describe_load_balancers()
    
    list_elb = response['LoadBalancerDescriptions']
    for elb in list_elb:
        print_pretty(elb)
    return returned
    
def getAutoScallingGroups():
    returned = []
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups()

    list_asg = response['AutoScalingGroups']
    for asg in list_asg:
       returned.append(getInfoAutoScallingGroups(asg))
    return returned

def getElasticIP():
    returned = []
    client = boto3.client('ec2')
    response = client.describe_addresses()
    
    list_eIP = response['Addresses']
    for eIP in list_eIP:
        temp = getInfoElasticIP(eIP)
        if (temp): print(json.dumps(temp,default = myconverter))
    return returned

if __name__=="__main__":
    main()