id: 690bb8d5adbb0296a6bfb062_documentation
summary: AI Security Vulnerability Simulation Lab Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Exploring AI Security Vulnerabilities in Agentic Systems

## Introduction: Unveiling AI Security Vulnerabilities
Duration: 00:05
Welcome to the QuLab AI Security Vulnerability Simulation! In this comprehensive codelab, you will dive into the critical and evolving domain of AI security, specifically focusing on agentic AI systems. With the increasing adoption of AI agents in sensitive applications like industrial safety monitoring, understanding and mitigating their vulnerabilities is paramount.

This lab provides a unique opportunity for hands-on experience in simulating various adversarial attack scenarios, such as **prompt injection** and **data poisoning**, on a simulated industrial safety monitoring system. By interacting with our custom Streamlit application, you will gain practical insights into how these vulnerabilities manifest, their potential impact on system performance and security metrics, and how to effectively interpret the results.

We will explore crucial concepts like **'synthetic-identity risk'** and **'untraceable data leakage'**, and observe how different attack intensities and types can influence key operational metrics, including alert frequencies, detection latencies, and agent integrity scores. The ultimate goal is to equip you with a foundational understanding of adversarial testing techniques and highlight the indispensable role of robust risk controls in the design and deployment of secure and adaptive AI systems.

**What you will learn:**
*   **Identify common AI-security vulnerabilities** such as prompt injection, data poisoning, synthetic-identity risk, and untraceable data leakage.
*   **Understand the potential impact** of different attack vectors on an agentic AI system.
*   **Analyze changes in system behavior** and security metrics under simulated attack conditions.
*   **Grasp the practical implications** for designing more resilient and secure AI systems.
*   **Utilize a Streamlit application** to interactively simulate, visualize, and analyze AI security scenarios.

Let's begin our journey into securing agentic AI!

## Step 1: Setting Up the Environment and Understanding the Application Structure
Duration: 00:10
To get started with this codelab, you'll need to run the Streamlit application. If you have Python and Streamlit installed, you can run it from your terminal.

<aside class="positive">
If you don't have Streamlit installed, you can install it using pip:
```bash
pip install streamlit pandas numpy scipy plotly
```
</aside>

**Running the Application:**

Navigate to the directory containing `app.py` in your terminal and execute:
```bash
streamlit run app.py
```
This command will open the Streamlit application in your default web browser.

### Application Architecture
The application is structured to be modular and easy to navigate. Here's a quick overview of its components:

*   **`app.py`**: This is the main entry point of the Streamlit application. It sets up the page configuration, displays the main title and introductory markdown, and handles the navigation between different pages using a sidebar `selectbox`.
*   **`application_pages/` directory**: This directory contains the individual page scripts (`page1.py`, `page2.py`, `page3.py`). Each script defines the content and logic for a specific section of the codelab.
*   **`application_pages/utils.py`**: This file contains all the core utility functions shared across the different application pages. This includes functions for generating synthetic data, validating data, simulating attack impacts, and generating interactive plots.

Let's examine the `app.py` file:

```python
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
```
As you can see, `app.py` serves as a dispatcher, calling the `run_pageX()` function based on the user's selection in the sidebar. This modular approach allows for a clean separation of concerns and easy navigation through the different stages of the codelab.

## Step 2: Page 1: Overview & Data Generation
Duration: 00:15
The first page of our application, "Page 1: Overview & Data Generation", introduces the lab's goals and the synthetic dataset it uses. Crucially, this page is responsible for generating the baseline data that represents the normal, secure operation of our simulated industrial safety monitoring system. This baseline is essential for comparing against the attacked scenarios later.

### Learning Goals and Data Overview
The page starts by reiterating the learning goals and provides an overview of the synthetic data:
*   **Sensor Readings**: Time-series data from various industrial sensors (e.g., temperature, pressure).
*   **Agent Communication Logs**: Records of messages exchanged between AI agents (e.g., status updates, alerts, communications).
*   **Security Metrics**: Baseline measurements of system behavior, such as alert frequency and agent integrity scores.

This synthetic data is lightweight yet realistic enough to demonstrate AI security vulnerability concepts effectively.

### Fixed Simulation Parameters
The application uses several fixed parameters for data generation, ensuring consistency across simulations:

```python
# Fixed simulation parameters (as per notebook)
SIMULATION_DURATION_HOURS = 2
NUM_AGENTS = 10
BASE_ALERT_RATE_PER_HOUR = 0.5
ANOMALY_RATE_MULTIPLIER = 1.5
RANDOM_SEED = 42
```
These parameters define the scale and randomness of the generated data.

### Generating Baseline Data
The core functionality of this page is to generate the baseline data. This is handled by the `generate_synthetic_safety_data` function located in `application_pages/utils.py`.

Here's how `page1.py` calls this function and stores the results:

```python
# From application_pages/page1.py
# ...
from application_pages.utils import generate_synthetic_safety_data, SIMULATION_DURATION_HOURS, NUM_AGENTS, BASE_ALERT_RATE_PER_HOUR, ANOMALY_RATE_MULTIPLIER, RANDOM_SEED

def run_page1():
    # ... introductory markdown ...

    if 'sensor_data_baseline' not in st.session_state:
        sensor_data_baseline, agent_logs_baseline, security_metrics_baseline, simulation_config = \
            generate_synthetic_safety_data(NUM_AGENTS, SIMULATION_DURATION_HOURS, BASE_ALERT_RATE_PER_HOUR, ANOMALY_RATE_MULTIPLIER, RANDOM_SEED)

        st.session_state['sensor_data_baseline'] = sensor_data_baseline
        st.session_state['agent_logs_baseline'] = agent_logs_baseline
        st.session_state['security_metrics_baseline'] = security_metrics_baseline
        st.session_state['simulation_config'] = simulation_config

    st.success("Baseline data generated and stored in session state.")

    # ... data previews ...
```
<aside class="positive">
Notice the use of `st.session_state`. Streamlit's session state allows you to store and persist variables across reruns of the application. This is crucial here because `generate_synthetic_safety_data` is called only once, and its results are then available to other pages without re-computation.
</aside>

The `generate_synthetic_safety_data` function in `application_pages/utils.py` creates three DataFrames:
1.  **`sensor_data_df`**: Contains timestamped sensor readings (temperature, pressure) for each agent.
2.  **`agent_logs_df`**: Records communication logs for each agent, including message type, content, and an associated risk score.
3.  **`base_security_metrics_df`**: Provides a baseline for alert frequency and agent integrity scores over time for each agent.

After generation, the first five rows of each baseline DataFrame are displayed on "Page 1" for preview.

You can now review the introductory text and the generated data previews on "Page 1" of the Streamlit application. Once you're familiar with the baseline, proceed to the next step by navigating to "Page 2: Simulation Configuration & Validation" in the sidebar.

## Step 3: Page 2: Simulation Configuration & Validation
Duration: 00:20
"Page 2: Simulation Configuration & Validation" is where you define the parameters for simulating AI security vulnerabilities and validate the integrity of the generated baseline data. This page lays the groundwork for understanding the attack's impact.

### Methodology Overview
The page begins by outlining the simulation methodology:
1.  **Synthetic Data Generation**: (Completed on Page 1)
2.  **Interactive Parameter Definition**: Define attack type, intensity, and number of compromised agents.
3.  **Attack Simulation**: Apply mathematical models to modify security metrics based on attack parameters.
4.  **Visualization**: Generate plots to show attack effects.
5.  **Analysis and Interpretation**: Discuss observed impacts.

### Key Mathematical Foundations for Attack Simulation
A crucial aspect of this simulation is the use of mathematical models to quantify the impact of different attack types and intensities. These models are defined with specific coefficients (`C_TYPE_DICT`, `K_TYPE_DICT`, `D_TYPE_DICT`, `L_BASE`) from `application_pages/utils.py` that dictate how each attack type affects various metrics.

Here are the mathematical relationships:

#### Alert Frequency Over Time
The alert frequency under attack, $F_{alerts\_attacked}(t)$, is calculated as:
$$
F_{alerts\_attacked}(t) = F_{alerts\_base}(t) \cdot (1 + A_{intensity} \cdot C_{type})
$$
Where:
*   $F_{alerts\_base}(t)$ is the baseline alert frequency at time $t$.
*   $A_{intensity}$ is the user-defined attack intensity, $A_{intensity} \in [0, 1]$.
*   $C_{type}$ is a scaling factor specific to the `Attack Type`, reflecting its inherent impact potential. For example, a data poisoning attack might have a higher $C_{type}$ than a mild prompt injection.
    *   Current values: `{'Prompt Injection': 0.5, 'Data Poisoning': 0.8, 'Synthetic Identity': 0.6, 'Untraceable Data Leakage': 0.7}`

#### Detection Latency
The simulated detection latency, $L_{detection}$, is calculated as:
$$
L_{detection} = L_{base} + A_{intensity} \cdot D_{type}
$$
Where:
*   $L_{base}$ is a nominal baseline detection latency ($L_{base} = 5$ minutes).
*   $D_{type}$ is a coefficient related to the `Attack Type`, representing how challenging that specific attack is to detect quickly.
    *   Current values: `{'Prompt Injection': 20, 'Data Poisoning': 60, 'Synthetic Identity': 45, 'Untraceable Data Leakage': 30}` (in minutes)

#### Agent Integrity Score
The agent integrity score under attack, $I_{agent\_attacked}$, is calculated as:
$$
I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type})
$$
Where:
*   $I_{agent\_base}$ is the baseline agent integrity score.
*   $K_{type}$ is a coefficient for the `Attack Type`, reflecting its detrimental effect on agent trustworthiness or operational integrity. For uncompromised agents, $I_{agent\_attacked} = I_{agent\_base}$.
    *   Current values: `{'Prompt Injection': 0.4, 'Data Poisoning': 0.7, 'Synthetic Identity': 0.8, 'Untraceable Data Leakage': 0.5}`

### Configure Simulation Parameters
On this page, you interact with the sidebar to define the attack parameters.

```python
# From application_pages/page2.py
# ...
    st.sidebar.header("Simulation Controls")
    attack_intensity = st.sidebar.slider(
        label='Attack Intensity ($A_{intensity}$):',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get('attack_intensity', 0.5),
        step=0.1,
        help='Controls the severity of the simulated attack ($0.0$ = no attack, $1.0$ = maximum impact).'
    )
    st.session_state['attack_intensity'] = attack_intensity

    attack_type = st.sidebar.selectbox(
        label='Attack Type:',
        options=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'],
        index=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'].index(
            st.session_state.get('attack_type', 'Prompt Injection')
        ),
        help='Selects the type of AI security vulnerability to simulate.'
    )
    st.session_state['attack_type'] = attack_type

    num_compromised_agents = st.sidebar.slider(
        label='Number of Compromised Agents ($N_{agents}$):',
        min_value=0,
        max_value=5,
        value=st.session_state.get('num_compromised_agents', 1),
        step=1,
        help='Specifies the count of simulated agents affected by the attack.'
    )
    st.session_state['num_compromised_agents'] = num_compromised_agents
# ...
```
These parameters (`attack_intensity`, `attack_type`, `num_compromised_agents`) are stored in `st.session_state` so they can be retrieved and used on "Page 3" for the actual simulation.

### Data Validation Summary
Before running the simulation, it's good practice to validate the integrity of our baseline data. "Page 2" automatically performs validation checks on the Sensor Data, Agent Logs, and Security Metrics DataFrames. This is handled by the `validate_and_summarize_data` function in `application_pages/utils.py`.

```python
# From application_pages/utils.py
def validate_and_summarize_data(df, df_name, expected_columns, expected_dtypes, critical_fields_no_null=None, unique_key=None):
    st.subheader(f" Validating {df_name} ")
    try:
        # 1. Check if expected columns are present
        # ...
        # 2. Check data types
        # ...
        # 3. Check critical fields for nulls
        # ...
        # 4. Check uniqueness of the unique key
        # ...
        st.subheader(f"{df_name} Summary Statistics:")
        st.dataframe(df.describe())
        st.success(f"{df_name} validation successful.")
    except AssertionError as e:
        st.error(f"Validation failed for {df_name}: {e}")
    except Exception as e:
        st.error(f"An error occurred during validation of {df_name}: {e}")
```
This function checks for:
*   Presence of all expected columns.
*   Correct data types for each column.
*   Absence of null values in critical fields.
*   Uniqueness of specified key columns.

It then displays descriptive statistics for each DataFrame. This ensures that the data we're working with is well-formed and reliable for simulation.

Experiment with the "Simulation Controls" in the sidebar. Observe how the mathematical models described above would change for different attack types and intensities. Once you are satisfied with your chosen parameters and have reviewed the data validation summary, navigate to "Page 3: Vulnerability Simulation & Analysis" to see the attack in action.

## Step 4: Page 3: Vulnerability Simulation & Analysis
Duration: 00:25
"Page 3: Vulnerability Simulation & Analysis" is the culmination of our codelab. Here, the configured attack parameters are applied to the baseline data, simulating the impact of the chosen AI security vulnerability. This page then visualizes and analyzes the results, providing key insights into the system's behavior under attack.

### Simulating Attack Impact
The first step on this page is to retrieve the baseline security metrics and the attack parameters from `st.session_state`. These are then passed to the `simulate_vulnerability_impact` function from `application_pages/utils.py`.

```python
# From application_pages/page3.py
# ...
    if (
        'security_metrics_baseline' in st.session_state and
        'simulation_config' in st.session_state and
        'attack_intensity' in st.session_state and
        'attack_type' in st.session_state and
        'num_compromised_agents' in st.session_state
    ):
        security_metrics_baseline = st.session_state['security_metrics_baseline']
        simulation_config = st.session_state['simulation_config']
        attack_intensity = st.session_state['attack_intensity']
        attack_type = st.session_state['attack_type']
        num_compromised_agents = st.session_state['num_compromised_agents']

        # ... display configured parameters ...

        try:
            attacked_security_metrics, attack_events_df = simulate_vulnerability_impact(
                security_metrics_baseline, attack_type, attack_intensity, num_compromised_agents, simulation_config
            )
            st.session_state['security_metrics_attacked'] = attacked_security_metrics
            st.session_state['attack_events_df'] = attack_events_df
            st.success("Vulnerability simulation completed successfully!")
        except ValueError as e:
            st.error(f"Simulation error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred during simulation: {e}")
# ...
```

The `simulate_vulnerability_impact` function applies the mathematical models discussed in Step 3:
1.  **Alert Frequency Modification**: Uses $F_{alerts\_attacked}(t) = F_{alerts\_base}(t) \cdot (1 + A_{intensity} \cdot C_{type})$ to increase alert frequencies.
2.  **Agent Integrity Score Reduction**: Randomly selects `num_compromised_agents` and applies $I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type})$ to reduce their integrity scores.
3.  **Detection Latency Calculation**: Calculates the `simulated_detection_latency` using $L_{detection} = L_{base} + A_{intensity} \cdot D_{type}$.
4.  **Attack Events DataFrame**: Creates a summary `attack_events_df` with details of the attack and its severity.

The resulting `attacked_security_metrics` and `attack_events_df` are then stored back into `st.session_state`.

After the simulation, a preview of the `attacked_security_metrics` and `attack_events_df` is displayed, allowing you to see the raw changes.

### Visualizations
The most impactful part of "Page 3" is the series of visualizations that graphically demonstrate the attack's effects. These plots are generated using Plotly, making them interactive.

#### 1. Trend Plot: Alert Frequency Over Time
This plot compares the average alert frequency for both baseline (normal operation) and attacked scenarios. A significant increase or divergence in the attacked scenario's alert frequency indicates a successful disruption of the system's normal alerting mechanisms.

```python
# From application_pages/utils.py
def plot_alert_frequency_trend_plotly(base_df, attacked_df, attack_type, attack_intensity):
    base_df_agg = base_df.groupby('timestamp')['alert_frequency'].mean().reset_index()
    attacked_df_agg = attacked_df.groupby('timestamp')['alert_frequency'].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=base_df_agg['timestamp'], y=base_df_agg['alert_frequency'],
                             mode='lines+markers', name='Baseline', marker=dict(symbol='circle')))
    fig.add_trace(go.Scatter(x=attacked_df_agg['timestamp'], y=attacked_df_agg['alert_frequency'],
                             mode='lines+markers', name='Attacked', marker=dict(symbol='x')))

    fig.update_layout(
        title=f"Alert Frequency Over Time: Baseline vs. Attacked<br>({attack_type} at {attack_intensity*100:.0f}% Intensity)",
        xaxis_title='Time',
        yaxis_title='Average Alert Frequency',
        hovermode='x unified',
        legend_title_text='Scenario',
        height=500,
        width=800
    )
    st.plotly_chart(fig, use_container_width=True)
```

#### 2. Relationship Plot: Attack Severity vs. Detection Latency
This scatter plot visualizes the correlation between the severity of the simulated attack and the system's ability to detect it in a timely manner. Higher detection latency can indicate a less resilient system, potentially leading to prolonged negative consequences.

```python
# From application_pages/utils.py
def plot_attack_severity_vs_latency_plotly(attack_events_df):
    if attack_events_df.empty:
        st.warning("No attack events to plot for Attack Severity vs. Detection Latency.")
        return

    fig = px.scatter(attack_events_df, x='attack_severity', y='simulated_detection_latency',
                     color='attack_type',
                     title='Attack Severity vs. Simulated Detection Latency',
                     labels={'attack_severity': 'Attack Severity',
                             'simulated_detection_latency': 'Simulated Detection Latency (Minutes)'},
                     hover_data=['attack_intensity', 'num_compromised_agents'],
                     height=500,
                     width=800)
    
    fig.update_layout(legend_title_text='Attack Type')
    st.plotly_chart(fig, use_container_width=True)
```

#### 3. Aggregated Comparison: Agent Integrity Scores
This bar chart directly compares the average integrity scores of compromised versus uncompromised agents. It effectively highlights the direct impact of the attack on the trustworthiness and operational health of affected AI agents.

```python
# From application_pages/utils.py
def plot_agent_integrity_comparison_plotly(attacked_df):
    # ... error handling ...
    
    integrity_comparison = attacked_df.groupby('is_compromised')['agent_integrity_score'].mean().reset_index()
    integrity_comparison['Agent Status'] = integrity_comparison['is_compromised'].map({True: 'Compromised', False: 'Uncompromised'})

    fig = px.bar(integrity_comparison, x='Agent Status', y='agent_integrity_score',
                 title='Average Agent Integrity Scores: Compromised vs. Uncompromised',
                 labels={'agent_integrity_score': 'Average Integrity Score'},
                 color='Agent Status',
                 height=500,
                 width=800)
    
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    fig.update_layout(yaxis_range=[0, 1.1]) # Extend y-axis to show labels
    st.plotly_chart(fig, use_container_width=True)
```

Observe these visualizations carefully. Try changing the attack parameters on "Page 2" and re-running the simulation on "Page 3" to see how different configurations alter the outcomes.

### Discussion & Conclusion
The final section of "Page 3" provides a summary and discussion of the key takeaways from the simulation. It reinforces the understanding of how AI security vulnerabilities impact agentic AI systems and the importance of proactive defense strategies.

**Key takeaways from this lab:**
*   **Impact of Attack Intensity**: Higher attack intensity generally leads to more pronounced effects across all metrics, emphasizing the need for robust defense mechanisms.
*   **Vulnerability-Specific Effects**: Different attack types exhibit distinct patterns of impact, underscoring the importance of understanding the unique characteristics of each vulnerability.
*   **Importance of Timely Detection**: The relationship between attack severity and detection latency highlights that delays in identifying and mitigating attacks can lead to amplified negative consequences.
*   **Agent Integrity**: Compromised agents show a clear degradation in integrity, pointing to the necessity of agent-level security monitoring and recovery protocols.

This lab provides a foundational understanding of AI security risks and the efficacy of simulated adversarial testing. By visualizing these impacts, we can better design, implement, and validate adaptive AI systems that are resilient against emerging threats.

### References
Finally, the page provides a list of references, including the theoretical basis for the lab and the libraries used.

## Step 5: Summary and Next Steps
Duration: 00:05
Congratulations! You have successfully navigated through the QuLab AI Security Vulnerability Simulation.

### What You've Learned
*   **Fundamental Concepts**: Gained an understanding of critical AI security vulnerabilities such as prompt injection, data poisoning, synthetic-identity risk, and untraceable data leakage in the context of agentic AI systems.
*   **Application Workflow**: Explored the modular structure of a Streamlit application, from data generation to parameter configuration and result visualization.
*   **Mathematical Modeling**: Understood how mathematical formulas can be used to simulate the impact of attacks on key metrics like alert frequency, detection latency, and agent integrity.
*   **Data Validation**: Learned the importance of data validation to ensure the integrity of simulation inputs.
*   **Adversarial Analysis**: Interpreted interactive visualizations to analyze the effects of various attack types and intensities on system performance and security.
*   **Practical Implications**: Derived practical insights into designing more secure and resilient AI systems by observing attack impacts.

### Further Exploration
Here are some ideas to continue your learning journey:

*   **Modify Coefficients**: Experiment with changing the `C_TYPE_DICT`, `K_TYPE_DICT`, and `D_TYPE_DICT` values in `application_pages/utils.py` to see how different attack characteristics would alter the simulation results.
*   **Add New Attack Types**: Extend the `simulate_vulnerability_impact` function and the coefficient dictionaries to introduce new hypothetical attack types.
*   **Enhance Data Generation**: Modify `generate_synthetic_safety_data` to create more complex or realistic baseline scenarios.
*   **Develop Mitigation Strategies**: Think about how you might incorporate simulated mitigation strategies (e.g., increased monitoring, agent isolation) into the `simulate_vulnerability_impact` function and visualize their effectiveness.
*   **Explore Different Plot Types**: Use other Plotly visualizations to represent the data in new ways.

<aside class="positive">
Remember, the power of simulation lies in its ability to safely model and understand complex real-world phenomena. By continuing to experiment with this framework, you can deepen your understanding of AI security and contribute to building more robust AI systems.
</aside>

Thank you for participating in this QuLab codelab!
