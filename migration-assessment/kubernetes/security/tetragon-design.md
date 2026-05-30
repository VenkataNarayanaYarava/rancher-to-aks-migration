# Tetragon Runtime Observability Design

## Objective

Tetragon is used to provide runtime security observability for the Radiant PetClinic workload during and after migration to AKS.

## Why Tetragon

Tetragon provides eBPF-based visibility into runtime activity inside Kubernetes workloads. It helps detect unexpected process execution, suspicious binaries, privilege escalation attempts, and unexpected network activity.

## Monitored Namespace

`radiant-petclinic`

## Runtime Events Monitored

| Event Type | Purpose |
|---|---|
| Process execution | Detect unexpected shell or binary execution |
| Network activity | Identify unexpected outbound connections |
| Suspicious runtime behavior | Support post-migration security monitoring |

## Example Detection Scenario

If an operator or attacker runs a shell inside the PetClinic pod:

```bash
kubectl exec -it deployment/radiant-petclinic-deployment -n radiant-petclinic -- sh

```

Tetragon can capture this as a process execution event.

## Hypercare Usage

During migration hypercare, Tetragon events can help identify:

* Unexpected shell execution
* Unexpected outbound traffic
* Suspicious binaries
* Runtime behavior changes after migration

## Operational Response

| Event                                    | Action                                                                   |
| ---------------------------------------- | ------------------------------------------------------------------------ |
| Unexpected shell execution               | Investigate user activity and validate change ticket                     |
| Unexpected outbound connection           | Review Network Policies and application logs                             |
| Suspicious binary execution              | Escalate to Security Team                                                |
| Runtime behavior changes after migration | Compare against baseline behavior and validate application functionality |
