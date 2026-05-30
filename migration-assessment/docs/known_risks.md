# Known Risks

| Risk                                                          | Impact                                                     | Mitigation                                                                |
| ------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| Local k3d environment differs from AKS production environment | Kubernetes behavior may differ during migration            | Validate manifests and ingress behavior in AKS staging environment        |
| No HTTPS/TLS currently configured                             | Insecure external traffic exposure                         | Configure TLS certificates and HTTPS ingress before production deployment |
| Local hosts file mapping used for DNS                         | DNS resolution issues outside local environment            | Configure proper DNS records in production                                |
| No centralized monitoring/logging stack                       | Operational visibility limitations                         | Integrate Azure Monitor, Prometheus, or Grafana                           |
| HPA depends on metrics-server availability                    | Autoscaling may fail if metrics-server becomes unavailable | Validate metrics-server health and monitoring                             |
| No external database currently configured                     | Future database migration may introduce complexity         | Plan managed database deployment strategy in AKS                          |
| Network policies not fully validated                          | Potential unintended traffic blocking                      | Perform connectivity and security testing                                 |
| Single application architecture                               | Monolithic application may limit independent scaling       | Consider future microservices decomposition if required                   |
| Local container images used in k3d                            | Images not centrally managed                               | Use Azure Container Registry (ACR) for production images                  |
| Helm chart still under development                            | Deployment standardization incomplete                      | Finalize and validate Helm templates                                      |
