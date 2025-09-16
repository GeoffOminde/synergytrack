import streamlit as st
import requests
import pandas as pd
API = "http://localhost:8000"

st.set_page_config(page_title="SynergyTrack Analytics", layout="wide")
st.title("SynergyTrack Analytics Dashboard")

token = st.text_input("JWT token", type="password")
headers = {"Authorization": f"Bearer {token}"} if token else {}

col1, col2 = st.columns(2)
with col1:
    st.subheader("Projects")
    r = requests.get(f"{API}/projects"); projects = r.json()
    st.dataframe(pd.DataFrame(projects))
with col2:
    st.subheader("Campaigns")
    r = requests.get(f"{API}/campaigns"); camps = r.json()
    st.dataframe(pd.DataFrame(camps))

st.subheader("KPI Inference")
vals = st.text_input("Comma-separated metric values", "10,20,30,40,50")
if st.button("Run AI"):
    v = [float(x.strip()) for x in vals.split(",")]
    r = requests.post(f"{API}/ai/kpi/infer", json={"values": v})
    st.json(r.json())
