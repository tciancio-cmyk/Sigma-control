import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Construction Portfolio Control – Sigma Engine")

# -------------------------
# NUMERO CANTIERI
# -------------------------
num_projects = st.number_input(
    "Number of Projects",
    min_value=1,
    max_value=20,
    value=3
)

projects_data = []

# -------------------------
# PARAMETRI MODELLO
# -------------------------
max_values = {
    "incomplete": 30,
    "interference": 10,
    "changes": 5,
    "rework": 20,
    "saturation": 100
}

weights = {
    "incomplete": 1.2,
    "interference": 1.5,
    "changes": 1.0,
    "rework": 2.0,
    "saturation": 1.3
}

# -------------------------
# INPUT PROGETTI
# -------------------------
for i in range(int(num_projects)):

    st.subheader(f"Project {i+1}")

    name = st.text_input(f"Project Name {i+1}", key=f"name_{i}")

    if name:

        col1, col2, col3 = st.columns(3)

        with col1:
            incomplete = st.number_input(f"Incomplete tasks {name}", 0, 100, 10)

        with col2:
            interference = st.number_input(f"Interferences {name}", 0, 50, 5)

        with col3:
            changes = st.number_input(f"Priority changes {name}", 0, 20, 3)

        col4, col5 = st.columns(2)

        with col4:
            rework = st.number_input(f"Rework % {name}", 0.0, 100.0, 10.0)

        with col5:
            saturation = st.number_input(f"Saturation % {name}", 0.0, 120.0, 85.0)

        # -------------------------
        # NORMALIZZAZIONE
        # -------------------------
        norm = {
            "incomplete": incomplete / max_values["incomplete"],
            "interference": interference / max_values["interference"],
            "changes": changes / max_values["changes"],
            "rework": rework / max_values["rework"],
            "saturation": saturation / max_values["saturation"]
        }

        # -------------------------
        # SIGMA CALCOLATO
        # -------------------------
        sigma = sum(weights[k] * norm[k] for k in norm)

        # -------------------------
        # PRIORITY (puoi migliorarlo dopo)
        # -------------------------
        value = st.slider(f"Value / Impact {name}", 1.0, 10.0, 5.0)

        priority = sigma * value

        projects_data.append({
            "Project": name,
            "Sigma": sigma,
            "Value": value,
            "Priority": priority,
            **norm
        })

# -------------------------
# ANALISI
# -------------------------
if projects_data:

    df = pd.DataFrame(projects_data)

    # -------------------------
    # RANKING
    # -------------------------
    st.header("Portfolio Ranking")

    df_sorted = df.sort_values(by="Priority", ascending=False)

    st.dataframe(df_sorted[["Project", "Sigma", "Value", "Priority"]], use_container_width=True)

    # -------------------------
    # CRITICAL PROJECT
    # -------------------------
    top = df_sorted.iloc[0]

    st.header("Decision Focus")

    colA, colB, colC = st.columns(3)

    colA.metric("Critical Project", top["Project"])
    colB.metric("Sigma", round(top["Sigma"], 2))
    colC.metric("Priority", round(top["Priority"], 2))

    if top["Sigma"] < 3:
        st.success("LOW RISK → Monitor")
    elif top["Sigma"] < 6:
        st.warning("MEDIUM RISK → Stabilize")
    else:
        st.error("HIGH RISK → Immediate Intervention")

    # -------------------------
    # BREAKDOWN SIGMA (KEY PART)
    # -------------------------
    st.header("Sigma Breakdown (Critical Project)")

    breakdown = {
        "Incomplete": weights["incomplete"] * top["incomplete"],
        "Interference": weights["interference"] * top["interference"],
        "Changes": weights["changes"] * top["changes"],
        "Rework": weights["rework"] * top["rework"],
        "Saturation": weights["saturation"] * top["saturation"]
    }

    breakdown_df = pd.DataFrame.from_dict(breakdown, orient="index", columns=["Contribution"])

    st.bar_chart(breakdown_df)

    # -------------------------
    # VISUAL PORTFOLIO
    # -------------------------
    st.header("Portfolio Map")

    st.scatter_chart(df.set_index("Project")[["Sigma", "Priority"]])

else:
    st.info("Insert at least one project to start analysis")
