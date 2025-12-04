id: 690bb8d5adbb0296a6bfb062_documentation
summary: AI Security Vulnerability Simulation Lab Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: AI Security Vulnerability Simulation Lab

## 1. Introduction to the AI Security Vulnerability Simulation Lab
Duration: 02:00

Welcome to QuLab: AI Security Vulnerability Simulation Lab! In this codelab, you will dive into an interactive environment designed to simulate and analyze various AI security vulnerabilities within an industrial context. This lab is crucial for developers and AI safety teams looking to understand how different attack vectors impact AI systems and how to design robust defenses.

The core purpose of this application is to provide a hands-on experience in exploring the consequences of AI attacks such as prompt injection, data poisoning, synthetic identity, and untraceable data leakage. By manipulating attack parameters, you will observe real-time changes in critical security metrics like alert frequency, detection latency, and agent integrity scores.

<aside class="positive">
<b>Why is this important?</b> Modern industrial operations increasingly rely on agentic AI systems for monitoring and control. Undetected AI attacks can lead to severe consequences, from hidden physical anomalies and data exfiltration to cascading system failures. This lab empowers you to act as both a "red teamer" (simulating attacks) and a "blue teamer" (analyzing their impact and strategizing defenses), preparing you to build more resilient AI systems.
</aside>

**Key Concepts You Will Explore:**

*   **Attack Intensity ($A_{intensity}$):** A scalar value (0.0 to 1.0) controlling the severity of the simulated attack.
*   **Attack Types:** Different categories of AI vulnerabilities, each with unique impact characteristics (e.g., Prompt Injection, Data Poisoning).
*   **Number of Compromised Agents ($N_{agents}$):** The count of AI agents affected by the simulated attack.
*   **Alert Frequency Over Time ($F_{alerts\_attacked}(t)$):** How the rate of system alerts changes during an attack.
*   **Detection Latency ($L_{detection}$):** The simulated time taken to detect an ongoing attack.
*   **Agent Integrity Scores ($I_{agent\_attacked}$):** A metric reflecting the trustworthiness and operational health of individual AI agents under attack.

By the end of this codelab, you will have a comprehensive understanding of how these concepts interrelate and how to interpret their impact using interactive visualizations.

## 2. Setting Up Your Development Environment
Duration: 01:00

To begin, ensure you have Python installed (version 3.8 or higher is recommended) and `pip` for package management.

1.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install Streamlit and other dependencies:**
    The application uses `streamlit`, `pandas`, `numpy`, `matplotlib`, and `seaborn`.
    ```bash
    pip install streamlit pandas numpy matplotlib seaborn
    ```

3.  **Save the application files:**
    Create an `app.py` file and a directory `application_pages` with `ai_security_overview.py` and `ai_security_simulation.py` inside it. Copy the provided code into these files.

4.  **Run the Streamlit application:**
    Navigate to the directory containing `app.py` in your terminal and run:
    ```bash
    streamlit run app.py
    ```
    This command will open the application in your web browser, typically at `http://localhost:8501`.

## 3. Exploring the Application Overview
Duration: 03:00

Upon launching the application, you'll land on the "AI Security Lab Overview" page. This page, powered by `application_pages/ai_security_overview.py`, provides the narrative and context for the lab.

The main content includes:

*   **Mission Brief:** Sets the scene at "Aurora Industrial Safety Systems" and outlines the initial suspicious behaviors reported, such as agent impersonation, data exfiltration, prompt injection, and data poisoning. Your role is to experiment with these scenarios.
*   **What You Will Practice:** Clearly lists the objectives: configuring attack scenarios, observing metric changes, and interpreting dashboards. This introduces the key parameters ($A_{intensity}$, Attack Type, $N_{agents}$) and metrics ($F_{alerts\_attacked}(t)$, $L_{detection}$, $I_{agent\_attacked}$).
*   **Business Context: Why This Matters:** An expandable section explaining the real-world implications of AI attacks on industrial safety and uptime. It reinforces the "red team meets blue team" philosophy.
*   **How to Use This Lab:** Provides instructions on navigating the sidebar and exploring the different sections within the "Full Simulation Workspace".
*   **Mini-Challenge Before You Dive In:** A set of tasks to get you started with experimenting with the controls and observing initial changes.

<aside class="positive">
Take a moment to read through this overview. Understanding the mission brief and business context will help you interpret the simulation results more effectively in later steps. Pay special attention to the "How to Use This Lab" section as it guides your interaction with the application.
</aside>

## 4. Understanding the Core Simulation Workspace Structure
Duration: 02:00

Now, from the sidebar, switch the `Navigation` dropdown to **"Full Simulation Workspace"**. This is where the core simulation logic resides, implemented in `application_pages/ai_security_simulation.py`.

This page is structured into several sections, guiding you through the simulation process:

*   **Current Simulation Configuration:** Summarizes the parameters you've set.
*   **Setup and Library Imports:** Confirms that necessary libraries are loaded.
*   **Synthetic Data Generation:** Creates the baseline data representing a healthy industrial system.
*   **Data Validation and Initial Statistics:** Ensures the synthetic data is valid before simulation.
*   **Vulnerability Simulation – Attack Logic:** Applies the chosen attack parameters to the baseline data.
*   **Mathematical Foundations of Attack Simulation:** Explains the formulas used to model attack impact.
*   **Trend Plot – Alert Frequency Over Time:** Visualizes how alert rates change.
*   **Relationship Plot – Attack Severity vs. Detection Latency:** Shows the correlation between attack severity and detection time.
*   **Aggregated Comparison – Agent Integrity Scores:** Compares the health of compromised versus uncompromised agents.
*   **Discussion and Reflection Prompts:** Encourages critical thinking based on your observations.
*   **Key Takeaways:** Summarizes the main learnings from the lab.

**High-Level Application Architecture:**

Here's a simplified architectural overview of how the Streamlit application processes your input and generates insights:

```mermaid
graph TD
    A[Streamlit Sidebar Controls] --> B{Application Logic (app.py)};
    B --> C[AI Security Lab Overview];
    B --> D[Full Simulation Workspace];

    D -- User Input --> E[Attack Configuration Panel];
    E -- $A_{intensity}$, Attack Type, $N_{agents}$ --> F[Synthetic Data Generation (generate_synthetic_safety_data)];
    F --> G[Baseline Sensor Data];
    F --> H[Baseline Agent Logs];
    F --> I[Baseline Security Metrics];

    G & H & I --> J[Data Validation (validate_and_summarize_data)];
    J -- Validated Baseline Data --> K[Vulnerability Simulation (simulate_vulnerability_impact)];
    K -- Attack Parameters & COEFFS --> L[Attacked Security Metrics];
    K -- Attack Parameters --> M[Attack Events];

    L --> N[Plot Alert Frequency Trend (plot_alert_frequency_trend)];
    M --> O[Plot Attack Severity vs. Latency (plot_attack_severity_vs_latency)];
    L --> P[Plot Agent Integrity Comparison (plot_agent_integrity_comparison)];

    N & O & P --> Q[Streamlit Dashboard (Visualizations & Dataframes)];
```
This diagram illustrates the flow from user interaction in the sidebar, through data generation and validation, to the core simulation logic, and finally to the visual outputs on the Streamlit dashboard.

## 5. Configuring Attack Scenarios with Sidebar Controls
Duration: 03:00

The sidebar on the left side of your screen is your primary interface for configuring the simulation. This section of the code is handled by the `_sidebar_controls()` function in `ai_security_simulation.py`.

1.  **Locate the Attack Configuration Panel:** In the Streamlit sidebar, you'll see a section titled "🎛️ Attack Configuration Panel".

2.  **Experiment with the Controls:**
    *   **Select Attack Intensity ($A_{intensity}$):** This slider allows you to choose a value between $0.0$ (no attack) and $1.0$ (maximum intensity). Drag the slider and observe how the "Current Simulation Configuration" section updates.
    *   **Select Attack Type:** This dropdown lets you choose from different vulnerability types: 'Prompt Injection', 'Data Poisoning', 'Synthetic Identity', and 'Untraceable Data Leakage'. Each type has different coefficients that influence the simulation.
    *   **Select Number of Compromised Agents ($N_{agents}$):** This slider determines how many of the 10 simulated agents are affected by the attack.

3.  **Observe the Configuration Summary:** Just below the main title on the "Full Simulation Workspace" page, you'll find the "⚙️ Current Simulation Configuration" section. This fragment, `_show_configuration_summary()`, dynamically displays your selected parameters, ensuring you always know the current state of your simulation.

<aside class="positive">
As you adjust these controls, pay attention to the descriptions for each. Understanding these parameters is key to effectively testing different attack scenarios and observing their specific impacts.
</aside>

## 6. Synthetic Data Generation and Baseline Analysis
Duration: 04:00

Before simulating an attack, the application first generates a baseline dataset representing a healthy, operational industrial system. This is done by the `generate_synthetic_safety_data()` function.

This function creates three primary DataFrames:

1.  **Sensor Data:** Records of various sensor types (temperature, pressure, vibration) from multiple agents over time, including normal and anomalous readings.
2.  **Agent Logs:** Simulated operational logs from agents, including heartbeats, data transfers, status updates, and alerts.
3.  **Security Metrics:** Baseline integrity scores and alert counts for each agent.

<aside class="positive">
The `generate_synthetic_safety_data` function uses `st.cache_data`. This means that if you don't change the input parameters to this function (which are defined as constants like `NUM_AGENTS`, `SIMULATION_DURATION_HOURS`, etc.), Streamlit will reuse the previously generated data, making the app much faster and more responsive when you only change attack-related parameters.
</aside>

In the "Full Simulation Workspace", navigate to **"Section 5: Synthetic Data Generation"**. You will see:

*   ** Sensor Data (Baseline) **: A preview of the `sensor_data_baseline` DataFrame.
*   ** Agent Logs (Baseline) **: A preview of the `agent_logs_baseline` DataFrame.
*   ** Security Metrics (Baseline) **: A preview of the `security_metrics_baseline` DataFrame.

Examine the head of these DataFrames. Notice the `timestamp`, `agent_id`, `value`, `status` in sensor data; `log_type`, `severity`, `message` in agent logs; and `total_alerts_generated`, `average_integrity_score` in security metrics. These represent the normal, uncompromised state of your industrial AI system.

## 7. Data Validation and Initial Statistics
Duration: 02:00

After generating the synthetic data, it's crucial to validate its structure and integrity. The `validate_and_summarize_data()` function performs a series of checks to ensure the data is sound before any attack simulations are applied. This is located in **"Section 6: Data Validation and Initial Statistics"**.

The validation process covers:

*   **DataFrame Type Check:** Ensures the input is indeed a pandas DataFrame.
*   **Missing Columns Check:** Verifies that all expected columns are present.
*   **Data Type Consistency:** Confirms that columns have their anticipated data types (e.g., `datetime64[ns]` for timestamps, `int64` for agent IDs).
*   **Critical Fields Null Check:** Checks for missing values in essential columns.
*   **Unique Key Validation:** Ensures that specified unique identifiers (or combinations of columns) do not contain duplicates.

You'll see validation messages for each DataFrame (Sensor Data, Agent Logs, Security Metrics), indicating whether checks passed or failed. If all checks pass, a success message will be displayed. If any fail, a detailed error message will guide you.

Below the validation messages, you'll also find `describe()` statistics for the numeric columns in each DataFrame, providing a quick summary of their distribution (mean, std, min, max, quartiles).

<aside class="negative">
If data validation fails, it can highlight issues in the data generation process itself. In a real-world scenario, corrupted or incomplete telemetry could be an early indicator of an ongoing attack or system malfunction.
</aside>

## 8. Simulating Vulnerability Impact and Attack Logic
Duration: 04:00

This is the core of the simulation, handled by the `simulate_vulnerability_impact()` function. In **"Section 7: Vulnerability Simulation – Attack Logic"**, the application takes the baseline security metrics and applies the attack parameters you configured in the sidebar.

The `simulate_vulnerability_impact` function:

1.  **Selects Compromised Agents:** Based on `num_compromised_agents`, a subset of agents is randomly chosen to be "compromised".
2.  **Applies Coefficients:** It uses pre-defined `COEFFS` (coefficients) specific to each `attack_type` to model the impact.
    *   `C_type`: Influences alert frequency.
    *   `K_type`: Influences agent integrity scores.
    *   `D_type`: Influences detection latency.
3.  **Perturbs Metrics:** It calculates new `alert_frequency` and `average_integrity_score` values for the affected agents based on `attack_intensity` and the respective coefficients.
4.  **Generates Attack Events:** It records an `attack_events` DataFrame, which includes `detection_latency` and `attack_severity` metrics derived from the attack parameters.

You'll see two new dataframes after this step:

*   ** Attacked Security Metrics **: A preview of `security_metrics_attacked`. Compare this to the baseline security metrics. You should observe changes in alert frequencies and integrity scores, especially for compromised agents if any are selected.
*   ** Attack Events **: A preview of `attack_events`. This DataFrame summarizes the simulated attack, including its severity and calculated detection latency.

<aside class="positive">
Pay close attention to how the `average_integrity_score` changes for specific agents, and how `alert_frequency` (if displayed) is modified based on your chosen attack parameters. These immediate changes are the first indicators of an attack's success.
</aside>

## 9. Understanding the Mathematical Foundations
Duration: 03:00

To fully grasp how the simulation works, it's essential to understand the underlying mathematical models. **"Section 4: Mathematical Foundations of Attack Simulation"** (which is rendered after Section 7 in the Streamlit app) explains the formulas used to quantify the impact of attacks.

1.  **Alert Frequency Over Time ($F_{alerts\_attacked}(t)$):**
    The alert frequency under attack is modeled as an increase over the baseline frequency:
    $$F_{alerts\_attacked}(t) = F_{alerts\_base}(t) \cdot (1 + A_{intensity} \cdot C_{type})$$
    Here, $F_{alerts\_base}(t)$ is the baseline alert frequency, $A_{intensity}$ is the attack intensity from the sidebar, and $C_{type}$ is a coefficient specific to the chosen attack type.

2.  **Detection Latency ($L_{detection}$):**
    The simulated detection latency represents the delay between an attack and its detection:
    $$L_{detection} = L_{base} + A_{intensity} \cdot D_{type}$$
    $L_{base}$ is a baseline latency, and $D_{type}$ is a coefficient specific to the attack type, indicating how much that type of attack impacts detection time.

3.  **Agent Integrity Score ($I_{agent\_attacked}$):**
    The integrity score for a compromised agent is reduced from its baseline:
    $$I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type})$$
    $I_{agent\_base}$ is the baseline integrity score, and $K_{type}$ is a coefficient specific to the attack type, determining how severely integrity is affected.

<aside class="info">
These equations provide a simplified but effective way to model complex security scenarios. The coefficients ($C_{type}$, $K_{type}$, $D_{type}$) are defined in the `COEFFS` dictionary within `ai_security_simulation.py` and are crucial for differentiating the impact of various attack types.
</aside>

## 10. Visualizing Alert Frequency Trend
Duration: 03:00

One of the most immediate impacts of an AI attack can be a distortion of system alerts. **"Section 8: Trend Plot – Alert Frequency Over Time"** presents a line graph generated by `plot_alert_frequency_trend()` that visualizes this.

The plot displays two lines:
*   **Baseline:** Represents the normal alert frequency without any attack.
*   **Attacked:** Shows the alert frequency when the configured attack is active.

Observe how the "Attacked" line deviates from the "Baseline" line.
*   **Increased Alerts:** For many attack types (especially Data Poisoning or Prompt Injection designed to overwhelm), you'll see a noticeable spike in alert frequency.
*   **Fluctuation/Noise:** The attack might also introduce more erratic behavior in the alert stream.

<aside class="info">
Try increasing the `Attack Intensity` or switching `Attack Type` in the sidebar and observe how the "Attacked" line changes. Consider: would your Security Operations Center (SOC) distinguish this as a genuine threat or simply dismiss it as noise?
</aside>

## 11. Visualizing Attack Severity vs. Detection Latency
Duration: 03:00

In **"Section 9: Relationship Plot – Attack Severity vs. Detection Latency"**, you'll find a scatter plot generated by `plot_attack_severity_vs_latency()`. This plot helps you understand the relationship between how severe an attack is and how long it takes for the system to detect it.

*   **X-axis: Attack Severity:** A calculated value representing the overall impact of the attack (proportional to $A_{intensity} \times N_{agents}$).
*   **Y-axis: Simulated Detection Latency (Minutes):** The time it takes for the system to theoretically detect the attack, as calculated by the `simulate_vulnerability_impact` function using the $L_{detection}$ formula.

Each point on the scatter plot represents a simulated attack event. If multiple attack events are simulated (which happens if you run the simulation multiple times with different parameters), you might see a trend.

<aside class="info">
A critical insight from this plot is identifying scenarios where even moderate attack severities lead to long detection latencies. Such a finding would prompt a review of monitoring rules and anomaly detection algorithms.
</aside>

## 12. Visualizing Agent Integrity Comparison
Duration: 03:00

The integrity of individual AI agents is a crucial metric for evaluating system health. **"Section 10: Aggregated Comparison – Agent Integrity Scores"** presents a bar chart generated by `plot_agent_integrity_comparison()` that compares the average integrity scores of compromised agents versus uncompromised agents.

The bar chart will typically show:

*   **Compromised Agents:** The average integrity score for agents identified as being under attack.
*   **Uncompromised Agents:** The average integrity score for agents not affected by the attack.

When `num_compromised_agents` is greater than zero and `attack_intensity` is above zero, you should see a clear difference in the average integrity scores, with compromised agents showing a lower score.

<aside class="info">
Observe the gap between the bars. A significant difference indicates that the attack successfully degraded the integrity of the compromised agents. In a real deployment, a large drop in an agent's integrity score could trigger automated actions like quarantining the agent or triggering a more in-depth investigation.
</aside>

## 13. Discussion and Key Takeaways
Duration: 02:00

You've now explored all the functionalities of the QuLab application. This final section, **"Section 11: Discussion and Reflection Prompts"** and **"Section 12: Key Takeaways"**, encourages you to consolidate your learning.

Take a moment to reflect on the following questions, using the charts and dataframes you've observed:

*   Under which attack types does alert frequency spike the most?
*   When you increase $N_{agents}$ while keeping intensity fixed, how does that change severity and latency?
*   Which combination of $A_{intensity}$ and attack type would you prioritize for red-teaming in a real system?

**Key Takeaways from this Codelab:**

*   **Simulation as a Proactive Tool:** AI security vulnerabilities can and should be explored through synthetic simulations before AI systems are deployed in critical environments.
*   **Simplicity in Modeling:** Even simple mathematical models are effective for stress-testing monitoring logic, understanding potential failure modes, and informing defense strategies.
*   **Importance of Visualization:** Clear visualization of metrics like alerts, detection latency, and agent integrity is vital for quickly understanding attack impact and effectively communicating risks to both technical and non-technical stakeholders.
*   **Holistic Defense:** Effective AI security requires considering multiple attack vectors and their varied impacts on system behavior and agent health.

Congratulations! You have successfully navigated the QuLab AI Security Vulnerability Simulation Lab. You now have a solid foundation for understanding, simulating, and thinking critically about the security of agentic AI systems.
