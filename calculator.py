import streamlit as st

def show(get_history_func, save_history_func):
    st.title("🎓 Academic Analytics Engine")
    
    # Matching top tab configuration from screenshot
    calc_tab, target_tab, analytics_tab = st.tabs([
        "📊 Multi-Semester Calculator", 
        "🎯 Target Engine", 
        "📈 Performance Analytics"
    ])
    
    # Grading reference point layout 
    grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}

    with calc_tab:
        # Counter line tracking layout
        num_semesters = st.number_input("Number of Semesters to Calculate", min_value=1, max_value=12, value=1, step=1)
        
        running_total_qp = 0.0
        running_total_cu = 0
        
        for s in range(int(num_semesters)):
            with st.expander(f"📘 Semester {s+1} Configuration", expanded=True):
                num_courses = st.number_input(f"Number of Courses (Semester {s+1})", min_value=1, max_value=20, value=4, step=1, key=f"num_crs_{s}")
                
                sem_qp = 0.0
                sem_cu = 0
                
                # Dynamic inputs loop
                for c in range(int(num_courses)):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.text_input("Course Code", placeholder="e.g., CHM101", key=f"code_{s}_{c}")
                    with col2:
                        units = st.number_input("Units", min_value=1, max_value=6, value=3, step=1, key=f"units_{s}_{c}")
                    with col3:
                        grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key=f"grade_{s}_{c}")
                    
                    sem_qp += units * grade_points[grade]
                    sem_cu += units
                
                # Semester computations display
                if sem_cu > 0:
                    sem_gpa = sem_qp / sem_cu
                    st.markdown(f"**Semester {s+1} GPA:** `{sem_gpa:.2f}` | **Units Registered:** `{sem_cu}`")
                    
                running_total_qp += sem_qp
                running_total_cu += sem_cu

        # Summary Computation Metrics Block
        st.divider()
        if running_total_cu > 0:
            final_cgpa = running_total_qp / running_total_cu
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Cumulative Units (CU)", running_total_cu)
            c2.metric("Total Quality Points (QP)", running_total_qp)
            c3.metric("Calculated CGPA", f"{final_cgpa:.2f}")
            
            label = st.text_input("Provide a label to log this record:", placeholder="e.g., 200L First Semester Split")
            if st.button("💾 Save to System History Log", use_container_width=True):
                save_history_func(st.session_state.username, final_cgpa, final_cgpa, running_total_cu, running_total_qp, label if label else "Multi-Term Split")
                st.success("Calculation successfully added to timeline historical logs!")
                st.rerun()

    with target_tab:
        st.subheader("🎯 Goal Optimization Engine")
        st.write("Determine the metrics required in upcoming terms to reach your graduation targets.")
        # Target calculator elements can go here

    with analytics_tab:
        st.subheader("📈 Performance Breakdown Analytics")
        st.info("Visual breakdowns of historic scores will display here once metrics load.")
