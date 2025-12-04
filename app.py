import streamlit as st

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
# Your code starts here
st.markdown("""
In this lab, you will explore an AI Security Vulnerability Simulation Lab. Use the sidebar to navigate between an interactive scenario overview and the full simulation workspace. The business goal is to help an industrial AI safety team understand how different AI attacks (like prompt injection or data poisoning) can change alerts, agent integrity, and detection latency so they can design better defenses.
""")

page = st.sidebar.selectbox(label="Navigation", options=["AI Security Lab Overview", "Full Simulation Workspace"])

if page == "AI Security Lab Overview":
    from application_pages.ai_security_overview import main
    main()
elif page == "Full Simulation Workspace":
    from application_pages.ai_security_simulation import main
    main()
# Your code ends here
