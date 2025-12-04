Here's a comprehensive `README.md` for your Streamlit application lab project, formatted for clarity and professionalism.

---

# 🔐 QuLab: AI Security Vulnerability Simulation Lab

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Title

**QuLab: AI Security Vulnerability Simulation Lab**

## Description

The QuLab AI Security Vulnerability Simulation Lab is an interactive Streamlit application designed to help industrial AI safety teams understand and experiment with common AI attacks. By simulating scenarios such as prompt injection, data poisoning, synthetic identity, and untraceable data leakage, users can observe their impact on critical security metrics like alert frequency, detection latency, and agent integrity.

This lab provides a safe, synthetic environment to act as both a "red teamer" (configuring attacks) and a "blue teamer" (analyzing their impact on monitoring systems). The business goal is to empower teams to design more robust defenses for agentic AI systems deployed in critical industrial environments like factories, refineries, and power plants, where continuous uptime and safety are paramount.

## Features

This application offers the following key functionalities:

*   **Interactive Attack Configuration**: Easily adjust parameters such as:
    *   **Attack Intensity ($A_{intensity}$)**: Control the severity of the simulated attack (0.0 to 1.0).
    *   **Attack Type**: Select from various AI security vulnerabilities, including Prompt Injection, Data Poisoning, Synthetic Identity, and Untraceable Data Leakage.
    *   **Number of Compromised Agents ($N_{agents}$)**: Specify how many agents are affected by the attack.
*   **Synthetic Data Generation**: On-the-fly creation of realistic, time-series data for:
    *   **Sensor Readings**: Simulate industrial sensor data (temperature, pressure, vibration) with normal and anomalous states.
    *   **Agent Logs**: Generate communication logs, status updates, and simulated alerts from autonomous agents.
    *   **Baseline Security Metrics**: Establish initial performance metrics for agents before attacks.
*   **Real-time Vulnerability Simulation**: Applies mathematical models to perturb baseline metrics based on configured attack parameters, showcasing changes in:
    *   **Alert Frequency**: How often the system raises alerts under attack.
    *   **Detection Latency**: The simulated time taken to detect an ongoing attack.
    *   **Agent Integrity Scores**: The health and trustworthiness of individual agents.
*   **Dynamic Visualizations**: Clear and informative plots to interpret simulation results:
    *   **Alert Frequency Over Time**: Trend plot comparing baseline vs. attacked alert behavior.
    *   **Attack Severity vs. Detection Latency**: Scatter plot to understand the relationship between attack scale and detection time.
    *   **Agent Integrity Comparison**: Bar chart showing average integrity scores for compromised vs. uncompromised agents.
*   **Data Validation Module**: A robust function to check the structural integrity, data types, and absence of critical nulls in generated datasets.
*   **Mathematical Modeling Transparency**: Explicitly outlines the equations used to simulate attack impacts on metrics.
*   **Guided Exploration**: An "AI Security Lab Overview" page provides a mission brief, learning objectives, business context, and a "Mini-Challenge" to guide users through their first experiments.
*   **Clear Navigation**: Seamless switching between the introductory overview and the full simulation workspace via the sidebar.

## Getting Started

Follow these instructions to get the QuLab application up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/quolab-ai-security-lab.git
    cd quolab-ai-security-lab
    ```
    (Replace `your-username/quolab-ai-security-lab.git` with the actual repository URL if different).

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    First, create a `requirements.txt` file in your project root with the following content:

    ```
    streamlit>=1.0
    pandas>=1.0
    numpy>=1.20
    matplotlib>=3.3
    seaborn>=0.11
    ```

    Then install:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2.  **Access the Application**:
    Your web browser should automatically open to `http://localhost:8501` (or another port if 8501 is in use).

3.  **Navigate the Lab**:
    *   **AI Security Lab Overview**: This is the default starting page. It provides a mission brief, explains what you'll practice, offers business context, and guides you on how to use the lab. It also includes a "Mini-Challenge" to kickstart your experiments.
    *   **Full Simulation Workspace**: Use the `Navigation` selectbox in the left sidebar to switch to this page. Here, you'll find the interactive `Attack Configuration Panel` in the sidebar to adjust attack intensity, type, and the number of compromised agents. The main content area will display synthetic data, validation results, mathematical foundations, and the three key plots that visualize the attack's impact.

4.  **Experiment with Attacks**:
    *   Use the sliders and selectbox in the sidebar to change `Attack Intensity`, `Attack Type`, and `Number of Compromised Agents`.
    *   Observe how the "Attacked Security Metrics" tables and the three plots (`Alert Frequency Trend`, `Attack Severity vs. Detection Latency`, `Agent Integrity Scores`) change in real-time.
    *   Reflect on the `Discussion and Reflection Prompts` and `Key Takeaways` at the bottom of the "Full Simulation Workspace" page.

## Project Structure

The project is organized as follows:

```
quolab-ai-security-lab/
├── app.py                            # Main Streamlit application entry point
├── requirements.txt                  # Python dependencies
├── application_pages/                # Directory for individual application pages
│   ├── __init__.py                   # Makes application_pages a Python package
│   ├── ai_security_overview.py       # Defines the 'AI Security Lab Overview' page
│   └── ai_security_simulation.py     # Defines the 'Full Simulation Workspace' page
└── README.md                         # This README file
```

## Technology Stack

*   **Streamlit**: For building the interactive web application and user interface.
*   **Python 3.8+**: The core programming language.
*   **Pandas**: For data manipulation and analysis, especially with DataFrames.
*   **NumPy**: For numerical operations and generating synthetic data.
*   **Matplotlib**: For creating static, animated, and interactive visualizations.
*   **Seaborn**: Built on Matplotlib, providing a high-level interface for drawing attractive and informative statistical graphics.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

1.  **Fork** the repository.
2.  **Create a new branch** for your feature or fix: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and ensure the code adheres to the existing style.
4.  **Test your changes** thoroughly.
5.  **Commit your changes** with a descriptive message.
6.  **Push your branch** to your forked repository.
7.  **Open a Pull Request** against the `main` branch of this repository, describing your changes in detail.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

*(Note: You might need to create a `LICENSE` file in your repository with the MIT License text.)*

## Contact

For questions, feedback, or collaborations, please reach out to:

*   **QuantUniversity**: [https://www.quantuniversity.com/](https://www.quantuniversity.com/)
*   **GitHub**: [https://github.com/your-username](https://github.com/your-username) (Replace with your actual GitHub profile)

---