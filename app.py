for i in range(int(num_projects)):

    st.subheader(f"Project {i+1}")

    name = st.text_input(f"Project Name {i+1}", key=f"name_{i}")

    if name:

        col1, col2, col3 = st.columns(3)

        with col1:
            incomplete = st.number_input(f"Incomplete {name}", 0, 100, 10)

        with col2:
            interference = st.number_input(f"Interference {name}", 0, 50, 5)

        with col3:
            changes = st.number_input(f"Changes {name}", 0, 20, 3)

        col4, col5 = st.columns(2)

        with col4:
            rework = st.number_input(f"Rework % {name}", 0.0, 100.0, 10.0)

        with col5:
            saturation = st.number_input(f"Saturation % {name}", 0.0, 120.0, 85.0)

        # CALCOLO SIGMA QUI
