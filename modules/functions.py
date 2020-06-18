import json
import boto3
from collections import defaultdict
import pprint
import datetime
from pkg_resources import resource_filename

def main( ):
        
    ans=True
    while ans:
        print("""
        1.Listado de instancias de EC2 segun estado.
        2.Listado de instancias de db (RDS) segun estado.
        3.Listado de grupos de auto-escalado con desired>0.

        4.Listado de balanceadores de carga.
        5.Listado de grupos de auto-escalado creados.
        6.Listado de IPs elasticas (que no esten conectadas a instancias)
        7.Listado de instancias de EC2.
        8.Listado de instancias de db (RDS).
        9.Listado de buckets S3.
        10.Listado de funciones lambda.

        11.Listado de servicios desplegados.
        12. Quit
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
            print_pretty(getAutoScalingGroupsByDesiredCapacity(region))
        elif ans==4:
            print_pretty(getElasticLoadBalancers(region))
        elif ans==5:
            print_pretty(getAutoScalingGroups(region))
        elif ans==6:
            print_pretty(getElasticIP(region,"false"))
        elif ans==7:
            print_pretty(getAllInstancesEC2(region))
        elif ans==8:
            print_pretty(getAllInstancesRDS(region))
        elif ans==9:
            print_pretty(getBuckets(region))
        elif ans==10:
            print_pretty(getLambda(region))
        elif ans==11:
            print_pretty(getNumberServices(region))
        elif ans ==12:
            ans = None
        else:
            print("\n Opcion incorrecta")


def myconverter(o):
 if isinstance(o, datetime.datetime):
    return o.__str__()

def print_pretty(response):
    pp = pprint.PrettyPrinter()
    pp.pprint(response)

def getInfoInstanceEC2(instance,owner,regionName):

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

    print_instance = { "Id" : InstanceId, "Type" : InstanceType , "State" : State,
     "Private IP" : PrivateIpAddress,"Public IP" : PublicIpAddress, "Launch time" : LaunchTime,
      "Owner": owner, "Region name" : regionName }
    return print_instance

def getInfoElasticLoadBalancer(elb,regionName):
    
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

    if 'Type' in elb:
        Type=elb['Type']
    else:
        Type='classic'

    print_instance = { "LoadBalancerName" : LoadBalancerName, "DNSName" : DNSName , "State" : State,
     "CreatedTime" : CreatedTime, "Type" : Type, "Region name" : regionName }

    return print_instance

def getInfoInstanceRDS(dbinstance,regionName):

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

    if 'MasterUsername' in dbinstance:
        MasterUsername=dbinstance['MasterUsername']
    else:
        MasterUsername=''
    
    print_instance = { "DBInstanceIdentifierId" : DBInstanceIdentifier,
    "DBInstanceClass" : DBInstanceClass , "DBInstanceStatus" : DBInstanceStatus,
     "Engine" : Engine, "Intance Create Time" : InstanceCreateTime,
     "MasterUsername" : MasterUsername, "Region name" : regionName }
    return print_instance

def getInfoElasticIP(elasticip,regionName):

    if 'InstanceId' in elasticip:
        InstanceId=elasticip['InstanceId']
    else:
        InstanceId=''
   
    if 'AllocationId' in elasticip:
        AllocationId=elasticip['AllocationId']
    else:
        AllocationId=''

    if 'PrivateIpAddress' in elasticip:
        PrivateIpAddress=elasticip['PrivateIpAddress']
    else :
        PrivateIpAddress=''
    
    if 'PublicIp' in elasticip:
        PublicIp=elasticip['PublicIp']
    else :
        PublicIp=''

    print_elasticip = { "InstanceId" : InstanceId, "PublicIp" : PublicIp, "PrivateIpAddress" : PrivateIpAddress,
     "Region name" : regionName}
    return print_elasticip

def getInfoAutoScalingGroups(asg, regionName):

    if 'AutoScalingGroupName' in asg:
        AutoScalingGroupName=asg['AutoScalingGroupName']
    else:
        AutoScalingGroupName=''

    if 'DesiredCapacity' in asg:
        DesiredCapacity=asg['DesiredCapacity']
    else:
        DesiredCapacity=''


    if 'MinSize' in asg:
        MinSize=asg['MinSize']
    else:
        MinSize=''

    if 'MaxSize' in asg:
        MaxSize=asg['MaxSize']
    else:
        MaxSize=''

    if 'AvailabilityZones' in asg:
        AvailabilityZones=asg['AvailabilityZones']
    else:
        AvailabilityZones=''

    if 'CreatedTime' in asg:
        CreatedTime=json.dumps(asg['CreatedTime'],default = myconverter)
    else:
        CreatedTime=''


    print_asg = { "AutoScalingGroupName" : AutoScalingGroupName , 
    "AvailabilityZones" : AvailabilityZones, "CreatedTime" : CreatedTime, 
    "DesiredCapacity" : DesiredCapacity, "MinSize": MinSize, "MaxSize": MaxSize,
    "Region name" : regionName }
    return print_asg

def getInfoLambda (lamb, regionName):

    if 'FunctionName' in lamb:
        FunctionName=lamb['FunctionName']
    else:
        FunctionName=''

    if 'CodeSize' in lamb:
        CodeSize=lamb['CodeSize']
    else:
        CodeSize=''


    if 'LastModified' in lamb:
        LastModified=lamb['LastModified']
    else:
        LastModified=''

    if 'Runtime' in lamb:
        Runtime=lamb['Runtime']
    else:
        Runtime=''

    if 'MemorySize' in lamb:
        MemorySize=lamb['MemorySize']
    else:
        MemorySize=''

    print_lamb = { "FunctionName" : FunctionName , 
    "CodeSize" : CodeSize, "LastModified" : LastModified,
    "Runtime" : Runtime, 'MemorySize':MemorySize, "Region name" : regionName }
    return print_lamb

def getAllInstancesEC2(region):
    list_instances = []
    regionName = get_region_name(region)

    ec2 = boto3.client('ec2',region_name=region)
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                owner = ''
                if ('Tags' in instance):
                    for tag in instance['Tags']:
                        if 'owner' in tag['Key']:
                            owner = tag['Value']
                list_instances.append(getInfoInstanceEC2(instance,owner,regionName))

    except:
        print("An exception occurred")

    return list_instances     
                
def getBuckets(region):
    list_buckets = []
    s3 = boto3.resource('s3',region_name=region)
    
    try:
        for bucket in s3.buckets.all():
            list_buckets.append(bucket.name)
            
    except:
        print("An exception occurred")
    
    return list_buckets

def getInstancesByStateEC2(region,state):
    list_instances = []
    regionName = get_region_name(region)

    ec2 = boto3.client('ec2',region_name=region)
    
    try:
        response = ec2.describe_instances(
            Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    state
                ]
            }
            ]
        )
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                owner = ''
                for tag in instance['Tags']:
                    if 'owner' in tag['Key']:
                        owner = tag['Value']
                        list_instances.append(getInfoInstanceEC2(instance,owner,regionName))
    except:
        print("An exception occurred")

    return list_instances

def getAllInstancesRDS(region):
    list_databases = []
    regionName = get_region_name(region)

    rds = boto3.client('rds',region_name=region)
    
    try:
        response = rds.describe_db_instances()
        for dbinstance in response['DBInstances']:
            list_databases.append(getInfoInstanceRDS(dbinstance,regionName))
    except:
        print("An exception occurred")

    return list_databases

def getInstancesByStateRDS(region,state):
    list_databases = []
    regionName = get_region_name(region)

    rds = boto3.client('rds',region_name=region)
    
    try:
        response = rds.describe_db_instances()
        for dbinstance in response['DBInstances']:
            if (dbinstance['DBInstanceStatus'] == state):
                list_databases.append(getInfoInstanceRDS(dbinstance,regionName))
    except:
        print("An exception occurred")

    return list_databases

def getElasticLoadBalancers(region):
    list_elbalancers = []
    regionName = get_region_name(region)
    
    elb = boto3.client('elb',region_name=region)
    elbv2 = boto3.client('elbv2',region_name=region)
    
    try:
        response = elb.describe_load_balancers()
        for elbalancer in response['LoadBalancerDescriptions']:
            list_elbalancers.append(getInfoElasticLoadBalancer(elbalancer,regionName))
        
        response = elbv2.describe_load_balancers()
        for elbalancer in response['LoadBalancers']:
            list_elbalancers.append(getInfoElasticLoadBalancer(elbalancer,regionName))
        
    except:
        print("An exception occurred")

    return list_elbalancers
    
def getAutoScalingGroups(region):
    list_autoscaling = []
    regionName = get_region_name(region)

    autoscaling = boto3.client('autoscaling',region_name=region)
    
    try:
        response = autoscaling.describe_auto_scaling_groups()
        for asg in response['AutoScalingGroups']:
            list_autoscaling.append(getInfoAutoScalingGroups(asg,regionName))

    except:
        print("An exception occurred")

    return list_autoscaling

def getAutoScalingGroupsByDesiredCapacity(region):
    list_autoscaling = []
    regionName = get_region_name(region)

    autoscaling = boto3.client('autoscaling',region_name=region)
    
    try:
        response = autoscaling.describe_auto_scaling_groups()
        for asg in response['AutoScalingGroups']:
            if (int(asg['DesiredCapacity']) > 0 ):
                list_autoscaling.append(getInfoAutoScalingGroups(asg,regionName))

    except:
        print("An exception occurred")

    return list_autoscaling

def getElasticIP(region,isEmpty):
    list_elasticIP = []
    regionName = get_region_name(region)

    ec2 = boto3.client('ec2',region_name=region)

    try:
        response = ec2.describe_addresses()
        for eIP in response['Addresses']:
            if (isEmpty == "true"):
                if (eIP['InstanceId'] == ''): list_elasticIP.append(getInfoElasticIP(eIP,regionName))
            else:
                list_elasticIP.append(getInfoElasticIP(eIP,regionName))
    
    except:
        print("An exception occurred")

    return list_elasticIP

def getLambda(region):
    list_lambda = []
    regionName = get_region_name(region)

    Lambda = boto3.client('lambda',region_name=region)

    try:
        response = Lambda.list_functions() 
        for fLambda in response['Functions']:
            list_lambda.append(getInfoLambda(fLambda,regionName))
    
    except:
        print("An exception occurred")

    return list_lambda

def getNumberServices(region):
    ec2 = getInstancesByStateEC2(region,"running")
    rds = getInstancesByStateRDS(region,"running")
    autoscaling = getAutoScalingGroupsByDesiredCapacity(region)
    elasticIP = getElasticIP(region,"true")
    elb = getElasticLoadBalancers(region)
    lamb = getLambda(region)

    returned = {
        "ec2" : { "number" : len(ec2), "info" : ec2 },
        "rds" : { "number" : len(rds), "info" : rds },
        "autoscaling" : { "number" : len(autoscaling), "info" : autoscaling },
        "elasticIP" : { "number" : len(elasticIP), "info" : elasticIP },
        "elb" : { "number" : len(elb), "info" : elb },
        "lamb" : { "number" : len(lamb), "info" : lamb }
    }
    return returned

def get_region_name(region_code):
    default_region = 'EU (Ireland)'
    endpoint_file = resource_filename('botocore', 'data/endpoints.json')
    try:
        with open(endpoint_file, 'r') as f:
            data = json.load(f)
        return data['partitions'][0]['regions'][region_code]['description']
    except IOError:
        return default_region



if __name__=="__main__":
    main()
