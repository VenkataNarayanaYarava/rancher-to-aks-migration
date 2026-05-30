## Install Tetragon

helm repo add cilium https://helm.cilium.io
helm repo update

helm install tetragon cilium/tetragon \
  --namespace kube-system

## Verify

kubectl rollout status -n kube-system ds/tetragon -w

## Check Pods

kubectl get pods -n kube-system -l app.kubernetes.io/name=tetragon

## Create and Apply the Tetrapolicy
kubectl apply -f security/tetragon/tracing-policy.yaml

## Generate Runtime Event

kubectl exec -it deployment/radiant-petclinic-deployment \
  -n radiant-petclinic -- sh

## View Tetragon Events

kubectl logs -n kube-system -l app.kubernetes.io/name=tetragon -f

Look for events related to: radiant-petclinic, execve, sh

## Save Event

kubectl logs -n kube-system -l app.kubernetes.io/name=tetragon \
  > tetragon-events.log