## Step 1 - Kubernetes Workload Health

##### ----> kubectl get all -n radiant-petclinic

![alt text](image-3.png)

#### ----> kubectl get pods -n radiant-petclinic -o wide

![alt text](image-2.png)

#### ----> kubectl describe deployment radiant-petclinic-deployment -n radiant-petclinic

![alt text](image-4.png)


## Step 2 - Ingress Validation

#### ----> kubectl get ingress -n radiant-petclinic

![alt text](image-5.png)

#### ----> curl -I http://radiant-petclinic.local

![alt text](image-6.png)

#### Evidence:

- Ingress exists
- HTTP 200 response
- Application accessible

## Step 3 - HPA Validation

#### ----> kubectl get hpa -n radiant-petclinic
#### ----> kubectl describe hpa radiant-petclinic-hpa -n radiant-petclinic

![alt text](image-7.png)

## Step 4 - PDB Validation

#### ----> kubectl get pdb -n radiant-petclinic
#### ----> kubectl describe pdb radiant-petclinic-pdb -n radiant-petclinic

![alt text](image-8.png)




