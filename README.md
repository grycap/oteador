# Oteador

Oteador is a serverless platform for monitoring the allocated resources in an AWS account

## Introduction

Oteador provides fast cost-effective insights on the use of AWS resources. It consists of:

* A serverless back-end composed of an [Amazon API Gateway](https://aws.amazon.com/api-gateway/) REST API that invokes an [AWS Lambda](https://aws.amazon.com/lambda) function that queries the allocated resources from the following [Amazon AWS](https://aws.amazon.com) services: Amazon EC2 (instances, elastic IPs, Auto Scaling groups and load balancers), Amazon S3 (buckets), Amazon RDS (DB instances) and AWS Lambda (functions).

* A REST-based service provided by [Amazon API Gateway](https://aws.amazon.com/api-gateway/) (integrated with [Cognito](https://aws.amazon.com/cognito) to manage authentication).

* A Vue.js-based web portal (integrated in the [cloudtrail-tracker-ui](https://github.com/grycap/cloudtrail-tracker-ui) repository) that queries the REST-based service to visually depict high-level aggregated information concerning the use of resources in AWS by the different users based on the events information. A live site for demo purposes is provided at: [http://cloudtrailtracker.cursocloudaws.net](http://cloudtrailtracker.cursocloudaws.net) accesible with user/password `demo` / `demoDem0!`.

This repository provides the code for the Oteador back-end based on API Gateway and AWS Lambda.
## Requirements

The following tools/libraries are required:

- The [serverless](https://serverless.com/) framework.
- The [Boto 3](http://boto3.readthedocs.io/en/latest/) library.

You can install the requirements by issuing the following commands on either a GNU/Linux or macOS machine:

```sh
sudo apt-get install python-pip && pip install --upgrade pip
npm install -g serverless
pip install -r requeriments.txt
```
## Local Installation and Deployment on AWS

1. Clone the project with Git or download it:

```sh
git clone https://github.com/grycap/oteador.git
cd oteador
```

2. Edit the `config.yml` file and, at least, specify the right values for the following parameters:

* `role`: The ARN of the IAM Role allocated to the created Lambda function.
* `bucket`: The name of the bucket that will be used for the deployment.
* `region`: The name of the region where Oteador will be deployed.


3. Deploy oteador with the serverless framework:

```sh
sls deploy --aws-profile another-aws-profile
```

Notice that if you want to deploy this application with another AWS profile, you should issue:

```sh
sls deploy 
```

## Using Oteador

The REST API provided by the API Gateway endpoint receives the queries. You can query it using `curl` or use web portal [cloudtrail-tracker-ui](https://github.com/grycap/cloudtrail-tracker-ui). Here are some sample commands that use `curl` to query the REST API, assuming the endpoint of the API Gateway is available in `https://api.mysite.com/oteador`:

### List all Buckets S3

Obtain the list of Amazon's S3 buckets are used.

```sh
curl --url 'https://api.mysite.com/oteador/AllBuckets/region/your-region'
```

### List all Instances EC2

Obtain the list of Amazon's EC2 instances are used.

```sh
curl --url 'https://api.mysite.com/oteador/AllInstancesEC2/region/your-region'
```

### List all Instances RDS

Obtain the list of Amazon's RDS instances are used.

```sh
curl --url 'https://api.mysite.com/oteador/AllInstancesRDS/region/your-region'
```

### List all Elastic Load Balancers

Obtain the list of Elastic Load Balancing are used.

```sh
curl --url 'https://api.mysite.com/oteador/ElasticLoadBalancing/region/your-region'
```

### List all Auto Scalling Groups

Obtain the list of Auto Scalling Groups are used.

```sh
curl --url 'https://api.mysite.com/oteador/AutoScallingGroups/region/your-region'
```

### List all Elastic IPs

Obtain the list of Elastic IPs are used.

```sh
curl --url 'https://api.mysite.com/oteador/ElasticIP/region/your-region'
```
