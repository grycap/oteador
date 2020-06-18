import os , sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from modules import functions

def handler(event, context):
    if "service" not in event:
        if event.get('region'):
            return action("getNumberServices",event.get('region'))

    elif event['service'] == "AllBuckets":
        return action("AllBuckets",event.get('region'))

    elif event['service'] == 'AllInstancesEC2':
        return action("AllInstancesEC2",event.get('region'))

    elif event['service'] == 'AllInstancesRDS':
        return action("AllInstancesRDS",event.get('region'))

    elif event['service'] == 'InstancesByStateEC2':
      if event.get('state'):
        return action("InstancesByStateEC2",event.get('region'),event.get('state'))

    elif event['service'] == 'InstancesByStateRDS':
      if event.get('state'):
          return action("InstancesByStateRDS",event.get('region'),state=event.get('').get('state'))

    elif event['service'] == 'ElasticLoadBalancing':
        return action("ElasticLoadBalancing",event.get('region'))

    elif event['service'] == 'AutoScalingGroups':
        return action("AutoScalingGroups",event.get('region'))

    elif event['service'] == 'ElasticIP':
        return action("ElasticIP",event.get('region'))

    elif event['service'] == 'Lambda':
        return action("Lambda",event.get('region'))

    else: 
        return 'No accion'
 
  
def action(method, region, state=None):
    
    consulta = ""
    if method == "getNumberServices":
        consulta = functions.getNumberServices(region)
        
    if method == "AllBuckets":
        consulta = functions.getBuckets(region)

    elif method == "AllInstancesEC2":
        consulta = functions.getAllInstancesEC2(region)

    elif method == "AllInstancesRDS":
        consulta = functions.getAllInstancesRDS(region)

    elif method == "InstancesByStateEC2":
        consulta = functions.getInstancesByStateEC2(region,state)

    elif method == "InstancesByStateRDS":
        consulta = functions.getInstancesByStateRDS(region,state)

    elif method == "ElasticLoadBalancing":
        consulta = functions.getElasticLoadBalancers(region)

    elif method == "AutoScalingGroups":
        consulta = functions.getAutoScalingGroups(region)

    elif method == "ElasticIP":
        consulta = functions.getElasticIP(region,"false")

    elif method == "Lambda":
        consulta = functions.getLambda(region)
           
    response = consulta
        
    return response


if __name__ == '__main__':
    #event = { "service": "InstancesByStateEC2", "state" : "stopped"}
    event = { "region" : "us-east-1"}
    res = handler(event, None)
    functions.print_pretty(res)
