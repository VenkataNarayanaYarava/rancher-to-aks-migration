# Rollback Plan

## Objective

Provide a controlled rollback procedure if migration issues occur during or after AKS cutover.

---

## Rollback Triggers

Rollback should be initiated if any of the following occur:

* Application unavailable
* Database connectivity failure
* Critical functionality broken
* Ingress routing failure
* Performance degradation
* Security issue detected

---

## Rollback Procedure

### Step 1 – Stop Traffic to AKS

Update DNS to point back to the previous Rancher environment.

### Step 2 – Validate Legacy Environment

Verify:

* Application reachable
* Database accessible
* Monitoring healthy

### Step 3 – Confirm Recovery

Validate:

* Homepage access
* Owner search
* Veterinarian page
* Database transactions

### Step 4 – Incident Review

Document:

* Root cause
* Timeline
* Corrective actions

---

## Rollback Success Criteria

* Traffic restored to previous environment
* No user-facing errors
* Monitoring healthy
* Business operations restored

---

## Ownership

| Activity               | Owner            |
| ---------------------- | ---------------- |
| DNS Rollback           | Network Team     |
| Application Validation | Application Team |
| Incident Review        | Migration Team   |
