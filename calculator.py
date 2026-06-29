import streamlit as st
import pandas as pd
import io
import database

def show():
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.title("🏛️ COSMAS AT SUG TOP SEAT")

    st.title("🎓 CGPA Calculator")

    if "courses" not in st.session_state:
        st.session_state.courses = []

    st.subheader("Select Academic Period")
    semester_options = [
        "100L - First Semester", "100L - Second Semester",
        "200L - First Semester", "200L - Second Semester",
        "300L - First Semester", "300L - Second Semester",
        "400L - First Semester", "400L - Second Semester",
        "500L - First Semester", "500L - Second Semester"
    ]
    selected_semester = st.selectbox("Which semester are you calculating for?", semester_options)

    # Automatically fetch past baselines safely
    history_data = database.get_history(st.session_state.username)
    prev_cu = 0
    prev_qp = 0.0
    
    if history_data:
        for row in history_data:
            if len(row) > 4: # Verify columns exist before adding
                prev_cu += row[3]
                prev_qp += row[4]

    st.info(f"📋 Carried Forward Baseline: {prev_cu} Credit Units | {prev_qp:.2f} Quality Points")
    st.divider()

    grades = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}

    with st.form("course_form"):
        code = st.text_input("Course Code")
        c1, c2 = st.columns(2)
        with c1:
            cu = st.number_input("Credit Units", 1, 6, 3)
        with c2:
            grade = st.selectbox("Grade", list(grades.keys()))

        add = st.form_submit_button("➕ Add Course")
        if add:
            code = code.strip().upper()
            if code == "":
                st.error("Enter a course code.")
            elif any(x["Course"] == code for x in st.session_state.courses):
                st.warning("Course already added.")
            else:
                st.session_state.courses.append({
                    "Course": code,
                    "Credit Units": cu,
                    "Grade": grade,
                    "GP": grades[grade],
                    "Quality Points": cu * grades[grade]
                })
                st.success(f"{code} added successfully.")

    if st.session_state.courses:
        df = pd.DataFrame(st.session_state.courses)
        total_cu = df["Credit Units"].sum()
        total_qp = df["Quality Points"].sum()

        semester_gpa = total_qp / total_cu
        grand_cu = prev_cu + total_cu
        grand_qp = prev_qp + total_qp
        cgpa = grand_qp / grand_cu

        st.divider()
        c1, c2 = st.columns(2)
        c1.metric(f"{selected_semester} GPA", f"{semester_gpa:.2f}")
        c2.metric("Cumulative CGPA", f"{cgpa:.2f}")

        if cgpa >= 4.50: st.success("🏆 First Class")
        elif cgpa >= 3.50: st.info("🥇 Second Class Upper")
        elif cgpa >= 2.40: st.info("🥈 Second Class Lower")
        elif cgpa >= 1.50: st.warning("🎓 Third Class")
        else: st.error("⚠️ Pass")

        st.divider()
        st.subheader("Courses added to active grid:")
        st.dataframe(df[["Course", "Credit Units", "Grade", "Quality Points"]], use_container_width=True)

        course = st.selectbox("Delete Course", df["Course"])
        if st.button("Delete"):
            st.session_state.courses = [c for c in st.session_state.courses if c["Course"] != course]
            st.rerun()

        st.divider()

        if st.button("💾 Save Result", use_container_width=True):
            database.save_history(st.session_state.username, semester_gpa, cgpa, total_cu, total_qp, selected_semester)
            st.success(f"Calculation for {selected_semester} saved.")
            st.session_state.courses = []
            st.rerun()

        st.divider()

        table_rows = "".join([
            f"<tr><td style='padding:8px; border-bottom:1px solid #ddd;'>{c['Course']}</td><td style='padding:8px; border-bottom:1px solid #ddd;'>{c['Credit Units']}</td><td style='padding:8px; border-bottom:1px solid #ddd;'>{c['Grade']}</td><td style='padding:8px; border-bottom:1px solid #ddd;'>{c['Quality Points']}</td></tr>"
            for c in st.session_state.courses
        ])
        
        html_layout = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 25px; border: 3px solid #6b21a8; border-radius: 12px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="text-align: center; background-color: #6b21a8; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">🏛️ COSMAS AT SUG TOP SEAT</h1>
                <p style="margin: 5px 0 0 0; font-style: italic; font-size: 14px;">Support • Pray • Canvass</p>
            </div>
            <div style="padding: 20px 5px; color: #333;">
                <p style="margin: 8px 0;"><b>Student Account:</b> {st.session_state.username}</p>
                <p style="margin: 8px 0;"><b>Academic Stage:</b> {selected_semester}</p>
                <hr style="border: 0; border-top: 2px solid #6b21a8; margin: 15px 0;">
                <table style="width: 100%; text-align: left; border-collapse: collapse;">
                    <thead>
                        <tr style="background-color: #f3e8ff; color: #6b21a8;">
                            <th style="padding: 10px;">Course Code</th>
                            <th style="padding: 10px;">Units</th>
                            <th style="padding: 10px;">Grade</th>
                            <th style="padding: 10px;">Quality Points</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 16px; font-weight: bold; padding: 10px 5px; background-color: #fafafa; border-radius: 6px;">
                    <span style="color: #555;">Semester GPA: {semester_gpa:.2f}</span>
                    <span style="color: #6b21a8;">Cumulative CGPA: {cgpa:.2f}</span>
                </div>
            </div>
            <div style="text-align: center; border-top: 1px solid #eee; padding-top: 15px; margin-top: 15px; font-size: 11px; color: #999;">
                Official Verification Slip • Cosmas Performance Campaign Portal
            </div>
        </div>
        """

        st.download_button(
            "📥 Download Custom Branded Print Slip (HTML)",
            html_layout,
            file_name=f"{selected_semester.replace(' ', '')}_slip.html",
            mime="text/html",
            use_container_width=True
        )
    else:
        st.info("No courses added yet.")
