def diagnose(incomplete, interference, priority, rework, saturation, PI):
    """
    Identify main driver and suggest actions
    """

    drivers = {
        "Incomplete": incomplete,
        "Interference": interference,
        "Priority": priority,
        "Rework": rework,
        "Saturation": saturation,
        "Productivity Loss": (1 - PI)
    }

    main = max(drivers, key=drivers.get)

    actions_map = {
        "Incomplete": [
            "Reduce WIP",
            "Close open tasks",
            "Limit workfronts"
        ],
        "Interference": [
            "Resequence activities",
            "Separate crews",
            "Optimize logistics"
        ],
        "Priority": [
            "Freeze short-term plan",
            "Limit changes"
        ],
        "Rework": [
            "Stop critical work",
            "Increase QC",
            "Review method"
        ],
        "Saturation": [
            "Reduce workload",
            "Add targeted resources",
            "Remove bottlenecks"
        ],
        "Productivity Loss": [
            "Improve execution methods",
            "Train workforce",
            "Increase supervision"
        ]
    }

    return main, actions_map[main]
