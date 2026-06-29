import streamlit as st

def show(get_history_func, save_history_func, get_user_func):
    # COSMAS PERSISTENT BANNER
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px;">COSMAS AT SUG TOP SEAT</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-family: sans-serif;">Support • Pray • Canvass</p>
        </div>
        """, unsafe_allow_html=True)

    st.title("Academic Analytics Engine")
    
    calc_tab, target_tab, analytics_tab = st.tabs([
        "Multi-Semester Calculator", "Target Engine", "Performance Analytics"
    ])
    
    grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    
    # Fetch User Profile Data
    user = get_user_func(st.session_state.username)
    current_level_str = user["current_level"] if user and "current_level" in user else "100L"
    user_display_name = user["fullname"] if user and "fullname" in user else "Student User"
    user_matric_display = user["matric_no"] if user and "matric_no" in user else "N/A"

    try:
        profile_level_num = int(current_level_str.replace("L", ""))
    except:
        profile_level_num = 100

    # Fetch saved history records from DB to determine level completion states
    history_records = get_history_func(st.session_state.username)
    
    saved_levels = set()
    history_qp_map = {}
    history_cu_map = {}
    
    if history_records:
        for record in history_records:
            label = record[5].lower() if record[5] else ""
            if "100l" in label:
                saved_levels.add(100)
                history_qp_map[100] = float(record[4]) if len(record) > 4 else float(record[2]) * int(record[3])
                history_cu_map[100] = int(record[3])
            elif "200l" in label:
                saved_levels.add(200)
                history_qp_map[200] = float(record[4]) if len(record) > 4 else float(record[2]) * int(record[3])
                history_cu_map[200] = int(record[3])
            elif "300l" in label:
                saved_levels.add(300)
                history_qp_map[300] = float(record[4]) if len(record) > 4 else float(record[2]) * int(record[3])
                history_cu_map[300] = int(record[3])

    with calc_tab:
        st.markdown(f"### 🎯 Session Performance Core Workspace")
        st.caption(f"Currently tracking up to your profile state (**{current_level_str}**). Manage entries below.")

        cumulative_qp = 0.0
        cumulative_cu = 0
        all_calculated_courses_log = []

        target_render_levels = [100]
        if profile_level_num >= 200: target_render_levels.append(200)
        if profile_level_num >= 300: target_render_levels.append(300)
        if profile_level_num >= 400: target_render_levels.append(400)

        for lvl in target_render_levels:
            is_saved_in_db = lvl in saved_levels
            
            if is_saved_in_db:
                status_color = "#22c55e"  
                status_text = "🟢 Completed & Saved in History"
                bg_style = "rgba(34, 197, 94, 0.1)"
            else:
                status_color = "#ef4444"  
                status_text = "🔴 Empty / Session Record Unfilled"
                bg_style = "rgba(239, 68, 68, 0.08)"

            st.markdown(f"""
            <div style="background-color: {bg_style}; border-left: 5px solid {status_color}; padding: 12px 15px; border-radius: 4px; margin-top: 15px; margin-bottom: 5px;">
                <span style="font-weight: bold; font-size: 1.1rem; color: white;">{lvl}L Session Container Block</span>
                <span style="float: right; font-size: 0.9rem; color: {status_color}; font-weight: bold;">{status_text}</span>
            </div>
            """, unsafe_allow_html=True)

            if is_saved_in_db:
                use_stored = st.checkbox(f"Use database saved historical records for {lvl}L calculations", value=True, key=f"db_check_{lvl}")
                if use_stored:
                    cumulative_qp += history_qp_map[lvl]
                    cumulative_cu += history_cu_map[lvl]
                    st.info(f"Loaded {lvl}L from database: `{history_cu_map[lvl]} Units` | Cumulative GPA Base applied.")
                    continue 

            with st.expander(f"Edit/Fill {lvl}L Course Evaluation Registry Matrix", expanded=not is_saved_in_db):
                num_semesters = st.number_input(f"Semesters to compute for {lvl}L", min_value=1, max_value=2, value=2, step=1, key=f"sem_count_{lvl}")
                
                lvl_qp = 0.0
                lvl_cu = 0
                
                for sem_idx in range(int(num_semesters)):
                    sem_term_str = "First Semester" if sem_idx == 0 else "Second Semester"
                    st.markdown(f"**{lvl}L - {sem_term_str}**")
                    
                    num_courses = st.number_input(f"Number of Courses", min_value=1, max_value=15, value=3, step=1, key=f"num_crs_{lvl}_{sem_idx}")
                    
                    for c in range(int(num_courses)):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            # --- CHANGED PLACEHOLDER TO BE COMPLETELY NEUTRAL ---
                            code = st.text_input("Course Code", placeholder="Enter Course Code", key=f"code_{lvl}_{sem_idx}_{c}")
                        with col2:
                            units = st.number_input("Units", min_value=1, max_value=6, value=3, step=1, key=f"units_{lvl}_{sem_idx}_{c}")
                        with col3:
                            grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key=f"grade_{lvl}_{sem_idx}_{c}")
                        
                        lvl_qp += units * grade_points[grade]
                        lvl_cu += units
                        
                        all_calculated_courses_log.append({
                            "semester_label": f"{lvl}L - {sem_term_str}",
                            "code": code if code.strip() else "UNNAMED",
                            "units": units,
                            "grade": grade,
                            "level": lvl
                        })

                if lvl_cu > 0 and not is_saved_in_db:
                    st.markdown(f"📊 **Current Workspace Tally for {lvl}L:** GPA: `{lvl_qp/lvl_cu:.2f}` | Credit Units: `{lvl_cu}` (Don't forget to save below!)")
                
                if lvl_cu > 0:
                    if st.button(f"Save & Lock {lvl}L Record Line to Database", key=f"save_btn_{lvl}", use_container_width=True):
                        st.balloons()
                        save_history_func(
                            st.session_state.username,
                            lvl_qp / lvl_cu,
                            lvl_qp / lvl_cu,
                            lvl_cu,
                            lvl_qp,
                            f"{lvl}L Official Standing Record"
                        )
                        st.success(f"{lvl}L metrics saved to database successfully! Reloading status engine...")
                        st.rerun()

                cumulative_qp += lvl_qp
                cumulative_cu += lvl_cu

        st.divider()

        if cumulative_cu > 0:
            final_cgpa = cumulative_qp / cumulative_cu
            
            st.markdown("### 📊 Overall Global Academic Standings Matrix")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Cumulative Units (CU)", cumulative_cu)
            c2.metric("Total Quality Points (QP)", cumulative_qp)
            c3.metric("Overall Calculated CGPA", f"{final_cgpa:.2f}")

            st.markdown("<br>", unsafe_allow_html=True)
            document_text = f"""==================================================
COSMAS ACADEMIC WORKSPACE REPORT
==================================================
Verified Evaluation Performance Sheet
Generated for: {user_display_name}
Matric Number: {user_matric_display}
Current Profile Standing: {current_level_str}

--------------------------------------------------
COMPUTED ACADEMIC MATRIX READOUT:
--------------------------------------------------
* TOTAL CREDIT UNITS: {cumulative_cu} Units
* TOTAL QUALITY PTS : {cumulative_qp:.2f}
* OVERALL CGPA      : {final_cgpa:.2f}

--------------------------------------------------
COURSE REGISTER PROFILE BREAKDOWN:
--------------------------------------------------
"""
            current_sem_heading = ""
            for course in all_calculated_courses_log:
                if course["semester_label"] != current_sem_heading:
                    current_sem_heading = course["semester_label"]
                    document_text += f"\n[{current_sem_heading}]\n"
                document_text += f"  - {course['code'].upper()}: Units: {course['units']} | Grade: {course['grade']}\n"

            document_text += f"""
--------------------------------------------------
CAMPUS ADVOCACY MANDATE PROMISE:
--------------------------------------------------
This report tool is brought to you courtesy of the 
Cosmas Leadership Mobilization Campaign Initiative.

★ SUPPORT • PRAY • CANVASS ★
A New Era of Student Leadership Excellence Begins.
👉 VOTE FOR COSMAS FOR SUG TOP SEAT!
==================================================
Powered by Cosmas and Team
==================================================
"""
            st.download_button(
                label="Download Complete Certified Multi-Session Report (TXT)",
                data=document_text,
                file_name=f"Cosmas_Global_CGPA_Report.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("Fill out your course metrics breakdown within any of the session container panels above to view your unified graduation CGPA calculation.")

    # TARGET ENGINE TIMELINE
    with target_tab:
        st.subheader("🎯 Cosmas Target Engine Optimization Hub")
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            current_cgpa_input = st.number_input("Your Current CGPA Base", min_value=0.0, max_value=5.0, value=3.0, step=0.01)
            total_units_passed = st.number_input("Total Credit Units Completed So Far", min_value=1, value=40, step=1)
        with t_col2:
            target_cgpa_goal = st.number_input("Your Target/Goal CGPA", min_value=0.0, max_value=5.0, value=4.5, step=0.01)
            upcoming_units_load = st.number_input("Total Credit Units to Take Next Semester", min_value=1, value=24, step=1)
            
        if st.button("Run Projection Matrix Target", type="primary", use_container_width=True):
            current_points = current_cgpa_input * total_units_passed
            combined_units_goal = total_units_passed + upcoming_units_load
            required_total_points = target_cgpa_goal * combined_units_goal
            needed_semester_points = required_total_points - current_points
            required_semester_gpa = needed_semester_points / upcoming_units_load
            
            st.markdown("---")
            if required_semester_gpa > 5.0:
                st.error(f"Mathematically out of reach! To hit {target_cgpa_goal:.2f}, you would need a semester GPA of **{required_semester_gpa:.2f}**.")
            elif required_semester_gpa < 0.0:
                st.success(f"You are already way ahead! You need a GPA of less than 0.00 to keep your target balance.")
            else:
                st.info(f"Target Acquired! To reach your target CGPA of **{target_cgpa_goal:.2f}** at the end of next semester, you need to hit an average GPA of **{required_semester_gpa:.2f}** across your next {upcoming_units_load} units.")

    # HISTORY ANALYTICS VISUALIZER
    with analytics_tab:
        st.subheader("📈 Performance Analytics Dashboard")
        if history_records and len(history_records) > 0:
            import pandas as pd
            data_points = [{"Index": idx + 1, "Label Pin": item[5] if item[5] else f"Run {idx+1}", "CGPA Tracking Line": float(item[2]), "Units Done": int(item[3])} for idx, item in enumerate(history_records)]
            df = pd.DataFrame(data_points)
            st.dataframe(df[["Label Pin", "CGPA Tracking Line", "Units Done"]], use_container_width=True)
            st.line_chart(data=df, x="Label Pin", y="CGPA Tracking Line")
        else:
            st.warning("No tracking records saved to the database history yet.")
