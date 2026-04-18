import streamlit as st

st.title("Sigma Control – Decision Engine")

st.header("Input KPI")

incomplete = st.slider("Incomplete Tasks", 0.0, 5.0, 1.0)
interference = st.slider("Interference", 0.0, 5.0, 1.0)
changes = st.slider("Priority Changes", 0.0, 5.0, 1.0)
rework = st.slider("Rework", 0.0, 5.0, 1.0)
saturation = st.slider("Saturation", 0.0, 5.0, 1.0)

sigma = incomplete + interference + changes + rework + saturation

st.subheader("Result")

st.metric("Sigma Index", round(sigma, 2))

if sigma < 3:
    st.success("GREEN → ACCELERATE")
elif sigma < 6:
    st.warning("YELLOW → STABILIZE")
else:
    st.error("RED → RECOVER CONTROL")
