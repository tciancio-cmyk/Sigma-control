import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Construction Portfolio Control – Sigma + Decision Engine")

st.markdown("""
### 📘 Model Logic
This system evaluates construction performance using:
- **Flow stability (Incomplete, Interference, Priority)**
- **Quality (Rework)**
- **Resource utilization (Saturation – hours based)**
- **Efficiency (Productivity)**

👉 Output:
- Sigma (system instability)
- Priority (where to intervene)
- Root cause + Actions
""")

num_projects = st.number_input(
    "Number of Projects",
    1, 10, 2,
    help="Total number of projects to analyze in the portfolio"
)

projects = []

for i in range(int(num_projects)):

    st.markdown("---")
    name = st.text_input(
        f"Project {i+1}",
        key=f"name_{i}",
        help="Insert project or site name"
    )

    if name:

        st.markdown(f"## {name}")

        # =========================
        # FLOW KPI
        # =========================
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🔵 Incomplete Index")
            planned = st.number_input(
                "Planned activities",
                1, 1000, 100,
                key=f"p_{i}",
                help="Total activities planned in the period (daily/weekly baseline)"
            )
            open_t = st.number_input(
                "Open tasks",
                0, 500, 10,
                key=f"o_{i}",
                help="Activities started but not completed"
            )
            blocked = st.number_input(
                "Blocked tasks",
                0, 500, 5,
                key=f"b_{i}",
                help="Activities stopped due to constraints (access, materials, approvals)"
            )
            reopened = st.number_input(
                "Reopened tasks",
                0, 500, 2,
                key=f"r_{i}",
                help="Activities reopened due to defects or errors"
            )

            incomplete = (open_t + blocked + reopened) / planned

        with col2:
            st.markdown("### 🟠 Interference Index")
            interferences = st.number_input(
                "Interferences",
                0, 100, 5,
                key=f"int_{i}",
                help="Number of conflicts between crews or overlapping activities"
            )
            workfronts = st.number_input(
                "Active workfronts",
                1, 50, 10,
                key=f"wf_{i}",
                help="Number of parallel work areas"
            )

            interference = interferences / workfronts

        with col3:
            st.markdown("### 🟡 Priority Instability")
            changes = st.number_input(
                "Unplanned changes",
                0, 50, 3,
                key=f"ch_{i}",
                help="Changes to plan not originally scheduled"
            )

            priority_index = changes / planned

        # =========================
        # QUALITY + RESOURCES
        # =========================
        col4, col5 = st.columns(2)

        with col4:
            st.markdown("### 🔴 Rework Index")
            rework_qty = st.number_input(
                "Rework quantity",
                0.0, 10000.0, 50.0,
                key=f"rw_{i}",
                help="Quantity of work redone due to defects"
            )
            total_qty = st.number_input(
                "Total executed",
                1.0, 10000.0, 500.0,
                key=f"tot_{i}",
                help="Total executed production in same unit"
            )

            rework = rework_qty / total_qty

        with col5:
            st.markdown("### 🟣 Saturation (Hours-Based)")
            equip_avail = st.number_input(
                "Equipment available hours",
                1.0, 10000.0, 100.0,
                key=f"ea_{i}",
                help="Total available machine hours"
            )
            equip_used = st.number_input(
                "Equipment used hours",
                0.0, 10000.0, 80.0,
                key=f"eu_{i}",
                help="Actual working machine hours"
            )

            man_avail = st.number_input(
                "Manpower available hours",
                1.0, 10000.0, 100.0,
                key=f"ma_{i}",
                help="Total workforce hours available"
            )
            man_used = st.number_input(
                "Manpower used hours",
                0.0, 10000.0, 85.0,
                key=f"mu_{i}",
                help="Actual worked hours"
            )

            logistics = st.slider(
                "Logistic congestion",
                0, 10, 3,
                key=f"log_{i}",
                help="0 = smooth logistics, 10 = severe congestion"
            )

            E = min(equip_used / equip_avail, 1.2)
            M = min(man_used / man_avail, 1.2)
            L = logistics / 10

            saturation = 0.4*E + 0.4*M + 0.2*L

        # =========================
        # PRODUCTIVITY
        # =========================
        col6, col7 = st.columns(2)

        with col6:
            st.markdown("### 🟢 Equipment Productivity")
            output_e = st.number_input(
                "Actual output (equipment)",
                0.0, 100000.0, 500.0,
                key=f"oe_{i}",
                help="Production achieved (m3, ton, m, etc.)"
            )
            rate_e = st.number_input(
                "Standard rate (equipment)",
                0.1, 1000.0, 10.0,
                key=f"re_{i}",
                help="Expected production per hour"
            )

            PI_e = output_e / (rate_e * equip_used) if equip_used > 0 else 0

        with col7:
            st.markdown("### 🟢 Manpower Productivity")
            output_m = st.number_input(
                "Actual output (manpower)",
                0.0, 100000.0, 500.0,
                key=f"om_{i}",
                help="Production achieved by workforce"
            )
            rate_m = st.number_input(
                "Standard rate (manpower)",
                0.1, 1000.0, 8.0,
                key=f"rm_{i}",
                help="Expected output per hour"
            )

            PI_m = output_m / (rate_m * man_used) if man_used > 0 else 0

        PI_total = 0.5 * PI_e + 0.5 * PI_m

        # =========================
        # VALUE
        # =========================
        st.markdown("### ⚫ Value / Impact")

        col8, col9, col10, col11 = st.columns(4)

        with col8:
            contract = st.slider("Contract weight", 1, 10, 5,
                help="Relative importance of project in portfolio")
        with col9:
            delay = st.slider("Delay impact (days)", 0, 100, 10,
                help="Potential delay impact in days")
        with col10:
            client = st.slider("Client criticality", 1, 10, 5,
                help="Client sensitivity / visibility")
        with col11:
            cost = st.slider("Cost exposure", 1, 10, 5,
                help="Financial risk level")

        value = 0.3*contract + 0.3*(delay/10) + 0.2*client + 0.2*cost

        # =========================
        # SIGMA
        # =========================
        sigma = (
            1.2*incomplete +
            1.5*interference +
            1.0*priority_index +
            2.0*rework +
            1.3*saturation +
            1.5*(1 - PI_total)
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

        actions_map = {
            "Incomplete": ["Reduce WIP", "Close open tasks", "Limit fronts"],
            "Interference": ["Resequence work", "Separate crews", "Fix logistics"],
            "Priority": ["Freeze plan", "Reduce changes"],
            "Rework": ["Stop work", "Increase QC", "Review method"],
            "Saturation": ["Reduce load", "Add resources", "Remove bottlenecks"],
            "Productivity Loss": ["Improve methods", "Train team", "Increase supervision"]
        }

        actions = actions_map[main_driver]

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
    st.header("📊 Portfolio Ranking")
    st.dataframe(df, use_container_width=True)

    top = df.iloc[0]

    st.header("🎯 Decision Focus")

    st.metric("Project", top["Project"])
    st.metric("Sigma", round(top["Sigma"], 2))
    st.metric("Priority", round(top["Priority"], 2))
    st.metric("Main Issue", top["Driver"])
    st.metric("Productivity", round(top["PI"], 2))

    st.markdown("### Recommended Actions")
    for a in top["Actions"].split(","):
        st.write(f"- {a}")

else:
    st.info("Insert project data to start analysis")
