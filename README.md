# AI Security Vulnerability Simulation Lab (QuLab Project)

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## 1. Project Title and Description

This Streamlit application, "AI Security Vulnerability Simulation Lab," is a hands-on educational project designed to explore and analyze AI-security vulnerabilities within agentic AI systems, specifically in the context of industrial safety monitoring. It provides a controlled environment to simulate real-world threats like 'synthetic-identity risk' and 'untraceable data leakage', along with adversarial testing techniques such as prompt injection and data poisoning.

The lab focuses on providing a practical understanding of:
*   Identifying common AI-security vulnerabilities.
*   The impact of adversarial attacks on AI system behavior.
*   Analyzing the effectiveness of various defense strategies and risk controls.

Built with an emphasis on accessibility and performance, this lab is designed to run end-to-end on a mid-spec laptop (8 GB RAM) in under 5 minutes, utilizing exclusively open-source Python libraries. Each major step includes clear code comments and narrative explanations ("what" and "why") to facilitate learning.

## 2. Features

The application provides a guided, interactive experience through several key features:

*   **Interactive Configuration**: Users can dynamically adjust simulation parameters such as `Attack Intensity`, `Attack Type` (e.g., Prompt Injection, Data Poisoning), and `Number of Compromised Agents` to customize attack scenarios.
*   **Mathematical Modeling of Attacks**: Transparent mathematical foundations are presented to quantify the impact of different vulnerabilities on system metrics like alert frequency, detection latency, and agent integrity scores.
*   **Synthetic Data Generation**: Creates a lightweight, realistic synthetic dataset simulating industrial sensor readings, AI agent communication logs, and baseline security metrics to establish a controlled testing environment.
*   **Data Validation & Initial Statistics**: Performs crucial validation checks on the generated data (column names, types, uniqueness, null values) and provides summary statistics for initial data understanding.
*   **Vulnerability Simulation Engine**: Implements core attack logic to apply the simulated vulnerabilities, modifying baseline metrics to reflect the impact of 'synthetic-identity risk' and 'untraceable data leakage'.
*   **Dynamic Visualizations**: Generates comparative trend plots (e.g., Alert Frequency Over Time) to visually demonstrate the difference between baseline (unattacked) and attacked system behavior.
*   **Educational Discussion**: Provides a dedicated section to discuss observed results, reinforce learning outcomes, and connect practical simulations to theoretical concepts of AI security, risk controls, and red-teaming.
*   **Comprehensive References**: Lists all foundational documents and open-source libraries used, offering further resources for deeper exploration.

## 3. Getting Started

Follow these instructions to set up and run the AI Security Vulnerability Simulation Lab on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ai-security-vulnerability-lab.git
    cd ai-security-vulnerability-lab
    ```
    *(Note: Replace `https://github.com/yourusername/ai-security-vulnerability-lab.git` with the actual repository URL if available, otherwise, assume local file structure.)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    Create a `requirements.txt` file in the root directory with the following content:
    ```
    streamlit>=1.0.0
    pandas>=1.0.0
    numpy>=1.0.0
    matplotlib>=3.0.0
    seaborn>=0.11.0
    ipywidgets>=7.0.0 # Although IPywidgets is referenced, it's primarily for Jupyter, not direct Streamlit usage. Including for completeness based on references.
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

## 4. Usage

To run the Streamlit application:

1.  **Ensure your virtual environment is activated** (if you created one).
2.  **Navigate to the project's root directory** in your terminal.
3.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
4.  Your default web browser should automatically open a new tab displaying the application (usually at `http://localhost:8501`).

### Basic Usage Instructions:
*   **Navigate Pages**: Use the sidebar on the left to navigate through the different sections of the lab (Overview, Setup, Configuration, etc.).
*   **Configure Simulation**: Go to the "Configuration" page to interactively set parameters for the attack simulation using sliders and select boxes.
*   **Observe Results**: Progress through the subsequent pages to see synthetic data generation, validation, vulnerability simulation, and visual analysis of the attack's impact.
*   **Learn**: Pay attention to the narrative text and code comments on each page, especially the "Discussion" section, to grasp the learning outcomes.

## 5. Project Structure

The project is organized into a main application file and a directory for individual Streamlit pages:

```
ai-security-vulnerability-lab/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # List of Python dependencies
└── application_pages/          # Directory containing individual Streamlit page scripts
    ├── overview.py
    ├── setup.py
    ├── configuration.py
    ├── mathematical_foundations.py
    ├── synthetic_data.py
    ├── data_validation.py
    ├── vulnerability_simulation.py
    ├── visualizations.py
    ├── discussion.py
    ├── conclusion.py
    └── references.py
```

*   `app.py`: Handles global Streamlit configuration, sidebar navigation, and routes to the appropriate page script based on user selection.
*   `application_pages/`: Each `.py` file within this directory represents a distinct page in the Streamlit application, encapsulating the content and logic for that specific section of the lab.

## 6. Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: The framework used for building the interactive web application.
*   **Pandas**: Essential for data manipulation and analysis, particularly with DataFrames.
*   **NumPy**: Provides fundamental support for large, multi-dimensional arrays and mathematical functions.
*   **Matplotlib**: Used for creating static, interactive, and animated visualizations.
*   **Seaborn**: A high-level data visualization library based on Matplotlib, offering attractive statistical graphics.
*   **IPywidgets**: (Referenced in the lab's resources) While primarily for Jupyter notebooks, it demonstrates the broader ecosystem of interactive components.

## 7. Contributing

This project is primarily designed as a lab for educational purposes. However, if you find issues or have suggestions for improvements, feel free to:

1.  **Fork** the repository.
2.  **Create a new branch** for your feature or bug fix (`git checkout -b feature/your-feature-name`).
3.  **Make your changes**.
4.  **Commit your changes** (`git commit -m 'Add new feature'`).
5.  **Push to the branch** (`git push origin feature/your-feature-name`).
6.  **Open a Pull Request**.

## 8. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Note: You might need to create a `LICENSE` file in your repository if one doesn't exist.)*

## 9. Contact

For questions, feedback, or further information about this lab project, please feel free to:

*   Open an issue on the GitHub repository.
*   Visit [QuantUniversity's website](https://www.quantuniversity.com/) for more educational resources.


## License

## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@quantuniversity.com](mailto:info@quantuniversity.com)
