# k8s_controller.py
from kubernetes import client, config
from datetime import datetime
import os

# Load kube config once
config.load_kube_config()
core_v1_api = client.CoreV1Api()

def start_pod(model_name, cpu_request, memory_request):
    """
    Start a pod with specified model, CPU and memory limits.
    """
    pod_name = f"{model_name}-pod"
    container_spec = client.V1Container(
        name=model_name,
        image=_resolve_model_image(model_name),
        resources=client.V1ResourceRequirements(
            requests={"cpu": cpu_request, "memory": memory_request},
            limits={"cpu": cpu_request, "memory": memory_request}
        )
    )

    pod_spec = client.V1Pod(
        metadata=client.V1ObjectMeta(name=pod_name),
        spec=client.V1PodSpec(containers=[container_spec])
    )

    try:
        core_v1_api.create_namespaced_pod(namespace="default", body=pod_spec)
        _log_event("START", pod_name)
    except client.exceptions.ApiException as e:
        raise RuntimeError(f"Failed to start pod: {e}")

def _resolve_model_image(model_name):
    model_map = {
        "gpt2": "ghcr.io/huggingface/transformers-pytorch-gpt2",
        "bert": "ghcr.io/huggingface/transformers-pytorch-bert",
        "stable-diffusion": "ghcr.io/stabilityai/stable-diffusion",
        "resnet": "pytorch/torchserve:latest",
        "nginx": "nginx:latest"
    }
    return model_map.get(model_name, "nginx:latest")


def stop_pod(model_name):
    """
    Stop a pod by deleting it from the default namespace.
    """
    pod_name = f"{model_name}-pod"
    try:
        core_v1_api.delete_namespaced_pod(name=pod_name, namespace="default")
        _log_event("STOP", pod_name)
    except client.exceptions.ApiException as e:
        raise RuntimeError(f"Failed to stop pod: {e}")

def _log_event(action, pod_name):
    """
    Append start/stop logs with timestamps.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/pod_log.txt", "a") as log:
        log.write(f"[{action}] {pod_name} at {datetime.now()}\n")

def get_last_log(model_name, action):
    """
    Return the most recent log for a given action and model.
    """
    log_path = "logs/pod_log.txt"
    if not os.path.exists(log_path):
        return "No logs yet."
    
    with open(log_path, "r") as log:
        lines = log.readlines()
    
    pod_name = f"{model_name}-pod"
    for line in reversed(lines):
        if f"[{action}]" in line and pod_name in line:
            return line.strip()
    return f"No recent {action.lower()} log found for {model_name}."