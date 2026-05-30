# Ingress Controller Decision

## Selected Solution
NGINX Ingress Controller

## Reason

- Mature Kubernetes ingress solution
- Large community adoption
- Well documented
- Supports TLS termination
- Supports path and host-based routing
- Easy AKS integration

## NGINX vs HAProxy

| Feature | NGINX Ingress | HAProxy Ingress |
|----------|----------|----------|
| Kubernetes Adoption | High | Medium |
| Community Support | Large | Moderate |
| Documentation | Extensive | Good |
| AKS Usage | Common | Less Common |
| Operational Familiarity | High | Medium |

Decision:
NGINX selected because of wider Kubernetes adoption and operational familiarity.

## TLS Strategy

Development:
- HTTP only

Production:
- cert-manager
- Let's Encrypt certificates
- Automatic certificate renewal
- HTTPS enforced

## DNS Strategy

Development:
radiant-petclinic.local

Production:
petclinic.company.com

DNS records point to:
Azure Load Balancer Public IP

Traffic Flow:
DNS
→ Azure Load Balancer
→ NGINX Ingress
→ Service
→ Pods

## DNS Cutover Strategy

1. Deploy application to AKS.
2. Validate application functionality.
3. Reduce DNS TTL before migration.
4. Update DNS record to AKS Load Balancer IP.
5. Validate production traffic.
6. Monitor during hypercare period.
