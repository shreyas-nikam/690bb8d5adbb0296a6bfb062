This `README.md` provides a comprehensive overview of the **QuLab: AI Security Vulnerability Simulation Lab** Streamlit application.

---

# QuLab: AI Security Vulnerability Simulation Lab

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

**QuLab** is an interactive Streamlit application designed to provide a hands-on learning experience in understanding and analyzing AI security vulnerabilities within agentic AI systems. Specifically, this lab simulates various attack scenarios on an industrial safety monitoring system, demonstrating the impact of threats like prompt injection, data poisoning, synthetic-identity risk, and untraceable data leakage.

Through interactive configuration and visualizations, users can observe how these vulnerabilities manifest, affect system performance and security metrics, and gain practical insights into adversarial testing techniques and the importance of robust risk controls in AI system design.

## Table of Contents

- [Project Title and Description](#project-title-and-description)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Title and Description

**QuLab: AI Security Vulnerability Simulation Lab**

This Streamlit application serves as a laboratory project to explore the critical domain of AI security vulnerabilities in agentic AI systems. It simulates an industrial safety monitoring system and allows users to apply various adversarial attacks, such as **prompt injection** and **data poisoning**, as well as study concepts like **synthetic-identity risk** and **untraceable data leakage**.

The primary goal is to equip users with practical insights into how these vulnerabilities affect system behavior, including alert frequencies, detection latencies, and agent integrity scores. By providing a controlled environment with interactive visualizations and data analysis, the lab aims to foster a deeper understanding of adversarial testing techniques and the necessity for robust risk management in AI system development.

## Features

The QuLab application offers a range of features to facilitate an in-depth exploration of AI security:

*   **Synthetic Data Generation**: Generates realistic baseline data simulating an industrial safety monitoring system, including sensor readings, agent communication logs, and initial security metrics.
*   **Interactive Attack Configuration**: Allows users to dynamically define attack parameters via a sidebar, including:
    *   **Attack Type**: Select from 'Prompt Injection', 'Data Poisoning', 'Synthetic Identity', and 'Untraceable Data Leakage'.
    *   **Attack Intensity**: Control the severity of the simulated attack on a scale from 0.0 to 1.0.
    *   **Number of Compromised Agents**: Specify how many agents within the system are affected.
*   **Mathematical Model-Based Simulation**: Implements defined mathematical relationships to simulate the impact of chosen attack parameters on key security metrics, such as:
    *   Alert Frequency Over Time
    *   Detection Latency
    *   Agent Integrity Score
*   **Comprehensive Data Validation**: Provides an automated summary and validation check for the generated baseline data to ensure its integrity and correctness before simulation.
*   **Interactive Visualizations**: Utilizes Plotly to generate dynamic charts and graphs that clearly illustrate the differences between baseline (normal operation) and attacked scenarios, including:
    *   Trend plots of alert frequency.
    *   Scatter plots showing the relationship between attack severity and detection latency.
    *   Bar charts comparing agent integrity scores for compromised vs. uncompromised agents.
*   **Educational Content**: Includes detailed explanations of AI security concepts, learning goals, and methodological foundations (including the mathematical models used) to enrich the learning experience.
*   **Multi-Page Navigation**: Organizes the lab into distinct sections using Streamlit's sidebar navigation for a structured workflow:
    *   **Page 1: Overview & Data Generation**: Introduces the lab, learning goals, and generates initial baseline data.
    *   **Page 2: Simulation Configuration & Validation**: Explains the simulation methodology, allows parameter configuration, and validates data.
    *   **Page 3: Vulnerability Simulation & Analysis**: Executes the simulation and presents detailed analytical visualizations and conclusions.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Ensure you have the following installed:

*   **Python**: Version 3.8 or higher.
*   **pip**: Python's package installer, usually comes with Python.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/quLab-ai-security-sim.git
    cd quLab-ai-security-sim
    ```
    *(Note: Replace `https://github.com/your-username/quLab-ai-security-sim.git` with the actual repository URL.)*

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```
    If `requirements.txt` is not provided, you can create it manually based on the `Technology Stack` section below, or run:
    ```bash
    pip install streamlit pandas numpy scipy plotly
    ```

## Usage

To run the Streamlit application:

1.  **Navigate to the project directory** (if you aren't already there):
    ```bash
    cd quLab-ai-security-sim
    ```

2.  **Ensure your virtual environment is activated** (if you created one):
    ```bash
    source venv/bin/activate
    ```

3.  **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser. If it doesn't open automatically, you'll see a local URL (e.g., `http://localhost:8501`) in your terminal, which you can navigate to manually.

### Basic Usage Instructions:

1.  **Page 1: Overview & Data Generation**: Start here to understand the lab's context and goals. The page automatically generates the baseline synthetic data needed for simulations. Review the data previews.
2.  **Page 2: Simulation Configuration & Validation**: Use the sidebar to configure the `Attack Intensity`, `Attack Type`, and `Number of Compromised Agents`. This page also details the mathematical models behind the simulation and performs essential data validation checks.
3.  **Page 3: Vulnerability Simulation & Analysis**: Once parameters are set on Page 2, navigate to this page. It will run the simulation based on your chosen parameters and display interactive plots visualizing the attack's impact on alert frequency, detection latency, and agent integrity. Read the discussion and conclusion for key insights.

## Project Structure

The project is organized into a modular structure to maintain clarity and scalability:

```
quLab-ai-security-sim/
├── app.py                      # Main Streamlit application entry point and page navigation logic.
├── application_pages/          # Directory containing individual Streamlit page implementations.
│   ├── __init__.py             # Makes application_pages a Python package.
│   ├── page1.py                # Implements "Page 1: Overview & Data Generation".
│   ├── page2.py                # Implements "Page 2: Simulation Configuration & Validation".
│   ├── page3.py                # Implements "Page 3: Vulnerability Simulation & Analysis".
│   └── utils.py                # Contains utility functions for data generation, validation, simulation logic, and plotting.
├── requirements.txt            # Lists Python dependencies for the project.
└── README.md                   # This comprehensive README file.
```

## Technology Stack

The QuLab application leverages the following technologies:

*   **Python**: The core programming language.
*   **Streamlit**: For creating the interactive web application user interface.
*   **Pandas**: For efficient data manipulation and analysis, especially with DataFrames.
*   **NumPy**: For numerical operations and array manipulation.
*   **SciPy**: Specifically for statistical functions (e.g., Poisson distribution for alert rates).
*   **Plotly**: For generating rich, interactive data visualizations.

## Contributing

Contributions to the QuLab project are welcome! If you have suggestions for improvements, new features, or find any bugs, please feel free to:

1.  **Fork the repository.**
2.  **Create a new branch** (`git checkout -b feature/AmazingFeature`).
3.  **Commit your changes** (`git commit -m 'Add some AmazingFeature'`).
4.  **Push to the branch** (`git push origin feature/AmazingFeature`).
5.  **Open a Pull Request.**

Please ensure your code adheres to good practices and includes appropriate documentation and tests where applicable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

*(Note: If you don't have a LICENSE file, you might want to create one or remove this section.)*

## Contact

For any questions, suggestions, or feedback, please reach out to:

*   **Your Name/Organization**: [Your Name/Organization Here]
*   **Email**: [your.email@example.com]
*   **Project Link**: [https://github.com/your-username/quLab-ai-security-sim](https://github.com/your-username/quLab-ai-security-sim)

---
Enjoy exploring the world of AI security vulnerabilities with QuLab!