"""Tests for Kubernetes service deployment."""

import subprocess


def test_nginx_service_exists():
    """Check if the nginx service exists."""
    result = subprocess.run(
        ["kubectl", "get", "services", "nginx-service"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    assert result.returncode == 0, (
        f"Service 'nginx-service' does not exist. "
        f"Error: {result.stderr.decode()}"
    )


def test_nginx_service_mapping_and_pods():
    """Check if the nginx service is correctly mapped to pods."""
    service_port_result = subprocess.run(
        ["kubectl", "get", "svc", "nginx-service", "-o",
         "jsonpath={.spec.ports[0].port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    pods_result = subprocess.run(
        ["kubectl", "get", "pods", "-l", "app=nginx", "-o",
         "jsonpath={.items[*].status.phase}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    service_port = service_port_result.stdout.decode('utf-8').strip()
    pods_status = pods_result.stdout.decode('utf-8')

    assert service_port == "80", f"Service port is not 80.\
        Found: {service_port}"

    assert "Running" in pods_status, \
        f"Not all Pods are running. Found statuses: {pods_status}"
