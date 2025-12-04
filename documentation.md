id: 690bb8d5adbb0296a6bfb062_documentation
summary: AI Security Vulnerability Simulation Lab Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
```
# AI Security Vulnerability Simulation Lab Codelab

## 1. Introduction to the AI Security Vulnerability Simulation Lab
Duration: 00:05:00

Welcome to the **AI Security Vulnerability Simulation Lab**! This codelab will guide you through a Streamlit application designed to provide hands-on experience in identifying, understanding, and analyzing critical AI-security vulnerabilities. The lab focuses specifically on agentic AI systems used for industrial safety monitoring.

<aside class="positive">
<b>Why is this lab important?</b> With the increasing adoption of AI in critical infrastructure and decision-making processes, understanding and mitigating AI-specific security risks is paramount. This lab offers a practical environment to explore these challenges without needing real-world compromised systems.
</aside>

#### Learning Outcomes
By the end of this codelab, you will be able to:
*   Understand the key insights contained in the simulated data.
*   Identify common AI-security vulnerabilities, including 'synthetic-identity risk' and 'untraceable data leakage'.
*   Learn about adversarial testing techniques like prompt injection and data poisoning.
*   Analyze the effectiveness of different defense strategies and risk controls in mitigating AI security threats.

#### Scope and Constraints
This lab is optimized for performance, designed to execute end-to-end on a mid-spec laptop (8 GB RAM) in fewer than 5 minutes. It exclusively uses open-source Python libraries from PyPI. All major steps include both code comments and brief narrative explanations of 'what' is happening and 'why'.

### Application Architecture Overview

The Streamlit application is structured into several distinct pages, each serving a specific purpose, accessible via a sidebar navigation. This modular design makes it easy to understand and extend the application's functionalities.

```mermaid
graph TD
    A[app.py (Main Entry Point)] --> B{Streamlit Sidebar Navigation}
    B --> C[Introduction Page]
    B --> D[Setup Page]
    B --> E[Configuration Page]
    B --> F[Simulation Page]
    B --> G[Visualization Page]

    C -- "application_pages/introduction.py" --> MainContent1[Explains Lab Purpose, Learning Outcomes]
    D -- "application_pages/setup.py" --> MainContent2[Handles Library Imports, Environment Prep]
    E -- "application_pages/configuration.py" --> MainContent3[User Input for Attack Parameters, Constants Display]
    F -- "application_pages/simulation.py" --> MainContent4[Generates Synthetic Data, Executes Attack Simulation]
    G -- "application_pages/visualization.py" --> MainContent5[Plots Simulation Results (Trends, Impact)]
```
*Figure 1: High-level Application Architecture*

As depicted above, `app.py` acts as the orchestrator, loading different content based on user selection in the sidebar. Each page (`introduction.py`, `setup.py`, etc.) encapsulates a specific functional aspect of the simulation lab.

## 2. Environment Setup and Library Imports
Duration: 00:02:00

The first functional step in any robust application is ensuring that all necessary dependencies are loaded and the environment is correctly set up. In this lab, the `setup.py` page handles this aspect.

<aside class="positive">
While the `setup.py` page in this Streamlit app primarily serves as an informational placeholder, in a real-world scenario, this section would contain actual code for installing dependencies (e.g., via `pip install -r requirements.txt`), setting environment variables, or performing initial data checks. For this lab, we assume all required libraries are pre-installed.
</aside>

The content of `application_pages/setup.py` simply informs the user that the necessary libraries have been "successfully loaded," indicating readiness for the subsequent steps.

```python
# application_pages/setup.py
import streamlit as st

def main():
    st.markdown("## Section 2: Setup and Library Imports")
    st.markdown(r"""
    First, we import all necessary Python libraries. This ensures that all required functionalities for data generation, manipulation, simulation, and visualization are available.

    The required libraries have been successfully loaded. We are now ready to define the parameters for our simulation and proceed with data generation and analysis.
    """)
```
This page ensures that conceptually, the user understands that foundational steps have been taken before diving into configuration and simulation.

## 3. Configuring the Simulation Parameters
Duration: 00:07:00

The "Configuration" page (`application_pages/configuration.py`) is where you, as a developer or security analyst, define the parameters for the AI security vulnerability simulation. This page uses Streamlit's sidebar widgets to allow interactive adjustment of key variables that influence the simulation's outcome.

### Simulation Constants

Before diving into user inputs, let's look at the fixed constants that define the simulation's baseline environment:

```python
# application_pages/configuration.py (partial)
# Constants
SIMULATION_DURATION_HOURS = 2       # Total duration of the simulated scenario
NUM_AGENTS = 10                     # Total number of AI agents being monitored
BASE_ALERT_RATE_PER_HOUR = 5        # Baseline frequency of security alerts from agents
ANOMALY_RATE_MULTIPLIER = 2.5       # Factor by which anomaly rates increase during attacks
RANDOM_SEED = 42                    # Seed for reproducibility of random processes
```
These constants establish the fundamental characteristics of our simulated industrial safety monitoring system.

### Interactive Configuration via Sidebar

The `main` function in `configuration.py` sets up the sidebar controls and displays the current configuration.

```python
# application_pages/configuration.py
import streamlit as st

# Constants (as defined above)
SIMULATION_DURATION_HOURS = 2
NUM_AGENTS = 10
BASE_ALERT_RATE_PER_HOUR = 5
ANOMALY_RATE_MULTIPLIER = 2.5
RANDOM_SEED = 42

def main():
    st.sidebar.title("AI Security Vulnerability Simulation Lab")
    st.sidebar.markdown("Adjust parameters to observe the impact of AI security vulnerabilities.")

    # Initialize st.session_state variables if they don't exist
    if 'selected_attack_intensity' not in st.session_state:
        st.session_state.selected_attack_intensity = 0.5
    if 'selected_attack_type' not in st.session_state:
        st.session_state.selected_attack_type = 'Prompt Injection'
    if 'selected_num_compromised_agents' not in st.session_state:
        st.session_state.selected_num_compromised_agents = 2

    # Sidebar user inputs
    st.session_state.selected_attack_intensity = st.sidebar.slider(
        "Select Attack Intensity ($A_{intensity}$)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.selected_attack_intensity,
        step=0.05,
        help="Controls the severity of the simulated attack, ranging from $0.0$ (no attack) to $1.0$ (maximum intensity)."
    )

    st.session_state.selected_attack_type = st.sidebar.selectbox(
        "Select Attack Type",
        options=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'],
        index=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'].index(st.session_state.selected_attack_type),
        help="Determines the specific type of AI security vulnerability being simulated."
    )

    st.session_state.selected_num_compromised_agents = st.sidebar.slider(
        "Select Number of Compromised Agents ($N_{agents}$)",
        min_value=0,
        max_value=NUM_AGENTS,
        value=st.session_state.selected_num_compromised_agents,
        step=1,
        help=f"Specifies how many of the simulated agents (out of {NUM_AGENTS}) are affected by the attack."
    )

    st.markdown("## Current Simulation Parameters")
    st.write(f"**Selected Attack Intensity:** {st.session_state.selected_attack_intensity}")
    st.write(f"**Selected Attack Type:** {st.session_state.selected_attack_type}")
    st.write(f"**Selected Number of Compromised Agents:** {st.session_state.selected_num_compromised_agents}")
    st.write(f"**Simulation Duration (Hours):** {SIMULATION_DURATION_HOURS}")
    st.write(f"**Number of Agents:** {NUM_AGENTS}")
    st.write(f"**Base Alert Rate (Per Hour):** {BASE_ALERT_RATE_PER_HOUR}")
    st.write(f"**Anomaly Rate Multiplier:** {ANOMALY_RATE_MULTIPLIER}")
    st.write(f"**Random Seed:** {RANDOM_SEED}")
```

#### Key Elements:
*   **`st.sidebar.title` and `st.sidebar.markdown`**: These set the title and an introductory message for the sidebar.
*   **`st.session_state`**: This crucial Streamlit feature allows values to be preserved across reruns of the application and across different pages. When you change a value using a widget, it updates `st.session_state`, ensuring consistency.
*   **`st.sidebar.slider`**: Used for `selected_attack_intensity` (a float from $0.0$ to $1.0$) and `selected_num_compromised_agents` (an integer from $0$ to `NUM_AGENTS`).
*   **`st.sidebar.selectbox`**: Used for `selected_attack_type`, offering predefined vulnerability types like 'Prompt Injection' and 'Data Poisoning'.
*   **Help Text**: Each widget includes a `help` parameter to provide context to the user about its function.
*   **Displaying Parameters**: The main content area of the "Configuration" page dynamically displays the currently selected and static simulation parameters.

By adjusting these controls, you can immediately see how different attack scenarios will be constructed for the simulation.

## 4. Executing the Vulnerability Simulation
Duration: 00:10:00

The "Simulation" page (`application_pages/simulation.py`) is the core of the lab, where the synthetic safety data is generated and the chosen AI security vulnerability is simulated. This page leverages two main functions: `generate_synthetic_safety_data` and `simulate_vulnerability_impact`.

### Simulation Flow

```mermaid
graph TD
    A[Start Simulation] --> B[Load Constants and Coefficients]
    B --> C{Call generate_synthetic_safety_data}
    C -- "Generates Baseline Data" --> D[Display Baseline Data (Sensor, Agent, Security Metrics)]
    D --> E{Retrieve User Config from st.session_state}
    E --> F{Call simulate_vulnerability_impact}
    F -- "Applies Attack to Baseline Metrics" --> G[Display Attacked Metrics and Attack Events]
    G --> H[End Simulation Step]
```
*Figure 2: Simulation Process Flow*

### Key Components

#### 1. Simulation Constants and Coefficients
Beyond the global constants, `simulation.py` defines specific coefficients that model the impact of different attack types.

```python
# application_pages/simulation.py (partial)
import streamlit as st
import pandas as pd
import numpy as np

# Constants (same as in configuration.py)
SIMULATION_DURATION_HOURS = 2
NUM_AGENTS = 10
BASE_ALERT_RATE_PER_HOUR = 5
ANOMALY_RATE_MULTIPLIER = 2.5
RANDOM_SEED = 42

# Coefficients for vulnerability impact
COEFFS = {
    'C_type': {'Prompt Injection': 0.5, 'Data Poisoning': 0.8, 'Synthetic Identity': 0.6, 'Untraceable Data Leakage': 0.7},
    'K_type': {'Prompt Injection': 0.4, 'Data Poisoning': 0.7, 'Synthetic Identity': 0.8, 'Untraceable Data Leakage': 0.5},
    'D_type': {'Prompt Injection': 20, 'Data Poisoning': 60, 'Synthetic Identity': 45, 'Untraceable Data Leakage': 30},
    'L_base': 5
}
```
*   **`C_type`**: Represents the **impact coefficient** on alert rates for each attack type. A higher value means a more significant increase in alerts.
*   **`K_type`**: Represents the **severity coefficient** on data integrity or latency for each attack type. Higher values indicate more severe data corruption or system delays.
*   **`D_type`**: Represents the **detection difficulty** or time delay in minutes for each attack type. Higher values mean the attack is harder/slower to detect.
*   **`L_base`**: A baseline latency value.

#### 2. `generate_synthetic_safety_data()`

This function is responsible for creating a realistic baseline dataset for an industrial safety monitoring system. Although the internal implementation is abstracted, its purpose is to produce:
*   `sensor_data_baseline`: Time-series data from various sensors.
*   `agent_logs_baseline`: Log entries generated by AI agents.
*   `security_metrics_baseline`: Baseline security performance indicators (e.g., alert rates, false positives).
*   `sim_config`: The configuration used for generation.

This baseline data simulates a healthy, uncompromised system before any attacks are introduced.

#### 3. `simulate_vulnerability_impact()`

This is where the magic happens! This function takes the baseline security metrics and applies the selected attack based on the user's configuration.

*   It uses `attack_type`, `attack_intensity`, and `num_compromised_agents` from `st.session_state` (passed as arguments) along with the `COEFFS` to calculate the impact.
*   For example, an attack might increase `alert_frequency`, degrade `data_integrity`, or introduce `system_latency` based on the coefficients for the chosen `attack_type`.
*   It returns:
    *   `security_metrics_attacked`: The security metrics after the simulated attack.
    *   `attack_events`: A log of specific attack events and their simulated immediate impacts.

#### Streamlit Integration

The `main` function orchestrates these calls and displays the results:

```python
# application_pages/simulation.py
def main():
    st.markdown("## Vulnerability Simulation")
    try:
        # Generate baseline data
        sensor_data_baseline, agent_logs_baseline, security_metrics_baseline, sim_config = generate_synthetic_safety_data(
            num_agents=NUM_AGENTS,
            simulation_duration_hours=SIMULATION_DURATION_HOURS,
            base_alert_rate=BASE_ALERT_RATE_PER_HOUR,
            anomaly_rate_multiplier=ANOMALY_RATE_MULTIPLIER,
            random_seed=RANDOM_SEED
        )

        st.subheader("Synthetic Data (Baseline)")
        st.dataframe(sensor_data_baseline.head())
        st.dataframe(agent_logs_baseline.head())
        st.dataframe(security_metrics_baseline.head())

        # Simulate the attack based on user's configuration
        security_metrics_attacked, attack_events = simulate_vulnerability_impact(
            base_metrics_df=security_metrics_baseline,
            attack_type=st.session_state.selected_attack_type,
            attack_intensity=st.session_state.selected_attack_intensity,
            num_compromised_agents=st.session_state.selected_num_compromised_agents,
            simulation_config=sim_config
        )

        st.subheader("Simulated Attack Results")
        st.dataframe(security_metrics_attacked.head())
        st.dataframe(attack_events.head())

    except Exception as e:
        st.error(f"An error occurred: {e}")
```
*   `st.dataframe(df.head())`: Used to display the first few rows of the generated Pandas DataFrames, allowing you to inspect the raw data.
*   Error Handling: A `try-except` block is included to catch and display any errors during the simulation process.

By interacting with this page, you can see how different attack types and intensities manifest in changed security metrics, such as increased alert frequencies or compromised agent integrity.

## 5. Visualizing Simulation Outcomes
Duration: 00:08:00

The "Visualization" page (`application_pages/visualization.py`) is crucial for understanding the impact of the simulated AI security vulnerabilities. It presents the results from the "Simulation" step in an easily digestible graphical format using `matplotlib` and `seaborn`.

<aside class="negative">
In the provided `visualization.py` code, placeholder `fake_` dataframes are used for plotting. In a complete application, these would be replaced with the actual `security_metrics_baseline`, `security_metrics_attacked`, and `attack_events` dataframes generated in the "Simulation" step, likely passed via `st.session_state` or a global object. For this codelab, we will explain the *intended purpose* of each plot.
</aside>

### Plotting Functions

The page defines three main plotting functions, each designed to highlight a different aspect of the simulation's impact.

#### 1. `plot_alert_frequency_trend()`
This function visualizes the trend of security alerts over time, comparing the baseline (uncompromised) state with the attacked state.

*   **Purpose**: To clearly show how an AI security attack leads to an increase in security alerts or changes in their pattern. This helps in identifying anomaly detection post-attack.
*   **Expected Output**: A line plot showing alert frequency (e.g., alerts per hour) on the y-axis against time on the x-axis, with two distinct lines for baseline and attacked scenarios.

#### 2. `plot_attack_severity_vs_latency()`
This plot explores the relationship between the severity of an attack event and the resulting system latency.

*   **Purpose**: To illustrate that more severe attacks (e.g., higher data corruption or resource consumption) can lead to increased operational latency in AI agents or the overall system. This highlights performance degradation as a side effect of attacks.
*   **Expected Output**: A scatter plot or regression plot showing attack severity on one axis and system latency (e.g., in milliseconds) on the other.

#### 3. `plot_agent_integrity_comparison()`
This function compares the integrity metrics of compromised agents versus uncompromised agents.

*   **Purpose**: To directly show the impact of an attack on the trustworthiness or reliability of specific AI agents. This can include metrics like data integrity score, accuracy, or false positive rates.
*   **Expected Output**: A bar chart or box plot comparing an integrity metric for two groups of agents: compromised and non-compromised.

### Streamlit Integration

The `main` function in `visualization.py` calls these plotting functions and renders them using Streamlit.

```python
# application_pages/visualization.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd # Added for fake data creation

# Plotting function stubs (actual implementation omitted for brevity, but described above)
def plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size):
    # ... plotting logic using base_df, attacked_df, attack_type, attack_intensity ...
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot([1,2,3], [5,6,7], label="Baseline") # Placeholder
    ax.plot([1,2,3], [5,9,12], label="Attacked") # Placeholder
    ax.set_title(f"Alert Frequency Trend ({attack_type} @ {attack_intensity})", fontsize=font_size)
    ax.set_xlabel("Time (Hours)", fontsize=font_size-2)
    ax.set_ylabel("Alert Frequency", fontsize=font_size-2)
    ax.legend()
    return fig

def plot_attack_severity_vs_latency(attack_events_df, font_size):
    # ... plotting logic using attack_events_df ...
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter([0.1, 0.5, 0.9], [10, 50, 90]) # Placeholder
    ax.set_title("Attack Severity vs. System Latency", fontsize=font_size)
    ax.set_xlabel("Attack Severity Score", fontsize=font_size-2)
    ax.set_ylabel("System Latency (ms)", fontsize=font_size-2)
    return fig

def plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size):
    # ... plotting logic using attacked_df, num_compromised_agents ...
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(['Compromised', 'Uncompromised'], [0.4, 0.9]) # Placeholder
    ax.set_title(f"Agent Integrity Comparison (N={num_compromised_agents} Compromised)", fontsize=font_size)
    ax.set_ylabel("Agent Integrity Score", fontsize=font_size-2)
    return fig


def main():
    st.markdown("## Visualization")
    try:
        # Prepare fake data for plotting (in a real app, these would come from st.session_state)
        # Using placeholder data for demonstration as actual data generation logic is omitted in the snippet
        fake_base_df = pd.DataFrame({'time': [1,2,3], 'alert_frequency': [5,6,7]})
        fake_attacked_df = pd.DataFrame({'time': [1,2,3], 'alert_frequency': [5,9,12], 'agent_integrity': [0.4, 0.5, 0.6]})
        fake_attack_events_df = pd.DataFrame({'severity_score': [0.1, 0.5, 0.9], 'latency_ms': [10, 50, 90]})

        font_size = 14 # Define a font size for consistent plotting

        st.subheader("Alert Frequency Trend")
        fig_trend = plot_alert_frequency_trend(fake_base_df, fake_attacked_df, 'Prompt Injection', 0.5, font_size)
        st.pyplot(fig_trend)
        plt.close(fig_trend) # Important to close figures to prevent memory issues

        st.subheader("Attack Severity vs. System Latency")
        fig_rel = plot_attack_severity_vs_latency(fake_attack_events_df, font_size)
        st.pyplot(fig_rel)
        plt.close(fig_rel)

        st.subheader("Agent Integrity Comparison")
        fig_comp = plot_agent_integrity_comparison(fake_attacked_df, 1, font_size) # Assuming 1 compromised agent for this fake data
        st.pyplot(fig_comp)
        plt.close(fig_comp)

    except Exception as e:
        st.error(f"An error occurred during visualization: {e}")

```
*   `st.pyplot(fig)`: This is Streamlit's function to display a `matplotlib` figure.
*   `plt.close(fig)`: It's a best practice to close `matplotlib` figures after displaying them with `st.pyplot` to free up memory, especially in long-running Streamlit applications.
*   `st.subheader()`: Used to provide titles for individual plots, enhancing readability.

This visualization step provides invaluable insights into the direct and indirect consequences of AI security vulnerabilities, allowing developers and analysts to grasp the magnitude and nature of the threats.

## 6. Understanding the Application Entry Point (`app.py`)
Duration: 00:03:00

Finally, let's look at `app.py`, which is the main entry point for the entire Streamlit application. This file sets up the overall page configuration, displays the header, and manages the navigation between different application pages.

```python
# app.py
import streamlit as st

# Configure the Streamlit page
st.set_page_config(page_title="AI Security Vulnerability Simulation Lab", layout="wide")

# Display a logo and separator in the sidebar
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()

# Main title for the application
st.title("AI Security Vulnerability Simulation Lab")
st.divider()

# Sidebar navigation selectbox
page = st.sidebar.selectbox(label="Navigation", options=["Introduction", "Setup", "Configuration", "Simulation", "Visualization"])

# Conditional loading of pages based on selection
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
```

#### Key Components:
*   **`st.set_page_config()`**: This function must be called as the very first Streamlit command. It configures global settings for your app, such as the page title (visible in the browser tab) and the layout (`"wide"` for more horizontal space).
*   **`st.sidebar.image()` and `st.sidebar.divider()`**: These commands add an image and a visual separator to the Streamlit sidebar, enhancing the application's branding and aesthetics.
*   **`st.title()` and `st.divider()`**: These create the main title for the application's content area and a horizontal divider for visual separation.
*   **`st.sidebar.selectbox()`**: This is the core navigation mechanism. It creates a dropdown menu in the sidebar with a list of page options. The user's selection is stored in the `page` variable.
*   **Conditional Page Loading**: The `if/elif` block checks the value of the `page` variable and dynamically imports and calls the `main()` function of the corresponding module from the `application_pages` directory. This pattern allows for a multi-page application structure within a single Streamlit script.

This `app.py` effectively acts as the central router, ensuring that only the relevant page content is displayed to the user at any given time, providing a smooth and organized user experience for the AI Security Vulnerability Simulation Lab.

Congratulations! You have now a comprehensive understanding of the AI Security Vulnerability Simulation Lab, its architecture, configuration, simulation logic, and visualization capabilities. This knowledge will enable you to effectively explore and analyze AI security threats in agentic systems.
```