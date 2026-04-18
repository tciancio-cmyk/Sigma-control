# KPI INPUT PER PROGETTO

incomplete = st.number_input(f"Incomplete tasks {name}", 0, 100, 10)
interference = st.number_input(f"Interferences {name}", 0, 50, 5)
changes = st.number_input(f"Priority changes {name}", 0, 20, 3)
rework = st.number_input(f"Rework % {name}", 0.0, 100.0, 10.0)
saturation = st.number_input(f"Saturation % {name}", 0.0, 120.0, 85.0)

# SOGLIE (baseline ingegneristica)
max_values = {
    "incomplete": 30,
    "interference": 10,
    "changes": 5,
    "rework": 20,
    "saturation": 100
}

# PESI (puoi adattarli)
weights = {
    "incomplete": 1.2,
    "interference": 1.5,
    "changes": 1.0,
    "rework": 2.0,
    "saturation": 1.3
}

# NORMALIZZAZIONE
norm_incomplete = incomplete / max_values["incomplete"]
norm_interference = interference / max_values["interference"]
norm_changes = changes / max_values["changes"]
norm_rework = rework / max_values["rework"]
norm_saturation = saturation / max_values["saturation"]

# SIGMA CALCOLATO
sigma = (
    weights["incomplete"] * norm_incomplete +
    weights["interference"] * norm_interference +
    weights["changes"] * norm_changes +
    weights["rework"] * norm_rework +
    weights["saturation"] * norm_saturation
)
