import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Construction Portfolio Control – Sigma Engine (Engineering Model)")

# -------------------------
# NUMERO CANTIERI
# -------------------------
num_projects = st.number_input(
    "Number of Projects",
    min_value=1,
    max_value=10,
    value=2,
    help="Numero totale di cantieri da analizzare"
)

projects = []

# -------------------------
# LOOP PROGETTI
# -------------------------
for i in range(int(num_projects)):

    st.markdown("---")
    name = st.text_input(f"Project {i+1}", key=f"name_{i}", help="Nome cantiere / progetto")

    if name:

        st.markdown(f"## {name}")

        # =========================
        # RIGA 1 – PRODUZIONE / FLUSSO
        # =========================
        col1, col2, col3 = st.columns(3)

        # -------- INCOMPLETE --------
        with col1:
            st.markdown("### Incomplete Index")
            planned = st.number_input(
                "Planned",
                1, 1000, 100,
                key=f"p_{i}",
                help="Numero attività pianificate nel periodo (giorno/settimana)"
            )
            open_t = st.number_input(
                "Open",
                0, 500, 10,
                key=f"o_{i}",
                help="Attività iniziate ma non completate"
            )
            blocked = st.number_input(
                "Blocked",
                0, 500, 5,
                key=f"b_{i}",
                help="Attività ferme per vincoli (accesso, materiali, approvazioni)"
            )
            reopened = st.number_input(
                "Reopened",
                0, 500, 2,
                key=f"r_{i}",
                help="Attività riaperte per errori o difetti"
            )

            incomplete = (open_t + blocked + reopened) / planned

        # -------- INTERFERENCE --------
        with col2:
            st.markdown("### Interference Index")
            interferences = st.number_input(
                "Interferences",
                0, 100, 5,
                key=f"int_{i}",
                help="Numero di conflitti operativi tra squadre o attività"
            )
            workfronts = st.number_input(
                "Workfronts",
                1, 50, 10,
                key=f"wf_{i}",
                help="Numero di fronti attivi contemporaneamente"
            )

            interference = interferences / workfronts

        # -------- PRIORITY --------
        with col3:
            st.markdown("### Priority Instability")
            changes = st.number_input(
                "Unplanned changes",
                0, 50, 3,
                key=f"ch_{i}",
                help="Numero modifiche non pianificate al programma"
            )

            priority_index = changes / planned

        # =========================
        # RIGA 2 – QUALITÀ / RISORSE / VALORE
        # =========================
        col4, col5, col6 = st.columns(3)

        # -------- REWORK --------
        with col4:
            st.markdown("### Rework Index")
            rework_qty = st.number_input(
                "Rework qty",
                0.0, 10000.0, 50.0,
                key=f"rw_{i}",
                help="Quantità di lavoro rifatto (m3, m2, ton, ecc.)"
            )
            total_qty = st.number_input(
                "Total executed",
                1.0, 10000.0, 500.0,
                key=f"tot_{i}",
                help="Produzione totale eseguita nello stesso periodo"
            )

            rework = rework_qty / total_qty

        # -------- SATURATION --------
        with col5:
            st.markdown("### Resource Saturation")
            equipment = st.slider(
                "Equipment %",
                0, 120, 80,
                key=f"eq_{i}",
                help="Utilizzo macchine critiche (%)"
            )
            manpower = st.slider(
                "Manpower %",
                0, 120, 85,
                key=f"mp_{i}",
                help="Utilizzo forza lavoro (%)"
            )
            logistics = st.slider(
                "Logistics",
                0, 10, 3,
                key=f"log_{i}",
                help="Congestione logistica (0 = fluido, 10 = critico)"
            )

            saturation = 0.4*(equipment/100) + 0.4*(manpower/100) + 0.2*(logistics/10)

        # -------- VALUE --------
        with col6:
            st.markdown("### Value / Impact")
            contract = st.slider(
                "Contract weight",
                1, 10, 5,
                key=f"c_{i}",
                help="% importanza del contratto nel portfolio"
            )
            delay = st.slider(
                "Delay impact",
                0, 100, 10,
                key=f"d_{i}",
                help="Giorni di ritardo potenziale"
            )
            client = st.slider(
                "Client criticality",
                1, 10, 5,
                key=f"cl_{i}",
                help="Sensibilità cliente / visibilità progetto"
            )
            cost = st.slider(
                "Cost exposure",
                1, 10, 5,
                key=f"co_{i}",
                help="Rischio economico associato"
            )

            value = 0.3*contract + 0.3*(delay/10) + 0.2*client + 0.2*cost

        # =========================
        # SIGMA
        # =========================
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

        priority_score = sigma * value

        projects.append({
            "Project": name,
            "Sigma": sigma,
            "Value": value,
            "Priority": priority_score,
            "Incomplete": incomplete,
            "Interference": interference,
            "Rework": rework,
            "Saturation": saturation
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

    colA, colB, colC = st.columns(3)

    colA.metric("Critical Project", top["Project"])
    colB.metric("Sigma", round(top["Sigma"], 2))
    colC.metric("Priority", round(top["Priority"], 2))

    if top["Sigma"] < 1:
        st.success("STABLE")
    elif top["Sigma"] < 2:
        st.warning("ATTENTION")
    else:
        st.error("CRITICAL")

    # Breakdown
    st.header("Sigma Breakdown")

    breakdown = {
        "Incomplete": top["Incomplete"],
        "Interference": top["Interference"],
        "Rework": top["Rework"],
        "Saturation": top["Saturation"]
    }

    st.bar_chart(pd.DataFrame.from_dict(breakdown, orient="index"))

else:
    st.info("Insert at least one project")
