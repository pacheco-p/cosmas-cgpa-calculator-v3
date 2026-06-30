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
    
    # Initialize session state for holding the current course list queue
    if "course_queue" not in st.session_state:
        st.session_state.course_queue = []

    level_map = ["100 LEVEL", "200 LEVEL", "300 LEVEL", "400 LEVEL", "500 LEVEL"]

    # --- AUTOMATIC BACKGROUND HISTORY LOADING ---
    user_history = get_history_func(st.session_state.username)
    
    auto_prev_units = 0
    auto_prev_qp = 0.0

    # Determine automated level and semester staging
    if not user_history:
        current_level = "100 LEVEL"
        current_semester = "1st Semester"
    else:
        latest_record = user_history[-1]
        # Check if the last record was only a first semester checkpoint
        if "1st Semester Only" in str(latest_record[5]):
            current_level = str(latest_record[5]).split(" - ")[0]
            current_semester = "2nd Semester"
            # Carry over background stats from preceding completed levels if any exist
            if len(user_history) > 1:
                auto_prev_units = int(user_history[-2][3])
                auto_prev_qp = float(user_history[-2][4])
        else:
            # Previous level is fully finalized; move up
            completed_levels = len(user_history)
            if completed_levels < len(level_map):
                current_level = level_map[completed_levels]
            else:
                current_level = f"Extra Level {completed_levels + 1}"
            current_semester = "1st Semester"
            auto_prev_units = int(latest_record[3])
            auto_prev_qp = float(latest_record[4])

    with calc_tab:
        # --- PREVIOUS ACADEMIC RECORD SECTION ---
        st.subheader("Academic Workspace Profile")
        st.markdown(f"📍 Current Session Panel: **⚡ {current_level} ({current_semester})**")
        
        if auto_prev_units > 0:
            st.caption(f"ℹ️ *Background Engine loaded previous running totals: {auto_prev_units} Units / {auto_prev_qp} QP.*")
        else:
            st.caption("ℹ️ *Starting fresh from 100 Level 1st Semester entry.*")
            
        st.divider()
        
        # --- CURRENT COURSE INPUT PANEL ---
        st.markdown("### Add New Course")
        
        course_code = st.text_input("Course Code", placeholder="Enter Course Code", key="input_course_code")
        
        col_cu, col_gr = st.columns(2)
        with col_cu:
            credit_units = st.number_input("Credit Units", min_value=1, max_value=6, value=3, step=1, key="input_credit_units")
        with col_gr:
            grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key="input_grade")
            
        # Add Course Button Logic
        if st.button("➕ Add Course", key="add_course_to_queue_btn"):
            display_code = course_code.strip().upper() if course_code.strip() else "COURSE"
            st.session_state.course_queue.append({
                "code": display_code,
                "units": credit_units,
                "grade": grade,
                "qp": credit_units * grade_points[grade]
            })
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # --- DISPLAY ADDED COURSES QUEUE PANEL ---
        if not st.session_state.course_queue:
            st.info(f"No courses listed in this active term panel yet.")
        else:
            st.markdown("#### Current Entries Summary")
            
            for idx, item in enumerate(st.session_state.course_queue):
                q_col1, q_col2, q_col3, q_col4 = st.columns([2, 1, 1, 1])
                q_col1.markdown(f"**{item['code']}**")
                q_col2.write(f"{item['units']} Units")
                q_col3.write(f"Grade: {item['grade']}")
                if q_col4.button("🗑️ Remove", key=f"remove_{idx}"):
                    st.session_state.course_queue.pop(idx)
                    st.rerun()
            
            if st.button("❌ Clear All Courses", key="clear_all_queue"):
                st.session_state.course_queue = []
                st.rerun()

        st.divider()

        # --- AUTOMATED MATHEMATICS MATRIX ENGINE ---
        current_qp = sum(item["qp"] for item in st.session_state.course_queue)
        current_cu = sum(item["units"] for item in st.session_state.course_queue)

        if current_cu > 0:
            current_gpa_calc = current_qp / current_cu
            
            if current_semester == "1st Semester":
                total_cumulative_qp = auto_prev_qp + current_qp
                total_cumulative_cu = auto_prev_units + current_cu
                display_cgpa = total_cumulative_qp / total_cumulative_cu
            else:
                # 2nd Semester looks back at the temporary 1st semester record metrics
                first_sem_qp = float(latest_record[4])
                first_sem_cu = int(latest_record[3])
                
                total_cumulative_qp = first_sem_qp + current_qp
                total_cumulative_cu = first_sem_cu + current_cu
                display_cgpa = total_cumulative_qp / total_cumulative_cu
            
            st.markdown("### 📊 Semester Computations")
            c1, c2 = st.columns(2)
            c1.metric("Semester Credit Units", f"{current_cu} Units")
            c2.metric("Calculated Semester GPA", f"{current_gpa_calc:.2f}")
            
            if current_semester == "2nd Semester":
                st.markdown(f"⚡ **Combined Running Level CGPA:** `{display_cgpa:.2f}` (Total: {total_cumulative_cu} Units Completed)")

            if st.button("💾 Save Performance to History Log", use_container_width=True):
                st.balloons()
                
                if current_semester == "1st Semester":
                    save_label = f"{current_level} - 1st Semester Only"
                    save_history_func(
                        st.session_state.username,
                        current_gpa_calc,        # Single Semester GPA column
                        current_gpa_calc,        # CGPA slot tracking running value
                        total_cumulative_cu,     
                        total_cumulative_qp,     
                        save_label
                    )
                else:
                    final_label = f"{current_level} Finalized"
                    save_history_func(
                        st.session_state.username,
                        current_gpa_calc,        # 2nd Semester GPA
                        display_cgpa,            # The structural level CGPA blend
                        total_cumulative_cu,     
                        total_cumulative_qp,     
                        final_label
                    )
                    
                st.success(f"{current_level} metrics committed successfully!")
                st.session_state.course_queue = [] 
                st.rerun()
        else:
            st.info(f"Add courses taken during your {current_level} {current_semester} to generate calculations.")

    # TARGET ENGINE TIMELINE
    with target_tab:
        st.subheader("🎯 Set Your Graduation Target Goal")
        st.markdown("Find out exactly what GPA you need to hit next semester to reach your target goal.")
        
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            default_target_cgpa = (auto_prev_qp / auto_prev_units) if auto_prev_units > 0 else 3.5
            default_target_units = auto_prev_units if auto_prev_units > 0 else 60

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
        st.subheader("📈 Your Progress Chart")
        if user_history and len(user_history) > 0:
            data_points = [{"Entry Point": item[5] if item[5] else f"Saved Record {idx+1}", "Semester GPA": float(item[1]), "CGPA": float(item[2])} for idx, item in enumerate(user_history)]
            df = pd.DataFrame(data_points)
            st.line_chart(data=df, x="Entry Point", y="CGPA")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("You haven't saved any semester history metrics yet.")
