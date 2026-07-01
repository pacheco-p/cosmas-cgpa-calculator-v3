import streamlit as st
import pandas as pd

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
    
    calc_tab, target_tab, analytics_tab = st.tabs([
        "🧮 Calculate GPA", "🎯 Set Target Goal", "📈 View Progress History"
    ])
    
    grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    
    # Initialize workspace session states
    if "course_queue" not in st.session_state:
        st.session_state.course_queue = []
    if "last_added_success" not in st.session_state:
        st.session_state.last_added_success = None
    if "course_code_value" not in st.session_state:
        st.session_state.course_code_value = ""

    # --- CHRONOLOGICAL SEMESTER TIMELINE MAPPING ---
    semester_map = [
        "100L - 1st Semester", "100L - 2nd Semester",
        "200L - 1st Semester", "200L - 2nd Semester",
        "300L - 1st Semester", "300L - 2nd Semester",
        "400L - 1st Semester", "400L - 2nd Semester",
        "500L - 1st Semester", "500L - 2nd Semester"
    ]
    
    # Fetch user save rows
    user_history = get_history_func(st.session_state.username)
    saved_count = len(user_history) if user_history else 0
    
    # Determine what semester label to assign this workspace session
    if saved_count < len(semester_map):
        current_semester_label = semester_map[saved_count]
    else:
        current_semester_label = f"Extra Semester (Row {saved_count + 1})"

    # --- AUTOMATIC BACKGROUND MATH ACCUMULATION ---
    auto_prev_units = 0
    auto_prev_qp = 0.0
    
    if saved_count > 0:
        try:
            auto_prev_units = int(user_history[-1][3])
            auto_prev_qp = float(user_history[-1][4])
        except (ValueError, IndexError):
            pass

    with calc_tab:
        # --- CURRENT CHRONOLOGICAL TARGET ANNOUNCEMENT ---
        st.subheader("Academic Workspace Profile")
        st.markdown(f"📍 Currently processing calculation for: **⚡ {current_semester_label}**")
        
        if auto_prev_units > 0:
            st.caption(f"ℹ️ *Background Engine loaded your previous cumulative standings automatically ({auto_prev_units} Units total from previous semesters).*")
        else:
            st.caption("ℹ️ *Starting fresh from 100Level 1st Semester entry.*")
            
        st.divider()
        
        # --- CURRENT COURSE INPUT PANEL ---
        st.markdown("### Add New Course")
        
        course_code = st.text_input(
            "Course Code", 
            value=st.session_state.course_code_value,
            placeholder="Enter Course Code", 
            key="input_course_code"
        )
        
        col_cu, col_gr = st.columns(2)
        with col_cu:
            credit_units = st.number_input("Credit Units", min_value=1, max_value=6, value=3, step=1, key="input_credit_units")
        with col_gr:
            grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key="input_grade")
            
        if st.button("➕ Add Course", key="add_course_to_queue_btn"):
            display_code = course_code.strip().upper() if course_code.strip() else "COURSE CODE"
            st.session_state.course_queue.append({
                "code": display_code,
                "units": credit_units,
                "grade": grade,
                "qp": credit_units * grade_points[grade]
            })
            
            # Update success status text banner
            st.session_state.last_added_success = f"✅ {display_code} added successfully."
            
            # Clear input bar field context
            st.session_state.course_code_value = ""
            st.rerun()

        if st.session_state.last_added_success:
            st.success(st.session_state.last_added_success)

        st.divider()

        # --- MATH ENGINE CORRELATION ---
        current_qp = sum(item["qp"] for item in st.session_state.course_queue)
        current_cu = sum(item["units"] for item in st.session_state.course_queue)
        
        total_cumulative_qp = auto_prev_qp + current_qp
        total_cumulative_cu = auto_prev_units + current_cu

        # Fallback tracking variables to prevent UI crashes during deletions
        current_gpa_calc = 0.0
        final_cgpa = (auto_prev_qp / auto_prev_units) if auto_prev_units > 0 else 0.0

        # --- LIVE GPA DISPLAY STANDINGS ---
        if current_cu > 0:
            current_gpa_calc = current_qp / current_cu
            final_cgpa = total_cumulative_qp / total_cumulative_cu
            
            c1, c2 = st.columns(2)
            c1.metric("Semester GPA", f"{current_gpa_calc:.2f}")
            c2.metric("Cumulative CGPA", f"{final_cgpa:.2f}")

            # Class Tier System Display
            if 4.50 <= final_cgpa <= 5.00:
                st.success("🏆 First Class")
            elif 3.50 <= final_cgpa < 4.50:
                st.success("🥈 Second Class Upper")
            elif 2.40 <= final_cgpa < 3.50:
                st.warning("🥉 Second Class Lower")
            elif 1.50 <= final_cgpa < 2.40:
                st.error("📋 Third Class")
            else:
                st.error("⚠️ Pass / Probation")
        else:
            st.info(f"Start adding courses taken during your **{current_semester_label}** to see real-time GPA computations.")

        st.divider()

        # --- COURSES DATAFRAME LOOP WORKSPACE ---
        st.markdown("### Courses Worksheet")
        if not st.session_state.course_queue:
            st.info("No courses listed in this active term panel yet.")
        else:
            df_data = [{
                "Course": item["code"],
                "Credit Units": item["units"],
                "Grade": item["grade"],
                "Quality Points": item["qp"]
            } for item in st.session_state.course_queue]
            
            course_df = pd.DataFrame(df_data)
            st.dataframe(course_df, use_container_width=True)
            
            # Deletion Line Selection Menu
            st.markdown("**Delete Course**")
            course_options = [item["code"] for item in st.session_state.course_queue]
            selected_to_delete = st.selectbox("Select course line item to wipe out", options=course_options, label_visibility="collapsed")
            
            if st.button("Delete Line", key="execute_deletion_btn"):
                for idx, item in enumerate(st.session_state.course_queue):
                    if item["code"] == selected_to_delete:
                        st.session_state.course_queue.pop(idx)
                        break
                st.session_state.last_added_success = None  
                st.rerun()
                
            st.divider()

            # --- SAVE COMPACT PROGRESSION ROW ACTION ---
           if st.button("💾 Save Result", use_container_width=True):
    st.balloons()

    save_history_func(
        st.session_state.username,
        current_gpa_calc,
        final_cgpa,
        total_cumulative_cu,
        total_cumulative_qp,
        current_semester_label
    )

    st.success(f"{current_semester_label} metrics committed to your ledger successfully!")

    st.session_state.course_queue = []
    st.session_state.last_added_success = None
    st.session_state.course_code_value = ""

    st.rerun()

            # Export options
            csv_file = course_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV Transcript Snapshot",
                data=csv_file,
                file_name=f"{current_semester_label.replace(' ', '_')}_grades.csv",
                mime="text/csv",
                use_container_width=True
            )

    # TARGET ENGINE TIMELINE
    with target_tab:
        st.subheader("🎯 Set Your Graduation Target Goal")
        st.markdown("Find out exactly what GPA you need to hit next semester to reach your target goal.")
        
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            default_target_cgpa = (auto_prev_qp / auto_prev_units) if auto_prev_units > 0 else 3.5
            default_target_units = auto_prev_units if auto_prev_units > 0 else 30

            current_cgpa_input = st.number_input("What is your current CGPA right now?", min_value=0.0, max_value=5.0, value=default_target_cgpa, step=0.01, key="target_curr_cgpa")
            total_units_passed = st.number_input("Total credit units completed so far?", min_value=1, value=default_target_units, step=1, key="target_units_passed")
        with t_col2:
            target_cgpa_goal = st.number_input("What is your target/goal CGPA?", min_value=0.0, max_value=5.0, value=4.0, step=0.01, key="target_goal_cgpa")
            upcoming_units_load = st.number_input("Total credit units you are taking next semester?", min_value=1, value=20, step=1, key="target_upcoming_load")
            
        if st.button("Calculate Needed GPA Target", type="primary", use_container_width=True, key="run_target_calc_engine"):
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

    # HISTORY ANALYTICS VISUALIZER
    with analytics_tab:
        st.subheader("📈 Semester Progress History")
        if user_history and len(user_history) > 0:
            data_points = [{"Semester": item[5] if item[5] else f"Record {idx+1}", "CGPA": float(item[2]), "Semester GPA": float(item[1])} for idx, item in enumerate(user_history)]
            df = pd.DataFrame(data_points)
            
            st.line_chart(data=df, x="Semester", y="CGPA")
            st.markdown("#### Chronological Transcript Ledger")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("You haven't saved any semester history metrics yet.")
