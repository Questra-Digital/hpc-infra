from flask import Flask, jsonify
from kubernetes import client, config

app = Flask(__name__)

def get_helm_managed_deployments():
    try:
        # Load the Kubernetes configuration from the default location or kubeconfig file
        config.load_incluster_config()

        # Create an instance of the Kubernetes API client for deployments
        api_instance = client.AppsV1Api()

        # Get deployments with the specified label selector
        deployments = api_instance.list_deployment_for_all_namespaces(label_selector='app.kubernetes.io/managed-by=Helm')

        # Use a set to keep track of unique namespace names
        unique_namespaces = set()

        # Collect unique namespace names
        for deployment in deployments.items:
            unique_namespaces.add(deployment.metadata.namespace)

        # Convert set to list for JSON serialization
        unique_namespaces_list = list(unique_namespaces)

        return {'namespaces': unique_namespaces_list}

    except Exception as e:
        return {'error': str(e)}
    

@app.route('/')
def hello_world():
    return 'Hello, World! This is a simple Flask server.'

@app.route('/helm_managed_deployments')
def helm_managed_deployments():
    return get_helm_managed_deployments()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
