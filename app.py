import streamlit as st

st.set_page_config(page_title="AI Security Vulnerability Simulation Lab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("AI Security Vulnerability Simulation Lab")
st.divider()

page = st.sidebar.selectbox(label="Navigation", options=["Introduction", "Setup", "Configuration", "Simulation", "Visualization"])

if page == "Introduction":
    from application_pages.introduction import main
    main()
elif page == "Setup":
    from application_pages.setup import main
    main()
elif page == "Configuration":
    from application_pages.configuration import main
    main()
elif page == "Simulation":
    from application_pages.simulation import main
    main()
elif page == "Visualization":
    from application_pages.visualization import main
    main()
