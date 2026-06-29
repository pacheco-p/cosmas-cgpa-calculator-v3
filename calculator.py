import streamlit as st

def show(get_history_func, save_history_func, get_user_func):
    # CLEAN, FRIENDLY CAMPUS BANNER
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <h2 style="color: white; margin: 0; font-family: 'Segoe UI', system-ui, sans-serif; font-weight: 800; letter-spacing: 1px;">COSMAS FOR SUG TOP SEAT</h2>
            <p style="color: #dbeafe; margin: 5px 0 0 0; font-family: 'Segoe UI', sans-serif; font-size: 1rem; font-weight: 500;">Support • Pray • Canvass</p>
        </div>
        """, unsafe_allow_html=True)

    st.title("CGPA Calculator & Tracker")
    st.markdown("Calculate your GPA across semesters, track your progress, and set your graduation targets easily.")
    
    calc_tab, target_tab, analytics_tab = st.tabs([
        "🧮 Calculate GPA", "🎯 Set Target Goal", "📈 View Progress History"
    ])
    
    grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    
    # Fetch User Profile Data
    user = get_user_func(st.session_state.username)
    current_level_str = user["current_level"] if user and "current_level" in user else "100L"
    user_display_name = user["fullname"] if user and "fullname" in user else "Student"
    user_matric_display = user["matric_no"] if user and "matric_no" in user else ""

    try:
        profile_level_num = int(current_level_str.replace("L", ""))
    except:
        profile_level_num = 100

    # Fetch saved history records from DB
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
        st.subheader("Your Semester Workspace")
        
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
                status_text = "🟢 Saved & Done"
                bg_style = "rgba(34, 197, 94, 0.08)"
            else:
                status_color = "#ef4444"  
                status_text = "🔴 Not Filled Yet"
                bg_style = "rgba(239, 68, 68, 0.05)"

            st.markdown(f"""
            <div style="background-color: {bg_style}; border-left: 4px solid {status_color}; padding: 10px 15px; border-radius: 6px; margin-top: 15px; margin-bottom: 5px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 700; font-size: 1rem; color: white;">{lvl} Level Courses</span>
                <span style="font-size: 0.85rem; color: {status_color}; font-weight: 700;">{status_text}</span>
            </div>
            """, unsafe_allow_html=True)

            if is_saved_in_db:
                use_stored = st.checkbox(f"Use saved {lvl}L data from history", value=True, key=f"db_check_{lvl}")
                if use_stored:
                    cumulative_qp += history_qp_map[lvl]
                    cumulative_cu += history_cu_map[lvl]
                    st.caption(f"✓ Using saved history: {history_cu_map[lvl]} Units loaded automatically.")
                    continue 

            with st.expander(f"Click here to type your {lvl}L courses", expanded=not is_saved_in_db):
                num_semesters = st.radio(f"How many semesters are you entering for {lvl}L?", [1, 2], index=1, horizontal=True, key=f"sem_count_{lvl}")
                
                lvl_qp = 0.0
                lvl_cu = 0
                
                for sem_idx in range(int(num_semesters)):
                    sem_title = "1st Semester" if sem_idx == 0 else "2nd Semester"
                    st.markdown(f"🔹 **{sem_title}**")
                    
                    # Track row counts dynamically per semester section
                    state_key = f"row_count_{lvl}_{sem_idx}"
                    if state_key not in st.session_state:
                        st.session_state[state_key] = 1  # Always defaults to 1 row automatically!
                    
                    # Generate dynamic rows
                    for c in range(st.session_state[state_key]):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            code = st.text_input("Course Code", placeholder="Enter Course Code", key=f"code_{lvl}_{sem_idx}_{c}", label_visibility="collapsed")
                        with col2:
                            units = st.number_input("Units", min_value=1, max_value=6, value=3, step=1, key=f"units_{lvl}_{sem_idx}_{c}")
                        with col3:
                            grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key=f"grade_{lvl}_{sem_idx}_{c}")
                        
                        lvl_qp += units * grade_points[grade]
                        lvl_cu += units
                        
                        all_calculated_courses_log.append({
                            "semester_label": f"{lvl}L - {sem_title}",
                            "code": code if code.strip() else "Course",
                            "units": units,
                            "grade": grade,
                            "level": lvl
                        })
                    
                    # Clean add button underneath rows
                    if st.button(f"➕ Add Another Course Row ({sem_title})", key=f"add_btn_{lvl}_{sem_idx}"):
                        st.session_state[state_key] += 1
                        st.rerun()
                        
                    st.markdown("<br>", unsafe_allow_html=True)

                if lvl_cu > 0 and not is_saved_in_db:
                    current_gpa = lvl_qp / lvl_cu
                    st.success(f"📝 {lvl}L Current Entry: **GPA: {current_gpa:.2f}** | **Total Units: {lvl_cu}**")
                    
                    if st.button(f"Save & Lock {lvl}L Results", key=f"save_btn_{lvl}", use_container_width=True):
                        st.balloons()
                        save_history_func(
                            st.session_state.username,
                            current_gpa,
                            current_gpa,
                            lvl_cu,
                            lvl_qp,
                            f"{lvl}L Record"
                        )
                        st.success("Saved! Updating your dashboard status...")
                        st.rerun()

                cumulative_qp += lvl_qp
                cumulative_cu += lvl_cu

        st.divider()

        if cumulative_cu > 0:
            final_cgpa = cumulative_qp / cumulative_cu
            
            st.markdown("### 📊 Your Overall Standings")
            c1, c2 = st.columns(2)
            c1.metric("Total Credit Units Passed", f"{cumulative_cu} Units")
            c2.metric("Your Calculated Cumulative CGPA", f"{final_cgpa:.2f}")

            st.markdown("<br>", unsafe_allow_html=True)
            document_text = f"""==================================================
COSMAS ACADEMIC WORKSPACE REPORT
==================================================
Name: {user_display_name}
Matric Number: {user_matric_display}

Summary Findings:
* TOTAL UNITS EARNED: {cumulative_cu}
* OVERALL CGPA      : {final_cgpa:.2f}

Course Breakdown:
"""
            current_sem_heading = ""
            for course in all_calculated_courses_log:
                if course["semester_label"] != current_sem_heading:
                    current_sem_heading = course["semester_label"]
                    document_text += f"\n[{current_sem_heading}]\n"
                document_text += f"  - {course['code'].upper()}: {course['units']} Units | Grade: {course['grade']}\n"

            document_text += f"""
--------------------------------------------------
★ SUPPORT • PRAY • CANVASS ★
👉 VOTE FOR COSMAS FOR SUG TOP SEAT!
==================================================
"""
            st.download_button(
                label="📥 Download My Result Sheet (TXT)",
                data=document_text,
                file_name=f"My_CGPA_Report.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("Open any of the level rows above and enter your courses to calculate your total graduation CGPA automatically!")

    # TARGET ENGINE TIMELINE
    with target_tab:
        st.subheader("🎯 Set Your Graduation Target Goal")
        st.markdown("Find out exactly what GPA you need to hit next semester to reach your target goal.")
        
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            current_cgpa_input = st.number_input("What is your current CGPA right now?", min_value=0.0, max_value=5.0, value=3.5, step=0.01)
            total_units_passed = st.number_input("Total credit units completed so far?", min_value=1, value=60, step=1)
        with t_col2:
            target_cgpa_goal = st.number_input("What is your target/goal CGPA?", min_value=0.0, max_value=5.0, value=4.0, step=0.01)
            upcoming_units_load = st.number_input("Total credit units you are taking next semester?", min_value=1, value=20, step=1)
            
        if st.button("Calculate Needed GPA Target", type="primary", use_container_width=True):
            current_points = current_cgpa_input * total_units_passed
            combined_units_goal = total_units_passed + upcoming_units_load
            required_total_points = target_cgpa_goal * combined_units_goal
            needed_semester_points = required_total_points - current_points
            required_semester_gpa = needed_semester_points / upcoming_units_load
            
            st.markdown("---")
            if required_semester_gpa > 5.0:
                st.error(f"Mathematically impossible this semester! To hit a {target_cgpa_goal:.2f} CGPA, you would need a semester GPA of {required_semester_gpa:.2f}.")
            elif required_semester_gpa < 0.0:
                st.success(f"Easy win! You are already ahead of your goal. You'll maintain it even with low scores.")
            else:
                st.info(f"Target Acquired! To hit your goal of **{target_cgpa_goal:.2f}**, you need to get an average GPA of **{required_semester_gpa:.2f}** in your courses next semester.")

    # HISTORY ANALYTUALS VISUALIZER
    with analytics_tab:
        st.subheader("📈 Your Progress Chart")
        if history_records and len(history_records) > 0:
            import pandas as pd
            data_points = [{"Semester": item[5] if item[5] else f"Saved Record {idx+1}", "CGPA": float(item[2])} for idx, item in enumerate(history_records)]
            df = pd.DataFrame(data_points)
            st.line_chart(data=df, x="Semester", y="CGPA")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("You haven't saved any semester history metrics yet. Go to the calculation tab and hit 'Save & Lock' to start mapping your chart.")
