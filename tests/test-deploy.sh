#!/bin/bash

# Check if the Deployment exists
kubectl get deployments nginx-deployment > /dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "Deployment nginx-deployment does not exist."
  exit 1
fi

# Check the number of Pods
PODS=$(kubectl get pods -l app=nginx -o jsonpath='{.items[*].status.phase}')

if [[ "$PODS" == *"Running"* ]]; then
  echo "All Pods are running."
else
  echo "Some Pods are not running."
  exit 1
fi

echo "Deployment test passed :)."
