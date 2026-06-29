import streamlit as st

def show(get_statistics_func, get_user_func):
    # 1. COSMAS BANNER HEADLINER
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        # Fallback stylized banner text if the image asset is loading/missing
        st.markdown("""
        <div style="background: linear-gradient(90deg, #6b21a8 0%, #1e1b4b 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px;">COSMAS AT SUG TOP SEAT</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-family: sans-serif;">Support • Pray • Canvass</p>
        </div>
        """, unsafe_allow_html=True)

    # Fetch User Profile Context
    user = get_user_func(st.session_state.username)
    
    if user:
        fullname = user['fullname']
        matric_no = user['matric_no']
        department = user['department']
        current_level = user['current_level']
        
        # 2. DYNAMIC WELCOME BANNER (Tracks sessions to say Welcome vs Welcome Back)
        if "returning_user" not in st.session_state:
            st.markdown(f"<h2 style='font-family: sans-serif; color: #ffffff; margin-bottom: 5px;'>Welcome, {fullname} 🎓</h2>", unsafe_allow_html=True)
            st.session_state.returning_user = True
        else:
            st.markdown(f"<h2 style='font-family: sans-serif; color: #ffffff; margin-bottom: 5px;'>Welcome back, {fullname}! 👋</h2>", unsafe_allow_html=True)
            
        st.markdown("<p style='color: #94a3b8; margin-top: 0; margin-bottom: 25px;'>Here is your real-time academic standing performance hub.</p>", unsafe_allow_html=True)
        
        # 3. SIDE-BY-SIDE SPLIT GRID: Profile Card vs Quick Metrics Analytics
        col_profile, col_metrics = st.columns([1.2, 1])
        
        with col_profile:
            st.markdown(f"""
            <div style="background-color: #1e293b; padding: 22px; border-radius: 10px; border-left: 5px solid #6b21a8; height: 100%;">
                <h4 style="margin-top: 0; color: #ffffff; font-family: sans-serif; margin-bottom: 15px;">Student Academic Profile</h4>
                <table style="width: 100%; border-collapse: collapse; color: #cbd5e1; font-family: sans-serif; font-size: 14px;">
                    <tr style="border-bottom: 1px solid #334155;"><td style="padding: 8px 0; font-weight: bold; width: 35%;">Name:</td><td>{fullname}</td></tr>
                    <tr style="border-bottom: 1px solid #334155;"><td style="padding: 8px 0; font-weight: bold;">Matric Number:</td><td>{matric_no}</td></tr>
                    <tr style="border-bottom: 1px solid #334155;"><td style="padding: 8px 0; font-weight: bold;">Department:</td><td>{department}</td></tr>
                    <tr><td style="padding: 8px 0; font-weight: bold;">Current Standing:</td><td><span style="background-color: #6b21a8; color: #ffffff; padding: 3px 10px; border-radius: 4px; font-weight: bold; font-size: 12px;">{current_level}</span></td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
        with col_metrics:
            stats = get_statistics_func(st.session_state.username)
            if stats and stats[0] > 0:
                total_calculations, max_cgpa, avg_cgpa = stats
                
                # Visual Quick-View Metric Boxes
                st.markdown(f"""
                <div style="background-color: #1e293b; padding: 22px; border-radius: 10px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                    <h4 style="margin-top: 0; color: #ffffff; font-family: sans-serif; margin-bottom: 15px;">Performance Summary</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div style="background-color: #0f172a; padding: 12px; border-radius: 6px; text-align: center;">
                            <span style="font-size: 12px; color: #94a3b8; display: block;">Highest CGPA</span>
                            <span style="font-size: 22px; font-weight: bold; color: #10b981;">{max_cgpa:.2f}</span>
                        </div>
                        <div style="background-color: #0f172a; padding: 12px; border-radius: 6px; text-align: center;">
                            <span style="font-size: 12px; color: #94a3b8; display: block;">Average CGPA</span>
                            <span style="font-size: 22px; font-weight: bold; color: #6366f1;">{avg_cgpa:.2f}</span>
                        </div>
                    </div>
                    <div style="background-color: #0f172a; padding: 10px; border-radius: 6px; text-align: center; margin-top: 15px;">
                        <span style="font-size: 12px; color: #94a3b8;">Total Computation Syncs: <b>{total_calculations}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: #1e293b; padding: 22px; border-radius: 10px; height: 100%; text-align: center;">
                    <h4 style="margin-top: 0; color: #ffffff; font-family: sans-serif;">Performance Summary</h4>
                    <p style="color: #94a3b8; font-size: 14px; margin-top: 20px;">No computations recorded on this engine yet.</p>
                    <p style="color: #6b21a8; font-size: 13px; font-weight: bold;">Go to CGPA Calculator to start!</p>
                </div>
                """, unsafe_allow_html=True)

        # 4. BOTTOM WORKSPACE: SEMESTER PROGRESSION TIMELINE BLOCK
        st.markdown("<br><h4 style='font-family: sans-serif; color: #ffffff; margin-bottom: 15px;'>Academic Progression Roadmap</h4>", unsafe_allow_html=True)
        
        # Build out a clean roadmap block matching your tracking engine timeline
        st.markdown(f"""
        <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b;">
            <p style="color: #cbd5e1; font-size: 14px; margin: 0;">Your current targeted baseline trajectory is set to <b>{current_level}</b>.</p>
            <div style="display: flex; gap: 10px; margin-top: 15px; overflow-x: auto; padding-bottom: 5px;">
                <div style="background-color: #1e293b; padding: 10px 15px; border-radius: 6px; min-width: 130px; text-align: center; border-bottom: 3px solid #6b21a8;">
                    <span style="font-size: 12px; color: #94a3b8; display: block;">100 Level</span>
                    <span style="font-size: 11px; color: #cbd5e1; font-weight: bold;">Completed</span>
                </div>
                <div style="background-color: #1e293b; padding: 10px 15px; border-radius: 6px; min-width: 130px; text-align: center; border-bottom: 3px solid #6b21a8;">
                    <span style="font-size: 12px; color: #94a3b8; display: block;">200 Level</span>
                    <span style="font-size: 11px; color: #cbd5e1; font-weight: bold;">Completed</span>
                </div>
                <div style="background-color: #1e293b; padding: 10px 15px; border-radius: 6px; min-width: 130px; text-align: center; border-bottom: 3px solid #f59e0b;">
                    <span style="font-size: 12px; color: #94a3b8; display: block;">300 Level</span>
                    <span style="font-size: 11px; color: #f59e0b; font-weight: bold;">In Progress</span>
                </div>
                <div style="background-color: #1e293b; padding: 10px 15px; border-radius: 6px; min-width: 130px; text-align: center; opacity: 0.5;">
                    <span style="font-size: 12px; color: #94a3b8; display: block;">400 Level</span>
                    <span style="font-size: 11px; color: #cbd5e1;">Pending</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("Failed to load dashboard parameters. Please log out and back in again.")
