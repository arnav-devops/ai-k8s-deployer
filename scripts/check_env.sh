#!/bin/bash
echo "✅ Checking environment..."

echo -n "Python: "; python3 --version
echo -n "pip: "; pip3 --version
echo -n "Docker: "; docker --version
echo -n "Minikube: "; minikube version
echo -n "kubectl: "; kubectl version --client