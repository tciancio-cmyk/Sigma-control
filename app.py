import streamlit as st

st.title("Construction Portfolio Control – Director Level")

projects = ["Project A", "Project B", "Project C", "Project D"]

results = []

for p in projects:
    st.header(p)

    col1, col2 = st.columns(2)

    with col1:
        sigma = st.slider(f"Sigma {p}", 0.0, 10.0, 3.0)

    with col2:
        value = st.slider(f"Value / Impact {p}", 1.0, 10.0, 5.0)

    priority = sigma * value

    results.append({
        "project": p,
        "sigma": sigma,
        "value": value,
        "priority": priority
    })

# -------------------------
# GLOBAL RANKING
# -------------------------
st.header("Priority Ranking")

sorted_results = sorted(results, key=lambda x: x["priority"], reverse=True)

for r in sorted_results:
    st.write(
        f"{r['project']} → Priority: {round(r['priority'],2)} "
        f"(σ={r['sigma']}, V={r['value']})"
    )

# -------------------------
# DECISION
# -------------------------
top = sorted_results[0]

st.header("Action Focus")

st.metric("Critical Project", top["project"])
st.metric("Priority Score", round(top["priority"], 2))

if top["sigma"] < 3:
    st.success("LOW RISK → Monitor")
elif top["sigma"] < 6:
    st.warning("MEDIUM RISK → Stabilize")
else:
    st.error("HIGH RISK → Immediate Intervention")
