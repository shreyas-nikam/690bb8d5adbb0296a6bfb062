# AI Security Vulnerability Simulation Lab

![Streamlit App Screenshot](https://www.quantuniversity.com/assets/img/logo5.jpg)
*(Placeholder for an actual screenshot of the application if available)*

## 📚 Project Description

This Streamlit application serves as an "AI Security Vulnerability Simulation Lab," designed to provide hands-on experience in identifying, understanding, and analyzing AI-security vulnerabilities within agentic AI systems used for industrial safety monitoring.

The lab provides a simulated environment where users can explore different types of AI attacks, adjust their intensity, and observe their impact on system metrics. It aims to educate participants on the nuances of AI security threats, including 'synthetic-identity risk' and 'untraceable data leakage', and the effectiveness of potential defense strategies.

**Learning Outcomes:**
*   Understand the key insights contained in the uploaded document and supporting data.
*   Identify common AI-security vulnerabilities, including 'synthetic-identity risk' and 'untraceable data leakage'.
*   Learn about adversarial testing techniques like prompt injection and data poisoning.
*   Analyze the effectiveness of different defense strategies and risk controls in mitigating AI security threats.

**Scope and Constraints:**
This lab is designed to execute end-to-end on a mid-spec laptop (8 GB RAM) in fewer than 5 minutes. It exclusively uses open-source Python libraries from PyPI. All major steps include both code comments and brief narrative cells explaining 'what' is happening and 'why'.

## ✨ Features

The application is structured into several interactive pages, accessible via a sidebar navigation:

*   **Introduction**: Provides an overview of the lab, its objectives, and scope.
*   **Setup**: Confirms the successful loading of necessary Python libraries, preparing the environment for simulations.
*   **Configuration**: Allows users to dynamically adjust key simulation parameters, such as:
    *   Attack Intensity ($A_{intensity}$)
    *   Attack Type (e.g., Prompt Injection, Data Poisoning, Synthetic Identity, Untraceable Data Leakage)
    *   Number of Compromised Agents ($N_{agents}$)
*   **Simulation**: Executes the core vulnerability simulation, generating synthetic safety data and applying the configured attack parameters. It displays both baseline and attacked security metrics.
*   **Visualization**: Presents the simulation results through interactive plots and charts, illustrating the impact of various vulnerabilities on system behavior (e.g., alert frequency, attack severity, agent integrity).

## 🚀 Getting Started

Follow these instructions to get the application up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository (if applicable)**:
    ```bash
    git clone https://github.com/your-username/ai-security-vulnerability-lab.git
    cd ai-security-vulnerability-lab
    ```
    *(If this is a local project, you might skip cloning and just navigate to your project directory.)*

2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    Create a `requirements.txt` file in your project root with the following content:
    ```
    streamlit>=1.20.0
    pandas>=1.4.0
    numpy>=1.22.0
    matplotlib>=3.5.0
    seaborn>=0.11.0
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

## 💡 Usage

To run the Streamlit application:

1.  **Navigate to the project directory** (if you haven't already):
    ```bash
    cd /path/to/your/ai-security-vulnerability-lab
    ```

2.  **Ensure your virtual environment is active** (if you created one).

3.  **Execute the Streamlit command**:
    ```bash
    streamlit run app.py
    ```

4.  This will open the application in your default web browser (usually at `http://localhost:8501`).
5.  Use the **sidebar navigation** to explore the different sections of the lab.
6.  On the **Configuration** page, use the sliders and select boxes in the sidebar to adjust simulation parameters and observe their effects in the **Simulation** and **Visualization** pages.

## 📁 Project Structure

```
.
├── app.py                            # Main Streamlit application entry point
├── application_pages/                # Directory containing individual Streamlit page logic
│   ├── __init__.py                   # Makes application_pages a Python package
│   ├── introduction.py               # Introduces the lab and its objectives
│   ├── setup.py                      # Handles initial setup and library imports confirmation
│   ├── configuration.py              # Manages simulation parameter inputs via sidebar
│   ├── simulation.py                 # Core logic for data generation and vulnerability simulation
│   └── visualization.py              # Logic for plotting and displaying simulation results
└── requirements.txt                  # List of Python dependencies
```

## 🛠️ Technology Stack

*   **Framework**: [Streamlit](https://streamlit.io/) - For building interactive web applications with Python.
*   **Data Manipulation**: [Pandas](https://pandas.pydata.org/) - For data generation and analysis.
*   **Numerical Operations**: [NumPy](https://numpy.org/) - For numerical computing.
*   **Plotting**:
    *   [Matplotlib](https://matplotlib.org/) - For creating static, interactive, and animated visualizations.
    *   [Seaborn](https://seaborn.pydata.org/) - For making attractive and informative statistical graphics.
*   **Language**: Python 3.8+

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this lab, here's how you can contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Write clear commit messages.
5.  Push your branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request, describing your changes in detail.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(You should create a LICENSE file in your project root if you choose a specific license.)*

## 📧 Contact

For any questions or feedback, please reach out:

*   **Project Maintainer**: [Your Name/Organization Name]
*   **Email**: [your.email@example.com]
*   **GitHub**: [https://github.com/your-username/ai-security-vulnerability-lab](https://github.com/your-username/ai-security-vulnerability-lab)

