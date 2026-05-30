# Dependency Summary

## Application Dependencies

# Dependency Summary

| Dependency Type    | Dependency                        | Purpose                                 | Criticality |
| ------------------ | --------------------------------- | --------------------------------------- | ----------- |
| Ingress            | NGINX Ingress Controller          | Routes external traffic to application  | High        |
| Service-to-Service | Kubernetes Service                | Routes traffic to application pods      | High        |
| Database           | None                              | No external database configured         | Low         |
| Message Queue      | None                              | No message queue configured             | Low         |
| Filesystem         | None                              | No shared filesystem configured         | Low         |
| External API       | None                              | No external API integrations configured | Low         |
| Secrets            | Kubernetes Secrets (Future Scope) | Production secret management            | Medium      |
| Platform           | Kubernetes (k3d)              | Container orchestration                 | High        |
| Platform           | Docker                            | Container runtime                       | High        |
| DNS                | Local Hosts File Mapping          | Resolves radiant-petclinic.local        | Medium      |

---

# OnPrem Architecture Diagram

                        Internet / Browser
                                 |
                                 v
                  +-----------------------------+
                  |     NGINX Ingress Controller |
                  |   Host: radiant-petclinic.local
                  +-----------------------------+
                                 |
                                 v
                  +-----------------------------+
                  |   Kubernetes Service         |
                  | radiant-petclinic-service    |
                  |         ClusterIP            |
                  +-----------------------------+
                                 |
                 ---------------------------------
                 |               |               |
                 v               v               v
        +---------------+ +---------------+ +---------------+
        | PetClinic Pod | | PetClinic Pod | | PetClinic Pod |
        |   SpringBoot  | |   SpringBoot  | |   SpringBoot  |
        |     :8080     | |     :8080     | |     :8080     |
        +---------------+ +---------------+ +---------------+
```mermaid
graph LR
  subgraph External
    User["External User"]
    NGINX["nginx ingress controller\n(namespace: ingress-nginx)"]
  end

  subgraph AppNamespace["Namespace: radiant-petclinic"]
    Ingress["Ingress\nradiant-petclinic-ingress"]
    Service["Service\nradiant-petclinic-service\nClusterIP: 80"]
    Deployment["Deployment\nradiant-petclinic-deployment\napp=radiant-petclinic"]
    Pod["Pod(s)\ncontainerPort: 8080\nliveness/readiness probes"]
    HPA["HPA\nminReplicas=2\nmaxReplicas=5\nCPU target=70%"]
    PDB["PodDisruptionBudget\nminAvailable=1"]
    NPDefault["NetworkPolicy\ndefault-deny\n(all ingress/egress denied)"]
    NPAllow["NetworkPolicy\nallow-nginx-ingress\nallow ingress from namespace: ingress-nginx"]
  end

  User -->|HTTP request| NGINX
  NGINX -->|Ingress rule\nhost radiant-petclinic.local| Ingress
  Ingress -->|routes to service| Service
  Service -->|ClusterIP 80 → targetPort 8080| Pod
  Deployment -->|manages replica pods| Pod
  HPA -.->|scales deployment| Deployment
  PDB -.->|ensures availability| Deployment
  NPDefault -.->|blocks all traffic by default| Pod
  NPAllow -.->|allows ingress from nginx controller| Pod

```
## Future Production Dependencies

| Dependency | Purpose |
|---|---|
| Azure Kubernetes Service (AKS) | Production orchestration |
| Azure Container Registry (ACR) | Image storage |
| Azure Monitor | Logging and monitoring |
| MySQL Database | Persistent backend storage |
| Azure Key Vault | Secrets management |

---

## Risk Notes

- Ingress routing depends on proper DNS resolution.
- Network policies may block ingress traffic if misconfigured.
- HPA scaling depends on metrics-server availability.
- Application currently uses local container images in k3d environment.