id: 690bb8d5adbb0296a6bfb062_user_guide
summary: AI Security Vulnerability Simulation Lab User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Exploring AI Security Vulnerabilities in Agentic Systems

## Step 1: Introduction to AI Security Vulnerabilities and the QuLab Application
Duration: 00:05

Welcome to the QuLab, a hands-on laboratory designed to explore the critical field of **AI security vulnerabilities within agentic AI systems**. In today's rapidly evolving technological landscape, AI agents are increasingly deployed in sensitive environments, such as industrial safety monitoring. While highly efficient, these systems are also susceptible to sophisticated attacks that can compromise their integrity, performance, and ultimately, safety.

This codelab will provide you with a unique opportunity to interact with a simulated industrial safety monitoring system and observe how various AI security threats manifest. We'll delve into concepts like:
-   **Prompt Injection**: A type of attack where malicious instructions are inserted into a prompt to manipulate an AI model's behavior.
-   **Data Poisoning**: An attack where malicious data is fed into a model's training set, leading it to learn incorrect or biased patterns.
-   **Synthetic-Identity Risk**: The danger posed by AI agents creating or mimicking fake identities to bypass security protocols or propagate misinformation.
-   **Untraceable Data Leakage**: The challenge of identifying and preventing sensitive information from being leaked by AI systems in ways that are hard to track.
-   **Alert Frequency**: How often the system generates warnings or alerts.
-   **Detection Latency**: The time it takes for the system to identify an anomalous or malicious event.
-   **Agent Integrity Score**: A measure of the trustworthiness and reliability of individual AI agents.

By the end of this lab, you'll gain practical insights into adversarial testing techniques and understand the paramount importance of robust risk controls in designing secure and adaptive AI systems. We will achieve this through interactive visualizations and data analysis, helping you grasp the real-world implications of these vulnerabilities.

Let's begin by navigating through the application using the sidebar. The main application page, `app.py`, provides an initial overview and routes to three distinct pages, each focusing on a different aspect of our simulation.

<aside class="positive">
<b>The goal of this lab is not to dive into the code behind the simulation, but to understand the practical impact of AI security vulnerabilities and the concepts involved.</b>
</aside>

## Step 2: Understanding the Simulation Environment and Baseline Data Generation
Duration: 00:07

To effectively study AI security vulnerabilities, we need a controlled environment. In this lab, we use **synthetic data** to simulate the normal operations of an industrial safety monitoring system. This allows us to observe the effects of attacks without handling sensitive real-world data.

Navigate to **"Page 1: Overview & Data Generation"** using the sidebar.

<aside class="positive">
If you just started the application, you should already be on "Page 1: Overview & Data Generation".
</aside>

On this page, you'll find:
-   **Learning Goals**: A clear outline of what you'll achieve by completing this lab.
-   **Data/Inputs Overview**: An explanation of the types of synthetic data generated.
-   **Fixed Simulation Parameters**: These are the foundational settings for our simulated environment.

```console
- Simulation Duration: 2 hours
- Number of Agents: 10
- Base Alert Rate (per hour): 0.5
- Anomaly Rate Multiplier: 1.5
- Random Seed: 42
```
These parameters ensure a consistent and reproducible baseline for our experiments.

The application automatically generates three key datasets representing the normal, secure operation of our industrial safety system:
1.  **Sensor Data Baseline**: This simulates real-time readings from various industrial sensors (e.g., temperature, pressure).
2.  **Agent Logs Baseline**: This captures communications and actions between our AI agents.
3.  **Security Metrics Baseline**: This includes initial measurements of system health, such as alert frequencies and agent integrity scores.

Scroll down to the "Baseline Data Preview (First 5 Rows)" section. Here, you can see snippets of the generated dataframes.

<aside class="positive">
Observe the `agent_integrity_score` in the "Security Metrics Baseline". In this normal state, agent integrity scores are typically high, indicating healthy and trustworthy agents.
</aside>

This baseline data represents our 'normal' or 'secure' state. All subsequent attack simulations will build upon and deviate from this baseline, allowing us to quantify the impact of vulnerabilities.

## Step 3: Configuring Attack Scenarios and Data Validation
Duration: 00:10

Now that we have our baseline, we can start configuring our attack scenarios.

Navigate to **"Page 2: Simulation Configuration & Validation"** using the sidebar.

This page first outlines the **Methodology Overview** for our lab, which involves synthetic data generation, interactive parameter definition, attack simulation, visualization, and analysis.

A crucial part of our simulation is the **mathematical foundations** that define how attacks impact our system metrics. This lab uses simplified formulas to model these complex interactions, making the concepts tangible:

### Alert Frequency Over Time
The alert frequency under attack, $F_{alerts\_attacked}(t)$, is calculated as:
$$ F_{alerts\_attacked}(t) = F_{alerts\_base}(t) \cdot (1 + A_{intensity} \cdot C_{type}) $$
-   $F_{alerts\_base}(t)$ is the baseline alert frequency.
-   $A_{intensity}$ is the **Attack Intensity** you will define (between 0.0 and 1.0). A higher intensity means a stronger attack.
-   $C_{type}$ is a scaling factor specific to the **Attack Type** (e.g., Prompt Injection, Data Poisoning). This value reflects how much a specific type of attack inherently increases alert frequency. Different attack types have different $C_{type}$ values (e.g., `{'Prompt Injection': 0.5, 'Data Poisoning': 0.8}`).

### Detection Latency
The simulated detection latency, $L_{detection}$, is calculated as:
$$ L_{detection} = L_{base} + A_{intensity} \cdot D_{type} $$
-   $L_{base}$ is a nominal baseline detection latency (set to 5 minutes).
-   $D_{type}$ is a coefficient related to the **Attack Type**, indicating how difficult that specific attack is to detect quickly. Different attack types have different $D_{type}$ values (e.g., `{'Prompt Injection': 20, 'Data Poisoning': 60}` minutes). A higher $D_{type}$ means longer detection times.

### Agent Integrity Score
The agent integrity score under attack, $I_{agent\_attacked}$, is calculated for compromised agents as:
$$ I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type}) $$
-   $I_{agent\_base}$ is the baseline agent integrity score.
-   $K_{type}$ is a coefficient for the **Attack Type**, reflecting its detrimental effect on agent trustworthiness. Different attack types have different $K_{type}$ values (e.g., `{'Prompt Injection': 0.4, 'Data Poisoning': 0.7}`). A higher $K_{type}$ means a greater reduction in integrity.
-   For **uncompromised agents**, their integrity score remains $I_{agent\_base}$.

### Configure Simulation Parameters
Now, it's your turn to configure the attack! On the **sidebar** (left side of the screen), you will see the "Simulation Controls".
-   **Attack Intensity ($A_{intensity}$)**: Use the slider to set the severity of the attack. Try a value like `0.7`.
-   **Attack Type**: Select the type of vulnerability you want to simulate. Start with **'Prompt Injection'**.
-   **Number of Compromised Agents ($N_{agents}$)**: Specify how many AI agents are affected by the attack. Try `3`.

<aside class="negative">
Remember, the goal is to understand how these parameters affect the system. Feel free to experiment with different combinations later!
</aside>

### Data Validation Summary
Before moving on, the application performs a **Data Validation Summary** to ensure the integrity and structure of the baseline data generated in Step 2. This step checks for:
-   Presence of all expected columns.
-   Correct data types for each column.
-   Absence of null values in critical fields.
-   Uniqueness of key identifiers.

Scroll down to see the validation results for "Sensor Data Baseline", "Agent Logs Baseline", and "Security Metrics Baseline". You should see `st.success` messages if everything is validated correctly. This confirms our baseline data is ready for simulation.

## Step 4: Simulating Vulnerabilities and Analyzing the Impact
Duration: 00:15

With the attack parameters configured and data validated, we can now simulate the vulnerability and analyze its impact.

Navigate to **"Page 3: Vulnerability Simulation & Analysis"** using the sidebar.

This page first displays a summary of the attack parameters you selected in the previous step:
-   **Attack Type**: The vulnerability being simulated.
-   **Attack Intensity**: The severity of the attack.
-   **Number of Compromised Agents**: How many agents are directly affected.

The application then runs the `simulate_vulnerability_impact` function, which applies the mathematical models discussed in Step 3 to the baseline security metrics. This generates two new datasets:
-   **Attacked Security Metrics**: The security metrics after the attack, showing the changes in alert frequency and agent integrity.
-   **Attack Events**: A summary of the attack itself, including its severity and the simulated detection latency.

Scroll down to see the "Attacked Data Preview". You will find the first 5 rows of `Attacked Security Metrics` and `Attack Events` dataframes. Notice how the `alert_frequency` might be higher and `agent_integrity_score` might be lower for some agents compared to the baseline, especially for compromised ones. Also, observe the `simulated_detection_latency` in the `Attack Events` dataframe.

### Visualizations
The most insightful part of this lab is the **Visualizations** section. These plots illustrate the impact of the simulated AI security vulnerability:

#### 1. Trend Plot: Alert Frequency Over Time
This plot shows two lines: "Baseline" (our normal operation) and "Attacked" (under the simulated vulnerability).
-   **Observe**: How does the "Attacked" alert frequency compare to the "Baseline"?
-   **Interpret**: A noticeable increase in alert frequency in the "Attacked" scenario indicates that the AI system is generating more alerts due to the attack. This could signify unusual activity, system distress, or even malicious attempts to overload the monitoring system with false positives.

#### 2. Relationship Plot: Attack Severity vs. Detection Latency
This scatter plot helps us understand the relationship between how severe an attack is and how quickly the system can detect it. Each point represents an attack event.
-   **Observe**: Look at the X-axis (Attack Severity) and Y-axis (Simulated Detection Latency). Do you see a trend where higher severity attacks lead to longer detection times?
-   **Interpret**: Longer detection latency means the attack has more time to cause damage before it's identified and mitigated. This highlights the critical importance of low detection latency in a secure AI system. Different attack types might also cluster differently, showing how some vulnerabilities are inherently harder to detect than others.

#### 3. Aggregated Comparison: Agent Integrity Scores
This bar chart provides a clear comparison of the average integrity scores between agents that were 'Compromised' by the attack and those that remained 'Uncompromised'.
-   **Observe**: Compare the height of the "Compromised" bar to the "Uncompromised" bar.
-   **Interpret**: A lower integrity score for compromised agents directly indicates a degradation in their trustworthiness and reliability. This is a critical metric for assessing the health of individual AI agents and the overall security posture of the agentic system.

<aside class="positive">
<b>Experiment Time!</b> Go back to "Page 2: Simulation Configuration & Validation" using the sidebar. Change the "Attack Intensity" to `0.2` and then to `1.0`. Change the "Attack Type" to 'Data Poisoning' or 'Synthetic Identity'. Change the "Number of Compromised Agents". Then, return to "Page 3: Vulnerability Simulation & Analysis" to observe how the visualizations change with different parameters. This will solidify your understanding of the impact of various attack vectors.
</aside>

## Step 5: Key Takeaways and Conclusion
Duration: 00:03

You have successfully navigated through the QuLab application, simulating AI security vulnerabilities and analyzing their impact on an industrial safety monitoring system.

Scroll down to the "Discussion & Conclusion" section on "Page 3". This section summarizes the key insights derived from the simulations:
-   **Impact of Attack Intensity**: How the strength of an attack directly correlates with its effects.
-   **Vulnerability-Specific Effects**: The unique ways different attack types (e.g., prompt injection vs. data poisoning) manifest within the system.
-   **Importance of Timely Detection**: The crucial role of swift attack identification in minimizing negative consequences.
-   **Agent Integrity**: The direct relationship between attacks and the trustworthiness of individual AI agents.

This lab provided a foundational, yet practical, understanding of AI security risks. By visualizing these impacts, you are better equipped to comprehend the challenges in designing, implementing, and validating adaptive AI systems that can withstand emerging threats. Understanding these vulnerabilities is the first step towards building more resilient and secure AI solutions.

You can also review the "References" section for additional resources on AI security.

Congratulations on completing the QuLab on AI Security Vulnerabilities! You now have a stronger grasp of how these complex concepts translate into tangible impacts on AI system performance and security.
