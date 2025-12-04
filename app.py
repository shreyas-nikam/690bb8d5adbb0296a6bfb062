import streamlit as st

st.set_page_config(page_title='QuLab', layout='wide')
st.sidebar.image('https://www.quantuniversity.com/assets/img/logo5.jpg')
st.sidebar.divider()
st.title('QuLab')
st.divider()
st.markdown("""
In this lab, explore AI security vulnerabilities through interactive simulations and visualizations.
""")

page = st.sidebar.selectbox('Navigation', ['Overview', 'Simulation'])
if page == 'Overview':
    from application_pages.page_1 import main
    main()
elif page == 'Simulation':
    from application_pages.page_2 import main
    main()
