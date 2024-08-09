#!/bin/bash

# Check if the Service exists
kubectl get services nginx-service > /dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "Service nginx-service does not exist."
  exit 1
fi

# Check if the Service is correctly mapped to the Pods
SERVICE_PORT=$(kubectl get svc nginx-service -o jsonpath='{.spec.ports[0].port}')
PODS=$(kubectl get pods -l app=nginx -o jsonpath='{.items[*].status.phase}')

if [[ "$SERVICE_PORT" -eq 80 && "$PODS" == *"Running"* ]]; then
  echo "Service is correctly mapped and Pods are running."
else
  echo "Service or Pods are not in the expected state."
  exit 1
fi

echo "Service test passed."
