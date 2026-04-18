from config import WEIGHTS

def value(contract, delay, client, cost):
    """
    Project importance based on:
    - contract weight
    - delay exposure
    - client sensitivity
    - cost risk
    """
    return 0.3*contract + 0.3*(delay/10) + 0.2*client + 0.2*cost


def sigma(incomplete, interference, priority, rework, saturation, PI):
    """
    Global instability index
    """
    return (
        WEIGHTS["incomplete"] * incomplete +
        WEIGHTS["interference"] * interference +
        WEIGHTS["priority"] * priority +
        WEIGHTS["rework"] * rework +
        WEIGHTS["saturation"] * saturation +
        WEIGHTS["productivity"] * (1 - PI)
    )


def priority_score(sigma, value):
    """Decision priority"""
    return sigma * value
