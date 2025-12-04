import streamlit as st


def main() -> None:
    """Overview and story-driven introduction for the AI Security Vulnerability Simulation Lab."""
    st.markdown(r"""
    # 🔐 AI Security Vulnerability Simulation Lab – Mission Brief

    You are the lead AI security engineer at **Aurora Industrial Safety Systems**, a company that deploys agentic AI systems to monitor factories, refineries, and power plants. These agents continuously read sensor data, communicate with each other, and raise alerts when they detect anomalies.

    Recently, the Cyber Defense team has reported suspicious behavior:

    - Some agents appear to be **impersonated** (possible synthetic-identity risk).
    - Sensitive configuration snippets might be leaking through **covert data exfiltration channels**.
    - A red-teaming exercise hinted at successful **prompt injection** and **data poisoning** attacks.

    Your task in this lab is to **experiment with these attack scenarios**, see how they affect security metrics, and reason about defenses.
    """)

    st.markdown(r"""
    ## 🎯 What You Will Practice

    In this interactive lab, you will:

    - Configure attack scenarios with different:
        - **Attack intensity** $A_{intensity}$
        - **Attack type** (Prompt Injection, Data Poisoning, Synthetic Identity, Untraceable Data Leakage)
        - **Number of compromised agents** $N_{agents}$
    - Observe how attacks change:
        - Alert frequency over time $F_{alerts\_attacked}(t)$
        - Detection latency $L_{detection}$
        - Agent integrity scores $I_{agent\_attacked}$
    - Interpret visual dashboards to answer:
        - When does the system raise *too many* alerts?
        - How quickly are severe attacks detected?
        - How badly are compromised agents degraded compared to healthy ones?
    """)

    with st.expander("💡 Business Context: Why This Matters", expanded=True):
        st.markdown(r"""
        Aurora's industrial customers depend on **continuous uptime** and **safety guarantees**. A single undetected attack on the AI monitoring layer could:

        - Hide real-world physical anomalies (e.g., overheating, pressure spikes).
        - Leak sensitive production data to competitors.
        - Cause cascading shutdowns or safety incidents.

        By experimenting in this lab, you are essentially acting as the **red team meets blue team**:

        - As a *red teamer*, you amplify or tweak the attacks.
        - As a *blue teamer*, you read the charts and metrics, and think:
            - *Would our monitoring team catch this in time?*
            - *Which controls (rate limits, anomaly detection, access control) would help most?*
        """)

    st.markdown(r"""
    ## 🧭 How to Use This Lab

    1. Open the **sidebar** and choose:
        - An **attack intensity** $A_{intensity}$ between $0$ and $1$.
        - An **attack type** from the dropdown.
        - A **number of compromised agents** $N_{agents}$.
    2. Switch to the **Full Simulation Workspace** from the navigation sidebar.
    3. Explore the sections in order:
        - Synthetic data baseline
        - Validation and initial statistics
        - Vulnerability simulation
        - Visual story through three plots
    4. Come back to this page any time if you need to recall the scenario.
    """)

    st.markdown(r"""
    ## 🏁 Mini-Challenge Before You Dive In

    When you move to the **Full Simulation Workspace**, try these:

    1. Set $A_{intensity} = 0.0$ and $N_{agents} = 0$. Observe the baseline.
    2. Increase $A_{intensity}$ to $0.8$ with **Data Poisoning** and $N_{agents} = 5$:
        - How does the alert trend change?
        - How does $L_{detection}$ change?
    3. Switch to **Synthetic Identity** at medium intensity:
        - Do compromised agents clearly stand out in integrity scores?

    Use your observations to reason about **detection rules** and **risk controls** you would recommend to Aurora's leadership.
    """)


if __name__ == "__main__":
    main()
