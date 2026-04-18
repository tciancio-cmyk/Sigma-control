import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Construction Portfolio Control – Sigma + Decision Engine")

num_projects = st.number_input("Number of Projects", 1, 10, 2)

projects = []

for i in range(int(num_projects)):

    st.markdown("---")
    name = st.text_input(f"Project {i+1}", key=f"name_{i}")

    if name:

        st.markdown(f"## {name}")

        # =========================
        # FLOW KPI
        # =========================
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### Incomplete")
            planned = st.number_input("Planned", 1, 1000, 100, key=f"p_{i}")
            open_t = st.number_input("Open", 0, 500, 10, key=f"o_{i}")
            blocked = st.number_input("Blocked", 0, 500, 5, key=f"b_{i}")
            reopened = st.number_input("Reopened", 0, 500, 2, key=f"r_{i}")
            incomplete = (open_t + blocked + reopened) / planned

        with col2:
            st.markdown("### Interference")
            interferences = st.number_input("Interferences", 0, 100, 5, key=f"int_{i}")
            workfronts = st.number_input("Workfronts", 1, 50, 10, key=f"wf_{i}")
            interference = interferences / workfronts

        with col3:
            st.markdown("### Priority Instability")
            changes = st.number_input("Unplanned changes", 0, 50, 3, key=f"ch_{i}")
            priority_index = changes / planned

        # =========================
        # QUALITY + RESOURCES
        # =========================
        col4, col5 = st.columns(2)

        with col4:
            st.markdown("### Rework")
            rework_qty = st.number_input("Rework qty", 0.0, 10000.0, 50.0, key=f"rw_{i}")
            total_qty = st.number_input("Total qty", 1.0, 10000.0, 500.0, key=f"tot_{i}")
            rework = rework_qty / total_qty

        with col5:
            st.markdown("### Saturation (Hours-Based)")
            equip_avail = st.number_input("Equip avail h", 1.0, 10000.0, 100.0, key=f"ea_{i}")
            equip_used = st.number_input("Equip used h", 0.0, 10000.0, 80.0, key=f"eu_{i}")

            man_avail = st.number_input("Man avail h", 1.0, 10000.0, 100.0, key=f"ma_{i}")
            man_used = st.number_input("Man used h", 0.0, 10000.0, 85.0, key=f"mu_{i}")

            logistics = st.slider("Logistics", 0, 10, 3, key=f"log_{i}")

            E = min(equip_used / equip_avail, 1.2)
            M = min(man_used / man_avail, 1.2)
            L = logistics / 10

            saturation = 0.4*E + 0.4*M + 0.2*L

        # =========================
        # PRODUCTIVITY
        # =========================
        col6, col7 = st.columns(2)

        with col6:
            st.markdown("### Equipment Productivity")
            output_e = st.number_input("Actual output E", 0.0, 100000.0, 500.0, key=f"oe_{i}")
            rate_e = st.number_input("Std rate E", 0.1, 1000.0, 10.0, key=f"re_{i}")
            PI_e = output_e / (rate_e * equip_used) if equip_used > 0 else 0

        with col7:
            st.markdown("### Manpower Productivity")
            output_m = st.number_input("Actual output M", 0.0, 100000.0, 500.0, key=f"om_{i}")
            rate_m = st.number_input("Std rate M", 0.1, 1000.0, 8.0, key=f"rm_{i}")
            PI_m = output_m / (rate_m * man_used) if man_used > 0 else 0

        PI_total = 0.5 * PI_e + 0.5 * PI_m

        # =========================
        # VALUE
        # =========================
        col8, col9, col10, col11 = st.columns(4)

        with col8:
            contract = st.slider("Contract", 1, 10, 5, key=f"c_{i}")
        with col9:
            delay = st.slider("Delay", 0, 100, 10, key=f"d_{i}")
        with col10:
            client = st.slider("Client", 1, 10, 5, key=f"cl_{i}")
        with col11:
            cost = st.slider("Cost", 1, 10, 5, key=f"co_{i}")

        value = 0.3*contract + 0.3*(delay/10) + 0.2*client + 0.2*cost

        # =========================
        # SIGMA
        # =========================
        weights = {
            "incomplete": 1.2,
            "interference": 1.5,
            "priority": 1.0,
            "rework": 2.0,
            "saturation": 1.3,
            "productivity": 1.5
        }

        sigma = (
            weights["incomplete"] * incomplete +
            weights["interference"] * interference +
            weights["priority"] * priority_index +
            weights["rework"] * rework +
            weights["saturation"] * saturation +
            weights["productivity"] * (1 - PI_total)
        )

        priority_score = sigma * value

        # =========================
        # DECISION ENGINE
        # =========================
        drivers = {
            "Incomplete": incomplete,
            "Interference": interference,
            "Priority": priority_index,
            "Rework": rework,
            "Saturation": saturation,
            "Productivity Loss": (1 - PI_total)
        }

        main_driver = max(drivers, key=drivers.get)

        def get_actions(driver):
            if driver == "Incomplete":
                return ["Reduce WIP", "Close tasks", "Limit fronts"]
            if driver == "Interference":
                return ["Resequence", "Separate crews", "Fix logistics"]
            if driver == "Priority":
                return ["Freeze plan", "Limit changes"]
            if driver == "Rework":
                return ["Stop work", "Increase QC"]
            if driver == "Saturation":
                return ["Reduce load", "Add resources"]
            if driver == "Productivity Loss":
                return ["Improve method", "Train team"]
            return []

        actions = get_actions(main_driver)

        projects.append({
            "Project": name,
            "Sigma": sigma,
            "Priority": priority_score,
            "Driver": main_driver,
            "PI": PI_total,
            "Actions": ", ".join(actions)
        })

# =========================
# OUTPUT
# =========================
if projects:

    df = pd.DataFrame(projects).sort_values(by="Priority", ascending=False)

    st.markdown("---")
    st.header("Portfolio Ranking")
    st.dataframe(df, use_container_width=True)

    top = df.iloc[0]

    st.header("Decision Focus")

    st.metric("Project", top["Project"])
    st.metric("Sigma", round(top["Sigma"], 2))
    st.metric("Priority", round(top["Priority"], 2))
    st.metric("Main Issue", top["Driver"])
    st.metric("Productivity", round(top["PI"], 2))

    st.markdown("### Actions")
    for a in top["Actions"].split(","):
        st.write(f"- {a}")

else:
    st.info("Insert projects")
