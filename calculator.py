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

    # --- AUTOMATIC BACKGROUND HISTORY LOADING ---
    user_history = get_history_func(st.session_state.username)
    auto_prev_units = 0
    auto_prev_qp = 0.0

    if user_history and len(user_history) > 0:
        latest_record = user_history[-1]
        try:
            auto_prev_units = int(latest_record[3])
            auto_prev_qp = float(latest_record[4])
        except (ValueError, IndexError):
            pass

    with calc_tab:
        # --- PREVIOUS ACADEMIC RECORD SECTION ---
        st.subheader("Previous Academic Record")
        
        if auto_prev_units > 0:
            st.caption(f"🔄 **Automatically loaded your latest saved history record ({auto_prev_units} Units background data).**")
        else:
            st.caption("No previous records found in history. Enter your past metrics below if you are in 200L or above.")

        col_prev_cu, col_prev_qp = st.columns(2)
        with col_prev_cu:
            prev_units = st.number_input("Previous Credit Units", min_value=0, value=auto_prev_units, step=1, key="prev_units_input")
        with col_prev_qp:
            prev_qp = st.number_input("Previous Quality Points", min_value=0.0, value=auto_prev_qp, step=1.0, key="prev_qp_input")
            
        st.divider()
        
        # --- CURRENT COURSE INPUT PANEL ---
        st.markdown("### Add New Course")
        course_code = st.text_input("Course Code", placeholder="Enter Course Code", key="input_course_code")
        
        col_cu, col_gr = st.columns(2)
        with col_cu:
            credit_units = st.number_input("Credit Units", min_value=1, max_value=6, value=3, step=1, key="input_credit_units")
        with col_gr:
            grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key="input_grade")
            
        # Add Course Action
        if st.button("➕ Add Course", key="add_course_to_queue_btn"):
            display_code = course_code.strip().upper() if course_code.strip() else "COURSE"
            st.session_state.course_queue.append({
                "code": display_code,
                "units": credit_units,
                "grade": grade,
                "qp": credit_units * grade_points[grade]
            })
            st.success(f"{display_code} added successfully!")
            st.rerun()

        st.divider()

        # --- MATH ENGINE ---
        current_qp = sum(item["qp"] for item in st.session_state.course_queue)
        current_cu = sum(item["units"] for item in st.session_state.course_queue)
        
        total_cumulative_qp = prev_qp + current_qp
        total_cumulative_cu = prev_units + current_cu

        # --- DYNAMIC KPIS & METRIC DISPLAY (Image 0c49b5c4) ---
        if total_cumulative_cu > 0:
            final_cgpa = total_cumulative_qp / total_cumulative_cu
            current_gpa_calc = (current_qp / current_cu) if current_cu > 0 else 0.0
            
            c1, c2 = st.columns(2)
            c1.metric("Semester GPA", f"{current_gpa_calc:.2f}")
            c2.metric("Cumulative CGPA", f"{final_cgpa:.2f}")

            # Class Tier System Logic Banner
            if 4.50 <= final_cgpa <= 5.00:
                st.success("🏆 First Class")
            elif 3.50 <= final_cgpa < 4.50:
                st.success("🥈 Second Class Upper")
            elif 2.40 <= final_cgpa < 3.50:
                st.warning("🥉 Second Class Lower")
            elif 1.50 <= final_cgpa < 2.40:
                st.error("📋 Third Class")
            else:
                st.error("⚠️ Pass / Technical Probation")
        else:
            st.info("Add running semester lines to generate standings visualization results.")

        st.divider()

        # --- COURSES DATAFRAME & SINGLE DELETION ENGINE (Image e1340bac) ---
        st.markdown("### Courses")
        if not st.session_state.course_queue:
            st.info("No courses currently in the worksheet loop.")
        else:
            # Build clean structured dataframe
            df_data = [{
                "Course": item["code"],
                "Credit Units": item["units"],
                "Grade": item["grade"],
                "Quality Points": item["qp"]
            } for item in st.session_state.course_queue]
            
            course_df = pd.DataFrame(df_data)
            st.dataframe(course_df, use_container_width=True)
            
            # Delete Course Dropdown Management Row
            st.markdown("**Delete Course**")
            course_options = [item["code"] for item in st.session_state.course_queue]
            selected_to_delete = st.selectbox("Select target course line item to remove", options=course_options, label_visibility="collapsed")
            
            if st.button("Delete", key="execute_deletion_btn"):
                for idx, item in enumerate(st.session_state.course_queue):
                    if item["code"] == selected_to_delete:
                        st.session_state.course_queue.pop(idx)
                        break
                st.rerun()
                
            st.divider()

            # --- SAVE & EXPORT BACKEND ACTIONS ---
            if st.button("💾 Save Result", use_container_width=True):
                if total_cumulative_cu > 0:
                    st.balloons()
                    save_history_func(
                        st.session_state.username,
                        final_cgpa,
                        current_gpa_calc,
                        total_cumulative_cu,
                        total_cumulative_qp,
                        f"Compiled Record ({total_cumulative_cu} CU)"
                    )
                    st.success("Standings committed to tracker ledger database successfully!")
                    st.session_state.course_queue = [] 
                    st.rerun()

            # Generate dynamic downloadable CSV payload file byte stream
            csv_file = course_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_file,
                file_name=f"academic_transcript_snapshot.csv",
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
            data_points = [{"Entry Point": item[5] if item[5] else f"Saved Record {idx+1}", "CGPA": float(item[2])} for idx, item in enumerate(user_history)]
            df = pd.DataFrame(data_points)
            st.line_chart(data=df, x="Entry Point", y="CGPA")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("You haven't saved any semester history metrics yet.")        with col_gr:
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
            st.info("No courses added yet.")
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

        # --- MATH ENGINE ---
        current_qp = sum(item["qp"] for item in st.session_state.course_queue)
        current_cu = sum(item["units"] for item in st.session_state.course_queue)
        
        total_cumulative_qp = prev_qp + current_qp
        total_cumulative_cu = prev_units + current_cu

        if total_cumulative_cu > 0:
            final_cgpa = total_cumulative_qp / total_cumulative_cu
            
            st.markdown("### 📊 Your Overall Standings")
            c1, c2 = st.columns(2)
            c1.metric("Total Credit Units Passed", f"{total_cumulative_cu} Units")
            c2.metric("Your Calculated Cumulative CGPA", f"{final_cgpa:.2f}")

            if current_cu > 0:
                current_gpa_calc = current_qp / current_cu
                st.caption(f"Current Semester Specific GPA Profile: **{current_gpa_calc:.2f}** (across {current_cu} units)")
                
                if st.button("💾 Save Session Performance to History", use_container_width=True):
                    st.balloons()
                    save_history_func(
                        st.session_state.username,
                        final_cgpa,
                        current_gpa_calc,
                        total_cumulative_cu,
                        total_cumulative_qp,
                        f"Compiled Record ({total_cumulative_cu} CU)"
                    )
                    st.success("Standings committed to tracker ledger database successfully!")
                    st.session_state.course_queue = [] # Clear queue after saving
                    st.rerun()
        else:
            st.info("Enter your cumulative parameters above or add running semester lines to generate stats visualization results.")

    # TARGET ENGINE TIMELINE
    with target_tab:
        st.subheader("🎯 Set Your Graduation Target Goal")
        st.markdown("Find out exactly what GPA you need to hit next semester to reach your target goal.")
        
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            # We can also pre-fill the target tab using their loaded history values!
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
            import pandas as pd
            data_points = [{"Entry Point": item[5] if item[5] else f"Saved Record {idx+1}", "CGPA": float(item[2])} for idx, item in enumerate(user_history)]
            df = pd.DataFrame(data_points)
            st.line_chart(data=df, x="Entry Point", y="CGPA")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("You haven't saved any semester history metrics yet.")
