import streamlit as st

def show(get_history_func, save_history_func, get_user_func):
    st.title("Academic Analytics Engine")
    
    calc_tab, target_tab, analytics_tab = st.tabs([
        "Multi-Semester Calculator", "Target Engine", "Performance Analytics"
    ])
    
    grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    user = get_user_func(st.session_state.username)
    current_level = user["current_level"] if user else "100L"

    try:
        user_level_num = int(current_level.replace("L", ""))
    except:
        user_level_num = 100

    all_semesters_pool = [
        {"level": 100, "term": "First Semester"}, {"level": 100, "term": "Second Semester"},
        {"level": 200, "term": "First Semester"}, {"level": 200, "term": "Second Semester"},
        {"level": 300, "term": "First Semester"}, {"level": 300, "term": "Second Semester"},
        {"level": 400, "term": "First Semester"}, {"level": 400, "term": "Second Semester"}
    ]

    with calc_tab:
        num_semesters = st.number_input("Number of Semesters to Calculate", min_value=1, max_value=8, value=1, step=1)
        
        running_total_qp = 0.0
        running_total_cu = 0
        
        for s in range(int(num_semesters)):
            if s >= len(all_semesters_pool): break
            sem_info = all_semesters_pool[s]
            sem_level = sem_info["level"]
            sem_term = sem_info["term"]

            level_difference = (user_level_num - sem_level) // 100
            start_year = 2025 - level_difference
            end_year = 2026 - level_difference
            predicted_session = f"{start_year}/{end_year}"

            display_label = f"{sem_level}L - {sem_term} ({predicted_session} Session)"

            with st.expander(display_label, expanded=True):
                num_courses = st.number_input(f"Number of Courses", min_value=1, max_value=15, value=4, step=1, key=f"num_crs_{s}")
                sem_qp, sem_cu = 0.0, 0
                
                for c in range(int(num_courses)):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1: st.text_input("Course Code", placeholder="CHM101", key=f"code_{s}_{c}")
                    with col2: units = st.number_input("Units", min_value=1, max_value=6, value=3, step=1, key=f"units_{s}_{c}")
                    with col3: grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key=f"grade_{s}_{c}")
                    
                    sem_qp += units * grade_points[grade]
                    sem_cu += units
                
                if sem_cu > 0:
                    st.markdown(f"**Semester GPA:** `{sem_qp / sem_cu:.2f}` | **Units:** `{sem_cu}`")
                running_total_qp += sem_qp
                running_total_cu += sem_cu

        st.divider()
        if running_total_cu > 0:
            final_cgpa = running_total_qp / running_total_cu
            c1, c2, c3 = st.columns(3)
            c1.metric("Cumulative Units (CU)", running_total_cu)
            c2.metric("Total Quality Points (QP)", running_total_qp)
            c3.metric("Calculated CGPA", f"{final_cgpa:.2f}")
            
            label = st.text_input("Record Name/Label:", placeholder="e.g. 200L Finished Standings")
            if st.button("Save Record Tracking Line", use_container_width=True):
                save_history_func(st.session_state.username, final_cgpa, final_cgpa, running_total_cu, running_total_qp, label if label else "Manual Calculation Log")
                st.success("Calculations synchronized successfully.")
                st.rerun()
