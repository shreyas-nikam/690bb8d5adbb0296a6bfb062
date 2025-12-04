id: 690bb8d5adbb0296a6bfb062_documentation
summary: AI Security Vulnerability Simulation Lab Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI Security Vulnerability Simulation Lab with Streamlit

## Step 1: Introduction to the AI Security Simulation Lab
Duration: 00:05

Welcome to the AI Security Vulnerability Simulation Lab! In today's rapidly evolving technological landscape, Artificial Intelligence (AI) systems are becoming increasingly ubiquitous, driving innovation across various sectors. However, with their growing adoption comes the critical need to understand and mitigate their unique security vulnerabilities.

<aside class="positive">
This lab provides a hands-on experience to understand **AI security vulnerabilities** through interactive simulations and visualizations. It's designed to give developers insights into common attack vectors, such as **synthetic-identity risk**, and demonstrate the importance of effective risk controls.
</aside>

**Why is AI Security Important?**
AI systems can be susceptible to various attacks, including data poisoning, model evasion, and adversarial attacks, which can lead to biased decisions, privacy breaches, and even system failures. Understanding these risks is crucial for building robust, secure, and trustworthy AI applications.

This Streamlit application serves as a foundational platform to:
*   **Explore AI security concepts:** Get acquainted with the types of vulnerabilities that AI systems face.
*   **Simulate attacks:** Observe the impact of different attack types and intensities on AI system metrics.
*   **Visualize outcomes:** Understand the effects of attacks through clear, interactive plots.

The application is structured into two main sections:
1.  **Overview:** Introduces the lab and its core objectives.
2.  **Simulation:** Allows users to run simulated attacks and visualize their impact.

### Application Architecture Overview
The application uses Streamlit's multi-page capability to manage different sections. The `app.py` file acts as the main entry point, handling global configurations and navigation, while individual pages (`page_1.py`, `page_2.py`) contain the specific logic and UI for their respective sections.

<pre><code>
                               +--+
                               |         app.py              |
                               | (Main Streamlit Entrypoint) |
                               +-++
                                     |
                                     | Configures page, sidebar, navigation
                                     v
                  +-+
                  |  Sidebar Navigation (st.sidebar.selectbox)   |
                  +-+
                         |                       |
                         |  Selects "Overview"   |  Selects "Simulation"
                         v                       v
            ++     +--+
            | application_pages/  |     | application_pages/       |
            | page_1.py           |     | page_2.py                |
            | (Overview Page)     |     | (Simulation Page)        |
            ++     +--+
                      |                                |
                      v                                v
            Displays introduction       Generates synthetic data, simulates
            and high-level context      attacks, plots impact, displays visualizations
</code></pre>

This modular structure makes the application easy to extend and maintain, allowing developers to add new simulation scenarios or overview content without significant refactoring.

## Step 2: Setting Up Your Development Environment
Duration: 00:05

Before you can run the AI Security Vulnerability Simulation Lab, you need to set up your development environment.

### Prerequisites
*   **Python 3.7+:** Ensure you have a recent version of Python installed.
*   **pip:** Python's package installer, which usually comes with Python.

### Installation Steps

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate   # On Windows
    ```

2.  **Install the required Python packages:**
    The application primarily uses `streamlit`, `pandas`, `matplotlib`, and `seaborn`.
    ```bash
    pip install streamlit pandas matplotlib seaborn numpy
    ```
    We also include `numpy` as it's often used with `pandas` and for numerical operations in simulation.

3.  **Create the application files:**
    You'll need to create the following file structure:
    ```
    .
    ├── app.py
    └── application_pages/
        ├── page_1.py
        └── page_2.py
    ```
    Copy the code provided in the subsequent steps into their respective files.

## Step 3: Understanding the Main Application Entry Point (`app.py`)
Duration: 00:10

The `app.py` file is the heart of your Streamlit application. It sets up the global page configuration, displays the main title and branding, and manages navigation between different parts of the lab.

Copy the following code into your `app.py` file:

```python
import streamlit as st

# Configure the Streamlit page
st.set_page_config(page_title='QuLab', layout='wide')

# Display a logo in the sidebar
st.sidebar.image('https://www.quantuniversity.com/assets/img/logo5.jpg')
st.sidebar.divider()

# Main title for the application
st.title('QuLab')
st.divider()

st.markdown("""
In this lab, explore AI security vulnerabilities through interactive simulations and visualizations.
""")

# Sidebar navigation for switching between pages
page = st.sidebar.selectbox('Navigation', ['Overview', 'Simulation'])

# Conditional rendering based on sidebar selection
if page == 'Overview':
    from application_pages.page_1 import main
    main()
elif page == 'Simulation':
    from application_pages.page_2 import main
    main()
```

### Code Explanation:
*   `st.set_page_config(page_title='QuLab', layout='wide')`: This line configures the browser tab title and sets the page layout to `wide`, allowing for more content to be displayed horizontally.
*   `st.sidebar.image(...)` and `st.sidebar.divider()`: These add branding (a logo) and visual separation to the sidebar.
*   `st.title('QuLab')` and `st.markdown(...)`: These display the main application title and a brief introductory text on the main content area.
*   `st.sidebar.selectbox('Navigation', ['Overview', 'Simulation'])`: This is the key component for navigation. It creates a dropdown menu in the sidebar, allowing users to switch between the "Overview" and "Simulation" pages.
*   `if page == 'Overview': ... elif page == 'Simulation': ...`: This block dynamically imports and calls the `main()` function from the selected page's module. This is Streamlit's common pattern for implementing multi-page applications.

## Step 4: Deep Dive into the Overview Page (`application_pages/page_1.py`)
Duration: 00:05

The `application_pages/page_1.py` file contains the content for the "Overview" section of the lab. Its primary purpose is to introduce the user to the lab's objectives and the concepts they will explore.

Create a folder named `application_pages` in the same directory as `app.py`. Then, create `page_1.py` inside the `application_pages` folder and copy the following code into it:

```python
import streamlit as st

def main():
    st.title('AI Security Vulnerability Simulation Lab - Overview')
    st.markdown('''\n    ## Introduction\n    Explore AI security vulnerabilities through interactive simulation. \n    Understand common vulnerabilities like 'synthetic-identity risk' and learn about effective risk controls.\n    ''')

if __name__ == '__main__':
    main()
```

### Code Explanation:
*   `def main():`: This function encapsulates the Streamlit components for this page. It's called by `app.py` when the "Overview" option is selected.
*   `st.title(...)`: Displays a specific title for the overview page.
*   `st.markdown(...)`: Renders the introductory text about AI security vulnerabilities, interactive simulation, `synthetic-identity risk`, and risk controls using Markdown formatting.

<aside class="positive">
Using `st.markdown` with triple quotes `'''...'''` allows you to write multi-line markdown content, including headers (`## Introduction`), making it easy to format rich text.
</aside>

## Step 5: Exploring the Simulation Page (`application_pages/page_2.py`)
Duration: 00:20

The `application_pages/page_2.py` file is where the core simulation logic and visualization reside. This page allows users to simulate the impact of various attack types on a hypothetical AI system and visualize the changes over time.

**Important Note:** The original provided `page_2.py` relied on two undefined functions: `generate_synthetic_safety_data` and `simulate_vulnerability_impact`. For this codelab to be executable and comprehensive, we will provide placeholder implementations for these functions. These placeholders will mimic the expected behavior, allowing the plotting function to work correctly. In a real-world scenario, these would contain complex logic based on actual data models and attack simulations.

Create `page_2.py` inside the `application_pages` folder and copy the following code into it:

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime

#  Placeholder Functions for Simulation 
# In a real application, these would contain complex data generation and attack logic.

def generate_synthetic_safety_data(num_points, base_alert_rate, max_base_variation, random_seed):
    """
    Generates synthetic baseline safety data (e.g., alert frequencies).
    """
    np.random.seed(random_seed)
    timestamps = [datetime.datetime.now() - datetime.timedelta(minutes=i) for i in range(num_points)][::-1]
    # Simulate a baseline alert count with some natural variation
    alerts = np.random.normal(loc=base_alert_rate, scale=max_base_variation, size=num_points)
    alerts = np.maximum(0, alerts).astype(int) # Ensure non-negative integer alert counts
    df = pd.DataFrame({'timestamp': timestamps, 'alert_count': alerts})
    return df

def simulate_vulnerability_impact(base_df, attack_type, attack_intensity, impact_factor, config):
    """
    Simulates the impact of a vulnerability on the baseline data.
    For this placeholder, it simply increases alert counts based on intensity.
    """
    attacked_df = base_df.copy()
    # A simple simulation: increase alert count based on intensity and a fixed impact factor
    # In a real scenario, 'attack_type' would dictate a more complex modification
    attacked_df['alert_count'] = attacked_df['alert_count'] + \
                                 (attacked_df['alert_count'] * attack_intensity * impact_factor).astype(int)
    attacked_df['alert_count'] = np.maximum(0, attacked_df['alert_count']) # Ensure non-negative alerts
    
    # In a full simulation, attack_events would detail when/how attacks occurred
    attack_events = {} 
    return attacked_df, attack_events

#  Visualization Function 

@st.cache_data
def plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size):
    """
    Plots the trend of alert frequency for both baseline and attacked scenarios.
    Uses st.cache_data for performance optimization.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot baseline data
    sns.lineplot(x='timestamp', y='alert_count', data=base_df, ax=ax, label='Baseline', marker='o')
    
    # Plot attacked data
    sns.lineplot(x='timestamp', y='alert_count', data=attacked_df, ax=ax, 
                 label=f'Attacked ({attack_type} - {attack_intensity*100:.0f}%)', 
                 linestyle='dashed', marker='x')
    
    ax.set_title('Alert Frequency Over Time', fontsize=font_size)
    ax.set_xlabel('Timestamp', fontsize=font_size*0.8)
    ax.set_ylabel('Alert Count', fontsize=font_size*0.8)
    ax.tick_params(axis='both', which='major', labelsize=font_size*0.7)
    ax.legend(fontsize=font_size*0.8)
    plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    return fig


def main():
    st.title('AI Security Vulnerability Simulation Lab - Simulation')
    st.markdown('''\n    Simulate various attack types and intensities and visualize their impact on system metrics.\n    ''')

    # Example synthetic data generation and attack simulation
    # Parameters for synthetic data: num_points, base_alert_rate, max_base_variation, random_seed
    sensor_data_baseline = generate_synthetic_safety_data(num_points=50, 
                                                        base_alert_rate=10, 
                                                        max_base_variation=3, 
                                                        random_seed=42)

    # Parameters for attack simulation: base_df, attack_type, attack_intensity, impact_factor, config
    security_metrics_attacked, attack_events = simulate_vulnerability_impact(
        sensor_data_baseline, 'Data Poisoning', 0.5, 5, {} # 0.5 intensity, impact factor 5
    )

    st.subheader('Trend Plot: Simulated Alert Frequency')
    # Plot the trend
    fig_trend = plot_alert_frequency_trend(sensor_data_baseline, security_metrics_attacked, 'Data Poisoning', 0.5, 14)
    st.pyplot(fig_trend)

    st.markdown('''
    Above, you can observe how an attack (e.g., 'Data Poisoning') at a certain intensity affects the 'Alert Count' over time compared to a baseline scenario. The dashed line represents the system under attack.
    ''')
    
    # Display raw data for inspection (optional)
    st.subheader('Raw Simulated Data (Baseline vs. Attacked)')
    col1, col2 = st.columns(2)
    with col1:
        st.write("Baseline Data")
        st.dataframe(sensor_data_baseline)
    with col2:
        st.write("Attacked Data")
        st.dataframe(security_metrics_attacked)


if __name__ == '__main__':
    main()
```

### Code Explanation:

#### Placeholder Functions (`generate_synthetic_safety_data`, `simulate_vulnerability_impact`)
*   These functions are crucial for generating the data needed for plotting.
*   `generate_synthetic_safety_data`: Creates a `pandas.DataFrame` with `timestamp` and `alert_count` columns, simulating normal system behavior. It uses `numpy` for random data generation.
*   `simulate_vulnerability_impact`: Takes the `base_df` and modifies it based on `attack_type` and `attack_intensity`. Our placeholder simply increases the `alert_count` to demonstrate an impact. In a real-world application, this would involve more sophisticated modeling of how specific attacks (e.g., data poisoning, adversarial examples) affect system metrics.

#### Visualization Function (`plot_alert_frequency_trend`)
*   `@st.cache_data`: This is a Streamlit caching decorator. It tells Streamlit to run the function only once if its inputs haven't changed. This is extremely useful for performance, especially with resource-intensive operations like plotting or data loading, as it prevents re-running the function every time the Streamlit app re-renders.
*   The function uses `matplotlib.pyplot` and `seaborn` to create a line plot comparing the `base_df` (baseline data) and `attacked_df` (data after simulation of an attack).
*   `sns.lineplot(...)`: Used for drawing line plots with statistical estimation. Here, it plots `alert_count` against `timestamp`.
*   `fig, ax = plt.subplots(...)`: Creates a Matplotlib figure and a set of subplots.
*   `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()`, `ax.legend()`, `plt.xticks(rotation=45)`: Standard Matplotlib commands for customizing plot appearance, labels, and legends for better readability.
*   `plt.tight_layout()`: Automatically adjusts subplot parameters for a tight layout.

#### `main()` Function
*   `st.title(...)` and `st.markdown(...)`: Provide the page title and description.
*   **Data Generation & Simulation:**
    *   `sensor_data_baseline = generate_synthetic_safety_data(...)`: Calls the placeholder function to get initial data.
    *   `security_metrics_attacked, attack_events = simulate_vulnerability_impact(...)`: Calls the placeholder to generate attacked data. Here, we hardcode `Data Poisoning` as the attack type and `0.5` as intensity for demonstration.
*   `st.subheader('Trend Plot')` and `st.pyplot(fig_trend)`: Displays a subheader and then renders the `matplotlib` figure generated by `plot_alert_frequency_trend` in the Streamlit application.
*   `st.columns(2)` and `st.dataframe(...)`: Optionally displays the raw baseline and attacked data in two columns, which can be helpful for debugging or detailed inspection.

<aside class="negative">
The placeholder functions `generate_synthetic_safety_data` and `simulate_vulnerability_impact` are simplified. For a real-world AI security lab, these would be significantly more complex, involving detailed models of AI system behavior, different attack methodologies, and more realistic data generation techniques. Developers should extend these functions to incorporate specific vulnerabilities and AI models they wish to study.
</aside>

## Step 6: Running the Application and Experimentation
Duration: 00:05

Now that all the files are in place, you can run the Streamlit application and start exploring the AI Security Vulnerability Simulation Lab!

### Running the Application

1.  **Navigate to your project directory:** Open your terminal or command prompt and change your current directory to where your `app.py` file is located.
    ```bash
    cd path/to/your/project
    ```

2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

3.  **Access the application:** Streamlit will automatically open a new tab in your web browser, displaying the application. If it doesn't, it will provide a local URL (e.g., `http://localhost:8501`) that you can copy and paste into your browser.

### Experimentation

Once the application is running:

1.  **Explore the "Overview" page:** Read through the introduction to grasp the context of the lab.
2.  **Navigate to the "Simulation" page:** Use the sidebar dropdown to switch to the "Simulation" section.
3.  **Observe the plot:** You will see a "Trend Plot: Simulated Alert Frequency" showing a baseline and an attacked scenario.
4.  **Modify the simulation (for developers):**
    *   Open `application_pages/page_2.py` in your code editor.
    *   Locate the `main()` function.
    *   **Change attack parameters:** Experiment by modifying the `attack_type` or `attack_intensity` in the `simulate_vulnerability_impact` call:
        ```python
        security_metrics_attacked, attack_events = simulate_vulnerability_impact(
            sensor_data_baseline, 'DDoS', 0.8, 5, {} # Example: Change attack type and intensity
        )
        ```
    *   **Modify synthetic data:** Adjust parameters in `generate_synthetic_safety_data` to see how the baseline changes.
    *   **Enhance placeholder functions:** For a deeper understanding, try to implement more realistic logic within `generate_synthetic_safety_data` and `simulate_vulnerability_impact` to model different attack patterns (e.g., sudden spikes, gradual increase, periodic attacks) or specific AI security scenarios (e.g., data poisoning on classification accuracy, adversarial examples affecting object detection scores).
    *   **Add more visualizations:** Integrate other plots (e.g., histograms of alert counts, distribution plots) to provide more insights into the impact of attacks.

<aside class="positive">
Streamlit has a hot-reloading feature. Whenever you save changes to your Python files, the application in your browser will automatically detect the changes and prompt you to "Rerun" or "Always rerun". This makes development and experimentation very efficient!
</aside>

This concludes the guide for the AI Security Vulnerability Simulation Lab. You now have a foundational understanding of its structure, functionality, and how to extend it.
