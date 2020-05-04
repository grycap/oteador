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
        region = 'us-east-1'
        ans=input("Elige una opcion: ")
        if ans==1:
            state=raw_input("Estado (running,stopped,..): ")
            print_pretty(getInstancesByStateEC2(region,state))
        elif ans==2:
            state=raw_input("Estado (running,terminated,..): ")
            print_pretty(getInstancesByStateRDS(region,state))
        elif ans==3:
            print_pretty(getElasticLoadBalancers(region))
        elif ans==4:
            print_pretty(getAutoScallingGroups(region))
        elif ans==5:
            print_pretty(getElasticIP(region))
        elif ans==6:
            print_pretty(getAllInstancesEC2(region))
        elif ans==7:
            print_pretty(getAllInstancesRDS(region))
        elif ans==8:
            print_pretty(getBuckets(region))
        elif ans==9:
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

def getInfoElasticLoadBalancer(elb):
    
    

    if 'LoadBalancerName' in elb:
        LoadBalancerName=elb['LoadBalancerName']
    else:
        LoadBalancerName=''

    if 'DNSName' in elb:
        DNSName=elb['DNSName']
    else:
        DNSName=''

    if 'State' in elb:
        State=elb['State']['Code']
    else:
        State=''

    if 'CreatedTime' in elb:
        CreatedTime=json.dumps(elb['CreatedTime'],default = myconverter)
    else:
        CreatedTime=''

    print_instance = { "LoadBalancerName:" : LoadBalancerName, "DNSName" : DNSName , "State" : State,
     "CreatedTime" : CreatedTime }
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

    if 'InstanceCreateTime' in dbinstance:
        InstanceCreateTime=json.dumps(dbinstance['InstanceCreateTime'],default = myconverter)
    else :
        InstanceCreateTime=''
    
    print_instance = { "DBInstanceIdentifierId:" : DBInstanceIdentifier, "DBInstanceClass" : DBInstanceClass , "DBInstanceStatus" : DBInstanceStatus, "Engine" : Engine, "Intance Create Time" : InstanceCreateTime }
    return print_instance

def getInfoElasticIP(elasticip):
    if 'InstanceId' in elasticip and elasticip['InstanceId']!='':
        return
    
    if 'PrivateIpAddress' in elasticip:
        PrivateIpAddress=elasticip['PrivateIpAddress']
    else :
        PrivateIpAddress=''
    
    if 'PublicIp' in elasticip:
        PublicIp=elasticip['PublicIp']
    else :
        PublicIp=''

    print_elasticip = {"PublicIp" : PublicIp, "PrivateIpAddress" : PrivateIpAddress}
    return print_elasticip

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

def getAllInstancesEC2(region):
    returned = []
    
    client = boto3.client('ec2',region_name=region)
    try:
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
    except:
        print("An exception occurred")
    return returned     
                
def getBuckets(region):
    returned=[]
    s3 = boto3.resource('s3',region_name=region)
    
    try:
        for bucket in s3.buckets.all():
            returned.append(bucket.name)
    except:
        print("An exception occurred")
    
    return returned

     

def getInstancesByStateEC2(region,state):
    returned = []
    client = boto3.client('ec2',region_name=region)
    
    try:
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
                        returned.append(getInfoInstanceEC2(instance,owner))
    except:
        print("An exception occurred")

    return returned

def getAllInstancesRDS(region):
    returned = []
    client = boto3.client('rds',region_name=region)
    
    try:
        response = client.describe_db_instances()
        dbinstances = response['DBInstances']
        
        for dbinstance in dbinstances:
            print(json.dumps(getInfoInstanceRDS(dbinstance),default = myconverter))
            returned.append(getInfoInstanceRDS(dbinstance))
    except:
        print("An exception occurred")

    return returned

def getInstancesByStateRDS(region,state):
    returned = []
    client = boto3.client('rds',region_name=region)
    
    try:
        response = client.describe_db_instances()
        dbinstances = response['DBInstances']
        
        for dbinstance in dbinstances:
            if (dbinstance['DBInstanceStatus'] == state): #print(json.dumps(getInfoInstanceRDS(dbinstance),default = myconverter))
                returned.append(getInfoInstanceRDS(dbinstance))
    except:
        print("An exception occurred")

    return returned

def getElasticLoadBalancers(region):
    returned = []

    clientElb = boto3.client('elb',region_name=region)
    clientElbv2 = boto3.client('elbv2',region_name=region)
    
    try:
        response = clientElb.describe_load_balancers()
        print_pretty(response)
        list_lb = response['LoadBalancerDescriptions']
        for elb in list_lb:
            returned.append(getInfoElasticLoadBalancer(elb))
        
        response = clientElbv2.describe_load_balancers()
        print_pretty(response)
        list_lbv2 = response['LoadBalancers']
        for elb in list_lbv2:
            returned.append(getInfoElasticLoadBalancer(elb))
        
    except:
        print("An exception occurred")

    return returned
    
def getAutoScallingGroups(region):
    returned = []
    client = boto3.client('autoscaling',region_name=region)
    
    try:
        response = client.describe_auto_scaling_groups()
        list_asg = response['AutoScalingGroups']
        for asg in list_asg:
            returned.append(getInfoAutoScallingGroups(asg))

    except:
        print("An exception occurred")

    return returned

def getElasticIP(region):
    returned = []
    client = boto3.client('ec2',region_name=region)

    try:
        response = client.describe_addresses()
        list_eIP = response['Addresses']
        for eIP in list_eIP:
            temp = getInfoElasticIP(eIP)
            if (temp): returned.append(temp)
    
    except:
        print("An exception occurred")

    return returned

if __name__=="__main__":
    main()
