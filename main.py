import streamlit as st
from src.ui import run_app

st.set_page_config(
    page_title="Real-Time Object Detection Platform",
    page_icon="🎯",
    layout="wide",
)

run_app()
