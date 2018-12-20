
import os , sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from modules import functions

def handler(event, context):
    
    if event.get('AllBuckets', None):
        return action("AllBuckets")

    elif event.get('AllInstancesEC2', None):
        return action("AllInstancesEC2")

    elif event.get('AllInstancesRDS', None):
        return action("AllInstancesRDS")

    elif event.get('InstancesByStateEC2', None):
        if ('state' in event.get('InstancesByStateEC2')):
            return action("InstancesByStateEC2",event.get('InstancesByStateEC2').get('state'))

    elif event.get('InstancesByStateRDS', None):
        if ('state' in event.get('InstancesByStateRDS')):
            return action("InstancesByStateRDS",state=event.get('InstancesByStateRDS').get('state'))

    elif event.get('ElasticLoadBalancing', None):
        return action("ElasticLoadBalancing")

    elif event.get('AutoScallingGroups', None):
        return action("AutoScallingGroups")

    elif event.get('ElasticIP', None):
        return action("ElasticIP")

    else return "No acción"
 
  
def action(method, state=None):
    
    consulta = ""

    if method == "AllBuckets":
        consulta = functions.getBuckets()

    elif method == "AllInstancesEC2":
        consulta = functions.getAllInstancesEC2()

    elif method == "AllInstancesRDS":
        consulta = functions.getAllInstancesRDS()

    elif method == "InstancesByStateEC2":
        consulta = functions.getInstancesByStateEC2(state)

    elif method == "InstancesByStateRDS":
        consulta = functions.getInstancesByStateRDS(state)

    elif method == "ElasticLoadBalancing":
        consulta = functions.getElasticLoadBalancing()

    elif method == "AutoScallingGroups":
        consulta = functions.getAutoScallingGroups()

    elif method == "ElasticIP":
        consulta = functions.getElasticIP()
    
    body = {
            "message": "Go Serverless v1.0 ! Your function executed successfully ! ",
            "input": method,
            "response" : consulta
    }
        
    response = {
        "statusCode": 200,
        "body": body
    }
        
    return response


if __name__ == '__main__':
    event = {
        'InstancesByStateEC2' : {
            'state' : 'stopped'
        }
    }
    event = { "AutoScallingGroups": "AutoScallingGroups"}
    res = handler(event, None)
    functions.print_pretty(res)