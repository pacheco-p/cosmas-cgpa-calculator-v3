import streamlit as st

def show(get_history_func, save_history_func, get_user_profile_func):
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px;">COSMAS AT SUG TOP SEAT</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-family: sans-serif;">Support • Pray • Canvass</p>
        </div>
        """, unsafe_allow_html=True)

    st.title("GPA & CGPA Calculator Suite")
    st.markdown("Input your current semester values below to compute target metrics and save progress logs.")

    user_info = get_user_profile_func(st.session_state.username)

    # Initialize dynamic session containers for calculation row iterations
    if "num_courses" not in st.session_state:
        st.session_state.num_courses = 5

    col_controls = st.columns([1, 1, 3])
    with col_controls[0]:
        if st.button("➕ Add Course Row"):
            st.session_state.num_courses += 1
    with col_controls[1]:
        if st.button("➖ Remove Row") and st.session_state.num_courses > 1:
            st.session_state.num_courses -= 1

    course_data = []
    grade_scale = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}

    st.markdown("---")
    
    # Render interactive input configuration rows
    for i in range(st.session_state.num_courses):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            c_name = st.text_input(f"Course Code/Title {i+1}", key=f"c_name_{i}", placeholder="e.g., CHM 301")
        with col2:
            c_units = st.number_input(f"Units {i+1}", min_value=1, max_value=6, value=3, key=f"c_units_{i}")
        with col3:
            c_grade = st.selectbox(f"Grade {i+1}", list(grade_scale.keys()), key=f"c_grade_{i}")
        course_data.append((c_name, c_units, c_grade))

    st.markdown("---")

    col_calc_left, col_calc_right = st.columns([1, 1])
    
    with col_calc_left:
        st.subheader("Previous Academic Standings")
        prev_cgpa = st.number_input("Previous Cumulative CGPA", min_value=0.0, max_value=5.0, value=0.0, step=0.01)
        prev_units = st.number_input("Previous Total Earned Units", min_value=0, value=0, step=1)

    with col_calc_right:
        st.subheader("Save Configuration Metadata")
        semester_label = st.text_input("Semester / Level Label Pin", placeholder="e.g., 300L First Semester")

    if st.button("Compute Performance Summary Metrics", type="primary", use_container_width=True):
        total_current_units = sum(row[1] for row in course_data)
        total_quality_points = sum(row[1] * grade_scale[row[2]] for row in course_data)
        
        current_gpa = total_quality_points / total_current_units if total_current_units > 0 else 0.0
        
        # Calculate overall unified CGPA metric standing
        combined_units = prev_units + total_current_units
        combined_points = (prev_cgpa * prev_units) + total_quality_points
        current_cgpa = combined_points / combined_units if combined_units > 0 else current_gpa

        st.success(f"Calculation complete!")
        
        # Render visual metrics breakdown readout cards
        c1, c2, c3 = st.columns(3)
        c1.metric("Computed Semester GPA", f"{current_gpa:.2f}")
        c2.metric("New Cumulative CGPA", f"{current_cgpa:.2f}")
        c3.metric("Total Combined Units Completed", f"{combined_units} Units")

        # Automatically store inside local memory cache for file generating steps
        st.session_state.last_calc = {
            "gpa": current_gpa,
            "cgpa": current_cgpa,
            "units": combined_units,
            "qp": combined_points,
            "label": semester_label if semester_label.strip() else "Unlabeled Semester",
            "courses": course_data
        }

        if semester_label.strip():
            save_history_func(
                st.session_state.username,
                current_gpa,
                current_cgpa,
                combined_units,
                combined_points,
                semester_label
            )
            st.info("Performance entries successfully saved and synchronized to your history matrix timeline!")

    # Dynamic Branded Download Section
    if "last_calc" in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); padding: 20px; border-radius: 10px; border: 1px dashed #4338ca; text-align: center;">
                <h4 style="color: #ffffff; margin-top: 0; font-family: sans-serif;">📥 Download Your Verified Academic Document</h4>
                <p style="color: #94a3b8; font-size: 13px; margin-bottom: 15px;">Generate an official statement summary containing your calculated scores with campaign certification credentials.</p>
            </div>
            """, unsafe_allow_html=True)
        
        calc = st.session_state.last_calc
        user_display_name = user_info['fullname'] if user_info else "Student User"
        user_matric_display = user_info['matric_no'] if user_info else "N/A"
        
        # Building the formatted text document data payload
        document_text = f"""==================================================
COSMAS ACADEMIC WORKSPACE REPORT
==================================================
Verified Evaluation Performance Sheet
Generated for: {user_display_name}
Matric Number: {user_matric_display}
Target/Semester Window: {calc['label']}

--------------------------------------------------
COMPUTED ACADEMIC MATRIX READOUT:
--------------------------------------------------
* SEMESTER GPA      : {calc['gpa']:.2f}
* CUMULATIVE CGPA   : {calc['cgpa']:.2f}
* TOTAL CREDIT UNITS: {calc['units']} Units
* TOTAL QUALITY PTS : {calc['qp']:.2f}

--------------------------------------------------
COURSE INPUT REGISTER PROFILE:
--------------------------------------------------
"""
        for item in calc['courses']:
            c_title = item[0] if item[0].strip() else "Unnamed Course"
            document_text += f"- {c_title.upper()}: (Units: {item[1]}, Earned Grade: {item[2]})\n"
            
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
            file_name=f"Cosmas_CGPA_Report_{calc['label'].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
