# Deploy to EKS with Lambda from CodePipeline

This expects your deployment.yml and service.yml in a S3 bucket.
### Required Environment Variables

| Environment Variable | Value                                      |
|----------------------|--------------------------------------------|
| CLUSTER_NAME         | Name of your EKS Cluster                   |
| BUCKET_NAME          | Bucket where your deployment files exist   |
| KUBECONF             | /tmp/config                                |

### Required Role

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: lambda-access
  namespace: default
rules:
- apiGroups: ["extensions", ""]
  resources: ["pods", "deployments", "services"]
  verbs: ["get", "watch", "list", "update", "patch", "create"]
```

### Required Role Binding

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: lambda-user-role-binding
  namespace: default
subjects:
- kind: User
  name: lambda
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: lambda-access
  apiGroup: rbac.authorization.k8s.io
```

### Apply the role and role binding

```bash
kubectl apply -f ./role.yml
kubectl apply -f ./rolebinding.yml
```

### PS: The function is currently written to get input parameters like namespace, deployment file name and service file name from CodePipeline execution. You can modify it to suit your needs.


### Thanks to @alemf90 for his `eks-lambda-python` project without which this wouldn't have been possible.