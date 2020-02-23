# Oteador

Oteador is a Integrated Serverless Platform for Global AWS Monitoring.

# Introduction

Oteador is a tool that provides fast cost-effective insights on the use of an AWS services. It consists of:

* A serverless back-end composed of an [AWS Lambda](https://aws.amazon.com/lambda) makes a real-time query of [Amazon AWS](https://aws.amazon.com/es/) services.

* A REST-based service provided by [Amazon API Gateway](https://aws.amazon.com/api-gateway/) (optionally integrated with [Cognito](https://aws.amazon.com/cognito) to manage authentication).

* A Vue.js-based web portal (eventually available in the [cloudtrail-tracker-ui](https://github.com/grycap/cloudtrail-tracker-ui) repository) that queries the REST-based service to visually depict high-level aggregated information concerning the use of resources in AWS by the different users based on the events information. A live site for demo purposes is provided at: [http://cloudtrailtracker.cursocloudaws.net](http://cloudtrailtracker.cursocloudaws.net) accesible with user/password `demo` / `demoDem0!`.

## Requirements
The following tools/libraries are required:

- The [serverless](https://serverless.com/) framework.
- The [Boto 3](http://boto3.readthedocs.io/en/latest/) library.
- The [flatten_json](https://pypi.org/project/flatten_json/) library.

You can install the requirements by issuing on either a GNU/Linux os macOS machine:

```sh
sudo apt-get install python-pip && pip install --upgrade pip
npm install -g serverless
pip install -r requeriments
```
