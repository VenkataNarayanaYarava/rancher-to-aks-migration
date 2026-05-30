# Rancher to AKS Cutover Runbook

## Objective

Migrate the Radiant PetClinic application from the existing Rancher-managed Kubernetes environment to Azure Kubernetes Service (AKS) with minimal downtime.

---

## Pre-Cutover Checklist

### Infrastructure Validation

* [ ] AKS cluster deployed and accessible
* [ ] Azure Container Registry (ACR) configured
* [ ] NGINX Ingress Controller deployed
* [ ] Namespace `radiant-petclinic` created
* [ ] PostgreSQL database available
* [ ] Network Policies deployed
* [ ] HPA and PDB deployed
* [ ] Helm chart validated

### Application Validation

* [ ] Application image available in ACR
* [ ] Helm deployment successful
* [ ] Pods healthy and ready
* [ ] Database connectivity verified
* [ ] Ingress accessible
* [ ] Smoke tests completed

---

## Cutover Steps

### Step 1 – Freeze Changes

* Pause production deployments
* Notify stakeholders
* Confirm migration window

### Step 2 – Backup Validation

Verify:

* Database backup availability
* Helm chart version
* Kubernetes manifests
* Current deployment revision

### Step 3 – Deploy Application to AKS

```bash
helm upgrade --install radiant-petclinic ./helm/radiant-petclinic \
  --namespace radiant-petclinic \
  --create-namespace
```

Verify:

```bash
kubectl get pods -n radiant-petclinic
kubectl get ingress -n radiant-petclinic
```

### Step 4 – Validate Application

Verify:

* Application homepage
* Owner search
* Veterinarian page
* Database connectivity

### Step 5 – DNS Cutover

Update DNS:

```text
petclinic.company.com
```

to point to AKS Load Balancer public IP.

### Step 6 – Post-Cutover Validation

Validate:

* Application accessibility
* Pod health
* Ingress routing
* Database operations
* Monitoring dashboards

---

## Success Criteria

* Application accessible via production URL
* No critical errors
* Database connectivity successful
* No failed pods
* Monitoring healthy

---

## Ownership

| Activity               | Owner            |
| ---------------------- | ---------------- |
| AKS Deployment         | Platform Team    |
| DNS Update             | Network Team     |
| Application Validation | Application Team |
| Monitoring Validation  | Operations Team  |
