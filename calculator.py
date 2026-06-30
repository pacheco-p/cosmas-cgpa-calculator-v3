import streamlit as st
import pandas as pd

def show(get_history_func, save_history_func, get_user_func):
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
    
    if "course_queue" not in st.session_state:
        st.session_state.course_queue = []
    if "last_added_success" not in st.session_state:
        st.session_state.last_added_success = None
    if "course_code_value" not in st.session_state:
        st.session_state.course_code_value = ""

    # Clear history logic definitions
    level_map = ["100 LEVEL", "200 LEVEL", "300 LEVEL", "400 LEVEL", "500 LEVEL"]
    
    user_history = get_history_func(st.session_state.username)
    
    # Determine what level and semester we are on based on records
    # If no history, start at 100L 1st Semester. If 1st semester exists, fill 2nd Semester.
    if not user_history:
        current_level = "100 LEVEL"
        current_semester = "1st Semester"
        auto_prev_units = 0
        auto_prev_qp = 0.0
    else:
        latest_record = user_history[-1]
        # Check if the latest record is just a 1st Semester entry (meaning total units == 1st semester units)
        # For a level to be complete, both semesters must be compiled. 
        # We look at the label or check if we need to update or move to next level
        if "1st Semester Only" in str(latest_record[5]):
            current_level = str(latest_record[5]).split(" - ")[0]
            current_semester = "2nd Semester"
            # Previous units before this level started
            if len(user_history) > 1:
                auto_prev_units = int(user_history[-2][3])
                auto_prev_qp = float(user_history[-2][4])
            else:
                auto_prev_units = 0
                auto_prev_qp = 0.0
        else:
            # Current level is complete, move to next level index
            completed_levels = len(user_history)
            if completed_levels < len(level_map):
                current_level = level_map[completed_levels]
            else:
                current_level = f"Extra Level {completed_levels + 1}"
            current_semester = "1st Semester"
            auto_prev_units = int(latest_record[3])
            auto_prev_qp = float(latest_record[4])

    with calc_tab:
        st.subheader("Academic Workspace Profile")
        st.markdown(f"📍 Current Session Panel: **⚡ {current_level} ({current_semester})**")
        
        if auto_prev_units > 0:
            st.caption(f"ℹ️ *Background Engine loaded previous cumulative totals: {auto_prev_units} Units / {auto_prev_qp} QP.*")
        else:
            st.caption("ℹ️ *Starting fresh from 100 Level 1st Semester entry.*")
            
        st.divider()
        
        st.markdown("### Add New Course")
        course_code = st.text_input("Course Code", value=st.session_state.course_code_value, placeholder="e.g. CHM101", key="input_course_code")
        
        col_cu, col_gr = st.columns(2)
        with col_cu:
            credit_units = st.number_input("Credit Units", min_value=1, max_value=6, value=3, step=1, key="input_credit_units")
        with col_gr:
            grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key="input_grade")
            
        if st.button("➕ Add Course", key="add_course_to_queue_btn"):
            display_code = course_code.strip().upper() if course_code.strip() else "COURSE"
            st.session_state.course_queue.append({
                "code": display_code,
                "units": credit_units,
                "grade": grade,
                "qp": credit_units * grade_points[grade]
            })
            st.session_state.last_added_success = f"✅ {display_code} added."
            st.session_state.course_code_value = ""
            st.rerun()

        if st.session_state.last_added_success:
            st.success(st.session_state.last_added_success)

        st.divider()

        # Calculate current active workspace values
        current_qp = sum(item["qp"] for item in st.session_state.course_queue)
        current_cu = sum(item["units"] for item in st.session_state.course_queue)

        if current_cu > 0:
            current_gpa_calc = current_qp / current_cu
            
            if current_semester == "1st Semester":
                # For 1st semester, GPA and CGPA of this level match if fresh
                total_cumulative_qp = auto_prev_qp + current_qp
                total_cumulative_cu = auto_prev_units + current_cu
                display_cgpa = total_cumulative_qp / total_cumulative_cu
            else:
                # For 2nd semester, load the 1st semester's saved data to get the true level combo
                # latest_record holds the 1st semester info
                first_sem_qp = float(latest_record[4])
                first_sem_cu = int(latest_record[3])
                
                total_cumulative_qp = first_sem_qp + current_qp
                total_cumulative_cu = first_sem_cu + current_cu
                display_cgpa = total_cumulative_qp / total_cumulative_cu

            st.markdown(f"""
            <div style="margin-top: 15px; margin-bottom: 20px; font-family: sans-serif;">
                <h3 style="color: white; margin-bottom: 20px;">📊 Semester Computations</h3>
                <div style="display: flex; justify-content: space-between; align-items: flex-start; max-width: 90%;">
                    <div>
                        <span style="color: #94a3b8; font-size: 13px; display: block;">Semester Credit Units</span>
                        <span style="color: white; font-size: 32px; font-weight: bold;">{current_cu} Units</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #94a3b8; font-size: 13px; display: block;">Calculated Semester GPA</span>
                        <span style="color: white; font-size: 32px; font-weight: bold;">{current_gpa_calc:.2f}</span>
                    </div>
                </div>
                {"<p style='color: #3b82f6; font-size: 14px; margin-top: 15px;'>⚡ <b>Combined Running Level CGPA: " + f"{display_cgpa:.2f}</b></p>" if current_semester == "2nd Semester" else ""}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"Add courses taken during your {current_level} {current_semester}.")

        st.divider()

        st.markdown("### Courses Worksheet")
        if st.session_state.course_queue:
            df_data = [{"Course": item["code"], "Credit Units": item["units"], "Grade": item["grade"], "Quality Points": item["qp"]} for item in st.session_state.course_queue]
            st.dataframe(pd.DataFrame(df_data), use_container_width=True)
            
            if st.button("💾 Save Performance to History Log", use_container_width=True):
                st.balloons()
                
                if current_semester == "1st Semester":
                    # Save temporary 1st semester checkpoint row
                    save_label = f"{current_level} - 1st Semester Only"
                    save_history_func(
                        st.session_state.username,
                        current_gpa_calc,        # GPA column
                        current_gpa_calc,        # CGPA column temporarily matching
                        total_cumulative_cu,     # Combined units so far
                        total_cumulative_qp,     # Combined quality points so far
                        save_label
                    )
                else:
                    # It's 2nd semester! Overwrite or delete the temporary row and save a single unified Level row
                    # To do this seamlessly with your existing app setups, we save it with a finalized level label
                    final_label = f"{current_level} Finalized"
                    
                    # We pass the final combined CGPA to the database
                    save_history_func(
                        st.session_state.username,
                        current_gpa_calc,        # 2nd Semester GPA
                        display_cgpa,            # Unified True Cumulative CGPA for the entire level
                        total_cumulative_cu,     # Complete Level Units
                        total_cumulative_qp,     # Complete Level Quality Points
                        final_label
                    )
                    
                    # Optional: If your backend layout allows deletion, you can advise the user to remove the "1st Semester Only" row,
                    # or the code handles it natively on the History view.
                    
                st.success(f"{current_level} metadata committed successfully!")
                st.session_state.course_queue = []
                st.session_state.last_added_success = None
                st.rerun()

    with target_tab:
        st.subheader("🎯 Graduation Target Alignment")
        st.caption("Compute required GPA scores across upcoming levels.")

    with analytics_tab:
        st.subheader("📈 Transcript Profile History")
