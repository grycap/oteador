# Oteador

Oteador is a Integrated Serverless Platform for Global AWS Monitoring.

## Introduction

Oteador is a tool that provides fast cost-effective insights on the use of an AWS services. It consists of:

* A serverless back-end composed of an [AWS Lambda](https://aws.amazon.com/lambda) makes a real-time query of [Amazon AWS](https://aws.amazon.com/es/) services.

* A REST-based service provided by [Amazon API Gateway](https://aws.amazon.com/api-gateway/) (optionally integrated with [Cognito](https://aws.amazon.com/cognito) to manage authentication).

* A Vue.js-based web portal (eventually available in the [cloudtrail-tracker-ui](https://github.com/grycap/cloudtrail-tracker-ui) repository) that queries the REST-based service to visually depict high-level aggregated information concerning the use of resources in AWS by the different users based on the events information. A live site for demo purposes is provided at: [http://cloudtrailtracker.cursocloudaws.net](http://cloudtrailtracker.cursocloudaws.net) accesible with user/password `demo` / `demoDem0!`.

## Requirements

The following tools/libraries are required:

- The [serverless](https://serverless.com/) framework.
- The [Boto 3](http://boto3.readthedocs.io/en/latest/) library.

You can install the requirements by issuing on either a GNU/Linux os macOS machine:

```sh
sudo apt-get install python-pip && pip install --upgrade pip
npm install -g serverless
pip install -r requeriments
```
## Local Installation and Deployment on AWS

1. Clone the project with Git or download it:

```sh
git clone https://github.com/grycap/oteador.git
cd oteador
```

2. Edit the `config.yml` file and, at least, specify the right values for the following parameters:

* `role1`: The name of the role that permits execute lambda functions.
* `role2`: The name of the role that permits execute lambda functions.
* `bucket`: The name of the bucket that stores the event logs coming from Oteador.
* `region`: The name of the region of used bucket.


3. Deploy CloudTrailTracker with the serverless platform:

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

Obtain the list of Auto Scalling groups are used.

```sh
curl --url 'https://api.mysite.com/oteador/AutoScallingGroups/region/your-region'
```
