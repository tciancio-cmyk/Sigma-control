import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Construction Portfolio Control – Engineering Model")

num_projects = st.number_input("Number of Projects", 1, 10, 2)

projects = []

for i in range(int(num_projects)):

    st.header(f"Project {i+1}")
    name = st.text_input(f"Project Name {i+1}", key=f"name_{i}")

    if name:

        # -------------------------
        # INCOMPLETE
        # -------------------------
        planned = st.number_input(f"Planned activities {name}", 1, 1000, 100)
        open_t = st.number_input(f"Open tasks {name}", 0, 500, 10)
        blocked = st.number_input(f"Blocked tasks {name}", 0, 500, 5)
        reopened = st.number_input(f"Reopened tasks {name}", 0, 500, 2)

        incomplete = (open_t + blocked + reopened) / planned

        # -------------------------
        # INTERFERENCE
        # -------------------------
        interferences = st.number_input(f"Interferences {name}", 0, 100, 5)
        workfronts = st.number_input(f"Active workfronts {name}", 1, 50, 10)

        interference = interferences / workfronts

        # -------------------------
        # PRIORITY
        # -------------------------
        changes = st.number_input(f"Unplanned changes {name}", 0, 50, 3)

        priority_index = changes / planned

        # -------------------------
        # REWORK
        # -------------------------
        rework_qty = st.number_input(f"Rework quantity {name}", 0.0, 10000.0, 50.0)
        total_qty = st.number_input(f"Total executed {name}", 1.0, 10000.0, 500.0)

        rework = rework_qty / total_qty

        # -------------------------
        # SATURATION
        # -------------------------
        equipment = st.slider(f"Equipment utilization % {name}", 0, 120, 80)
        manpower = st.slider(f"Manpower utilization % {name}", 0, 120, 85)
        logistics = st.slider(f"Logistic congestion {name}", 0, 10, 3)

        saturation = 0.4*(equipment/100) + 0.4*(manpower/100) + 0.2*(logistics/10)

        # -------------------------
        # SIGMA
        # -------------------------
        weights = {
            "incomplete": 1.2,
            "interference": 1.5,
            "priority": 1.0,
            "rework": 2.0,
            "saturation": 1.3
        }

        sigma = (
            weights["incomplete"] * incomplete +
            weights["interference"] * interference +
            weights["priority"] * priority_index +
            weights["rework"] * rework +
            weights["saturation"] * saturation
        )

        # -------------------------
        # VALUE
        # -------------------------
        contract = st.slider(f"Contract weight {name}", 1, 10, 5)
        delay = st.slider(f"Delay impact (days) {name}", 0, 100, 10)
        client = st.slider(f"Client criticality {name}", 1, 10, 5)
        cost = st.slider(f"Cost exposure {name}", 1, 10, 5)

        value = 0.3*contract + 0.3*(delay/10) + 0.2*client + 0.2*cost

        priority_score = sigma * value

        projects.append({
            "Project": name,
            "Sigma": sigma,
            "Value": value,
            "Priority": priority_score
        })

# -------------------------
# OUTPUT
# -------------------------
if projects:

    df = pd.DataFrame(projects).sort_values(by="Priority", ascending=False)

    st.header("Portfolio Ranking")
    st.dataframe(df, use_container_width=True)

    top = df.iloc[0]

    st.header("Decision Focus")

    st.metric("Critical Project", top["Project"])
    st.metric("Sigma", round(top["Sigma"],2))
    st.metric("Priority", round(top["Priority"],2))

    if top["Sigma"] < 1:
        st.success("STABLE")
    elif top["Sigma"] < 2:
        st.warning("ATTENTION")
    else:
        st.error("CRITICAL")
