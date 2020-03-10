import os , sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from modules import functions

def handler(event, context):
    
    if event['service'] == "AllBuckets":
        return action("AllBuckets")

    elif event['service'] == 'AllInstancesEC2':
        return action("AllInstancesEC2")

    elif event['service'] == 'AllInstancesRDS':
        return action("AllInstancesRDS")

    elif event['service'] == 'InstancesByStateEC2':
      if event.get('state'):
        return action("InstancesByStateEC2",event.get('state'))

    elif event['service'] == 'InstancesByStateRDS':
      if event.get('state'):
          return action("InstancesByStateRDS",state=event.get('').get('state'))

    elif event['service'] == 'ElasticLoadBalancing':
        return action("ElasticLoadBalancing")

    elif event['service'] == 'AutoScallingGroups':
        return action("AutoScallingGroups")

    elif event['service'] == 'ElasticIP':
        return action("ElasticIP")
    else: 
        return 'No accion'
 
  
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
    #event = { "service": "InstancesByStateEC2", "state" : "stopped"}
    event = { "service" : "AllInstancesEC2"}
    res = handler(event, None)
    functions.print_pretty(res)
