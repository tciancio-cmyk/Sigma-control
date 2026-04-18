import streamlit as st
import pandas as pd

# DEBUG IMPORT
try:
    from engine.kpi import flow, rework_index, saturation, productivity, DEFINITIONS
    from engine.model import value, sigma, priority_score
    from engine.decision import diagnose

    st.success("✅ All imports OK")

except Exception as e:
    st.error(f"❌ Import error: {e}")
    st.stop()   
    
st.set_page_config(layout="wide")
st.title("Construction Portfolio Control – Sigma Engine")

st.markdown("""
### Model Logic
This system evaluates construction performance through:
- Flow stability
- Quality
- Resource saturation (hours-based)
- Productivity

Output:
- Sigma (instability)
- Priority (where to act)
- Root cause + actions
""")

n = st.number_input("Number of Projects", 1, 10, 2)

results = []

for i in range(int(n)):

    st.markdown("---")
    name = st.text_input("Project Name", key=f"name_{i}")

    if not name:
        continue

    st.markdown(f"## {name}")

    c1, c2, c3 = st.columns(3)

    with c1:
        planned = st.number_input("Planned", 1, 1000, 100, key=f"p_{i}", help=DEFINITIONS["planned"])
        open_t = st.number_input("Open", 0, 500, 10, key=f"o_{i}", help=DEFINITIONS["open"])
        blocked = st.number_input("Blocked", 0, 500, 5, key=f"b_{i}", help=DEFINITIONS["blocked"])
        reopened = st.number_input("Reopened", 0, 500, 2, key=f"r_{i}", help=DEFINITIONS["reopened"])

    with c2:
        interferences = st.number_input("Interferences", 0, 100, 5, key=f"int_{i}", help=DEFINITIONS["interferences"])
        workfronts = st.number_input("Workfronts", 1, 50, 10, key=f"wf_{i}", help=DEFINITIONS["workfronts"])

    with c3:
        changes = st.number_input("Changes", 0, 50, 3, key=f"ch_{i}", help=DEFINITIONS["changes"])

    c4, c5 = st.columns(2)

    with c4:
        rework_qty = st.number_input("Rework qty", 0.0, 10000.0, 50.0, key=f"rw_{i}", help=DEFINITIONS["rework_qty"])
        total_qty = st.number_input("Total qty", 1.0, 10000.0, 500.0, key=f"tot_{i}", help=DEFINITIONS["total_qty"])

    with c5:
        equip_avail = st.number_input("Equip avail h", 1.0, 10000.0, 100.0, key=f"ea_{i}", help=DEFINITIONS["equip_avail"])
        equip_used = st.number_input("Equip used h", 0.0, 10000.0, 80.0, key=f"eu_{i}", help=DEFINITIONS["equip_used"])
        man_avail = st.number_input("Man avail h", 1.0, 10000.0, 100.0, key=f"ma_{i}", help=DEFINITIONS["man_avail"])
        man_used = st.number_input("Man used h", 0.0, 10000.0, 85.0, key=f"mu_{i}", help=DEFINITIONS["man_used"])
        logistics = st.slider("Logistics", 0, 10, 3, key=f"log_{i}", help=DEFINITIONS["logistics"])

    c6, c7 = st.columns(2)

    with c6:
        output_e = st.number_input("Output E", 0.0, 100000.0, 500.0, key=f"oe_{i}", help=DEFINITIONS["output_e"])
        rate_e = st.number_input("Rate E", 0.1, 1000.0, 10.0, key=f"re_{i}", help=DEFINITIONS["rate_e"])

    with c7:
        output_m = st.number_input("Output M", 0.0, 100000.0, 500.0, key=f"om_{i}", help=DEFINITIONS["output_m"])
        rate_m = st.number_input("Rate M", 0.1, 1000.0, 8.0, key=f"rm_{i}", help=DEFINITIONS["rate_m"])

    c8, c9, c10, c11 = st.columns(4)

    with c8:
        contract = st.slider("Contract", 1, 10, 5, key=f"c_{i}", help=DEFINITIONS["contract"])
    with c9:
        delay = st.slider("Delay", 0, 100, 10, key=f"d_{i}", help=DEFINITIONS["delay"])
    with c10:
        client = st.slider("Client", 1, 10, 5, key=f"cl_{i}", help=DEFINITIONS["client"])
    with c11:
        cost = st.slider("Cost", 1, 10, 5, key=f"co_{i}", help=DEFINITIONS["cost"])

    # ENGINE
    incomplete, interference, priority = flow(planned, open_t, blocked, reopened, interferences, workfronts, changes)
    rework = rework_index(rework_qty, total_qty)
    sat = saturation(equip_used, equip_avail, man_used, man_avail, logistics)

    PI_e = productivity(output_e, rate_e, equip_used)
    PI_m = productivity(output_m, rate_m, man_used)
    PI = 0.5*(PI_e + PI_m)

    val = value(contract, delay, client, cost)
    sig = sigma(incomplete, interference, priority, rework, sat, PI)
    prio = priority_score(sig, val)

    driver, actions = diagnose(incomplete, interference, priority, rework, sat, PI)

    results.append({
        "Project": name,
        "Sigma": sig,
        "Priority": prio,
        "Driver": driver,
        "Productivity": PI,
        "Actions": ", ".join(actions)
    })

if results:
    df = pd.DataFrame(results).sort_values(by="Priority", ascending=False)

    st.markdown("---")
    st.header("Portfolio Ranking")
    st.dataframe(df, use_container_width=True)

    top = df.iloc[0]

    st.header("Decision Focus")
    st.metric("Project", top["Project"])
    st.metric("Sigma", round(top["Sigma"], 2))
    st.metric("Priority", round(top["Priority"], 2))
    st.metric("Main Issue", top["Driver"])

    st.markdown("### Actions")
    for a in top["Actions"].split(","):
        st.write(f"- {a}")
