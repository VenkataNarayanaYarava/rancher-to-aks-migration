# Migration Decisions

| Decision Area         | Selected Approach                    | Reason                                                        |
| --------------------- | ------------------------------------ | ------------------------------------------------------------- |
| Container Platform    | Kubernetes (k3d/k3s)                 | Simulates production Kubernetes environment locally           |
| Container Runtime     | Docker                               | Standard container packaging and runtime                      |
| Ingress Controller    | NGINX Ingress Controller             | Widely used Kubernetes ingress solution                       |
| Deployment Strategy   | Kubernetes Deployment                | Provides declarative application management                   |
| Service Exposure      | ClusterIP Service + Ingress          | Separates internal and external traffic routing               |
| Namespace Strategy    | Dedicated Namespace                  | Logical isolation of application resources                    |
| Scaling Strategy      | Horizontal Pod Autoscaler (HPA)      | Enables automatic scaling based on resource usage             |
| Availability Strategy | Pod Disruption Budget (PDB)          | Maintains minimum application availability during maintenance |
| Deployment Packaging  | Helm Charts                          | Supports reusable and configurable deployments                |
| Security Strategy     | Network Policies                     | Restricts unnecessary pod-to-pod communication                |
| Migration Target      | Azure Kubernetes Service (AKS)       | Managed Kubernetes platform for production deployment         |
| Secrets Management    | Kubernetes Secrets / Azure Key Vault | Secure management of application secrets                      |
| CI/CD Strategy        | GitHub Actions        | Automated build and deployment pipelines                      |

---

# Key Migration Notes

* Current environment uses k3d to simulate on-premises Kubernetes workloads.
* Architecture is designed to support future migration to AKS.
* Helm packaging improves deployment standardization across environments.
* NGINX ingress configuration supports external traffic routing and future TLS integration.
* HPA and PDB improve production readiness and operational stability.
