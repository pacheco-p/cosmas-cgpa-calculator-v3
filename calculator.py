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
    user = get_user_func(st.session_state.username)
    current_level = user["current_level"] if user else "100L"
    user_display_name = user["fullname"] if user else "Student User"
    user_matric_display = user["matric_no"] if user else "N/A"

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
        all_calculated_courses_log = []
        
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
                    with col1: 
                        code = st.text_input("Course Code", placeholder="CHM101", key=f"code_{s}_{c}")
                    with col2: 
                        units = st.number_input("Units", min_value=1, max_value=6, value=3, step=1, key=f"units_{s}_{c}")
                    with col3: 
                        grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key=f"grade_{s}_{c}")
                    
                    sem_qp += units * grade_points[grade]
                    sem_cu += units
                    
                    all_calculated_courses_log.append({
                        "semester_label": display_label,
                        "code": code if code.strip() else "UNNAMED",
                        "units": units,
                        "grade": grade,
                        "level": sem_level
                    })
                
                if sem_cu > 0:
                    st.markdown(f"**Semester GPA:** `{sem_qp / sem_cu:.2f}` | **Units:** `{sem_cu}`")
                running_total_qp += sem_qp
                running_total_cu += sem_cu

        st.markdown("### Previous Academic Standings (Editable)")
        col_prev_1, col_prev_2 = st.columns(2)
        with col_prev_1:
            # Fixed variable handling so you can go back and edit without errors
            prev_cgpa_val = st.number_input("Input/Edit Previous CGPA", min_value=0.0, max_value=5.0, value=0.0, step=0.01, key="editable_prev_cgpa")
        with col_prev_2:
            prev_units_val = st.number_input("Input/Edit Total Earned Units before this session", min_value=0, value=0, step=1, key="editable_prev_units")

        st.divider()
        
        # Incorporate previous standings if inputted
        if prev_units_val > 0:
            running_total_qp += (prev_cgpa_val * prev_units_val)
            running_total_cu += prev_units_val

        if running_total_cu > 0:
            final_cgpa = running_total_qp / running_total_cu
            c1, c2, c3 = st.columns(3)
            c1.metric("Cumulative Units (CU)", running_total_cu)
            c2.metric("Total Quality Points (QP)", running_total_qp)
            c3.metric("Calculated CGPA", f"{final_cgpa:.2f}")
            
            # Level Up Congratulatory Logic Check
            highest_calculated_level = max([c["level"] for c in all_calculated_courses_log]) if all_calculated_courses_log else 100
            if highest_calculated_level == 100 and running_total_cu > 12:
                st.balloons()
                st.markdown(f"""
                <div style="background-color: #1e3a8a; border-left: 5px solid #3b82f6; padding: 15px; border-radius: 4px; margin: 15px 0;">
                    <h4 style="color: white; margin: 0;">🎉 100Level Completed!</h4>
                    <p style="color: #93c5fd; margin: 5px 0 0 0;">Successfully moved to the next level. Let's keep building the academic momentum under Cosmas' leadership mandate!</p>
                </div>
                """, unsafe_allow_html=True)

            label = st.text_input("Record Name/Label:", placeholder="e.g. 100L Finished Standings")
            
            if st.button("Save Record Tracking Line", use_container_width=True):
                save_history_func(st.session_state.username, final_cgpa, final_cgpa, running_total_cu, running_total_qp, label if label else "Manual Calculation Log")
                st.success("Calculations synchronized successfully.")
                st.rerun()

            # BRANDED DOCUMENT DOWNLOAD COMPONENT
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); padding: 20px; border-radius: 10px; border: 1px dashed #4338ca; text-align: center;">
                    <h4 style="color: #ffffff; margin-top: 0; font-family: sans-serif;">📥 Download Your Verified Academic Document</h4>
                    <p style="color: #94a3b8; font-size: 13px; margin-bottom: 0px;">Generate an official summary breakdown report featuring Cosmas campaign verification badges.</p>
                </div>
                """, unsafe_allow_html=True)

            final_label = label.strip() if label.strip() else "Multi-Semester Evaluation"
            
            document_text = f"""==================================================
COSMAS ACADEMIC WORKSPACE REPORT
==================================================
Verified Evaluation Performance Sheet
Generated for: {user_display_name}
Matric Number: {user_matric_display}
Record Context: {final_label}

--------------------------------------------------
COMPUTED ACADEMIC MATRIX READOUT:
--------------------------------------------------
* TOTAL CREDIT UNITS: {running_total_cu} Units
* TOTAL QUALITY PTS : {running_total_qp:.2f}
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
                label="Download Certified Result Document (TXT)",
                data=document_text,
                file_name=f"Cosmas_CGPA_Report_{final_label.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ACTIVE TARGET ENGINE COMPONENT
    with target_tab:
        st.subheader("🎯 Cosmas Target Engine Optimization Hub")
        st.markdown("Calculate exactly what grades you need in your upcoming semesters to hit your dream graduation class.")
        
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            current_cgpa_input = st.number_input("Your Current CGPA", min_value=0.0, max_value=5.0, value=3.0, step=0.01)
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
                st.error(f"Mathematically out of reach! To hit {target_cgpa_goal:.2f}, you would need a semester GPA of **{required_semester_gpa:.2f}**, which is above the 5.00 limit. Aim for an achievable layout or increase your upcoming load context!")
            elif required_semester_gpa < 0.0:
                st.success(f"You are already way ahead! You need a GPA of less than 0.00 to keep your target balance. Keep cruising!")
            else:
                st.info(f"Target Acquired! To reach your target CGPA of **{target_cgpa_goal:.2f}** at the end of next semester, you need to hit an average GPA of **{required_semester_gpa:.2f}** across your next {upcoming_units_load} units.")
                st.markdown("### Suggested Campaign Advice:")
                st.write("Stay disciplined, make clean study schedules, and let's win together with Cosmas and Team!")

    # ACTIVE PERFORMANCE ANALYTICS HISTORY TRACKER
    with analytics_tab:
        st.subheader("📈 Performance Analytics Dashboard")
        st.markdown("Your saved history line records visualized over time.")
        
        history_records = get_history_func(st.session_state.username)
        
        if history_records and len(history_records) > 0:
            import pandas as pd
            
            # Format history list data elements into structured frame rows
            data_points = []
            for idx, item in enumerate(history_records):
                data_points.append({
                    "Index": idx + 1,
                    "Label Pin": item[5] if item[5] else f"Record Run {idx+1}",
                    "CGPA Tracking Line": float(item[2]),
                    "Units Done": int(item[3])
                })
            
            df = pd.DataFrame(data_points)
            
            # Display tracking metrics data grid table views
            st.dataframe(df[["Label Pin", "CGPA Tracking Line", "Units Done"]], use_container_width=True)
            st.markdown("### CGPA Progression Timeline Graphic")
            st.line_chart(data=df, x="Label Pin", y="CGPA Tracking Line")
        else:
            st.warning("No tracking records synced found in your history log yet. Compute a calculation matrix in the first tab and save your logs to unlock detailed metrics line charts here!")
