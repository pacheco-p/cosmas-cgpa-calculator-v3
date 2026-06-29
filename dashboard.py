import streamlit as st
import pandas as pd

def show(get_statistics_func, get_user_func):
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px;">COSMAS AT SUG TOP SEAT</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-family: sans-serif;">Support • Pray • Canvass</p>
        </div>
        """, unsafe_allow_html=True)

    user = get_user_func(st.session_state.username)
    
    if user:
        fullname = user['fullname']
        matric_no = user['matric_no']
        department = user['department']
        current_level = user['current_level']
        
        if "returning_user" not in st.session_state:
            st.markdown(f"<h2 style='font-family: sans-serif; color: #ffffff; margin-bottom: 5px;'>Welcome, {fullname} 🎓</h2>", unsafe_allow_html=True)
            st.session_state.returning_user = True
        else:
            st.markdown(f"<h2 style='font-family: sans-serif; color: #ffffff; margin-bottom: 5px;'>Welcome back, {fullname}! 👋</h2>", unsafe_allow_html=True)
            
        st.markdown("<p style='color: #94a3b8; margin-top: 0; margin-bottom: 25px;'>Academic dashboard overview performance hub.</p>", unsafe_allow_html=True)
        
        stats = get_statistics_func(st.session_state.username)
        import database as db
        recent_logs = db.get_history(st.session_state.username)

        col_profile, col_metrics = st.columns([1.1, 1])
        
        with col_profile:
            st.markdown(f"""
            <div style="background-color: #1e293b; padding: 22px; border-radius: 10px; border-left: 5px solid #1e3a8a; height: 100%;">
                <h4 style="margin-top: 0; color: #ffffff; font-family: sans-serif; margin-bottom: 15px;">Student Profile Matrix</h4>
                <table style="width: 100%; border-collapse: collapse; color: #cbd5e1; font-family: sans-serif; font-size: 14px;">
                    <tr style="border-bottom: 1px solid #334155;"><td style="padding: 8px 0; font-weight: bold; width: 35%;">Name:</td><td>{fullname}</td></tr>
                    <tr style="border-bottom: 1px solid #334155;"><td style="padding: 8px 0; font-weight: bold;">Matric Number:</td><td>{matric_no}</td></tr>
                    <tr style="border-bottom: 1px solid #334155;"><td style="padding: 8px 0; font-weight: bold;">Department:</td><td>{department}</td></tr>
                    <tr><td style="padding: 8px 0; font-weight: bold;">Current Level:</td><td><span style="background-color: #1e3a8a; color: #ffffff; padding: 3px 10px; border-radius: 4px; font-weight: bold; font-size: 12px;">{current_level}</span></td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
        with col_metrics:
            if recent_logs and stats and stats[0] > 0:
                total_calculations, max_cgpa, avg_cgpa = stats
                latest_cgpa = recent_logs[0][2] 
                
                st.markdown("""
                <div style="background-color: #1e293b; padding: 20px 22px 5px 22px; border-top-left-radius: 10px; border-top-right-radius: 10px;">
                    <h4 style="margin-top: 0; color: #ffffff; font-family: sans-serif; margin-bottom: 5px;">Performance Summary & Goals</h4>
                </div>
                """, unsafe_allow_html=True)
                
                with st.container():
                    st.markdown("<div style='background-color: #1e293b; padding: 0px 22px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;'>", unsafe_allow_html=True)
                    
                    if "target_cgpa" not in st.session_state:
                        st.session_state.target_cgpa = 4.50
                        
                    target_input = st.number_input(
                        "Set Target Class/Goal CGPA:", 
                        min_value=1.0, max_value=5.0, 
                        value=st.session_state.target_cgpa, 
                        step=0.05, 
                        key="dashboard_target_setter"
                    )
                    st.session_state.target_cgpa = target_input
                    
                    progress_pct = min(int((latest_cgpa / target_input) * 100), 100) if target_input > 0 else 0
                    
                    st.markdown(f"""
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                            <div style="background-color: #0f172a; padding: 12px; border-radius: 6px; text-align: center;">
                                <span style="font-size: 11px; color: #94a3b8; display: block;">Current CGPA Standings</span>
                                <span style="font-size: 24px; font-weight: bold; color: #10b981;">{latest_cgpa:.2f}</span>
                            </div>
                            <div style="background-color: #0f172a; padding: 12px; border-radius: 6px; text-align: center;">
                                <span style="font-size: 11px; color: #94a3b8; display: block;">Target Metric Goal</span>
                                <span style="font-size: 24px; font-weight: bold; color: #3b82f6;">{target_input:.2f}</span>
                            </div>
                        </div>
                        <div style="margin-top: 15px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; font-size: 12px; color: #cbd5e1; margin-bottom: 4px;">
                                <span>Goal Trajectory Progress</span>
                                <b>{progress_pct}%</b>
                            </div>
                            <div style="background-color: #334155; width: 100%; height: 8px; border-radius: 4px; overflow: hidden;">
                                <div style="background-color: #10b981; width: {progress_pct}%; height: 100%;"></div>
                            </div>
                        </div>
                        <p style='font-size: 11px; color: #94a3b8; text-align: center; margin: 10px 0 0 0; padding-bottom: 15px;'>
                            Total Computations Synced: <b>{total_calculations}</b> | Highest: <b>{max_cgpa:.2f}</b>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: #1e293b; padding: 22px; border-radius: 10px; height: 100%; text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <h4 style="margin-top: 0; color: #ffffff; font-family: sans-serif; margin-bottom: 10px;">Performance Summary</h4>
                    <p style="color: #94a3b8; font-size: 14px; margin-bottom: 0;">No computations logged yet.</p>
                    <p style="color: #64748b; font-size: 12px; margin-top: 5px;">Head over to the <b>CGPA Calculator</b> tab to lock in your semester standings.</p>
                </div>
                """, unsafe_allow_html=True)

        if recent_logs:
            st.markdown("<br><h4 style='font-family: sans-serif; color: #ffffff; margin-bottom: 10px;'>Recent Calculation Log Snapshot</h4>", unsafe_allow_html=True)
            df_snapshot = pd.DataFrame(
                recent_logs[:3], 
                columns=["ID", "GPA", "CGPA", "Total Units", "Quality Points", "Calculation Label / Semester", "Timestamp"]
            )
            df_snapshot = df_snapshot.drop(columns=["ID", "Timestamp"])
            st.dataframe(df_snapshot, use_container_width=True, hide_index=True)

        st.markdown("<br><h4 style='font-family: sans-serif; color: #ffffff; margin-bottom: 15px;'>Academic Roadmap Tracker</h4>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b;">
            <p style="color: #cbd5e1; font-size: 14px; margin: 0;">Baseline Academic Tracker Trajectory Timeline status: <b>{current_level}</b></p>
            <div style="display: flex; gap: 10px; margin-top: 15px; overflow-x: auto; padding-bottom: 5px;">
                <div style="background-color: #1e293b; padding: 10px 15px; border-radius: 6px; min-width: 120px; text-align: center; border-bottom: 3px solid #10b981;">
                    <span style="font-size: 11px; color: #94a3b8; display: block;">100 Level</span>
                    <span style="font-size: 11px; color: #cbd5e1; font-weight: bold;">Passed</span>
                </div>
                <div style="background-color: #1e293b; padding: 10px 15px; border-radius: 6px; min-width: 120px; text-align: center; border-bottom: 3px solid #10b981;">
                    <span style="font-size: 11px; color: #94a3b8; display: block;">200 Level</span>
                    <span style="font-size: 11px; color: #cbd5e1; font-weight: bold;">Passed</span>
                </div>
                <div style="background-color: #1e293b; padding: 10px 15px; border-radius: 6px; min-width: 120px; text-align: center; border-bottom: 3px solid #f59e0b;">
                    <span style="font-size: 11px; color: #94a3b8; display: block;">300 Level</span>
                    <span style="font-size: 11px; color: #f59e0b; font-weight: bold;">Active</span>
                </div>
                <div style="background-color: #1e293b; padding: 10px 15px; border-radius: 6px; min-width: 120px; text-align: center; opacity: 0.4;">
                    <span style="font-size: 11px; color: #94a3b8; display: block;">400 Level</span>
                    <span style="font-size: 11px; color: #cbd5e1;">Locked</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
