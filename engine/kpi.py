# =========================
# DEFINITIONS (Single Source of Truth)
# =========================
DEFINITIONS = {
    "planned": "Total activities planned in the period (daily/weekly baseline).",
    "open": "Activities started but not completed.",
    "blocked": "Activities stopped due to constraints (access, materials, approvals).",
    "reopened": "Activities reopened due to defects or errors.",
    "interferences": "Conflicts between crews or overlapping activities.",
    "workfronts": "Number of active parallel work areas.",
    "changes": "Unplanned changes to the execution plan.",
    "rework_qty": "Quantity of work redone due to defects.",
    "total_qty": "Total executed production in same unit.",
    "equip_avail": "Total available machine hours.",
    "equip_used": "Actual machine working hours.",
    "man_avail": "Total workforce available hours.",
    "man_used": "Actual workforce working hours.",
    "logistics": "Logistic congestion (0=fluid, 10=critical).",
    "output_e": "Actual output produced by equipment (m3, ton, m...).",
    "rate_e": "Expected production per hour (equipment).",
    "output_m": "Actual output produced by manpower.",
    "rate_m": "Expected production per hour (manpower).",
    "contract": "Relative importance of project in portfolio.",
    "delay": "Potential delay impact in days.",
    "client": "Client criticality / visibility.",
    "cost": "Financial exposure risk."
}

# =========================
# KPI CALCULATIONS
# =========================

def flow(planned, open_t, blocked, reopened, interferences, workfronts, changes):
    """
    Flow instability:
    - Incomplete: open + blocked + reopened vs planned
    - Interference: clashes per workfront
    - Priority: changes vs planned
    """
    incomplete = (open_t + blocked + reopened) / planned
    interference = interferences / workfronts
    priority = changes / planned
    return incomplete, interference, priority


def rework_index(rework_qty, total_qty):
    """Quality degradation"""
    return rework_qty / total_qty


def saturation(equip_used, equip_avail, man_used, man_avail, logistics):
    """
    Resource pressure based on:
    - Equipment usage
    - Manpower usage
    - Logistic congestion
    """
    E = min(equip_used / equip_avail, 1.2)
    M = min(man_used / man_avail, 1.2)
    L = logistics / 10
    return 0.4*E + 0.4*M + 0.2*L


def productivity(output, rate, hours):
    """
    Efficiency:
    actual output vs expected output
    """
    return output / (rate * hours) if hours > 0 else 0
