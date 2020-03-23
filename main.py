from kubernetes import client, config
import yaml
import boto3
import os.path
import base64
import boto3
import string
import json
import random
from botocore.signers import RequestSigner
from os import path

class EKSAuth(object):

    METHOD = 'GET'
    EXPIRES = 60
    EKS_HEADER = 'x-k8s-aws-id'
    EKS_PREFIX = 'k8s-aws-v1.'
    STS_URL = 'sts.amazonaws.com'
    STS_ACTION = 'Action=GetCallerIdentity&Version=2011-06-15'

    def __init__(self, cluster_id, region='us-east-1'):
        self.cluster_id = cluster_id
        self.region = region
    
    def get_token(self):
        """
        Return bearer token
        """
        session = boto3.session.Session()
        #Get ServiceID required by class RequestSigner
        client = session.client("sts",region_name=self.region)
        service_id = client.meta.service_model.service_id

        signer = RequestSigner(
            service_id,
            session.region_name,
            'sts',
            'v4',
            session.get_credentials(),
            session.events
        )

        params = {
            'method': self.METHOD,
            'url': 'https://' + self.STS_URL + '/?' + self.STS_ACTION,
            'body': {},
            'headers': {
                self.EKS_HEADER: self.cluster_id
            },
            'context': {}
        }

        signed_url = signer.generate_presigned_url(
            params,
            region_name=session.region_name,
            expires_in=self.EXPIRES,
            operation_name=''
        )

        return (
            self.EKS_PREFIX +
            base64.urlsafe_b64encode(
                signed_url.encode('utf-8')
            ).decode('utf-8')
        )


# Configure your cluster name and region here
KUBE_FILEPATH = '/tmp/config'
CLUSTER_NAME = os.environ('CLUSTER_NAME')
REGION = os.environ('AWS_REGION')
s3 = boto3.client('s3')
code_pipeline = boto3.client('codepipeline')
bucket_name = os.environ['BUCKET_NAME']
# We assuem that when the Lambda container is reused, a kubeconfig file exists.
# If it does not exist, it creates the file.

if not os.path.exists(KUBE_FILEPATH):
    
    kube_content = dict()
    # Get data from EKS API
    eks_api = boto3.client('eks',region_name=REGION)
    cluster_info = eks_api.describe_cluster(name=CLUSTER_NAME)
    certificate = cluster_info['cluster']['certificateAuthority']['data']
    endpoint = cluster_info['cluster']['endpoint']

    # Generating kubeconfig
    kube_content = dict()
    
    kube_content['apiVersion'] = 'v1'
    kube_content['clusters'] = [
        {
        'cluster':
            {
            'server': endpoint,
            'certificate-authority-data': certificate
            },
        'name':'kubernetes'
                
        }]

    kube_content['contexts'] = [
        {
        'context':
            {
            'cluster':'kubernetes',
            'user':'aws'
            },
        'name':'aws'
        }]

    kube_content['current-context'] = 'aws'
    kube_content['kind'] = 'Config'
    kube_content['users'] = [
    {
    'name':'aws',
    'user':'lambda'
    }]

    print(kube_content)
    # Write kubeconfig
    with open(KUBE_FILEPATH, 'w') as outfile:
        yaml.dump(kube_content, outfile, default_flow_style=False)

def handler(event, context):
    
    cplJobId = event['CodePipeline.job']['id']
    var = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
    var = json.loads(var)
    deployment_name=var["deployment_name"]
    service_name=var["service_name"]
    namespace=var["namespace"]
    
    deployment_file=var["deployment_file"]
    service_file=var=["service_file"]

    s3.download_file(bucket_name,deployment_file,'/tmp/deployment.yml')
    s3.download_file(bucket_name,service_file,'/tmp/service.yml')
    # Get Token
    eks = EKSAuth(CLUSTER_NAME)
    token = eks.get_token()
    # Configure
    config.load_kube_config()
    configuration = client.Configuration()
    configuration.api_key['authorization'] = token
    configuration.api_key_prefix['authorization'] = 'Bearer'
    # API
    api = client.ApiClient(configuration)
    v1 = client.CoreV1Api(api)
    
    # Get all the pods

    try:
        with open(path.join(path.dirname(__file__), "/tmp/deployment.yml")) as f:
            dep = yaml.load(f)
            k8s_beta = client.ExtensionsV1beta1Api()
            try:
                resp = k8s_beta.patch_namespaced_deployment(name=deployment_name, body=dep, namespace=namespace)
                print("Deployment created. status='%s'" % str(resp.status))
            except:
                resp = k8s_beta.create_namespaced_deployment(body=dep, namespace=namespace)
                print("Deployment created. status='%s'" % str(resp.status))

        with open(path.join(path.dirname(__file__), "/tmp/service.yml")) as f:
            dep = yaml.load(f)
            try:
                resp = v1.patch_namespaced_service(name=service_name, body=dep, namespace=namespace)
                print("Service created. status='%s'" % str(resp.status))
            except:
                resp = v1.create_namespaced_service(name=service_name, body=dep, namespace=namespace)
                print("Service created. status='%s'" % str(resp.status))

        
        code_pipeline.put_job_success_result(jobId=cplJobId)
        return 'Success'
    except Exception as e:
        code_pipeline.put_job_failure_result(jobId=cplJobId, failureDetails={'message': 'Job Failed', 'type': 'JobFailed'})
        print(e)
        raise e

