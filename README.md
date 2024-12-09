### MLFlow Tracking with MLFlow on AWS



## MLflow on AWS Setup:

1. Login to AWS console.
2. Create IAM user with AdministratorAccess
3. Export the credentials in your AWS CLI by running "aws configure"
4. Create a s3 bucket
5. Create EC2 machine (Ubuntu) & add Security groups 5000 port

## Screenshots of MLFlow Experiments Through EC2:

![image](https://github.com/user-attachments/assets/5d5adc3e-166b-487e-8e1a-e5b48281b477)


Run the following command on EC2 machine
```bash
sudo apt update

sudo apt install python3-pip

sudo apt install pipenv

sudo apt install virtualenv

mkdir mlflow

cd mlflow

pipenv install mlflow

pipenv install awscli

pipenv install boto3

pipenv shell


## Then set aws credentials
aws configure


#Finally 
mlflow server -h 0.0.0.0 --default-artifact-root s3:/mlflowtrackings3

#open Public IPv4 DNS to the port 5000


#set uri in your local terminal and in your code 

export MLFLOW_TRACKING_URI = http://ec2-107-21-195-23.compute-1.amazonaws.com:5000/

