
import streamlit as st

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, you will explore the fascinating and critical world of AI security vulnerabilities within agentic AI systems. We'll simulate various attack scenarios, such as prompt injection and data poisoning, on an industrial safety monitoring system. By interacting with the simulation, you'll gain hands-on experience in understanding how these vulnerabilities manifest, their impact on system performance and security metrics, and how to interpret the results.

This simulation provides a controlled environment to study concepts like 'synthetic-identity risk' and 'untraceable data leakage'. You'll see how different attack intensities and types can affect alert frequencies, detection latencies, and agent integrity scores. The goal is to equip you with practical insights into adversarial testing techniques and the importance of robust risk controls in AI system design.

Through interactive visualizations and data analysis, you will learn to:
- Identify common AI-security vulnerabilities.
- Understand the potential impact of different attack vectors.
- Analyze changes in system behavior under attack.
- Grasp the practical implications for designing more secure and adaptive AI systems.

Lets get started by navigating through the pages using the sidebar!
"""))

# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Page 1: Overview & Data Generation", "Page 2: Simulation Configuration & Validation", "Page 3: Vulnerability Simulation & Analysis"])
if page == "Page 1: Overview & Data Generation":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Page 2: Simulation Configuration & Validation":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Page 3: Vulnerability Simulation & Analysis":
    from application_pages.page3 import run_page3
    run_page3()
# Your code ends
