# ui.py
import streamlit as st
from k8s_controller import start_pod, stop_pod, get_last_log

st.set_page_config(page_title="Kubernetes AI Pod Launcher", layout="centered")



models = ["gpt2", "bert", "stable-diffusion", "resnet", "nginx"]
model = st.selectbox("Choose a model", models)

st.subheader("Resource Configuration")
col1, col2 = st.columns(2)
cpu = col1.text_input("CPU", "500m")
memory = col2.text_input("Memory", "512Mi")

st.subheader("Pod Actions")
if st.button("Start Pod"):
    try:
        start_pod(model, cpu, memory)
        st.success(f"Started pod for model: {model}")
        st.code(get_last_log(model, "START"))
    except Exception as e:
        st.error(str(e))

if st.button("Stop Pod"):
    try:
        stop_pod(model)
        st.warning(f"Stopped pod for model: {model}")
        st.code(get_last_log(model, "STOP"))
    except Exception as e:
        st.error(str(e))


