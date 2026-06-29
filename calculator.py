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
        all_calculated_courses_log = [] # Tracked list container to build the document download string
        
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
                    
                    # Log active rows into data dictionary
                    all_calculated_courses_log.append({
                        "semester_label": display_label,
                        "code": code if code.strip() else "UNNAMED",
                        "units": units,
                        "grade": grade
                    })
                
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

            # BRANDED DOCUMENT DOWNLOAD COMPONENT
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); padding: 20px; border-radius: 10px; border: 1px dashed #4338ca; text-align: center;">
                    <h4 style="color: #ffffff; margin-top: 0; font-family: sans-serif;">📥 Download Your Verified Academic Document</h4>
                    <p style="color: #94a3b8; font-size: 13px; margin-bottom: 0px;">Generate an official summary breakdown report featuring Cosmas campaign verification badges.</p>
                </div>
                """, unsafe_allow_html=True)

            final_label = label.strip() if label.strip() else "Multi-Semester Evaluation"
            
            # Construct formatted text payload layout
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

    # Placeholders for targets and analytics views
    with target_tab:
        st.subheader("Target Engine Optimization Hub")
        st.markdown("Set milestones to project what grade points you require in your upcoming sessions.")

    with analytics_tab:
        st.subheader("Performance Analytics Graphing Center")
        st.markdown("Visual charts mapping out your long term GPA trends will generate here.")
