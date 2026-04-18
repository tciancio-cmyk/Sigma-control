import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Construction Portfolio Control – Senior Director")

# -------------------------
# INPUT: numero cantieri
# -------------------------
num_projects = st.number_input("Number of Projects", min_value=1, max_value=20, value=3)

projects_data = []

st.header("Project Input")

for i in range(int(num_projects)):
    st.subheader(f"Project {i+1}")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input(f"Project Name {i+1}", key=f"name_{i}")

    with col2:
        sigma = st.slider(f"Sigma {i+1}", 0.0, 10.0, 3.0, key=f"sigma_{i}")

    with col3:
        value = st.slider(f"Value / Impact {i+1}", 1.0, 10.0, 5.0, key=f"value_{i}")

    priority = sigma * value

    if name:  # evita campi vuoti
        projects_data.append({
            "Project": name,
            "Sigma": sigma,
            "Value": value,
            "Priority": priority
        })

# -------------------------
# ANALISI
# -------------------------
if projects_data:
    df = pd.DataFrame(projects_data)

    st.header("Portfolio Ranking")

    df_sorted = df.sort_values(by="Priority", ascending=False)

    st.dataframe(df_sorted, use_container_width=True)

    # -------------------------
    # CRITICAL PROJECT
    # -------------------------
    top = df_sorted.iloc[0]

    st.header("Decision Focus")

    colA, colB, colC = st.columns(3)

    colA.metric("Critical Project", top["Project"])
    colB.metric("Sigma", round(top["Sigma"], 2))
    colC.metric("Priority Score", round(top["Priority"], 2))

    # -------------------------
    # DECISION LOGIC
    # -------------------------
    if top["Sigma"] < 3:
        st.success("LOW RISK → Monitor")
    elif top["Sigma"] < 6:
        st.warning("MEDIUM RISK → Stabilize")
    else:
        st.error("HIGH RISK → Immediate Intervention")

    # -------------------------
    # VISUAL
    # -------------------------
    st.header("Portfolio Visualization")
    st.scatter_chart(df_sorted.set_index("Project")[["Sigma", "Priority"]])

else:
    st.info("Insert at least one project name to activate analysis")
